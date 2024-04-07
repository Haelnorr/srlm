"""Endpoint for linking a users steam account"""
from flask import request
from api.srlm.app import db
from api.srlm.app.api.users import users_bp as users
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.models import User, Player
from api.srlm.app.spapi.slapid import get_slap_id


@users.route('/users/<int:user_id>/steam', methods=['POST'])
def link_user_steam(user_id):
    user = ensure_exists(User, id=user_id)

    data = request.get_json()
    force_fields(data, ['steam_id'])

    user.steam_id = data['steam_id']
    db.session.commit()

    response = get_slap_id(user.steam_id)
    if response.status_code == 200:
        slap_id = response.json()['id']

        player = ensure_exists(Player, return_none=True, slap_id=slap_id)

        if player is None:
            player = Player()
            player.slap_id = slap_id
            player.player_name = user.username
            db.session.add(player)
            db.session.commit()

        user.player = player
        db.session.commit()

        return responses.request_success(f'Player {player.player_name} succesfully linked to user {user.username}', 'api.users.get_player', player_id=player.id)

    else:
        return responses.request_success(f'Slap ID not found for the given steam ID. Steam ID linked to user {user.username}', 'api.users.get_user', user_id=user.id)
