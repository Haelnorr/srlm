"""Provides endpoints for League management related endpoints"""
from flask import Blueprint
from api.srlm.app.api import bp

league_bp = Blueprint('league', __name__)
bp.register_blueprint(league_bp)

from api.srlm.app.api.league import leagues, seasons, divisions, season_divisions, players, teams
