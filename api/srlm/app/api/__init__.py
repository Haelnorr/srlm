"""Provides all the routes and helper functions for the main API"""
from flask import Blueprint, request
from api.srlm.logger import get_logger

log = get_logger(__name__)

bp = Blueprint('api', __name__)


@bp.after_request
def after_request(response):
    log.debug(f'{request.remote_addr} {request.method} {request.scheme} {request.full_path} {response.status}')
    return response


@bp.route('/ready', methods=['GET'])
def is_ready():
    return 'READY', 200


from api.srlm.app.api import utils, auth, users, league, game
