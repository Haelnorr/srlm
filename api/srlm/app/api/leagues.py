from api.srlm.app import db
from api.srlm.app.api import bp, responses
from flask import request, url_for

from api.srlm.app.api.errors import BadRequest
from api.srlm.app.api.functions import force_fields, clean_data, force_unique, ensure_exists
from api.srlm.app.models import League, Season, Division
from api.srlm.app.api.auth import req_app_token
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/leagues', methods=['GET'])
@req_app_token
def get_leagues():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return League.to_collection_dict(sa.select(League), page, per_page, 'api.get_leagues')


@bp.route('/leagues/<int:league_id>', methods=['GET'])
@req_app_token
def get_league(league_id):
    league = ensure_exists(League, id=league_id)
    if league:
        return league.to_dict()


@bp.route('/leagues', methods=['POST'])
@req_app_token
def add_leagues():
    data = request.get_json()

    required_fields = unique_fields = valid_fields = ['name', 'acronym']
    force_fields(data, required_fields)
    force_unique(League, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    league = League()
    league.from_dict(cleaned_data)

    db.session.add(league)
    db.session.commit()

    return responses.create_success(f'League {league.name} added', 'api.get_league', league_id=league.id)


@bp.route('/leagues/<int:league_id>', methods=['PUT'])
@req_app_token
def update_leagues(league_id):
    data = request.get_json()

    league = ensure_exists(League, id=league_id)

    unique_fields = valid_fields = ['name', 'acronym']
    force_unique(League, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    league.from_dict(cleaned_data)

    db.session.commit()

    return responses.update_success(f'League {league.name} updated', 'api.get_league', league_id=league.id)


@bp.route('/leagues/<int:league_id>/seasons', methods=['GET'])
@req_app_token
def get_league_seasons(league_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    league = ensure_exists(League, id=league_id)

    query = league.seasons.order_by(Season.start_date.desc())

    seasons = Season.to_collection_dict(query, page, per_page, 'api.get_league_seasons', league_id=league_id)

    response = {
        'league': league.name,
        'acronym': league.acronym
    }
    response.update(seasons)

    return response


@bp.route('/leagues/<int:league_id>/divisions', methods=['GET'])
@req_app_token
def get_league_divisions(league_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    league = ensure_exists(League, id=league_id)

    divisions = Division.to_collection_dict(league.divisions, page, per_page, 'api.get_league_divisions', league_id=league_id)

    response = {
        'league': league.name,
        'acronym': league.acronym
    }
    response.update(divisions)

    return response
