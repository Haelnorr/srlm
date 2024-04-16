"""Endpoint for linking a users steam account"""
from apifairy import body, response, authenticate, other_responses
from flask import Blueprint
from api.srlm.app import db
from api.srlm.app.api.auth.utils import app_auth
from api.srlm.app.api.users import users_bp
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import LinkSuccessSchema, LinkSteamSchema
from api.srlm.app.models import User, Player
from api.srlm.app.spapi.slapid import get_slap_id


steam = Blueprint('steam', __name__)
users_bp.register_blueprint(steam)


@steam.route('/<int:user_id>/steam', methods=['POST'])
@body(LinkSteamSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def link_user_steam(data, user_id):
    """Link a users steam account. Will connect the user to player data using their SlapID"""
    user = ensure_exists(User, id=user_id)

    force_fields(data, ['steam_id'])

    user.steam_id = data['steam_id']
    db.session.commit()

    response_json = get_slap_id(user.steam_id)
    if response_json.status_code == 200:
        slap_id = response_json.json()['id']

        player = ensure_exists(Player, return_none=True, slap_id=slap_id)

        if player is None:
            player = Player()
            player.slap_id = slap_id
            player.player_name = user.username
            db.session.add(player)
            db.session.commit()

        user.player = player
        db.session.commit()

        return responses.request_success(f'Player {player.player_name} successfully linked to user {user.username}', 'api.players.get_player', player_id=player.id)

    else:
        return responses.request_success(f'Slap ID not found for the given steam ID. Steam ID linked to user {user.username}', 'api.users.get_user', user_id=user.id)
