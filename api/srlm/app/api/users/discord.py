"""Endpoints for managing Discord linking"""
from apifairy import body, response, authenticate, other_responses
from flask import request, Blueprint
from api.srlm.app import db
from api.srlm.app.api.users import users_bp
from api.srlm.app.api.auth.utils import user_auth, get_bearer_token, dual_auth, app_auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.errors import ResourceNotFound, UserAuthError, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import DiscordSchema, LinkSuccessSchema, UpdateDiscordSchema
from api.srlm.app.models import User, Discord


discord = Blueprint('discord', __name__)
users_bp.register_blueprint(discord)


@discord.route('/<int:user_id>/discord', methods=['GET'])
@response(DiscordSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_user_discord(user_id):
    """Get a users Discord information"""
    user_token = get_bearer_token(request.headers)['user']
    user = ensure_exists(User, id=user_id)

    authenticated = False
    if user is User.check_token(user_token):
        authenticated = True

    if user.discord is None:
        raise ResourceNotFound(f'User with ID {user_id} does not have a linked Discord account')

    return user.discord.to_dict(authenticated=authenticated)


@discord.route('/<int:user_id>/discord', methods=['POST'])
@body(DiscordSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(dual_auth)
@other_responses(unauthorized | not_found | bad_request)
def create_user_discord(data, user_id):
    """Link a users Discord account. Requires user token"""
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord:
        raise BadRequest('User already has a linked Discord account')

    required_fields = ['discord_id', 'access_token', 'refresh_token', 'expires_in']
    force_fields(data, required_fields)

    discord_db = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
    if discord_db is not None:
        raise BadRequest('Discord account is linked to another user')

    discord_db = Discord()
    discord_db.from_dict(data)
    discord_db.user = user

    db.session.add(discord_db)
    db.session.commit()

    return responses.create_success('Discord account linked', 'api.users.discord.get_user_discord', user_id=user_id)


@discord.route('/<int:user_id>/discord', methods=['PUT'])
@body(UpdateDiscordSchema())
@response(LinkSuccessSchema())
@authenticate(dual_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_user_discord(user_id):
    """Update a users Discord information. Requires user token"""
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
        discord_db = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
        if discord_db is not None:
            raise BadRequest('Discord account is linked to another user')

    user.discord.from_dict(data)
    db.session.commit()

    return responses.request_success('Discord account updated', 'api.users.discord.get_user_discord', user_id=user_id)


@discord.route('/<int:user_id>/discord', methods=['DELETE'])
@response(LinkSuccessSchema())
@authenticate(dual_auth)
@other_responses(unauthorized | not_found | bad_request)
def delete_user_discord(user_id):
    """Unlink a users Discord account. Requires user token"""
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord is None:
        raise BadRequest('User does not have a linked Discord account')

    db.session.query(Discord).filter(Discord.user_id == user.id).delete()
    db.session.commit()

    return responses.request_success('Discord account unlinked', 'api.users.get_user', user_id=user_id)
