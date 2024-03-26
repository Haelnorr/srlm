from flask import Blueprint

bp = Blueprint('api', __name__)

from api.srlm.app.api import errors, players, tokens, users, auth, permissions, divisions, leagues, seasons, teams, season_divisions
