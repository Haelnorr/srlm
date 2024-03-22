from flask import Blueprint

bp = Blueprint('auth', __name__)

from lds.app.auth import routes, forms, email, functions
