"""Endpoints Relating to SeasonDivisions"""
from api.srlm.app import db
from api.srlm.app.api.league import league_bp as league
from api.srlm.app.api.utils import responses
from flask import request
from api.srlm.app.api.utils.errors import ResourceNotFound, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields
from api.srlm.app.models import SeasonDivision, FreeAgent, Season, Division
from api.srlm.app.api.auth.utils import req_app_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@league.route('/season_division/<int:season_division_id>', methods=['GET'])
@req_app_token
def get_season_division(season_division_id):
    season_division = ensure_exists(SeasonDivision, id=season_division_id)
    return season_division.to_dict()


@league.route('/season_division', methods=['POST'])
@req_app_token
def add_season_division():
    data = request.get_json()
    required_fields = ['season_id', 'division_id']
    force_fields(data, required_fields)

    season = ensure_exists(Season, id=data['season_id'])
    division = ensure_exists(Division, id=data['division_id'])

    season_division_exists = ensure_exists(SeasonDivision, return_none=True, season_id=season.id, division_id=division.id)

    if season_division_exists:
        raise BadRequest('SeasonDivision already exists')

    season_division = SeasonDivision()
    season_division.season = season
    season_division.division = division
    db.session.add(season_division)
    db.session.commit()

    return responses.create_success(f'{season_division.get_readable_name()} created.',
                                    'api.league.get_season_division', season_division_id=season_division.id)


@league.route('/season_division/<int:season_division_id>/teams', methods=['GET'])
@req_app_token
def get_teams_in_season_division(season_division_id):
    # check season_division exists
    season_division = ensure_exists(SeasonDivision, id=season_division_id)
    # get list of teams
    teams = SeasonDivision.get_teams_dict(season_division.id)

    return teams


@league.route('/season_division/<int:season_division_id>/rookies', methods=['GET'])
@req_app_token
def get_rookies_in_season_division(season_division_id):
    # check season_division exists
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    return season_division.get_rookies_dict()


@league.route('/season_division/<int:season_division_id>/free_agents', methods=['GET'])
@req_app_token
def get_free_agents_in_season_division(season_division_id):
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    free_agents = FreeAgent.get_season_free_agents(season_division.id)

    if free_agents is None:
        raise ResourceNotFound('No free agents in the specified season')

    return free_agents


@league.route('/season_division/<int:season_division_id>/matches', methods=['GET'])
@req_app_token
def get_matches_in_season_division(season_division_id):
    season_division = ensure_exists(SeasonDivision, id=season_division_id)
    unplayed = request.args.get('unplayed', False, bool)
    matches = []
    for match in season_division.matches:
        if match.results is None or not unplayed:
            matches.append(match.to_simple_dict())

    response = season_division.to_simple_dict()
    response['matches'] = matches
    return response


@league.route('/season_division/<int:season_division_id>/finals', methods=['GET'])
@req_app_token
def get_finals_in_season_division(season_division_id):
    pass
