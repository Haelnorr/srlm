"""Provides endpoints for in-game related API endpoints"""
from flask import Blueprint
from api.srlm.app.api import bp

game_bp = Blueprint('game', __name__)
bp.register_blueprint(game_bp)

from api.srlm.app.api.game import lobby, match
