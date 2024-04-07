"""Main endpoints relating to Users"""
import sqlalchemy as sa
from flask import request, url_for
from api.srlm.app import db
from api.srlm.app.api.users import users_bp as users
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import force_fields, force_unique, clean_data, ensure_exists
from api.srlm.app.models import User
from api.srlm.app.api.utils.errors import UserAuthError, BadRequest, error_response
from api.srlm.app.api.auth.utils import user_auth, req_app_token, get_bearer_token
from api.srlm.app.email import send_password_reset_email  # TODO change this

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@users.route('/<int:user_id>', methods=['GET'])
@req_app_token
def get_user(user_id):
    """Gets a user"""
    user = ensure_exists(User, id=user_id)
    user_token = get_bearer_token(request.headers)['user']
    current_user = User.check_token(user_token)

    include_email = False

    if current_user and current_user.id == user.id:
        include_email = True

    return user.to_dict(include_email=include_email)


@users.route('/', methods=['GET'])
@req_app_token
def get_users(pagination):
    page = request.args.get('page', 1, int)
    per_page = min(request.args.get('per_page', 10, int), 100)
    return User.to_collection_dict(sa.select(User), page, per_page, 'api.users.get_users')


@users.route('/', methods=['POST'])
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

    return responses.create_success(f'User {user.username} added', 'api.users.get_user', user_id=user.id)


@users.route('/<int:user_id>', methods=['PUT'])
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
    return responses.request_success(f'User {user.username} updated', 'api.users.get_user', user_id=user.id)


@users.route('/<int:user_id>/new_password', methods=['POST'])
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


@users.route('/<int:user_id>/matches_streamed', methods=['GET'])
@req_app_token
def get_user_matches_streamed(user_id):
    pass


@users.route('/<int:user_id>/matches_reviewed', methods=['GET'])
@req_app_token
def get_user_matches_reviewed(user_id):
    pass


@users.route('/forgot_password', methods=['POST'])
@req_app_token
def request_password_reset():
    data = request.get_json()

    if 'username' not in data and 'email' not in data:
        raise BadRequest("No valid fields provided. Provide either 'username' or 'email'")

    valid_fields = ['username', 'email']
    search_args = clean_data(data, valid_fields)

    user = ensure_exists(User, join_method='or', **search_args)

    send_password_reset_email(user)  # TODO change this

    response = {
        'result': 'success',
        'user': user.id,
        '_links': {
            'user': url_for('api.users.get_user', user_id=user.id)
        }
    }
    return response


@users.route('/forgot_password/<reset_token>', methods=['GET'])
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
