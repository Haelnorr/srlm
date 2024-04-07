from flask import Blueprint
from api.srlm.app.api import bp

users_bp = Blueprint('users', __name__)
bp.register_blueprint(users_bp, url_prefix='/users')

from api.srlm.app.api.users import routes, permissions, discord, steam, twitch
