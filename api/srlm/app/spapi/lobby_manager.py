"""This module provides methods that manage in-game lobbies and retrieve/process the game stats"""
import datetime
import random
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from api.srlm.app import db, create_app
from api.srlm.app.models import Lobby, MatchData, Player, PlayerMatchData
from api.srlm.app.spapi.lobby import create_lobby
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


def generate_lobby(match, current_period=1, initial_stats=None, initial_score=None, finals_game=None, delay=120):
    # Unpacking relevant objects from match object
    season = match.season_division.season
    division = match.season_division.division
    league = season.league
    match_type = season.match_type

    # TM1 vs TM2 (Finals - Game 1) || OSL PL-S19
    finals_insert = f'(Finals - Game {finals_game}) ' if finals_game else ''
    lobby_name = f'{match.home_team.acronym} vs {match.away_team.acronym} {finals_insert}|| {league.acronym}' \
                 f' {division.acronym} - {season.acronym}'

    # Random 3 digit number
    password = str(random.randint(100, 999))

    # OSL-LeagueAPI
    creator_name = f'{league.acronym}-LeagueAPI'

    lobby_settings = {
        'region': league.server_region_value,
        'name': 'Haelnorr Test Lobby',  # lobby_name, # TODO
        'password': password,
        'creator_name': 'Haelnorr',  # creator_name, # TODO
        'is_periods': match_type.periods,
        'arena': match_type.arena,
        'mercy_rule': match_type.mercy_rule,
        'match_length': match_type.match_length,
        'game_mode': match_type.game_mode,
        'current_period': current_period,
        'initial_stats': initial_stats,
    }
    if initial_score:
        lobby_settings['initial_score'] = initial_score

    # create a new lobby with the slap API
    slap_lobby_id = create_lobby(lobby_settings)

    # create a lobby object in the database and store the lobby_id, match_id, password
    lobby = Lobby()
    lobby.lobby_id = slap_lobby_id
    lobby.match = match
    lobby.password = password

    db.session.add(lobby)
    db.session.commit()

    # start monitoring the lobby using a lobby monitor task
    monitor_task = lobby_monitor.apply_async(args=[lobby.id], countdown=delay)

    # Store task_id in the database
    lobby.task_id = monitor_task.id
    db.session.commit()

    # return the lobby
    return lobby


