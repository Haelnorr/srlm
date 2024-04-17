from datetime import datetime

from celery import shared_task

from api.srlm.app import db, create_app
from api.srlm.app.api.utils.functions import ensure_exists
from api.srlm.app.models import MatchData, Match, Player, PlayerMatchData
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


def period_from_log(log_json, match_id, region, created, gamemode, lobby_id):

    match = ensure_exists(Match, return_none=True, id=match_id)

    if match is None:
        return None

    period = MatchData()
    period.current_period = log_json['current_period']
    period.winner = log_json['winner']
    period.periods_enabled = bool(log_json['periods_enabled'])
    period.current_period = int(log_json['current_period'])
    period.custom_mercy_rule = log_json['custom_mercy_rule']
    period.end_reason = log_json['end_reason']
    period.home_score = int(log_json['score']['home'])
    period.away_score = int(log_json['score']['away'])
    period.arena = log_json['arena']
    period.region = region
    period.created = created
    period.gamemode = gamemode
    period.lobby_id = lobby_id
    period.match_id = 'Offline - no match ID'
    period.source = 'LogUpload'
    db.session.add(period)
    db.session.commit()

    teams = {
        'home': match.home_team_id,
        'away': match.away_team_id
    }

    for player in log_json['players']:
        player_db = ensure_exists(Player, return_none=True, slap_id=player['game_user_id'])
        if player_db is None:
            player_db = Player()
            player_db.player_name = player['username']
            player_db.slap_id = int(player['game_user_id'])
            player_db.first_season_id = match.season_division_id
            db.session.add(player_db)
            db.session.commit()

        valid_stats = ['goals', 'shots', 'assists', 'saves', 'primary_assists', 'secondary_assists', 'passes', 'blocks',
                       'takeaways', 'turnovers', 'possession_time_sec', 'game_winning_goals', 'post_hits',
                       'faceoffs_won', 'faceoffs_lost', 'score']

        player_data = PlayerMatchData()
        player_data.match_id = period.id
        player_data.player_id = player_db.id
        player_data.team_id = teams[player['team']]
        for stat in player['stats']:
            if stat in valid_stats:
                setattr(player_data, stat, player['stats'][stat])
        player_data.current_period = int(log_json['current_period'])
        db.session.add(player_data)
        db.session.commit()

    return True


@shared_task
def get_match_data(lobby_id):
    app, celery = create_app()
    with app.app_context():
        from api.srlm.app import db
        from api.srlm.app.models import Lobby
        from api.srlm.app.spapi.lobby import get_lobby_matches

        # get lobby info from db
        lobby = db.session.get(Lobby, lobby_id)
        log.info(f'Lobby {lobby.id} details pulled from database')

        teams = {
            'home': lobby.match.home_team,
            'away': lobby.match.away_team
        }

        # request match stats
        match_response = get_lobby_matches(lobby.lobby_id)
        log.info('Requested match stats from API')

        # save each period into match_data and player_match_data
        if match_response.status_code == 200:
            for match in match_response.json():
                log.info('Match data found')
                # attempts to parse match data and store in DB - returns match_data.id or False
                log.info('Parsing match stats')
                log.info(lobby.id)
                parse_match_stats(match, teams, lobby)

        return lobby.match.id


