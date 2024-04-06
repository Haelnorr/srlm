from flask import Blueprint

bp = Blueprint('api', __name__)

from api.srlm.app.api import auth, users, league, utils, games
