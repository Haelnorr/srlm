from flask import Blueprint

bp = Blueprint('main', __name__)

from lds.app.main import routes, forms
