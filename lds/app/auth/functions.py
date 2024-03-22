from lds.app import db
from lds.app.models import load_user, User


def get_permissions(user_id):
    user = load_user(user_id)
    permissions = user.get_permissions()
    return permissions


def check_username_exists(username):
    query = db.session.query(User).filter(User.username == username)
    exists = db.session.query(query.exists()).scalar()
    return exists


def check_email_exists(email):
    query = db.session.query(User).filter(User.email == email)
    exists = db.session.query(query.exists()).scalar()
    return exists
