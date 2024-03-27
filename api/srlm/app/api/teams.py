from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for
from api.srlm.app.models import Team
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/teams', methods=['GET'])
@req_app_token
def get_teams():
    # handle ?player_id=
    pass


@bp.route('/teams/<int:team_id>', methods=['GET'])
@req_app_token
def get_team(team_id):
    pass


@bp.route('/teams', methods=['POST'])
@req_app_token
def add_team():
    pass


@bp.route('/teams/<int:team_id>', methods=['PUT'])
@req_app_token
def update_team(team_id):
    pass


@bp.route('/teams/<int:team_id>/players', methods=['GET'])
@req_app_token
def get_team_players(team_id):
    pass


@bp.route('/teams/<int:team_id>/current_players', methods=['GET'])
@req_app_token
def get_team_current_players(team_id):
    pass


@bp.route('/teams/<int:team_id>/seasons', methods=['GET'])
@req_app_token
def get_team_seasons(team_id):
    pass


@bp.route('/teams/<int:team_id>/seasons', methods=['POST'])
@req_app_token
def register_team_season(team_id):
    pass
