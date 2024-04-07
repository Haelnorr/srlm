"""Endpoints relating to Teams"""
from datetime import datetime, timezone
from api.srlm.app import db
from api.srlm.app.api.league import league_bp as league
from api.srlm.app.api.utils import responses
from flask import request, url_for
import sqlalchemy as sa
from api.srlm.app.api.utils.errors import ResourceNotFound, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.models import Team, SeasonDivision, PlayerTeam
from api.srlm.app.api.auth.utils import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@league.route('/teams', methods=['GET'])
@req_app_token
def get_teams():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Team.to_collection_dict(sa.select(Team), page, per_page, 'api.league.get_teams')


@league.route('/teams/<int:team_id>', methods=['GET'])
@req_app_token
def get_team(team_id):
    team = ensure_exists(Team, id=team_id)
    return team.to_dict()


@league.route('/teams', methods=['POST'])
@req_app_token
def add_team():
    data = request.get_json()

    required_fields = unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'color', 'logo', 'founded_date']

    force_fields(data, required_fields)
    force_unique(Team, data, unique_fields)

    cleaned_data = clean_data(data, valid_fields)

    if cleaned_data['color'] == "":
        cleaned_data['color'] = None

    team = Team()
    team.from_dict(cleaned_data)

    db.session.add(team)
    db.session.commit()

    return responses.create_success(f'Team {team.name} created', 'api.league.get_team', team_id=team.id)


@league.route('/teams/<int:team_id>', methods=['PUT'])
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

    return responses.request_success(f'Team {team.name} updated', 'api.league.get_team', team_id=team.id)


@league.route('/teams/<int:team_id>/players', methods=['GET'])
@req_app_token
def get_team_players(team_id):
    team = ensure_exists(Team, id=team_id)

    current = request.args.get('current', False, bool)

    team_players = PlayerTeam.get_players_dict(team.id, current)

    return team_players


@league.route('/teams/<int:team_id>/players/season/<int:season_division_id>', methods=['GET'])
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
                    'self': url_for('api.league.get_player', player_id=player_assoc.player.id)
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
            'self': url_for('api.league.get_team_players_in_season', team_id=team.id, season_division_id=season_division.id),
            'team': url_for('api.league.get_team', team_id=team.id)
        }
    }
    return response


@league.route('/teams/<int:team_id>/seasons', methods=['GET'])
@req_app_token
def get_team_seasons(team_id):
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    if team.season_divisions.count() == 0:
        raise ResourceNotFound('Team has not played in any seasons')

    # return list of seasons
    seasons = SeasonDivision.get_seasons_dict(team.id)
    return seasons


@league.route('/teams/<int:team_id>/seasons', methods=['POST'])
@req_app_token
def register_team_season(team_id):
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    # validate input
    data = request.get_json()
    force_fields(data, ['season_division_id'])

    # ensure season exists
    season_division = ensure_exists(SeasonDivision, id=data['season_division_id'])

    team_registered = team.season_divisions.filter_by(id=season_division.id).first()

    if team_registered:
        raise BadRequest(f'Team {team.name} already registered to {season_division.get_readable_name()}')

    # register team
    team.season_divisions.append(season_division)
    db.session.commit()

    return responses.request_success(f'Team {team.name} registered to {season_division.get_readable_name()}',
                                     'api.league.get_season_division', season_division_id=season_division.id)


@league.route('/teams/<int:team_id>/seasons/<int:season_division_id>', methods=['DELETE'])
@req_app_token
def deregister_team_season(team_id, season_division_id):
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    # ensure season exists
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    team_registered = team.season_divisions.filter_by(id=season_division.id).first()

    if not team_registered:
        raise BadRequest(f'Team {team.name} not registered to {season_division.get_readable_name()}')

    team.season_divisions.remove(season_division)
    db.session.commit()

    return responses.request_success(f'Team {team.name} de-registered from {season_division.get_readable_name()}',
                                     'api.league.get_season_division', season_division_id=season_division.id)


@league.route('/teams/<int:team_id>/awards', methods=['GET'])
@req_app_token
def get_team_awards(team_id):
    pass


@league.route('/teams/<int:team_id>/awards', methods=['POST'])
@req_app_token
def give_team_award(team_id):
    pass
