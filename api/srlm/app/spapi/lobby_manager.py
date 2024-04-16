"""This module provides methods that manage in-game lobbies and retrieve/process the game stats"""
import random
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from api.srlm.app import db, create_app
from api.srlm.app.models import Lobby, MatchData, PlayerMatchData
from api.srlm.app.spapi.lobby import create_lobby
from api.srlm.app.api.game.utils import validate_stats, get_match_data
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
        'name': lobby_name,
        'password': password,
        'creator_name': creator_name,
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
