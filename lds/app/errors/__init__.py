from flask import Blueprint

bp = Blueprint('errors', __name__)

from lds.app.errors import handlers
