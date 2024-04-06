import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app import db
from api.srlm.app.models import User
from api.srlm.app.api.utils.errors import error_response, AppAuthError, UserAuthError
from functools import wraps
from flask import request

basic_auth = HTTPBasicAuth()
user_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status, 'User credentials invalid')


@user_auth.verify_token
def verify_token(token):
    user_token = token[34:]
    return User.check_token(user_token) if user_token else None


@user_auth.error_handler
def token_auth_error(status):
    raise UserAuthError()


def req_app_token(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            raise AppAuthError()

        app_token = get_bearer_token(request.headers)['app']

        if AuthorizedApp.check_token(app_token):
            return f(*args, **kws)
        else:
            raise AppAuthError()
    return decorated_function


def get_basic_token(headers):
    data = headers['Authorization']

    # this section gets the Basic Auth code from the auth headers
    basic_start = data.rfind('Basic ') + 6
    basic = data[basic_start:]
    if basic.find(' ') != -1:
        basic = basic[:basic.find(' ')]

    return basic


def get_bearer_token(headers):
    data = headers['Authorization']

    # gets the bearer code from the auth header
    bearer_start = data.rfind('Bearer ') + 7
    bearer = data[bearer_start:]
    if bearer.find(' ') != -1:
        bearer = bearer[:bearer.find(' ')]

    # extracts the app token from the bearer code - expects it to be the first 34 characters
    app_token = bearer[:34]
    user_token = bearer[34:]
    return {'app': app_token, 'user': user_token}
