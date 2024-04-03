import os
# TODO DELETE THIS FILE
import requests
from flask import url_for, render_template

from api.srlm.app.api import bp
from api.srlm.app.api.functions import ensure_exists
from api.srlm.app.models import Match, Lobby, SeasonDivision
from api.srlm.app.spapi.lobby_manager import generate_lobby
from api.srlm.app.task_manager.tasks import task_result, cancel_task


@bp.route('/', methods=['GET'])
def test():
    request = get_matches_in_season_division(41)

    return render_template('test.html', matches=request['matches'])


def get_matches_in_season_division(season_division_id):
    season_division = ensure_exists(SeasonDivision, id=season_division_id)
    matches = []
    for match in season_division.matches:
        if match.results is None:
            matches.append(match.to_simple_dict())

    response = season_division.to_simple_dict()
    response['matches'] = matches
    return response


@bp.route('/test/get_task/<task_id>', methods=['GET'])
def get_task(task_id):
    return task_result(task_id)


@bp.route('/test/abort_lobby/<lobby_id>', methods=['GET'])
def abort_lobby(lobby_id):
    lobby = ensure_exists(Lobby, id=lobby_id)
    cancel_task(lobby.task_id)
    return f'Cancelled task {lobby.task_id} - <a href="{url_for("api.test")}">View matches</a>: '


@bp.route('/test/lobby/<match_id>', methods=['GET'])
def add_test_lobby(match_id):
    match = ensure_exists(Match, id=match_id)
    result = generate_lobby(match, delay=0)
    return f'Created lobby for match {match.id} - <a href="{url_for("api.test")}">View matches</a>: '

