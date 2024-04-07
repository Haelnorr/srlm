"""Auth endpoints relating to permissions"""
from flask import request, url_for
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.models import Permission
from api.srlm.app.api.auth import auth_bp as auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import req_app_token
from api.srlm.app.api.utils.errors import BadRequest

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


# Checks if a permission with the given key exists in the database
def check_key_exists(key):
    query = db.session.query(Permission).filter(Permission.key == key)
    exists = db.session.query(query.exists()).scalar()
    return exists


@auth.route('/permissions/<perm_id_or_key>', methods=['GET'])
@req_app_token
def get_permission(perm_id_or_key):
    permission = ensure_exists(Permission, join_method='or', id=perm_id_or_key, key=perm_id_or_key)
    return permission.to_dict()


@auth.route('/permissions', methods=['GET'])
@req_app_token
def get_permissions():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Permission.to_collection_dict(sa.select(Permission), page, per_page, 'api.auth.get_permissions')


@auth.route('/permissions', methods=['POST'])
@req_app_token
def new_permission():
    data = request.get_json()

    required_fields = valid_fields = ['key', 'description']

    force_fields(data, required_fields)
    force_unique(Permission, data, ['key'])
    cleaned_data = clean_data(data, valid_fields)

    permission = Permission()
    permission.from_dict(cleaned_data)
    db.session.add(permission)
    db.session.commit()
    return responses.create_success(f"Permission {permission.key} created", 'api.auth.get_permission', perm_id_or_key=permission.id)


@auth.route('/permissions/<perm_id_or_key>', methods=['PUT'])
@req_app_token
def update_permission(perm_id_or_key):
    permission = ensure_exists(Permission, join_method='or', id=perm_id_or_key, key=perm_id_or_key)
    data = request.get_json()

    if 'key' in data and data['key'] != permission.key and check_key_exists(data['key']):
        raise BadRequest('Permission key is not unique')
    permission.from_dict(data)
    db.session.commit()
    return responses.request_success(f"Permission {permission.key} updated", 'api.auth.get_permission', perm_id_or_key=permission.id)


@auth.route('/permissions/<perm_id_or_key>/users', methods=['GET'])
@req_app_token
def list_users_with_permission(perm_id_or_key):
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

    response = {
        'permission': permission.description,
        'key': permission.key,
        'users': users,
        '_links': {
            'self': url_for('api.users.list_users_with_permission', perm_id_or_key=permission.id)
        }
    }

    return response
