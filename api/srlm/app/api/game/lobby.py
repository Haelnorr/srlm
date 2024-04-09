"""Provides routes for generating and cancelling in game lobbies"""
from apifairy import body, response, authenticate, other_responses
from flask import request, Blueprint
from api.srlm.app.api import bp
from api.srlm.app.api.auth.utils import app_auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import force_fields, ensure_exists
from api.srlm.app.fairy.errors import unauthorized, bad_request, not_found
from api.srlm.app.fairy.schemas import GenerateLobbySchema, LinkSuccessSchema, BasicSuccessSchema
from api.srlm.app.models import Match, Lobby
from api.srlm.app.spapi.lobby_manager import generate_lobby
from api.srlm.app.task_manager.tasks import cancel_task


lobby = Blueprint('lobby', __name__)
bp.register_blueprint(lobby, url_prefix='/lobby')


@lobby.route('', methods=['POST'])
@body(GenerateLobbySchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request | not_found)
def generate_lobby():
    """Generate a new in-game lobby"""
    data = request.get_json()

    force_fields(data, ['match_id'])
    match = ensure_exists(Match, id=data['match_id'])

    generate_lobby(match)

    return responses.create_success(f'Created lobby for {match.home_team.name} vs {match.away_team.name}.', 'api.match.get_match', match_id=match.id)


@lobby.route('/<int:lobby_id>', methods=['DELETE'])
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def abort_lobby(lobby_id):
    """Delete an active in-game lobby"""
    lobby = ensure_exists(Lobby, id=lobby_id)

    cancel_task(lobby.task_id)

    return responses.request_success(f'Lobby {lobby.id} aborted', 'api.match.get_match', match_id=lobby.match.id)
