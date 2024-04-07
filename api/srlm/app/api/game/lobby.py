"""Provides routes for generating and cancelling in game lobbies"""
from flask import request
from api.srlm.app.api.game import game_bp as game
from api.srlm.app.api.auth.utils import req_app_token
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import force_fields, ensure_exists
from api.srlm.app.models import Match, Lobby
from api.srlm.app.spapi.lobby_manager import generate_lobby
from api.srlm.app.task_manager.tasks import cancel_task


@game.route('/lobby', methods=['POST'])
@req_app_token
def generate_lobby():
    data = request.get_json()

    force_fields(data, ['match_id'])
    match = ensure_exists(Match, id=data['match_id'])

    generate_lobby(match)

    return responses.create_success(f'Created lobby for {match.home_team.name} vs {match.away_team.name}.', 'api.game.get_match', match_id=match.id)


@game.route('/lobby/<int:lobby_id>', methods=['DELETE'])
def abort_lobby(lobby_id):
    lobby = ensure_exists(Lobby, id=lobby_id)

    cancel_task(lobby.task_id)

    return responses.request_success(f'Lobby {lobby.id} aborted', 'api.game.get_match', match_id=lobby.match.id)
