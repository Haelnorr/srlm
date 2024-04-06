from flask import request
from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import req_app_token
from api.srlm.app.api.utils.errors import BadRequest
from api.srlm.app.api.utils.functions import force_fields, ensure_exists, clean_data
from api.srlm.app.models import SeasonDivision, Team, Match, MatchSchedule


@bp.route('/match', methods=['POST'])
@req_app_token
def create_match():
    data = request.get_json()

    required_fields = ['season_division_id', 'home_team_id', 'away_team_id']
    force_fields(data, required_fields)

    season_division = ensure_exists(SeasonDivision, id=data['season_division_id'])
    if data['home_team_id'] == data['away_team_id']:
        raise BadRequest('Team cannot play itself')
    home_team = ensure_exists(Team, id=data['home_team_id'])
    away_team = ensure_exists(Team, id=data['away_team_id'])
    # ensure they are registered to the season
    if season_division not in home_team.season_divisions:
        raise BadRequest(f'Team {home_team.name} not registered to {season_division.get_readable_name()}')
    if season_division not in away_team.season_divisions:
        raise BadRequest(f'Team {away_team.name} not registered to {season_division.get_readable_name()}')

    # create match
    valid_fields = ['season_division_id', 'home_team_id', 'away_team_id', 'round', 'match_week']
    cleaned_data = clean_data(data, valid_fields)
    match = Match()
    match.from_dict(cleaned_data)

    # create match_schedule entry
    match.schedule = MatchSchedule()

    db.session.add(match)
    db.session.commit()

    return responses.create_success(f'Match between {match.home_team.name} and {match.away_team.name} created', 'api.get_match', match_id=match.id)


@bp.route('/match/<int:match_id>', methods=['GET'])
@req_app_token
def get_match(match_id):
    match = ensure_exists(Match, id=match_id)
    response = match.to_dict()
    if match.results is not None:
        response = match.results.to_dict()
    return response


def get_match_review():
    pass


def update_match_review():
    pass


def get_match_stats():
    pass


def report_issue():
    pass
