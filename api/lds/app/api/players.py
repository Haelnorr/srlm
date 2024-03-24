from api.lds.app.api import bp

# create a new logger for this module
from api.lds.logger import get_logger
log = get_logger(__name__)


@bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    pass


@bp.route('/players', methods=['GET'])
def get_players():
    pass


@bp.route('/players', methods=['POST'])
def new_player():
    pass


@bp.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    pass
