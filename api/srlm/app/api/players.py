from api.srlm.app.api import bp
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/players/<int:player_id>', methods=['GET'])
@req_app_token
def get_player(player_id):
    pass


@bp.route('/players', methods=['GET'])
@req_app_token
def get_players():
    pass


@bp.route('/players', methods=['POST'])
@req_app_token
def new_player():
    pass


@bp.route('/players/<int:player_id>', methods=['PUT'])
@req_app_token
def update_player(player_id):
    pass


@bp.route('/players/<int:player_id>/current_team', methods=['GET'])
@req_app_token
def get_player_current_team(player_id):
    pass


@bp.route('/players/<int:player_id>/teams', methods=['GET'])
@req_app_token
def get_player_teams(player_id):
    pass


@bp.route('/players/<int:player_id>/stats', methods=['GET'])
@req_app_token
def get_player_stats(player_id):
    pass


@bp.route('/players/<int:player_id>/teams', methods=['POST'])
@req_app_token
def register_player_team(player_id):
    pass


@bp.route('/players/<int:player_id>/teams', methods=['DELETE'])
@req_app_token
def deregister_player_team(player_id):
    pass


@bp.route('/players/<int:player_id>/free_agent', methods=['POST'])
@req_app_token
def register_player_free_agent(player_id):
    pass
