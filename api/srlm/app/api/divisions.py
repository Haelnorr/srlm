from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for
from api.srlm.app.models import Division
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/divisions', methods=['GET'])
@req_app_token
def get_divisions():
    pass


@bp.route('/divisions/<int:division_id>', methods=['GET'])
@req_app_token
def get_division(division_id):
    pass


@bp.route('/divisions', methods=['POST'])
@req_app_token
def add_division():
    pass


@bp.route('/divisions/<int:division_id>', methods=['PUT'])
@req_app_token
def update_division(division_id):
    pass


@bp.route('/divisions/<int:division_id>/seasons', methods=['GET'])
@req_app_token
def get_seasons_of_division(division_id):
    pass
