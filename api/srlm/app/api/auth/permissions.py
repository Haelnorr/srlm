"""Auth endpoints relating to permissions"""
from apifairy import response, authenticate, other_responses, body, arguments
from flask import request, url_for, Blueprint
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PermissionSchema, LinkSuccessSchema, UpdatePermissionSchema, PermUsersSchema, \
    PaginationArgs, PermissionCollection
from api.srlm.app.models import Permission
from api.srlm.app.api.auth import auth_bp as auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import app_auth
from api.srlm.app.api.utils.errors import BadRequest

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


permissions = Blueprint('permissions', __name__)
auth.register_blueprint(permissions, url_prefix='/permissions')


# Checks if a permission with the given key exists in the database
def check_key_exists(key):
    query = db.session.query(Permission).filter(Permission.key == key)
    exists = db.session.query(query.exists()).scalar()
    return exists


@permissions.route('/<perm_id_or_key>', methods=['GET'])
@response(PermissionSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_permission(perm_id_or_key):
    """Get details of a permission"""
    permission = ensure_exists(Permission, join_method='or', id=perm_id_or_key, key=perm_id_or_key)
    return permission.to_dict()


@permissions.route('/', methods=['GET'])
@arguments(PaginationArgs())
@response(PermissionCollection())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_permissions(pagination):
    """Get a collection of all permissions"""
    page = pagination['page']
    per_page = pagination['per_page']
    return Permission.to_collection_dict(sa.select(Permission), page, per_page, 'api.auth.permissions.get_permissions')


@permissions.route('/', methods=['POST'])
@body(PermissionSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def new_permission():
    """Create a new permission"""
    data = request.get_json()

    required_fields = valid_fields = ['key', 'description']

    force_fields(data, required_fields)
    force_unique(Permission, data, ['key'])
    cleaned_data = clean_data(data, valid_fields)

    permission = Permission()
    permission.from_dict(cleaned_data)
    db.session.add(permission)
    db.session.commit()
    return responses.create_success(f"Permission {permission.key} created", 'api.auth.permissions.get_permission', perm_id_or_key=permission.id)


@permissions.route('/<perm_id_or_key>', methods=['PUT'])
@body(UpdatePermissionSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | bad_request | not_found)
def update_permission(perm_id_or_key):
    """Modify a permission"""
    permission = ensure_exists(Permission, join_method='or', id=perm_id_or_key, key=perm_id_or_key)
    data = request.get_json()

    if 'key' in data and data['key'] != permission.key and check_key_exists(data['key']):
        raise BadRequest('Permission key is not unique')
    permission.from_dict(data)
    db.session.commit()
    return responses.request_success(f"Permission {permission.key} updated", 'api.auth.permissions.get_permission', perm_id_or_key=permission.id)


@permissions.route('/<perm_id_or_key>/users', methods=['GET'])
@response(PermUsersSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def list_users_with_permission(perm_id_or_key):
    """List all users with the given permission"""
    permission = ensure_exists(Permission, join_method='or', id=perm_id_or_key, key=perm_id_or_key)

    users = []
    for user in permission.users:
        users.append({
            'id': user.id,
            'username': user.username,
            '_links': {
                'self': url_for('api.users.get_user', user_id=user.id)
            }
        })

    response_json = {
        'permission': permission.description,
        'key': permission.key,
        'users': users,
        '_links': {
            'self': url_for('api.auth.permissions.list_users_with_permission', perm_id_or_key=permission.id)
        }
    }

    return response_json
