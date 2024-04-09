"""Endpoints relating to Leagues"""
from apifairy import arguments, body, response, authenticate, other_responses

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import request, Blueprint

from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.functions import force_fields, clean_data, force_unique, ensure_exists
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, LeagueCollection, LeagueSchema, LinkSuccessSchema, \
    EditLeagueSchema, DivisionsInLeague, SeasonsInLeague
from api.srlm.app.models import League, Season, Division
from api.srlm.app.api.auth.utils import app_auth
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


leagues = Blueprint('leagues', __name__)
bp.register_blueprint(leagues, url_prefix='/leagues')


@leagues.route('', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(PaginationArgs())
@response(LeagueCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_leagues(pagination):
    """Get the collection of all leagues"""
    page = pagination['page']
    per_page = pagination['per_page']
    return League.to_collection_dict(sa.select(League), page, per_page, 'api.leagues.get_leagues')


@leagues.route('/<league_id_or_acronym>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(LeagueSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_league(league_id_or_acronym):
    """Get the details of a league"""
    league_db = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)
    if league_db:
        return league_db.to_dict()


@leagues.route('', methods=['POST'])
@body(LeagueSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_leagues():
    """Create a new league"""
    data = request.get_json()

    required_fields = unique_fields = valid_fields = ['name', 'acronym']
    force_fields(data, required_fields)
    force_unique(League, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    league_db = League()
    league_db.from_dict(cleaned_data)

    db.session.add(league_db)
    db.session.commit()

    return responses.create_success(f'League {league_db.name} added', 'api.leagues.get_league', league_id_or_acronym=league_db.id)


@leagues.route('/<league_id_or_acronym>', methods=['PUT'])
@body(EditLeagueSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_leagues(league_id_or_acronym):
    """Update an existing league"""
    data = request.get_json()

    league_db = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    unique_fields = valid_fields = ['name', 'acronym']
    force_unique(League, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    league_db.from_dict(cleaned_data)

    db.session.commit()

    return responses.request_success(f'League {league_db.name} updated', 'api.leagues.get_league', league_id_or_acronym=league_db.id)


@leagues.route('/<league_id_or_acronym>/seasons', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(PaginationArgs())
@response(SeasonsInLeague())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_league_seasons(pagination, league_id_or_acronym):
    """Get the list of seasons in a league"""
    page = pagination['page']
    per_page = pagination['per_page']

    league_db = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    query = league_db.seasons.order_by(Season.start_date.desc())

    seasons = Season.to_collection_dict(query, page, per_page, 'api.leagues.get_league_seasons', league_id_or_acronym=league_db.id)

    response_json = {
        'league': league_db.name,
        'acronym': league_db.acronym,
        'seasons': seasons
    }

    return response_json


@leagues.route('/<league_id_or_acronym>/divisions', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(PaginationArgs())
@response(DivisionsInLeague())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_league_divisions(pagination, league_id_or_acronym):
    """Get the list of division in a league"""
    page = pagination['page']
    per_page = pagination['per_page']

    league_db = ensure_exists(League, join_method='or', id=league_id_or_acronym, acronym=league_id_or_acronym)

    divisions = Division.to_collection_dict(league_db.divisions, page, per_page, 'api.leagues.get_league_divisions', league_id_or_acronym=league_db.id)

    response_json = {
        'league': league_db.name,
        'acronym': league_db.acronym,
        'divisions': divisions
    }

    return response_json
