from datetime import datetime

from celery import shared_task

from api.srlm.app import db, create_app
from api.srlm.app.api.utils.functions import ensure_exists
from api.srlm.app.models import MatchData, Match, Player, PlayerMatchData, MatchReview, Lobby
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


def period_from_log(log_json, match_id, region, created, gamemode, lobby_id):
    match = ensure_exists(Match, return_none=True, id=match_id)
    if match is None:
        return None

    period = create_match_data_entry_from_log(log_json, region, created, gamemode, lobby_id)
    create_player_match_data_entries_from_log(match, log_json, period)

    return True


def create_match_data_entry_from_log(log_json, region, created, gamemode, lobby_id):
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
    return period


def create_player_match_data_entries_from_log(match, log_json, period):
    teams = {
        'home': match.home_team_id,
        'away': match.away_team_id
    }

    for player in log_json['players']:
        player_db = ensure_exists(Player, return_none=True, slap_id=player['game_user_id'])
        if player_db is None:
            player_db = create_new_player_from_log(player, match)
        create_player_match_data_entry_from_log(player, player_db, period, teams, log_json)


def create_player_match_data_entry_from_log(player, player_db, period, teams, log_json):
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


def create_new_player_from_log(player, match):
    player_db = Player()
    player_db.player_name = player['username']
    player_db.slap_id = int(player['game_user_id'])
    player_db.first_season_id = match.season_division_id
    db.session.add(player_db)
    db.session.commit()
    return player_db


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
        match_db = create_match_data_entry_from_api(lobby, match)
        create_player_match_data_entries_from_api(match, lobby, match_db, teams)
        match_id = match_db.id if match_db.id else False

    return match_id


def create_match_data_entry_from_api(lobby, match):
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
    return match_db


def create_player_match_data_entries_from_api(match, lobby, match_db, teams):
    for player_data in match['game_stats']['players']:
        player = db.session.query(Player).filter_by(slap_id=player_data['game_user_id']).first()
        if not player:
            player = create_new_player_from_api(player_data, lobby.match.season_division_id)
        create_player_match_data_entry_from_api(player_data, player, match_db, teams, match)


def create_player_match_data_entry_from_api(player_data, player, match_db, teams, match):
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


def create_new_player_from_api(player_data, season_division_id):
    player = Player()
    player.slap_id = player_data['game_user_id']
    player.player_name = player_data['username']
    player.first_season_id = season_division_id
    db.session.add(player)
    db.session.commit()
    return player


class ValidationError(Exception):
    def __init__(self, cause):
        self.cause = cause

    def __str__(self):
        return repr(self.cause)


@shared_task
def validate_stats(match_id):
    app, celery = create_app()
    with app.app_context():
        from api.srlm.app import db

        log.info('Validating match stats!')
        match = db.session.get(Match, match_id)
        log.info(f'Pulled match {match.id} from database')

        expected_data = setup_validation_config(match)
        try:
            flags = perform_validation_checks(match, expected_data)
        except ValidationError as e:
            log.info(f'Error occur validating match {match.id}: {e.cause}')
            return
        finalize_checks(flags, match_id)


def setup_validation_config(match):
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

    return {
        'teams': teams,
        'match_type': match_type,
        'correct_periods': correct_periods,
        'correct_period_order': correct_period_order,
        'match_settings': match_settings
    }


def perform_validation_checks(match, expected_data):
    flags = 0

    flags = flags + check_lobby_count(match)

    periods = get_period_data(match.id)

    for period in periods:
        flags = flags + check_lobby_settings(period, expected_data['match_settings'], match.id)
        flags = flags + check_number_players_in_period(period, expected_data['match_type'].num_players, match.id)

    flags = flags + check_number_of_periods(periods.count(), expected_data['correct_periods'], match.id)
    flags = flags + check_periods_played_in_order(periods, expected_data['correct_period_order'], match.id)
    flags = flags + check_players_and_teams(match, expected_data['teams'], periods)
    return flags


def get_period_data(match_id):
    import sqlalchemy as sa
    periods = db.session.query(MatchData) \
        .join(MatchData.lobby) \
        .filter(Lobby.match_id == match_id) \
        .order_by(sa.asc(MatchData.created))
    return periods


def raise_flag(match_id, reason):
    flag = MatchReview()
    flag.reason = reason
    flag.match_id = match_id
    flag.raised_by = 'System'
    flag.type = 'AutoReview'
    db.session.add(flag)
    db.session.commit()


def check_lobby_count(match):
    num_lobbies = match.lobbies.count()
    if num_lobbies == 0:
        raise ValidationError(f'No lobbies found')
    elif num_lobbies > 1:
        lobby_ids = []
        for lobby in match.lobbies:
            if lobby.match_data.count() > 0:
                lobby_ids.append(lobby.id)
        if len(lobby_ids) > 1:
            raise_flag(match.id, f'Multiple lobbies created for match: {lobby_ids}')
            return 1
        elif len(lobby_ids) == 0:
            raise ValidationError(f'No lobbies with recorded match data found')
        else:
            return 0
    else:
        return 0


def check_lobby_settings(period, match_settings, match_id):
    period_settings = {
        'periods': period.periods_enabled,
        'game_mode': period.gamemode,
        'region': period.region
    }
    if period_settings != match_settings:
        flags = 0
        for field in period_settings:
            if period_settings[field] != match_settings[field]:
                raise_flag(match_id,
                           f'Game setting {field} incorrect for period {period.current_period}.'
                           f' Was {period_settings[field]}, should be {match_settings[field]}.')
                flags = flags + 1
        return flags
    else:
        return 0


