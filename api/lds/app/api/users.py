import sqlalchemy as sa
from flask import request, url_for
from api.lds.app import db
from api.lds.app.api import bp
from api.lds.app.models import User
from api.lds.app.api.errors import bad_request
from api.lds.app.auth.functions import check_username_exists, check_email_exists

# create a new logger for this module
from api.lds.logger import get_logger
log = get_logger(__name__)


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return User.query.get_or_404(user_id).to_dict()


@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(sa.select(User), page, per_page, 'api.get_users')


@bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if check_username_exists(data['username']):
        return bad_request('please select a different username')
    if check_email_exists(data['email']):
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201, {'Location': url_for('api.get_user', user_id=user.id)}


@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and check_username_exists(data['username']):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and check_email_exists(data['email']):
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()


@bp.route('/users/<int:user_id>/matches_streamed', methods=['GET'])
def get_user_matches_streamed(user_id):
    pass


@bp.route('/users/<int:user_id>/matches_reviewed', methods=['GET'])
def get_user_matches_reviewed(user_id):
    pass


@bp.route('/users/<int:user_id>/permissions', methods=['GET'])
def get_user_permissions(user_id):
    pass


@bp.route('/users/<int:user_id>/discord', methods=['GET'])
def get_user_discord(user_id):
    pass
