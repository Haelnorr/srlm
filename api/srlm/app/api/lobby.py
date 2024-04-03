from flask import request

from api.srlm.app.api import bp
from api.srlm.app.api.auth import req_app_token
from api.srlm.app.api.functions import force_fields, ensure_exists
from api.srlm.app.models import Match
from api.srlm.app.spapi.lobby_manager import generate_lobby


@bp.route('/lobby', methods=['POST'])
@req_app_token
def add_lobby():
    data = request.get_json()

    force_fields(data, ['match_id'])
    match = ensure_exists(Match, id=data['match_id'])

    result = generate_lobby(match)
