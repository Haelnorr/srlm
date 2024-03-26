from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for
from api.srlm.app.models import League
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/leagues', methods=['GET'])
@req_app_token
def get_leagues():
    pass


@bp.route('/leagues/<int:league_id>', methods=['GET'])
@req_app_token
def get_league(league_id):
    pass


@bp.route('/leagues', methods=['POST'])
@req_app_token
def add_leagues():
    pass


@bp.route('/leagues', methods=['PUT'])
@req_app_token
def update_leagues():
    pass


@bp.route('/leagues/<int:league_id>/seasons', methods=['GET'])
@req_app_token
def get_league_seasons(league_id):
    pass


@bp.route('/leagues/<int:league_id>/divisions', methods=['GET'])
@req_app_token
def get_league_divisions(league_id):
    pass
