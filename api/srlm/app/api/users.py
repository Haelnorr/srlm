import sqlalchemy as sa
from flask import request, url_for
from api.srlm.app import db
from api.srlm.app.api import bp, responses
from api.srlm.app.api.functions import force_fields, force_unique, clean_data, ensure_exists
from api.srlm.app.models import User, Permission, UserPermissions, Discord, Twitch
from api.srlm.app.api.errors import UserAuthError, ResourceNotFound, BadRequest, error_response
from api.srlm.app.api.auth import user_auth, req_app_token
from api.srlm.app.auth.functions import check_username_exists, check_email_exists, get_bearer_token
from api.srlm.app.auth.email import send_password_reset_email

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/users/<int:user_id>', methods=['GET'])
@req_app_token
def get_user(user_id):
    user = ensure_exists(User, id=user_id)
    user_token = get_bearer_token(request.headers)['user']
    current_user = User.check_token(user_token)

    include_email = False

    if current_user and current_user.id == user.id:
        include_email = True

    return user.to_dict(include_email=include_email)


@bp.route('/users', methods=['GET'])
@req_app_token
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(sa.select(User), page, per_page, 'api.get_users')


@bp.route('/users', methods=['POST'])
@req_app_token
def add_user():
    data = request.get_json()

    required_fields = valid_fields = ['username', 'email', 'password']
    unique_fields = ['username', 'email']

    force_fields(data, required_fields)
    force_unique(User, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    user = User()
    user.from_dict(cleaned_data, new_user=True)

    db.session.add(user)
    db.session.commit()

    return responses.create_success(f'User {user.username} added', 'api.get_user', user_id=user.id)


@bp.route('/users/<int:user_id>', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user(user_id):
    if user_auth.current_user().id != user_id:
        raise UserAuthError()
    data = request.get_json()

    user = ensure_exists(User, id=user_id)

    unique_fields = valid_fields = ['username', 'email']

    force_unique(User, data, unique_fields, self_id=user.id)

    user.from_dict(clean_data(data, valid_fields))
    db.session.commit()
    return responses.request_success(f'User {user.username} updated', 'api.get_user', user_id=user.id)


@bp.route('/users/<int:user_id>/new_password', methods=['POST'])
@req_app_token
@user_auth.login_required
def update_user_password(user_id):
    if user_auth.current_user().id != user_id:
        raise UserAuthError()
    user = ensure_exists(User, id=user_id)
    data = request.get_json()
    if 'password' not in data:
        raise BadRequest('Password field missing')

    user.set_password(data['password'])
    user.reset_pass = False
    user.revoke_token()
    token = user.get_token()
    db.session.commit()

    response = {
        'token': token,
        'expires': user.token_expiration
    }
    return response


@bp.route('/users/<int:user_id>/matches_streamed', methods=['GET'])
@req_app_token
def get_user_matches_streamed(user_id):
    pass


@bp.route('/users/<int:user_id>/matches_reviewed', methods=['GET'])
@req_app_token
def get_user_matches_reviewed(user_id):
    pass


@bp.route('/users/<int:user_id>/permissions', methods=['GET'])
@req_app_token
def get_user_permissions(user_id):
    user = ensure_exists(User, id=user_id)

    permissions = []
    for user_permission in user.permission_assoc:
        permissions.append(user_permission.to_dict())

    response = {
        'username': user.username,
        'permissions': permissions,
        '_links': {
            'self': url_for('api.get_user_permissions', user_id=user_id)
        }
    }

    return response


@bp.route('/users/<int:user_id>/permissions', methods=['POST'])
@req_app_token
def add_user_permissions(user_id):
    user = ensure_exists(User, id=user_id)

    data = request.get_json()
    if 'key' not in data:
        raise BadRequest("Permission 'key' field missing")
    permission = db.session.query(Permission).filter(Permission.key == data['key']).first()
    if permission is None:
        raise ResourceNotFound(f"Permission with key {data['key']}")
    if user.has_permission(permission.key):
        raise BadRequest('User already has the specified permission')

    user_perm = UserPermissions(user=user, permission=permission)

    if 'modifiers' in data:
        modifiers = data['modifiers']
        user_perm.additional_modifiers = modifiers

    db.session.add(user_perm)
    db.session.commit()

    return responses.create_success(f'Permission {user_perm.permssion.key} added to user {user_perm.user.username}', 'api.get_user_permissions', user_id=user_id)


@bp.route('/users/<int:user_id>/permissions', methods=['PUT'])
@req_app_token
def update_user_permissions(user_id):
    user = ensure_exists(User, id=user_id)
    data = request.get_json()

    required_fields = ['key', 'modifiers']

    force_fields(data, required_fields)

    permission = ensure_exists(Permission, key=data['key'])

    user_perm = ensure_exists(UserPermissions, user_id=user.id, permission_id=permission.id)

    modifiers = data['modifiers']
    if data['modifiers'] == "":
        modifiers = None
    user_perm.additional_modifiers = modifiers
    db.session.commit()

    return responses.create_success(f'Permission {user_perm.permssion.key} updated for user {user_perm.user.username}', 'api.get_user_permissions', user_id=user_id)


@bp.route('/users/<int:user_id>/permissions/revoke', methods=['POST'])
@req_app_token
def revoke_user_permissions(user_id):
    user = ensure_exists(User, id=user_id)
    data = request.get_json()

    force_fields(data, ['key'])

    permission = ensure_exists(Permission, key=data['key'])

    user_perm = ensure_exists(UserPermissions, return_none=True, user_id=user.id, permission_id=permission.id)
    if user_perm is None:
        raise ResourceNotFound(f"User {user.username} does not have the '{permission.key}' permission")

    db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).delete()
    db.session.commit()

    return responses.create_success(f'Permission {permission.key} revoked from user {user.username}', 'api.get_user_permissions', user_id=user_id)


@bp.route('/users/<int:user_id>/discord', methods=['GET'])
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


@bp.route('/users/<int:user_id>/discord', methods=['POST'])
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

    return responses.create_success('Discord account linked', 'api.get_user_discord', user_id=user_id)


@bp.route('/users/<int:user_id>/discord', methods=['PUT'])
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

    return responses.request_success('Discord account updated', 'api.get_user_discord', user_id=user_id)


@bp.route('/users/<int:user_id>/discord', methods=['DELETE'])
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

    return responses.request_success('Discord account unlinked', 'api.get_user', user_id=user_id)


@bp.route('/users/<int:user_id>/twitch', methods=['GET'])
@req_app_token
def get_user_twitch(user_id):
    user_token = get_bearer_token(request.headers)['user']
    user = ensure_exists(User, id=user_id)

    authenticated = False
    if user is User.check_token(user_token):
        authenticated = True

    if user.twitch is None:
        raise ResourceNotFound(f'User with ID {user_id} does not have a linked Twitch account')

    return user.twitch.to_dict(authenticated=authenticated)


@bp.route('/users/<int:user_id>/twitch', methods=['POST'])
@req_app_token
@user_auth.login_required
def create_user_twitch(user_id):
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

    return responses.create_success('Twitch account linked', 'api.get_user_twitch', user_id=user_id)


@bp.route('/users/<int:user_id>/twitch', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user_twitch(user_id):
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

    return responses.request_success('Twitch account updated', 'api.get_user_twitch', user_id=user_id)


@bp.route('/users/<int:user_id>/twitch', methods=['DELETE'])
@req_app_token
@user_auth.login_required
def delete_user_twitch(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.twitch is None:
        raise BadRequest('User does not have a linked Twitch account')

    db.session.query(Twitch).filter(Twitch.user_id == user.id).delete()
    db.session.commit()

    return responses.request_success('Twitch account unlinked', 'api.get_user', user_id=user_id)


@bp.route('/users/forgot_password', methods=['POST'])
@req_app_token
def request_password_reset():
    data = request.get_json()

    if 'username' not in data and 'email' not in data:
        raise BadRequest("No valid fields provided. Provide either 'username' or 'email'")

    valid_fields = ['username', 'email']
    search_args = clean_data(data, valid_fields)

    user = ensure_exists(User, join_method='or', **search_args)

    send_password_reset_email(user)

    response = {
        'result': 'success',
        'user': user.id,
        '_links': {
            'user': url_for('api.get_user', user_id=user.id)
        }
    }
    return response


@bp.route('/users/forgot_password/<reset_token>', methods=['GET'])
@req_app_token
def get_temp_token(reset_token):
    user = User.verify_reset_password_token(reset_token)
    if not user:
        return error_response(401, 'Password reset token is invalid or expired.')

    user.revoke_token()
    token = user.get_token(expires_in=300)
    user.reset_pass = True
    db.session.commit()
    return {'token': token, 'expires': user.token_expiration}
