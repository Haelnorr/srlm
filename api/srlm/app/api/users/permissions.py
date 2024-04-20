"""Endpoints for managing user permissions"""
from apifairy import body, response, authenticate, other_responses
from flask import url_for, request, Blueprint
from api.srlm.app import db
from api.srlm.app.api.users import users_bp
from api.srlm.app.api.auth.utils import app_auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import UserPermissionsList, UserPermissionsSchema, LinkSuccessSchema, \
    UpdateUserPermissionSchema, RevokeUserPermission, UpdateUserPermissionsSchema
from api.srlm.app.models import User, Permission, UserPermissions
from api.srlm.logger import get_logger


log = get_logger(__name__)


permissions = Blueprint('permissions', __name__)
users_bp.register_blueprint(permissions)


@permissions.route('/<int:user_id>/permissions', methods=['GET'])
@response(UserPermissionsList())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_user_permissions(user_id):
    """Get the users permissions"""
    user = ensure_exists(User, id=user_id)

    permissions_list = [
        {
            'key': up.permission.key,
            'mods': up.additional_modifiers if up.additional_modifiers else True
        }
        for up in user.permission_assoc
    ]

    response_json = {
        'username': user.username,
        'permissions': permissions_list,
        '_links': {
            'self': url_for('api.users.permissions.get_user_permissions', user_id=user_id)
        }
    }

    return response_json


@permissions.route('/<int:user_id>/permissions', methods=['POST'])
@body(UserPermissionsSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def add_user_permissions(data, user_id):
    """Grant a permission to a user"""
    user = ensure_exists(User, id=user_id)

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


@permissions.route('/<int:user_id>/permission', methods=['PUT'])
@body(UpdateUserPermissionSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_user_permission(data, user_id):
    """Update a users existing permission"""
    user = ensure_exists(User, id=user_id)

    required_fields = ['key', 'modifiers']

    force_fields(data, required_fields)

    permission = ensure_exists(Permission, key=data['key'])

    user_perm = ensure_exists(UserPermissions, user_id=user.id, permission_id=permission.id)

    modifiers = data['modifiers']
    if data['modifiers'] == "":
        modifiers = None
    user_perm.additional_modifiers = modifiers
    db.session.commit()

    return responses.request_success(f'Permission {user_perm.permssion.key} updated '
                                     f'for user {user_perm.user.username}',
                                     'api.users.permissions.get_user_permissions',
                                     user_id=user_id)


@permissions.route('/<int:user_id>/permissions', methods=['PUT'])
@body(UpdateUserPermissionsSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_user_permissions(data, user_id):
    """Update a users permissions
    Body of request should be a dictionary where the keys match the keys of permissions.<br>
    Value should be boolean where no additional_modifiers are required, and an array of the modifiers where they are
    """
    user = ensure_exists(User, id=user_id)

    log.debug(data)

    # loop through the permissions provided by the request
    for key in data:
        log.debug(key)
        # check its a valid permission
        perm = ensure_exists(Permission, return_none=True, key=key)

        def update_perm(permission):
            if permission:
                # check if user already has the perm
                user_perm = ensure_exists(UserPermissions,
                                          return_none=True,
                                          user_id=user.id,
                                          permission_id=permission.id)
                log.debug(user_perm)
                # if user doesnt have the perm and request is adding the permission
                if not user_perm and data[key]:
                    if type(data[key]) == list and len(data[key]) is 0:
                        return
                    user_perm = UserPermissions()
                    user_perm.user = user
                    user_perm.permission = permission
                    log.debug(f'created {user_perm}')

                if not user_perm:
                    return

                # check if mods were specified
                if type(data[key]) == list:
                    user_perm.additional_modifiers = ','.join(data[key])
                    log.debug(f'{key} modifiers: {user_perm.additional_modifiers}')

                db.session.add(user_perm)

                # if user has perm and the request set it to false, delete it
                if user_perm and (data[key] is False):
                    log.debug('deleting')
                    db.session.query(UserPermissions).filter_by(id=user_perm.id).delete()

        update_perm(perm)

    db.session.commit()

    return responses.request_success(f'Permissions updated '
                                     f'for user {user.username}',
                                     'api.users.permissions.get_user_permissions',
                                     user_id=user_id)




@permissions.route('/<int:user_id>/permissions/revoke', methods=['POST'])
@body(RevokeUserPermission())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def revoke_user_permissions(data, user_id):
    """Revoke a permission from a user"""
    user = ensure_exists(User, id=user_id)

    force_fields(data, ['key'])

    permission = ensure_exists(Permission, key=data['key'])

    user_perm = ensure_exists(UserPermissions, return_none=True, user_id=user.id, permission_id=permission.id)
    if user_perm is None:
        raise ResourceNotFound(f"User {user.username} does not have the '{permission.key}' permission")

    db.session.query(UserPermissions).filter_by(user_id=user.id, permission_id=permission.id).delete()
    db.session.commit()

    return responses.request_success(f'Permission {permission.key} revoked from user {user.username}',
                                     'api.users.permissions.get_user_permissions',
                                     user_id=user_id)
