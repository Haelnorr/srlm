from api.srlm.app import db
from api.srlm.app.models import User


def check_username_exists(username):
    query = db.session.query(User).filter(User.username == username)
    exists = db.session.query(query.exists()).scalar()
    return exists


def check_email_exists(email):
    query = db.session.query(User).filter(User.email == email)
    exists = db.session.query(query.exists()).scalar()
    return exists


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
