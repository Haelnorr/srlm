"""Endpoints for managing Discord linking"""
from flask import request
from api.srlm.app import db
from api.srlm.app.api.users import users_bp as users
from api.srlm.app.api.auth.utils import req_app_token, user_auth, get_bearer_token
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.errors import ResourceNotFound, UserAuthError, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.models import User, Discord


@users.route('/users/<int:user_id>/discord', methods=['GET'])
@req_app_token
def get_user_discord(user_id):
    user_token = get_bearer_token(request.headers)['user']
    user = ensure_exists(User, id=user_id)

    authenticated = False
    if user is User.check_token(user_token):
        authenticated = True

    if user.discord is None:
        raise ResourceNotFound(f'User with ID {user_id} does not have a linked Discord account')

    return user.discord.to_dict(authenticated=authenticated)


@users.route('/users/<int:user_id>/discord', methods=['POST'])
@req_app_token
@user_auth.login_required
def create_user_discord(user_id):
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord:
        raise BadRequest('User already has a linked Discord account')

    data = request.get_json()

    required_fields = ['discord_id', 'access_token', 'refresh_token', 'expires_in']
    force_fields(data, required_fields)

    discord = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
    if discord is not None:
        raise BadRequest('Discord account is linked to another user')

    discord = Discord()
    discord.from_dict(data)
    discord.user = user

    db.session.add(discord)
    db.session.commit()

    return responses.create_success('Discord account linked', 'api.users.get_user_discord', user_id=user_id)


@users.route('/users/<int:user_id>/discord', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user_discord(user_id):
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord is None:
        raise BadRequest('User does not have a linked Discord account')

    data = request.get_json()

    valid_fields = False
    for field in ['discord_id', 'access_token', 'refresh_token', 'expires_in']:
        if field in data:
            valid_fields = True

    if not valid_fields:
        raise BadRequest("No valid fields provided - provide one of the following: discord_id, access_token, refresh_token, expires_in")

    if 'discord_id' in data:
        discord = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
        if discord is not None:
            raise BadRequest('Discord account is linked to another user')

    user.discord.from_dict(data)
    db.session.commit()

    return responses.request_success('Discord account updated', 'api.users.get_user_discord', user_id=user_id)


@users.route('/users/<int:user_id>/discord', methods=['DELETE'])
@req_app_token
@user_auth.login_required
def delete_user_discord(user_id):
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord is None:
        raise BadRequest('User does not have a linked Discord account')

    db.session.query(Discord).filter(Discord.user_id == user.id).delete()
    db.session.commit()

    return responses.request_success('Discord account unlinked', 'api.users.get_user', user_id=user_id)
