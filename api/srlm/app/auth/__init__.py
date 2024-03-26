from flask import Blueprint

bp = Blueprint('auth', __name__)

from api.srlm.app.auth import email, functions
