"""Provides endpoints for creating matches and retrieving match data"""
from apifairy import body, response, authenticate, other_responses
from flask import request
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.api.game import game_bp as game
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import req_app_token, user_auth
from api.srlm.app.api.utils.errors import BadRequest
from api.srlm.app.api.utils.functions import force_fields, ensure_exists, clean_data
from api.srlm.app.fairy.errors import unauthorized, bad_request, not_found
from api.srlm.app.fairy.schemas import LinkSuccessSchema, NewMatchSchema, ViewMatchSchema, MatchReviewSchema
from api.srlm.app.models import SeasonDivision, Team, Match, MatchSchedule, MatchReview, MatchData


@game.route('/match', methods=['POST'])
@req_app_token
@body(NewMatchSchema())
@response(LinkSuccessSchema(), 201)
@authenticate(user_auth)
@other_responses(unauthorized | bad_request)
def create_match():
    """Create a new match"""
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

    return responses.create_success(f'Match between {match.home_team.name} and {match.away_team.name} created', 'api.game.get_match', match_id=match.id)


@game.route('/match/<int:match_id>', methods=['GET'])
@req_app_token
@response(ViewMatchSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found)
def get_match(match_id):
    """Get details of a match"""
    match = ensure_exists(Match, id=match_id)
    response_json = match.to_dict()
    return response_json


@game.route('/match/<int:match_id>/review', methods=['GET'])
@req_app_token
@response(MatchReviewSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found)
def get_match_review(match_id):
    """Get the flags and match data of a match"""
    match = ensure_exists(Match, id=match_id)

    flags = db.session.query(MatchReview).filter_by(match_id=match_id)

    flags_data = []
    for flag in flags:
        flags_data.append(flag.to_dict())

    lobby_ids = []
    for lobby in match.lobbies:
        lobby_ids.append(lobby.id)

    period_query = db.session.query(MatchData).filter(MatchData.lobby_id.in_(lobby_ids)).order_by(sa.asc(MatchData.created))
    periods = []
    for period in period_query:
        period_data = period.to_dict()
        period_data['player_data'] = []
        for player in period.player_data_assoc:
            period_data['player_data'].append(player.to_dict())
        periods.append(period_data)

    response_json = {
        'match_id': match.id,
        'match_details': match.to_simple_dict(),
        'periods': periods,
        'flags': flags_data,
    }

    return response_json


def update_match_review():
    pass


def get_match_stats():
    pass


def report_issue():
    pass
