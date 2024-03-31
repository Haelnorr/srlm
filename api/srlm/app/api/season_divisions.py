from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for

from api.srlm.app.api.errors import ResourceNotFound
from api.srlm.app.api.functions import ensure_exists
from api.srlm.app.models import SeasonDivision, FreeAgent
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/season_division/<int:season_division_id>', methods=['GET'])
@req_app_token
def get_season_division(season_division_id):
    pass


@bp.route('/season_division', methods=['POST'])
@req_app_token
def add_season_division(season_division_id):
    pass


@bp.route('/season_division/<int:season_division_id>/teams', methods=['GET'])
@req_app_token
def get_teams_in_season_division(season_division_id):
    pass


@bp.route('/season_division/<int:season_division_id>/rookies', methods=['GET'])
@req_app_token
def get_rookies_in_season_division(season_division_id):
    pass


@bp.route('/season_division/<int:season_division_id>/free_agents', methods=['GET'])
@req_app_token
def get_free_agents_in_season_division(season_division_id):
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    free_agents = FreeAgent.get_season_free_agents(season_division.id)

    if free_agents is None:
        raise ResourceNotFound('No free agents in the specified season')

    return free_agents


@bp.route('/season_division/<int:season_division_id>/matches', methods=['GET'])
@req_app_token
def get_matches_in_season_division(season_division_id):
    pass


@bp.route('/season_division/<int:season_division_id>/finals', methods=['GET'])
@req_app_token
def get_finals_in_season_division(season_division_id):
    pass
