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
