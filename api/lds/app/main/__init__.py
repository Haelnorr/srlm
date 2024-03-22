from flask import Blueprint

bp = Blueprint('main', __name__)

from api.lds.app.main import routes, forms
