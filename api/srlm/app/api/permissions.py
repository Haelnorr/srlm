from flask import request, url_for, abort
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.models import Permission
from api.srlm.app.api import bp
from api.srlm.app.api.auth import req_app_token
from api.srlm.app.api.errors import bad_request

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


# Checks if a permission with the given key exists in the database
def check_key_exists(key):
    query = db.session.query(Permission).filter(Permission.key == key)
    exists = db.session.query(query.exists()).scalar()
    return exists


@bp.route('/permissions/<int:perm_id>', methods=['GET'])
@req_app_token
def get_permission(perm_id):
    return Permission.query.get_or_404(perm_id).to_dict()


@bp.route('/permissions', methods=['GET'])
@req_app_token
def get_permissions():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Permission.to_collection_dict(sa.select(Permission), page, per_page, 'api.get_permissions')


@bp.route('/permissions', methods=['POST'])
@req_app_token
def new_permission():
    data = request.get_json()
    if 'key' not in data:
        return bad_request('must provide a key to create a new permission')
    if check_key_exists(data['key']):
        return bad_request('key already in use')
    permission = Permission()
    permission.from_dict(data)
    db.session.add(permission)
    db.session.commit()
    return permission.to_dict(), 201, {'Location': url_for('api.get_permission', perm_id=permission.id)}


@bp.route('/permissions/<int:perm_id>', methods=['PUT'])
@req_app_token
def update_permission(perm_id):
    permission = Permission.query.get_or_404(perm_id)
    data = request.get_json()
    if 'key' in data and data['key'] != permission.key and check_key_exists(data['key']):
        return bad_request('please use a different key')
    permission.from_dict(data)
    db.session.commit()
    return permission.to_dict()


@bp.route('/permissions/<int:perm_id>/users', methods=['GET'])
@req_app_token
def list_users_with_permission(perm_id):
    permission = db.session.get(Permission, perm_id)
    if not permission:
        abort(404)

    users = []
    for user in permission.users:
        users.append({
            'id': user.id,
            'username': user.username,
            '_links': {
                'self': url_for('api.get_user', user_id=user.id)
            }
        })

    response = {
        'permission': permission.description,
        'key': permission.key,
        'users': users,
        '_links': {
            'self': url_for('api.list_users_with_permission', perm_id=perm_id)
        }
    }

    return response
