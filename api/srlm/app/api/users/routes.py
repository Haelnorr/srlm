"""Main endpoints relating to Users"""
import sqlalchemy as sa
from apifairy import arguments, response, authenticate, other_responses, body
from flask import request, url_for
from api.srlm.app import db
from api.srlm.app.api.users import users_bp as users
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import force_fields, force_unique, clean_data, ensure_exists
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, TokenSchema, PasswordResetSchema, ChangePasswordSchema, \
    UserSchema, UserCollection, LinkSuccessSchema, UpdateUserSchema
from api.srlm.app.models import User
from api.srlm.app.api.utils.errors import UserAuthError, BadRequest, error_response
from api.srlm.app.api.auth.utils import get_bearer_token, app_auth, dual_auth

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@users.route('/<int:user_id>', methods=['GET'])
@response(UserSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_user(user_id):
    """Get a users details"""
    user = ensure_exists(User, id=user_id)
    user_token = get_bearer_token(request.headers)['user']
    current_user = User.check_token(user_token)

    include_email = False

    if current_user and current_user.id == user.id:
        include_email = True

    return user.to_dict(include_email=include_email)


@users.route('/', methods=['GET'])
@arguments(PaginationArgs())
@response(UserCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_users(pagination):
    """Get the collection of all users"""
    page = pagination['page']
    per_page = pagination['per_page']
    return User.to_collection_dict(sa.select(User), page, per_page, 'api.users.get_users')


@users.route('/', methods=['POST'])
@body(UserSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_user():
    """Create a new user"""
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
@body(UpdateUserSchema())
@response(LinkSuccessSchema())
@authenticate(dual_auth)
@other_responses(unauthorized | bad_request | not_found)
def update_user(user_id):
    """Update a users details. Requires user token"""
    if dual_auth.current_user().id != user_id:
        raise UserAuthError()
    data = request.get_json()

    user = ensure_exists(User, id=user_id)

    unique_fields = valid_fields = ['username', 'email']

    force_unique(User, data, unique_fields, self_id=user.id)

    user.from_dict(clean_data(data, valid_fields))
    db.session.commit()
    return responses.request_success(f'User {user.username} updated', 'api.users.get_user', user_id=user.id)


@users.route('/<int:user_id>/new_password', methods=['POST'])
@body(ChangePasswordSchema())
@response(TokenSchema())
@authenticate(dual_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_user_password(user_id):
    """Update a users. Revokes and issues a new token. Requires user token"""
    if dual_auth.current_user().id != user_id:
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

    response_json = {
        'token': token,
        'expires': user.token_expiration
    }
    return response_json


@users.route('/<int:user_id>/matches_streamed', methods=['GET'])
def get_user_matches_streamed(user_id):
    pass


@users.route('/<int:user_id>/matches_reviewed', methods=['GET'])
def get_user_matches_reviewed(user_id):
    pass


@users.route('/forgot_password', methods=['POST'])
@body(PasswordResetSchema())
@response(PasswordResetSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def request_password_reset():
    """Request a password reset token"""
    data = request.get_json()

    if 'username' not in data and 'email' not in data:
        raise BadRequest("No valid fields provided. Provide either 'username' or 'email'")

    valid_fields = ['username', 'email']
    search_args = clean_data(data, valid_fields)

    user = ensure_exists(User, join_method='or', **search_args)

    response_json = {
        'user': user.id,
        'reset_token': user.get_password_reset_token(),
        '_links': {
            'user': url_for('api.users.get_user', user_id=user.id)
        }
    }
    return response_json


@users.route('/forgot_password/<reset_token>', methods=['GET'])
@response(TokenSchema())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_temp_token(reset_token):
    """Get a temporary user auth token using the password reset token"""
    user = User.verify_reset_password_token(reset_token)
    if not user:
        return error_response(401, 'Password reset token is invalid or expired.')

    user.revoke_token()
    token = user.get_token(expires_in=300)
    user.reset_pass = True
    db.session.commit()
    return {'token': token, 'expires': user.token_expiration}