def check_number_players_in_period(period, num_players, match_id):
    if period.player_data_assoc.count() == num_players:
        return 0

    delete_spectator_data_entries(period, match_id)

    if period.player_data_assoc.count() == num_players:
        return 0

    raise_flag(match_id, f'Period {period.current_period} had incorrect number of players.')
    return 1


def delete_spectator_data_entries(period, match_id):
    for player in period.player_data_assoc:
        player_data = get_player_data(player, match_id)
        last_period = None
        for player_period in player_data:
            if last_period is None:
                last_period = player_period
            else:
                spectator = check_if_spectator(last_period, player_period)

                if spectator:
                    db.session.delete(player_period)
                    db.session.commit()
                else:
                    last_period = player_period


def check_if_spectator(last_period, player_period):
    tests = ['goals', 'shots', 'assists', 'saves', 'primary_assists', 'secondary_assists',
             'passes', 'blocks', 'takeaways', 'turnovers', 'game_winning_goals',
             'overtime_goals', 'post_hits', 'faceoffs_won', 'faceoffs_lost',
             'score', 'possession_time_sec']
    for test in tests:
        if getattr(last_period, test) != getattr(player_period, test):
            return False
    return True


def get_player_data(player, match_id):
    import sqlalchemy as sa
    player_data = db.session.query(PlayerMatchData) \
        .join(PlayerMatchData.match) \
        .join(MatchData.lobby) \
        .filter(PlayerMatchData.player_id == player.player_id) \
        .filter(Lobby.match_id == match_id) \
        .order_by(sa.asc(PlayerMatchData.current_period))
    return player_data


def check_number_of_periods(num_periods, correct_periods, match_id):
    if num_periods == correct_periods:
        return 0

    raise_flag(match_id, f'{num_periods} periods were recorded, should be {correct_periods}')
    return 1


def check_periods_played_in_order(periods, correct_period_order, match_id):
    period_order = [period.current_period for period in periods]
    if period_order == correct_period_order:
        return 0

    raise_flag(match_id, 'Periods were not played in correct order')
    return 1


def check_players_and_teams(match, teams, periods):
    flags = 0

    players_data = get_players_data(match.id)

    flags = flags + check_players_on_teams_or_free_agents(match, players_data, teams, periods)

    return flags


def get_players_data(match_id):
    players_data = db.session.query(PlayerMatchData) \
        .join(PlayerMatchData.match) \
        .join(MatchData.lobby) \
        .filter(Lobby.match_id == match_id)
    return players_data


def check_players_on_teams_or_free_agents(match, players_data, teams, periods):
    players_on_wrong_team = []
    flags = 0
    for player_data in players_data:
        # check player has a current team
        wrong_team_entry, flags_raised = check_player_has_team_or_free_agent(player_data, match.season_division, match.id, teams)
        players_on_wrong_team = players_on_wrong_team + wrong_team_entry
        flags = flags + flags_raised

    flags = flags + check_over_wrong_teams(players_on_wrong_team, teams, players_data, periods, match.id)

    return flags


def check_player_has_team_or_free_agent(player_data, season_division, match_id, teams):
    wrong_team_entry = []
    flags = 0
    player_current_team = player_data.player.current_team(season_division.season)
    if not player_current_team:
        # check if player is a free agent
        player_free_agent = player_data.player.season_association.filter_by(
            season_division_id=season_division.id).first()
        if not player_free_agent:
            raise_flag(match_id, f'Player {player_data.player.player_name} is not registered to season '
                                 f'in either a team or as a free agent')
            flags = flags + 1

        # free agents added to wrong team to ensure the count doesnt get unbalanced
        wrong_team_entry.append(('FA', player_data.team_id))

    # check if players current team is part of the match
    elif player_current_team.team not in teams.values():
        raise_flag(match_id, f'Player {player_data.player.player_name} is not a member of either team in the match')
        flags = flags + 1

    # check if player is on correct team
    elif player_current_team.team.id != player_data.team_id:
        wrong_team_entry.append((player_current_team.team.id, player_data.team_id))

    return wrong_team_entry, flags


def check_over_wrong_teams(players_wrong_team, teams, players_data, periods, match_id):
    flags = 0
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
        flip_all_players(valid_teams, players_data, periods)

    else:
        # raise player on incorrect team flags
        for player_data in players_data:
            if player_data.player.current_team():
                if player_data.player.current_team().team.id != player_data.team_id:
                    raise_flag(match_id, f'Player {player_data.player.player_name} played period '
                                         f'{player_data.match.current_period} for the wrong team')
                    flags = flags + 1

    return flags


def flip_all_players(valid_teams, players_data, periods):
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


def finalize_checks(flags, match_id):
    periods = get_period_data(match_id)
    for period in periods:
        period.processed = True
        if flags == 0:
            period.accepted = True
        db.session.add(period)
        db.session.commit()
    if flags == 0:
        process_match_result.delay(match_id)


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

        # for each player, get their last recorded period for the game and mark it as one used for stat lookups
        period_ids = []
        for period in accepted_periods:
            period_ids.append(period.id)
        players_data = db.session.query(PlayerMatchData).filter(
            PlayerMatchData.match_id.in_(period_ids)
        )
        sorted_player_ids = []
        for player_data in players_data:
            if player_data.player_id not in sorted_player_ids:
                player_last_period = players_data.filter(
                    PlayerMatchData.player_id == player_data.player_id
                ).order_by(sa.desc(PlayerMatchData.current_period)).first()
                player_last_period.stat_total = True
                db.session.add(player_last_period)
                db.session.commit()
                sorted_player_ids.append(player_data.player_id)



