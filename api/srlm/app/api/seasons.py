from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for
from api.srlm.app.models import Season
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/seasons', methods=['GET'])
@req_app_token
def get_seasons():
    pass


@bp.route('/seasons/<int:season_id>', methods=['GET'])
@req_app_token
def get_season(season_id):
    pass


@bp.route('/seasons', methods=['POST'])
@req_app_token
def add_season():
    pass


@bp.route('/seasons/<int:season_id>', methods=['PUT'])
@req_app_token
def update_season(season_id):
    pass


@bp.route('/seasons/<int:season_id>/divisions', methods=['GET'])
@req_app_token
def get_divisions_in_season(season_id):
    pass