def parse_match_stats(match, teams, lobby):
    already_added = db.session.query(MatchData).filter_by(match_id=match['id']).first()
    log.info(lobby.id)

    match_id = already_added.id if already_added else False

    if match['game_stats'] and not already_added:
        data = {
            'lobby_id': lobby.id,
            'processed': False,
            'match_id': match['id'],
            'region': match['region'],
            'gamemode': match['gamemode'],
            'created': datetime.strptime(match['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'arena': match['game_stats']['arena'],
            'home_score': match['game_stats']['score']['home'],
            'away_score': match['game_stats']['score']['away'],
            'winner': match['game_stats']['winner'],
            'end_reason': match['game_stats']['end_reason'],
            'current_period': int(match['game_stats']['current_period']),
            'periods_enabled': bool(match['game_stats']['periods_enabled']),
            'custom_mercy_rule': match['game_stats']['custom_mercy_rule'],
            'source': 'SlapAPI'
        }
        match_db = MatchData()
        match_db.from_dict(data)
        db.session.add(match_db)
        db.session.commit()

        for player_data in match['game_stats']['players']:
            # get player from slap id
            # if doesnt exist in db, create
            player = db.session.query(Player).filter_by(slap_id=player_data['game_user_id']).first()
            if not player:
                player = Player()
                player.slap_id = player_data['game_user_id']
                player.player_name = player_data['username']
                player.first_season_id = lobby.match.season_division_id
                db.session.add(player)
                db.session.commit()

            iter_fields = ['goals', 'shots', 'saves', 'assists', 'primary_assists', 'secondary_assists', 'passes',
                           'score', 'blocks', 'takeaways', 'turnovers', 'game_winning_goals', 'post_hits',
                           'faceoffs_won', 'faceoffs_lost', 'possession_time_sec']

            data = {
                'match_id': match_db.id,
                'player_id': player.id,
                'team_id': teams[player_data['team']].id
            }
            for field in iter_fields:
                if field in player_data['stats']:
                    data[field] = int(player_data['stats'][field])

            player_match_data = PlayerMatchData()
            player_match_data.from_dict(data)
            player_match_data.current_period = int(match['game_stats']['current_period'])
            db.session.add(player_match_data)
            db.session.commit()

        match_id = match_db.id if match_db.id else False

    return match_id


@shared_task
def validate_stats(match_id):
    app, celery = create_app()
    with app.app_context():
        import sqlalchemy as sa
        from api.srlm.app import db
        from api.srlm.app.models import Match, MatchReview

        log.info('Validating match stats!')
        match = db.session.get(Match, match_id)
        log.info(f'Pulled match {match.id} from database')

        # Getting relevant info for comparison
        teams = {
            'home': match.home_team,
            'away': match.away_team
        }
        match_type = match.season_division.season.match_type

        # periods_on is 1 or 0, so this formula gives either 3 or 1 (correct number of periods)
        correct_periods = 1 + (match_type.periods * 2)

        # uses correct_periods to get a comparison array to check the order
        correct_period_order = {1: [1], 3: [1, 2, 3]}[correct_periods]

        # the expected match settings
        match_settings = {
            'periods': match_type.periods,
            'game_mode': match_type.game_mode,
            'region': match.season_division.season.league.server_region_value
        }

        # setting defaults for the review flags
        defaults = {
            'match_id': match.id,
            'raised_by': 'System',
            'type': 'AutoReview'
        }

        # check num lobbies
        num_lobbies = match.lobbies.count()
        lobby_ids = []
        for lobby in match.lobbies:
            lobby_ids.append(lobby.id)
        if num_lobbies == 0:
            return f'No lobbies found for match {match.id}'
        if num_lobbies > 1:
            db.session.add(MatchReview(reason=f'Multiple lobbies created for match: {lobby_ids}', **defaults))

        periods = db.session.query(MatchData).filter(MatchData.lobby_id.in_(lobby_ids)).order_by(
            sa.asc(MatchData.created))
        period_ids = []

        period_order = []
        for period in periods:
            period_order.append(period.current_period)
            period_ids.append(period.id)
            # check lobby settings
            period_settings = {
                'periods': period.periods_enabled,
                'game_mode': period.gamemode,
                'region': period.region
            }
            if period_settings != match_settings:
                incorrect_fields = []
                for field in period_settings:
                    if period_settings[field] != match_settings[field]:
                        incorrect_fields.append((field, period_settings[field]))
                db.session.add(
                    MatchReview(reason=f'Game settings for period {period.current_period} were incorrect.', **defaults))

            # check number of players in period
            if period.player_data_assoc.count() != match_type.num_players:
                for player in period.player_data_assoc:
                    player_data = db.session.query(PlayerMatchData).filter(
                        sa.and_(
                            PlayerMatchData.match_id.in_(period_ids),
                            PlayerMatchData.player_id == player.player_id
                        )).order_by(sa.asc(PlayerMatchData.current_period))

                    last_period = None
                    for player_period in player_data:
                        if last_period is None:
                            last_period = player_period
                        else:
                            tests = ['goals', 'shots', 'assists', 'saves', 'primary_assists', 'secondary_assists',
                                     'passes', 'blocks', 'takeaways', 'turnovers', 'game_winning_goals',
                                     'overtime_goals', 'post_hits', 'faceoffs_won', 'faceoffs_lost',
                                     'score', 'possession_time_sec']
                            spectator = True
                            for test in tests:
                                if getattr(last_period, test) != getattr(player_period, test):
                                    spectator = False
                                    break
                            if spectator:
                                db.session.delete(player_period)
                                db.session.commit()
                            else:
                                last_period = player_period

                if period.player_data_assoc.count() != match_type.num_players:
                    db.session.add(
                        MatchReview(reason=f'Period {period.current_period} had incorrect number of '
                                           f'players.', **defaults))

        # check num periods
        if periods.count() != correct_periods:
            db.session.add(
                MatchReview(reason=f'{periods.count()} periods were recorded,'
                                   f' should be {correct_periods}', **defaults))
        # check periods played in order
        elif period_order != correct_period_order:
            db.session.add(MatchReview(reason='Periods were not played in correct order', **defaults))

        players_data = db.session.query(PlayerMatchData).filter(PlayerMatchData.match_id.in_(period_ids))

        # check players/teams
        players_wrong_team = []
        # check all players are registered to a team in the match or are free agents in the current season
        for player_data in players_data:
            # check player has a current team
            player_current_team = player_data.player.current_team(match.season_division.season)
            if not player_current_team:
                # check if player is a free agent
                player_free_agent = player_data.player.season_association.filter_by(
                    season_division_id=match.season_division.id).first()
                if not player_free_agent:
                    db.session.add(MatchReview(
                        reason=f'Player {player_data.player.player_name} is not a free agent in the current season/division',
                        **defaults))
                else:
                    # free agents added to wrong team
                    players_wrong_team.append(('FA', player_data.team_id))
            # check if players current team is part of the match
            elif player_current_team.team not in teams.values():
                db.session.add(MatchReview(
                    reason=f"Player {player_data.player.player_name} is not a member of either team in the match",
                    **defaults))

            # check if player is on correct team
            elif player_current_team.team.id != player_data.team_id:
                players_wrong_team.append((player_current_team.team.id, player_data.team_id))

        # check over players on wrong team -
        # if ALL players are playing with correct teams but just on wrong side (i.e. they chose AWAY instead of HOME)
        # fix up the records to match and don't raise a flag
        # else it will iterate back over all the wrong records and raise appropriate flags
        all_players_flipped = True
        valid_teams = [teams['home'].id, teams['away'].id]

        # if all players are flipped, then all the records should have been added to the above list
        if len(players_wrong_team) != players_data.count():
            all_players_flipped = False
        else:
            # free agents only needed in this list for the check above, remove them
            players_wrong_team = [player for player in players_wrong_team if not player[0] == 'FA']
            for player in players_wrong_team:
                if not (player[0] in valid_teams and player[1] in valid_teams):
                    all_players_flipped = False

        if all_players_flipped:
            # flip all the players teams around
            flip_team_id = {valid_teams[0]: valid_teams[1], valid_teams[1]: valid_teams[0]}
            for player_data in players_data:
                player_data.team_id = flip_team_id[player_data.team_id]
                db.session.add(player_data)

            flip_team_label = {'away': 'home', 'home': 'away'}
            for period in periods:
                try:
                    period.winner = flip_team_label[period.winner]
                except KeyError:
                    pass
                period.home_score, period.away_score = period.away_score, period.home_score
                db.session.add(period)

            db.session.commit()
        else:
            # raise player on incorrect team flags
            for player_data in players_data:
                if player_data.player.current_team():
                    if player_data.player.current_team().team.id != player_data.team_id:
                        db.session.add(MatchReview(
                            reason=f"Player {player_data.player.player_name} played period {player_data.match.current_period}"
                                   f" for the wrong team",
                            **defaults))
        db.session.commit()

        # if good, mark periods as accepted
        flags = db.session.query(MatchReview).filter_by(match_id=match.id).count()
        for period in periods:
            period.processed = True
            if flags == 0:
                period.accepted = True
            db.session.add(period)
            db.session.commit()

        if flags == 0:
            process_match_result.delay(match.id)


@shared_task
def process_match_result(match_id):
    app, celery = create_app()
    with app.app_context():
        import sqlalchemy as sa
        from datetime import timedelta
        from api.srlm.app import db
        from api.srlm.app.models import Match, MatchResult, MatchData

        log.info('Processing match result!')
        match = db.session.get(Match, match_id)
        log.info(f'Pulled match {match.id} from database')

        lobby_ids = []
        for lobby in match.lobbies:
            lobby_ids.append(lobby.id)

        accepted_periods = db.session.query(MatchData).filter(MatchData.lobby_id.in_(lobby_ids)).order_by(
            sa.desc(MatchData.current_period))
        last_period = accepted_periods.first()

        match_result = MatchResult()
        teams = {
            'home': {
                'team': match.home_team,
                'score': last_period.home_score
            },
            'away': {
                'team': match.away_team,
                'score': last_period.away_score
            }
        }
        flip = {
            'home': 'away',
            'away': 'home'
        }
        winner = teams[last_period.winner]
        loser = teams[flip[last_period.winner]]

        data = {
            'winner_id': winner['team'].id,
            'loser_id': loser['team'].id,
            'draw': True if last_period.home_score == last_period.away_score else False,
            'score_winner': winner['score'],
            'score_loser': loser['score'],
            'overtime': True if last_period.end_reason == 'Overtime' else False,
            'forfeit': False
        }

        match_length = match.season_division.season.match_type.match_length
        game_finished = last_period.created + timedelta(seconds=match_length)

        match_result.from_dict(data)
        match_result.completed_date = game_finished
        match_result.match = match
        db.session.add(match_result)
        db.session.commit()
