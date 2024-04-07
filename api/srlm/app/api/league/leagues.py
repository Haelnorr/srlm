"""Endpoints relating to Leagues"""
from api.srlm.app import db
from api.srlm.app.api.league import league_bp as league
from api.srlm.app.api.utils import responses
from flask import request
from api.srlm.app.api.utils.functions import force_fields, clean_data, force_unique, ensure_exists
from api.srlm.app.models import League, Season, Division
from api.srlm.app.api.auth.utils import req_app_token
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@league.route('/leagues', methods=['GET'])
@req_app_token
def get_leagues():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return League.to_collection_dict(sa.select(League), page, per_page, 'api.league.get_leagues')


@league.route('/leagues/<league_id_or_acronym>', methods=['GET'])
@req_app_token
def get_league(league_id_or_acronym):
    league = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)
    if league:
        return league.to_dict()


@league.route('/leagues', methods=['POST'])
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

    return responses.create_success(f'League {league.name} added', 'api.league.get_league', league_id_or_acronym=league.id)


@league.route('/leagues/<league_id_or_acronym>', methods=['PUT'])
@req_app_token
def update_leagues(league_id_or_acronym):
    data = request.get_json()

    league = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    unique_fields = valid_fields = ['name', 'acronym']
    force_unique(League, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    league.from_dict(cleaned_data)

    db.session.commit()

    return responses.request_success(f'League {league.name} updated', 'api.league.get_league', league_id_or_acronym=league.id)


@league.route('/leagues/<league_id_or_acronym>/seasons', methods=['GET'])
@req_app_token
def get_league_seasons(league_id_or_acronym):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    league = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    query = league.seasons.order_by(Season.start_date.desc())

    seasons = Season.to_collection_dict(query, page, per_page, 'api.league.get_league_seasons', league_id_or_acronym=league.id)

    response = {
        'league': league.name,
        'acronym': league.acronym
    }
    response.update(seasons)

    return response


@league.route('/leagues/<league_id_or_acronym>/divisions', methods=['GET'])
@req_app_token
def get_league_divisions(league_id_or_acronym):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    league = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    divisions = Division.to_collection_dict(league.divisions, page, per_page, 'api.league.get_league_divisions', league_id_or_acronym=league.id)

    response = {
        'league': league.name,
        'acronym': league.acronym
    }
    response.update(divisions)

    return response
