import datetime
import os
import random
from celery import shared_task, current_app
from celery.contrib.abortable import AbortableTask

from api.srlm.app import db, create_app
from api.srlm.app.models import Lobby, MatchData, Player, PlayerMatchData
from api.srlm.app.spapi.lobby import create_lobby
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)

app, celery = create_app()


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
        'name': 'Haelnorr Test Lobby',#lobby_name, # TODO
        'password': password,
        'creator_name': 'Haelnorr',#creator_name, # TODO
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
    with app.app_context():
        import time
        from api.srlm.app.models import Lobby
        from api.srlm.app.spapi.lobby import get_lobby, delete_lobby

        # get lobby info from db
        lobby = db.session.query(Lobby).filter_by(id=lobby_id).first()
        log.info(f'Lobby {lobby.id} details pulled from database')

        max_time = 1           # max time for process in minutes # TODO
        i = 0                   # counts loop increments
        check_interval = 10     # how often to check for abort signal in seconds
        finished = False        # loop controller
        end_reason = None           # used for return message and skip condition in loop
        parse_stats_task = None     # results from parse_stats_task
        process_stats_task = None   # results from process_stats_task

        # how often the monitor will check on the lobby via an API request
        # is based on match length (aka period length - default is 5 minutes)
        monitor_interval = lobby.match.season_division.season.match_type.match_length

        log.info(f'Initialized monitor ||| Max time: {max_time} minutes, Abort check interval: {check_interval} seconds,'
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
            if parse_stats_task:
                if parse_stats_task.state == 'FAILURE' or (parse_stats_task.state == 'SUCCESS' and not parse_stats_task.result):
                    log.info('Detected failed match data retrieval. Ignoring results')
                    parse_stats_task = None
                # checks if a match result has been stored in the DB, calls process task to review the stored data
                elif parse_stats_task.state == 'SUCCESS' and parse_stats_task.result:
                    log.info('Match data retrieved successfully, requesting processing of data')
                    # process_stats_task = process_match_stats.delay(parse_stats_task.result) # TODO

            # check if process_stats_task was run and completed successfully
            if process_stats_task:
                if process_stats_task.value == 'Match stats validated':
                    # if good signal received, exit from loop
                    log.info('Match results recorded - exiting monitor')
                    end_reason = 'Match results recorded'
                    finished = True

            # math to determine if API request should be made - skipped if task has been told to abort this loop
            if i % round(monitor_interval / check_interval) == 0 and not end_reason:
                # make API request
                log.info('Making API request')
                lobby_resp = get_lobby(lobby.lobby_id)
                if lobby_resp.status_code == 200:
                    lobby_info = lobby_resp.json()
                    log.info(f"Period: {lobby_info['current_period']} | In-Game: {lobby_info['in_game']}")
                    if (lobby_info['periods_enabled'] and lobby_info['current_period'] > 3) or (not lobby_info['periods_enabled'] and lobby_info['current_period'] > 1):
                        # looks like match is completed - tell another worker to get the match results
                        log.info('Detected possible match completion, requesting match data')
                        parse_stats_task = get_match_data.delay(lobby.id)

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

        # check if process_stats_task was run and completed successfully
        # if no good signal received, tell a get_match_data worker to get the match stats
        if end_reason != 'Match results recorded':
            log.info('Lobby closing without completed match data - making final match data request')
            match_ids = get_match_data.delay(lobby.id)
            # process stats from above ^ # TODO

        return {
            'end_reason': f'Lobby closed: {end_reason}',
            'lobby_deleted': delete
        }


@shared_task
def get_match_data(lobby_id):
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

        success = True   # defaults to true for comparison logic
        match_data_ids = []

        # save each period into match_data and player_match_data
        if match_response.status_code == 200:
            for match in match_response.json():
                log.info('Match data found')
                # attempts to parse match data and store in DB - returns match_data.id or False
                log.info('Parsing match stats')
                log.info(lobby.id)
                result = parse_match_stats(match, teams, lobby)

                if result:
                    match_data_ids.append(result)
                # if any of the match results fail to process, will change success to False
                success = success and result

        return match_data_ids if success else False


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
                player.first_season_id = lobby.match_db.season_division_id
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
