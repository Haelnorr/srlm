from celery import shared_task
from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.result import AsyncResult
from flask import redirect, url_for

from api.srlm.logger import get_logger
log = get_logger(__name__)


def create_lobby(match_id, lobby_settings):
    # get the details for creating a new lobby (match_id, password)
    log.info(f"You gave me {match_id} and {lobby_settings}")
    # generate the password
    # create a new lobby with the slap API
    # start monitoring the lobby using a lobby monitor task
    log.info('Starting a monitor!')
    task = lobby_monitor.delay(1, lobby_settings)
    # create a lobby object in the database and store the lobby_id, match_id, password and task_id
    # return success result
    log.info('Success!')
    return task.id


def task_result(task_id):
    result = AsyncResult(task_id)
    return {
        'ready': result.ready(),
        'successful': result.successful(),
        'value': result.result if result.ready() else None
    }


def cancel_task(task_id):
    task = AbortableAsyncResult(task_id)
    task.abort()


@shared_task(bind=True, base=AbortableTask)
def lobby_monitor(self, lobby_id, interval):
    # get lobby info from db
    import time

    max_time = 1            # max time for process in minutes
    i = 0                   # counts loop increments
    check_interval = 10     # how often to check for aborted in seconds
    finished = False        # loop controller
    monitor_interval = int(interval)   # how often the monitor will send an api request in seconds

    while not finished:
        if (i * check_interval) >= (max_time * 60):
            # checks if max time has elapsed
            return 'Aborted: Max time elapsed'
        if self.is_aborted():
            # checks if has been aborted
            return 'Aborted: Received abort request'

        i += 1

        if i % round(monitor_interval / check_interval) == 0:
            finished = True

        time.sleep(check_interval)


    return lobby_id
    # check after 2 minutes + match_length
    # enter control loop - max alive time and not aborted
        # check every match_length for status
        # if (periods_enabled is "True" and current_period >= 4) or (periods_enabled is "False" and current_period is 2) and in_game=false
            # tell a process_match_stats worker to get the match stats, wait for response
            # if good signal received, exit loop
    # if completed, destroy lobby, mark lobby as inactive
    # if no good signal received, tell a process_match_stats worker to get the match stats
    # terminate worker
    #pass


@shared_task
def process_match_stats(lobby_id):
    # get lobby info from db
    # request match stats
    # check match stats for correct number of valid periods
    # save each period into match_data, player_match_data and team_match_data
    # flag any potential issues or conflicts
    # if match data is valid and complete, return all good signal
    # if not, return not good signal
    pass
