"""Utilities for the authentication system"""
import requests
import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app import db
from api.srlm.app.models import User
from api.srlm.app.api.utils.errors import error_response, AppAuthError, UserAuthError, DualAuthError

basic_auth = HTTPBasicAuth()
user_auth = HTTPTokenAuth()
app_auth = HTTPTokenAuth()
dual_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status, 'User credentials invalid')


@user_auth.verify_token
def verify_user_token(token):
    user_token = token[34:]
    return User.check_token(user_token) if user_token else None


@user_auth.error_handler
def token_auth_error():
    raise UserAuthError()


@app_auth.verify_token
def verify_app_token(token):
    app_token = token[:34]
    return AuthorizedApp.check_token(app_token) if app_token else None


@app_auth.error_handler
def app_auth_error():
    raise AppAuthError()


@dual_auth.verify_token
def verify_dual_token(token):
    app_token = token[:34]
    user_token = token[34:]
    if app_token and user_token:
        return User.check_token(user_token)
    else:
        return None


def get_discord_info(token):
    api = 'https://discord.com/api/v9/users/@me'
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(api, headers=headers)


@dual_auth.error_handler
def dual_auth_error():
    raise DualAuthError()


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
