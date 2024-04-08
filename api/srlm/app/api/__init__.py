"""Provides all the routes and helper functions for the main API"""
from flask import Blueprint

bp = Blueprint('api', __name__)

from api.srlm.app.api import utils, auth, users, league, game
