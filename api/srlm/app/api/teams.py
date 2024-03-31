from datetime import datetime, timezone

from api.srlm.app import db
from api.srlm.app.api import bp, responses
from flask import request, url_for
import sqlalchemy as sa
from api.srlm.app.api.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.models import Team, SeasonDivision, PlayerTeam
from api.srlm.app.api.auth import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/teams', methods=['GET'])
@req_app_token
def get_teams():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Team.to_collection_dict(sa.select(Team), page, per_page, 'api.get_teams')


@bp.route('/teams/<int:team_id>', methods=['GET'])
@req_app_token
def get_team(team_id):
    team = ensure_exists(Team, id=team_id)
    return team.to_dict()


@bp.route('/teams', methods=['POST'])
@req_app_token
def add_team():
    data = request.get_json()

    required_fields = unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'color', 'logo', 'founded_date']

    force_fields(data, required_fields)
    force_unique(Team, data, unique_fields)

    cleaned_data = clean_data(data, valid_fields)

    if cleaned_data['color'] is "":
        cleaned_data['color'] = None

    team = Team()
    team.from_dict(cleaned_data)

    db.session.add(team)
    db.session.commit()

    return responses.create_success(f'Team {team.name} created', 'api.get_team', team_id=team.id)


@bp.route('/teams/<int:team_id>', methods=['PUT'])
@req_app_token
def update_team(team_id):
    data = request.get_json()

    team = ensure_exists(Team, id=team_id)

    unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'color', 'logo', 'founded_date']

    force_unique(Team, data, unique_fields, self_id=team.id)

    cleaned_data = clean_data(data, valid_fields)
    team.from_dict(cleaned_data)
    db.session.commit()

    return responses.request_success(f'Team {team.name} updated', 'api.get_team', team_id=team.id)


@bp.route('/teams/<int:team_id>/players', methods=['GET'])
@req_app_token
def get_team_players(team_id):
    team = ensure_exists(Team, id=team_id)

    current = request.args.get('current', False, bool)

    team_players = PlayerTeam.get_players_dict(team.id, current)

    return team_players


@bp.route('/teams/<int:team_id>/players/season/<int:season_division_id>', methods=['GET'])
@req_app_token
def get_team_players_in_season(team_id, season_division_id):
    # get team
    team = ensure_exists(Team, id=team_id)
    # get season_division
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    # query the teams playerlist for players active during the season
    # uses (player_start_date is earlier than season_end) and (player_end_date is later than season_start)
    season_start = datetime.combine(season_division.season.start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    season_end = datetime.combine(season_division.season.end_date, datetime.min.time()).replace(tzinfo=timezone.utc)

    players = {}
    for player_assoc in team.player_association:
        player_start_date = player_assoc.start_date.replace(tzinfo=timezone.utc)
        player_end_date = player_assoc.end_date.replace(tzinfo=timezone.utc) if player_assoc.end_date is not None else None
        if player_start_date < season_end and (player_end_date is None or player_end_date > season_start):
            player = {
                'name': player_assoc.player.player_name,
                'start_date': player_assoc.start_date,
                'end_date': player_assoc.end_date,
                '_links': {
                    'self': url_for('api.get_player', player_id=player_assoc.player.id)
                }
            }
            players[player_assoc.player.id] = player

    response = {
        'season_division': f'{season_division.get_readable_name()} ({season_division.season.league.acronym})',
        'team': team.name,
        'acronym': team.acronym,
        'color': team.color,
        'players': players,
        '_links': {
            'self': url_for('api.get_team_players_in_season', team_id=team.id, season_division_id=season_division.id),
            'team': url_for('api.get_team', team_id=team.id)
        }
    }
    return response


@bp.route('/teams/<int:team_id>/seasons', methods=['GET'])
@req_app_token
def get_team_seasons(team_id):
    pass


@bp.route('/teams/<int:team_id>/seasons', methods=['POST'])
@req_app_token
def register_team_season(team_id):
    pass


@bp.route('/teams/<int:team_id>/awards', methods=['GET'])
@req_app_token
def get_team_awards(team_id):
    pass


@bp.route('/teams/<int:team_id>/awards', methods=['POST'])
@req_app_token
def give_team_award(team_id):
    pass
