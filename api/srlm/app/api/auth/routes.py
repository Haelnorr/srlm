"""Main auth endpoints"""
from flask import request, url_for
from apifairy import response, other_responses, authenticate
from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app import db
from api.srlm.app.api.auth import auth_bp as auth
from api.srlm.app.api.auth.utils import basic_auth, user_auth, dual_auth, app_auth
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import get_bearer_token
from api.srlm.app.fairy.schemas import TokenSchema, BasicSuccessSchema, UserVerifySchema
from api.srlm.app.fairy.errors import unauthorized
from api.srlm.app.models import User


@auth.route('/user', methods=['POST'])
@authenticate(basic_auth)
@response(TokenSchema())
@other_responses(unauthorized)
def get_user_token():
    """Request an auth token for a user."""
    token = basic_auth.current_user().get_token()
    expires = basic_auth.current_user().token_expiration
    db.session.commit()
    return {'token': token, 'expires': expires}


@auth.route('/user', methods=['DELETE'])
@response(BasicSuccessSchema())
@authenticate(dual_auth)
@other_responses(unauthorized)
def revoke_user_token():
    """Revoke the users current auth token"""
    user_auth.current_user().revoke_token()
    db.session.commit()
    return responses.request_success('User token revoked')


@auth.route('/user/validate', methods=['POST'])
@response(UserVerifySchema())
@authenticate(dual_auth)
@other_responses(unauthorized)
def validate_user_token(

):
    """Check if the user token provided is valid"""
    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)

    response_json = {
        'user': user.id,
        'expires': user.token_expiration,
        '_links': {
            'user': url_for('api.users.get_user', user_id=user.id)
        }
    }
    return response_json


@auth.route('/app', methods=['POST'])
@response(TokenSchema())
@authenticate(app_auth)
@other_responses(unauthorized)
def request_new_app_token():
    """Request a new app token for the authorized app.
    Replaces the current token"""
    app_token = get_bearer_token(request.headers)['app']

    authorized_app = AuthorizedApp.check_token(app_token)
    token = authorized_app.get_new_token()
    db.session.commit()
    response_json = {
        'token': token,
        'expiry': authorized_app.token_expiration
    }
    return response_json


@auth.route('/app', methods=['GET'])
@response(TokenSchema())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_app_token():
    """Get the current app token and expiry date"""
    app_token = get_bearer_token(request.headers)['app']

    authorized_app = AuthorizedApp.check_token(app_token)
    response_json = {
        'token': authorized_app.token,
        'expiry': authorized_app.token_expiration
    }
    return response_json
