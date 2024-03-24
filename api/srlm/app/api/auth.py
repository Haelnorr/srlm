import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app import db
from api.srlm.app.models import User
from api.srlm.app.api.errors import error_response
from functools import wraps
from flask import request, abort

basic_auth = HTTPBasicAuth()
user_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@user_auth.verify_token
def verify_token(token):
    user_token = token[34:]
    return User.check_token(user_token) if user_token else None


@user_auth.error_handler
def token_auth_error(status):
    return error_response(status)


def req_app_token(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            abort(401)

        authorized_app = None
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        app_token = token[:34]

        # do proper token check, for now, test string
        authorized_app = AuthorizedApp.check_token(app_token)
        if authorized_app:
            return f(*args, **kws)
        else:
            abort(401)
    return decorated_function
