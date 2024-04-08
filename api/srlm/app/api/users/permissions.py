"""Endpoints for managing user permissions"""
from apifairy import body, response, authenticate, other_responses
from flask import url_for, request, Blueprint
from api.srlm.app import db
from api.srlm.app.api.users import users_bp
from api.srlm.app.api.auth.utils import req_app_token, user_auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.fairy.errors import unauthorized, forbidden, not_found, bad_request
from api.srlm.app.fairy.schemas import UserPermissionsCollection, UserPermissionsSchema, LinkSuccessSchema, \
    UpdateUserPermissionsSchema, RevokeUserPermission
from api.srlm.app.models import User, Permission, UserPermissions


permissions = Blueprint('permissions', __name__)
users_bp.register_blueprint(permissions)


@permissions.route('/<int:user_id>/permissions', methods=['GET'])
@req_app_token
@response(UserPermissionsCollection())
@authenticate(user_auth)
@other_responses(unauthorized | not_found)
def get_user_permissions(user_id):
    """Get the users permissions"""
    user = ensure_exists(User, id=user_id)

    permissions = []
    for user_permission in user.permission_assoc:
        permissions.append(user_permission.to_dict())

    response_json = {
        'username': user.username,
        'permissions': permissions,
        '_links': {
            'self': url_for('api.users.permissions.get_user_permissions', user_id=user_id)
        }
    }

    return response_json


@permissions.route('/<int:user_id>/permissions', methods=['POST'])
@req_app_token
@body(UserPermissionsSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def add_user_permissions(user_id):
    """Grant a permission to a user"""
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

    return responses.create_success(f'Permission {user_perm.permssion.key} added to user {user_perm.user.username}', 'api.users.permissions.get_user_permissions', user_id=user_id)


@permissions.route('/<int:user_id>/permissions', methods=['PUT'])
@req_app_token
@body(UpdateUserPermissionsSchema())
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_user_permissions(user_id):
    """Update a users existing permission"""
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

    return responses.request_success(f'Permission {user_perm.permssion.key} updated for user {user_perm.user.username}', 'api.users.permissions.get_user_permissions', user_id=user_id)


@permissions.route('/<int:user_id>/permissions/revoke', methods=['POST'])
@req_app_token
@body(RevokeUserPermission())
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def revoke_user_permissions(user_id):
    """Revoke a permission from a user"""
    user = ensure_exists(User, id=user_id)
    data = request.get_json()

    force_fields(data, ['key'])

    permission = ensure_exists(Permission, key=data['key'])

    user_perm = ensure_exists(UserPermissions, return_none=True, user_id=user.id, permission_id=permission.id)
    if user_perm is None:
        raise ResourceNotFound(f"User {user.username} does not have the '{permission.key}' permission")

    db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).delete()
    db.session.commit()

    return responses.request_success(f'Permission {permission.key} revoked from user {user.username}', 'api.users.permissions.get_user_permissions', user_id=user_id)
