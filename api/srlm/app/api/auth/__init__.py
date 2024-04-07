"""Provides all the auth endpoints"""
from flask import Blueprint
from api.srlm.app.api import bp

auth_bp = Blueprint('auth', __name__)
bp.register_blueprint(auth_bp, url_prefix='/auth')

from api.srlm.app.api.auth import routes, utils, permissions
