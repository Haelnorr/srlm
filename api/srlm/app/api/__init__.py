"""Provides all the routes and helper functions for the main API"""
from flask import Blueprint, request, Response
from api.srlm.logger import get_logger

log = get_logger(__name__)

bp = Blueprint('api', __name__)


@bp.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        # res.headers['Access-Control-Allow-Headers'] = 'Authorization'
        return res


@bp.after_request
def after_request(response):
    log.debug(f'{request.remote_addr} {request.method} {request.scheme} {request.full_path} {response.status}')
    return response


@bp.route('/ready', methods=['GET'])
def is_ready():
    return 'READY', 200


from api.srlm.app.api import utils, auth, users, league, game
