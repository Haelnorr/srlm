import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app.auth.functions import get_bearer_token
from api.srlm.app import db
from api.srlm.app.models import User
from api.srlm.app.api.errors import error_response, AppAuthError, UserAuthError
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
