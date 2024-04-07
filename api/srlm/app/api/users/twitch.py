"""Endpoints for managing Twitch linking"""
from apifairy import response, authenticate, other_responses, body
from flask import request
from api.srlm.app import db
from api.srlm.app.api.users import users_bp as users
from api.srlm.app.api.auth.utils import req_app_token, user_auth, get_bearer_token
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.errors import ResourceNotFound, UserAuthError, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, clean_data
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request, forbidden
from api.srlm.app.fairy.schemas import LinkSuccessSchema, TwitchSchema, UpdateTwitchSchema
from api.srlm.app.models import User, Twitch


@users.route('/users/<int:user_id>/twitch', methods=['GET'])
@req_app_token
@response(TwitchSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def get_user_twitch(user_id):
    """Get a users Twitch information"""
    user_token = get_bearer_token(request.headers)['user']
    user = ensure_exists(User, id=user_id)

    authenticated = False
    if user is User.check_token(user_token):
        authenticated = True

    if user.twitch is None:
        raise ResourceNotFound(f'User with ID {user_id} does not have a linked Twitch account')

    return user.twitch.to_dict(authenticated=authenticated)


@users.route('/users/<int:user_id>/twitch', methods=['POST'])
@req_app_token
@user_auth.login_required
@body(TwitchSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(user_auth)
@other_responses(unauthorized | forbidden | not_found | bad_request)
def create_user_twitch(user_id):
    """Link a users Twitch account. Requires user token"""
    user = ensure_exists(User, id=user_id)

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.twitch:
        raise BadRequest('User already has a linked Twitch account')

    data = request.get_json()

    required_fields = valid_fields = ['twitch_id', 'access_token', 'refresh_token', 'expires_in']

    force_fields(data, required_fields)

    twitch = db.session.query(Twitch).filter(Twitch.twitch_id == data['twitch_id']).first()
    if twitch is not None:
        raise BadRequest('Twitch account is linked to another user')

    twitch = Twitch()
    twitch.from_dict(clean_data(data, valid_fields))
    twitch.user = user

    db.session.add(twitch)
    db.session.commit()

    return responses.create_success('Twitch account linked', 'api.users.get_user_twitch', user_id=user_id)


@users.route('/users/<int:user_id>/twitch', methods=['PUT'])
@req_app_token
@user_auth.login_required
@body(UpdateTwitchSchema())
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | forbidden | not_found | bad_request)
def update_user_twitch(user_id):
    """Update a users Twitch information. Requires user token"""
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.twitch is None:
        raise BadRequest('User does not have a linked Twitch account')

    data = request.get_json()

    valid_fields = False
    for field in ['twitch_id', 'access_token', 'refresh_token', 'expires_in']:
        if field in data:
            valid_fields = True

    if not valid_fields:
        raise BadRequest("No valid fields provided - provide one of the following: twitch_id, access_token, refresh_token, expires_in")

    if 'twitch_id' in data:
        twitch = db.session.query(Twitch).filter(Twitch.twitch_id == data['twitch_id']).first()
        if twitch is not None:
            raise BadRequest('Twitch account is linked to another user')

    user.twitch.from_dict(data)
    db.session.commit()

    return responses.request_success('Twitch account updated', 'api.users.get_user_twitch', user_id=user_id)


@users.route('/users/<int:user_id>/twitch', methods=['DELETE'])
@req_app_token
@user_auth.login_required
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | forbidden | not_found)
def delete_user_twitch(user_id):
    """Unlink a users Twitch account. Requires user token"""
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.twitch is None:
        raise BadRequest('User does not have a linked Twitch account')

    db.session.query(Twitch).filter(Twitch.user_id == user.id).delete()
    db.session.commit()

    return responses.request_success('Twitch account unlinked', 'api.users.get_user', user_id=user_id)
