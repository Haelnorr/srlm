import sqlalchemy as sa
from flask import request, url_for
from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.models import User, Permission, UserPermissions, Discord
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
    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)

    include_email = False

    if user and user.id == user_id:
        include_email = True

    return User.query.get_or_404(user_id).to_dict(include_email=include_email)


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
    if 'username' not in data or 'email' not in data or 'password' not in data:
        raise BadRequest('Username, Email or Password field missing')
    if check_username_exists(data['username']):
        raise BadRequest('Username is not unique')
    if check_email_exists(data['email']):
        raise BadRequest('Email is not unique')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201, {'Location': url_for('api.get_user', user_id=user.id)}


@bp.route('/users/<int:user_id>', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user(user_id):
    if user_auth.current_user().id != user_id:
        raise UserAuthError()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and check_username_exists(data['username']):
        raise BadRequest('Username is not unique')
    if 'email' in data and data['email'] != user.email and check_email_exists(data['email']):
        raise BadRequest('Email is not unique')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()


@bp.route('/users/<int:user_id>/new_password', methods=['POST'])
@req_app_token
@user_auth.login_required
def update_user_password(user_id):
    if user_auth.current_user().id != user_id:
        raise UserAuthError()
    user = User.query.get_or_404(user_id)
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
    user = db.session.get(User, user_id)
    if not user:
        raise ResourceNotFound(f'User with ID {user_id}')

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
    user = db.session.get(User, user_id)
    if not user:
        raise ResourceNotFound(f'User with ID {user_id}')

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

    return get_user_permissions(user_id)


@bp.route('/users/<int:user_id>/permissions', methods=['PUT'])
@req_app_token
def update_user_permissions(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ResourceNotFound(f'User with ID {user_id}')

    data = request.get_json()
    if 'key' not in data:
        raise BadRequest("Permission 'key' field missing")
    permission = db.session.query(Permission).filter(Permission.key == data['key']).first()
    if permission is None:
        raise ResourceNotFound(f"Permission with key {data['key']}")

    if 'modifiers' not in data:
        raise BadRequest('Modifiers field missing')

    user_perm = db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).first()

    if user_perm is None:
        raise BadRequest('User does not have that permission')

    modifiers = data['modifiers']
    if data['modifiers'] == "":
        modifiers = None
    user_perm.additional_modifiers = modifiers
    db.session.commit()

    return get_user_permissions(user_id)


@bp.route('/users/<int:user_id>/permissions/revoke', methods=['POST'])
@req_app_token
def revoke_user_permissions(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ResourceNotFound(f'User with ID {user_id}')

    data = request.get_json()
    if 'key' not in data:
        raise BadRequest("Permission 'key' field missing")
    permission = db.session.query(Permission).filter(Permission.key == data['key']).first()
    if permission is None:
        raise ResourceNotFound(f"Permission with key {data['key']}")

    user_perm = db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).first()

    if user_perm is None:
        raise BadRequest('User does not have that permission')

    db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).delete()
    db.session.commit()

    return get_user_permissions(user_id)


@bp.route('/users/<int:user_id>/discord', methods=['GET'])
@req_app_token
def get_user_discord(user_id):
    user_token = get_bearer_token(request.headers)['user']
    user = db.session.get(User, user_id)

    authenticated = False
    if user is User.check_token(user_token):
        authenticated = True

    if not user:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.discord is None:
        raise ResourceNotFound(f'User with ID {user_id} does not have a linked discord account')

    return user.discord.to_dict(authenticated=authenticated)


@bp.route('/users/<int:user_id>/discord', methods=['POST'])
@req_app_token
@user_auth.login_required
def create_user_discord(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord:
        raise BadRequest('User already has a linked discord account')

    data = request.get_json()

    if ('discord_id' and 'access_token' and 'refresh_token' and 'expires_in') not in data:
        raise BadRequest("Missing field(s) - requires discord_id, access_token, refresh_token, expires_in")

    discord = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
    if discord is not None:
        raise BadRequest('Discord account is linked to another user')

    discord = Discord()
    discord.from_dict(data)
    discord.user = user

    db.session.add(discord)
    db.session.commit()

    return user.discord.to_dict(authenticated=True)


@bp.route('/users/<int:user_id>/discord', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user_discord(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord is None:
        raise BadRequest('User does not have a linked discord account')

    data = request.get_json()

    if ('discord_id' or 'access_token' or 'refresh_token' or 'expires_in') not in data:
        raise BadRequest("No valid fields provided - provide one of the following: discord_id, access_token, refresh_token, expires_in")

    discord = db.session.query(Discord).filter(Discord.discord_id == data['discord_id']).first()
    if discord is not None:
        raise BadRequest('Discord account is linked to another user')

    user.discord.from_dict(data)
    db.session.commit()

    return user.discord.to_dict(authenticated=True)


@bp.route('/users/<int:user_id>/discord', methods=['DELETE'])
@req_app_token
@user_auth.login_required
def delete_user_discord(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise ResourceNotFound(f'User with ID {user_id}')

    if user.id is not user_auth.current_user().id:
        raise UserAuthError()

    if user.discord is None:
        raise BadRequest('User does not have a linked discord account')

    db.session.query(Discord).filter(Discord.user_id == user.id).delete()
    db.session.commit()

    return '', 200


@bp.route('/users/forgot_password', methods=['POST'])
@req_app_token
def request_password_reset():
    data = request.get_json()
    user = None
    if 'username' not in data and 'email' not in data:
        raise BadRequest('Username or Email field missing')

    if 'username' in data and not check_username_exists(data['username']):
        raise ResourceNotFound(f"User with username {data['username']}")

    if 'email' in data and check_email_exists(data['email']):
        raise ResourceNotFound(f"User with email {data['email']}")

    user = db.session.query(User).filter(
        sa.or_(
            User.email == data['email'],
            User.username == data['username']
        )
    ).first()

    if user is None:
        raise error_response(501, 'Username or email matched but unable to load the user')

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