@shared_task(bind=True, base=AbortableTask)
def lobby_monitor(self, lobby_id):
    app, celery = create_app()
    with app.app_context():
        import time
        import sqlalchemy as sa
        from api.srlm.app.models import Lobby
        from api.srlm.app.spapi.lobby import get_lobby, delete_lobby

        # get lobby info from db
        lobby = db.session.query(Lobby).filter_by(id=lobby_id).first()
        match_type = lobby.match.season_division.season.match_type
        log.info(f'Lobby {lobby.id} details pulled from database')

        max_time = 60  # max time for process in minutes
        i = 0  # counts loop increments
        check_interval = 10  # how often to check for abort signal in seconds
        finished = False  # loop controller
        end_reason = None  # used for return message and skip condition in loop
        retrieve_stats_task = None  # results from retrieve_stats_task

        # how often the monitor will check on the lobby via an API request
        # is based on match length (aka period length - default is 5 minutes)
        monitor_interval = match_type.match_length

        log.info(
            f'Initialized monitor ||| Max time: {max_time} minutes, Abort check interval: {check_interval} seconds,'
            f' API Request Interval: {monitor_interval} seconds ({monitor_interval / 60} minutes)')

        while not finished:
            if (i * check_interval) >= (max_time * 60):
                # checks if max time has elapsed
                end_reason = 'Aborted - Max time elapsed'
                finished = True
            elif self.is_aborted():
                # checks if has been aborted
                end_reason = 'Aborted - Received abort request'
                finished = True

            # counts the loops, used for math
            i += 1

            # checks if a match result has been parsed from the API
            if retrieve_stats_task:
                # check if it was successful
                if retrieve_stats_task.state == 'SUCCESS':
                    period_data = db.session.query(MatchData).filter_by(
                        lobby_id=lobby.id,
                        periods_enabled=match_type.periods,
                        gamemode=match_type.game_mode
                    ).order_by(sa.asc(MatchData.current_period))
                    periods_valid = []
                    current_period = 1
                    for period in period_data:
                        if period.current_period == current_period:
                            player_count = db.session.query(PlayerMatchData).filter_by(
                                match_id=period.id
                            ).count()
                            if player_count == match_type.num_players:
                                periods_valid.append(current_period)
                                current_period += 1

                    if (periods_valid == [1, 2, 3] and match_type.periods) or (
                            periods_valid == [1] and not match_type.periods):
                        # looks like the match was completed with the correct number of periods and players
                        validate_stats.delay(lobby.match.id)
                        end_reason = 'Match results recorded'
                        finished = True
                        log.info('Match data retrieved successfully, requesting validation of data')
                    else:
                        retrieve_stats_task = None
                        # retrieved stats incomplete, need to wait for a new result

            # math to determine if API request should be made - skipped if task has been told to abort this loop
            if i % round(monitor_interval / check_interval) == 0 and not end_reason:
                # make API request
                log.info('Making API request')
                lobby_resp = get_lobby(lobby.lobby_id)
                if lobby_resp.status_code == 200:
                    lobby_info = lobby_resp.json()
                    log.info(f"Period: {lobby_info['current_period']} | In-Game: {lobby_info['in_game']}")
                    if (lobby_info['periods_enabled'] and lobby_info['current_period'] > 3) or (
                            not lobby_info['periods_enabled'] and lobby_info['current_period'] > 1):
                        # looks like match is completed - tell another worker to get the match results
                        log.info('Detected possible match completion, requesting match data')
                        retrieve_stats_task = get_match_data.delay(lobby.id)

            time.sleep(check_interval)

        # control loop exited, time to clean up
        log.info(f'Monitor closing. Reason: {end_reason}')

        # destroy the lobby in-game
        delete = delete_lobby(lobby.lobby_id)
        log.info(f'Delete lobby request sent: Status code {delete}')

        # mark lobby as inactive in database
        if delete == 200:
            lobby.active = False
            db.session.commit()
            log.info('Lobby marked as inactive')

        # check if get_match_data was run and found correct number of periods
        # if no good signal received, tell a get_match_data worker to get the match stats
        if end_reason != 'Match results recorded':
            log.info('Lobby closing without completed match data - making final match data request')
            get_match_data.delay(lobby.id)

        return {
            'end_reason': f'Lobby closed: {end_reason}',
            'lobby_deleted': delete
        }


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
                result = parse_match_stats(match, teams, lobby)

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
            'created': datetime.datetime.strptime(match['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
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
            db.session.add(MatchReview(reason='Multiple lobbies created for match', **defaults))

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

            if period.player_data_assoc.count() != match_type.num_players:
                db.session.add(
                    MatchReview(reason=f'Period {period.current_period} had incorrect number of players.', **defaults))

        # check num periods
        if periods.count() != correct_periods:
            db.session.add(
                MatchReview(reason=f'{periods.count()} periods were recorded, should be {correct_periods}', **defaults))
        # check periods played in order
        elif period_order != correct_period_order:
            db.session.add(MatchReview(reason='Periods were not played in correct order', **defaults))

        # check player count
        players_data = db.session.query(PlayerMatchData).filter(PlayerMatchData.match_id.in_(period_ids))
        if round(players_data.count() / periods.count()) != match_type.num_players:
            db.session.add(
                MatchReview(reason=f'Invalid number of players. Had {round(players_data.count() / periods.count())}, '
                                   f'should be {match_type.num_players}', **defaults))

        # check players/teams
        players_wrong_team = []
        # check all players are registered to a team in the match or are free agents in the current season
        for player_data in players_data:
            # check player has a current team
            player_current_team = player_data.player.current_team()
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
        if len(players_wrong_team) != (match_type.num_players * correct_periods):
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
                period.winner = flip_team_label[period.winner]
                period.home_score, period.away_score = period.away_score, period.home_score
                db.session.add(period)

            db.session.commit()
        else:
            # raise player on incorrect team flags
            for player_data in players_data:
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
        from datetime import datetime, timezone, timedelta
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
