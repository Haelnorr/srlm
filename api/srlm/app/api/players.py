from datetime import datetime, timezone

from flask import request, url_for
import sqlalchemy as sa

from api.srlm.app import db
from api.srlm.app.api import bp, responses
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.app.api.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.models import Player, SeasonDivision
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/players/<int:player_id>', methods=['GET'])
@req_app_token
def get_player(player_id):
    player = ensure_exists(Player, id=player_id)
    return player.to_dict()


@bp.route('/players', methods=['GET'])
@req_app_token
def get_players():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Player.to_collection_dict(sa.select(Player), page, per_page, 'api.get_players')


@bp.route('/players', methods=['POST'])
@req_app_token
def new_player():
    data = request.get_json()

    required_fields = ['player_name']
    unique_fields = ['slap_id', 'player_name']
    valid_fields = ['slap_id', 'player_name', 'rookie', 'first_season_id']

    force_fields(data, required_fields)
    force_unique(Player, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    if 'first_season_id' in cleaned_data:
        ensure_exists(SeasonDivision, id=cleaned_data['first_season_id'])

    player = Player()
    player.from_dict(cleaned_data)

    db.session.add(player)
    db.session.commit()

    return responses.create_success(f"Player {player.player_name} created", 'api.get_player', player_id=player.id)


@bp.route('/players/<int:player_id>', methods=['PUT'])
@req_app_token
def update_player(player_id):
    data = request.get_json()

    player = ensure_exists(Player, id=player_id)

    unique_fields = ['slap_id', 'player_name']
    valid_fields = ['slap_id', 'player_name', 'rookie', 'first_season_id']

    force_unique(Player, data, unique_fields, self_id=player.id)
    cleaned_data = clean_data(data, valid_fields)

    if 'first_season_id' in cleaned_data:
        ensure_exists(SeasonDivision, id=cleaned_data['first_season_id'])

    player.from_dict(cleaned_data)
    db.session.commit()

    return responses.request_success(f"Player {player.player_name} updated", 'api.get_player', player_id=player.id)


@bp.route('/players/<int:player_id>/teams', methods=['GET'])
@req_app_token
def get_player_teams(player_id):
    player = ensure_exists(Player, id=player_id)

    current = request.args.get('current', False, bool)
    if current:
        for team_assoc in player.team_association:
            now = datetime.now(timezone.utc)
            if team_assoc.start_date.replace(tzinfo=timezone.utc) < now and (team_assoc.end_date is None or team_assoc.end_date.replace(tzinfo=timezone.utc) > now):
                response = {
                    'player': player.player_name,
                    'current_team': {
                        'name': team_assoc.team.name,
                        'acronym': team_assoc.team.acronym,
                        'color': team_assoc.team.color,
                        'start_date': team_assoc.start_date
                    },
                    '_links': {
                        'self': url_for('api.get_player_teams', player_id=player.id),
                        'current_team': url_for('api.get_team', team_id=team_assoc.team.id)
                    }
                }
                return response

    else:
        teams = {}
        for team_assoc in player.team_association:
            if team_assoc.team.id not in teams:
                team_data = {
                    'name': team_assoc.team.name,
                    'acronym': team_assoc.team.acronym,
                    'color': team_assoc.team.color,
                    'dates': [
                        {
                            'start': team_assoc.start_date,
                            'end': team_assoc.end_date
                        }
                    ],
                    '_links': {
                        'self': url_for('api.get_team', team_id=team_assoc.team.id)
                    }
                }
                teams[team_assoc.team.id] = team_data
            else:
                dates = {
                    'start': team_assoc.start_date,
                    'end': team_assoc.end_date
                }
                teams[team_assoc.team.id]['dates'].append(dates)

        response = {
            'player': player.player_name,
            'teams': teams,
            '_links': {
                'self': url_for('api.get_player_teams', player_id=player.id)
            }
        }
        return response


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


@bp.route('/players/<int:player_id>/free_agent', methods=['GET'])
@req_app_token
def get_player_free_agent(player_id):
    pass


@bp.route('/players/<int:player_id>/free_agent', methods=['POST'])
@req_app_token
def register_player_free_agent(player_id):
    pass


@bp.route('/players/<int:player_id>/awards', methods=['GET'])
@req_app_token
def get_player_awards(player_id):
    pass


@bp.route('/players/<int:player_id>/awards', methods=['POST'])
@req_app_token
def give_player_award(player_id):
    pass
