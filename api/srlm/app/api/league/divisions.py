"""Endpoints relating to Divisions"""
from apifairy import arguments, body, response, authenticate, other_responses

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from flask import request, url_for, Blueprint
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.functions import force_fields, clean_data, ensure_exists, force_unique
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, DivisionCollection, DivisionSchema, LinkSuccessSchema, \
    UpdateDivisionSchema, SeasonsOfDivision
from api.srlm.app.models import Division, League
from api.srlm.app.api.auth.utils import app_auth
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


divisions = Blueprint('divisions', __name__)
bp.register_blueprint(divisions, url_prefix='/divisions')


@divisions.route('', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(PaginationArgs())
@response(DivisionCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_divisions(pagination):
    """Get the collection of all divisions"""
    page = pagination['page']
    per_page = pagination['per_page']
    return Division.to_collection_dict(sa.select(Division), page, per_page, 'api.divisions.get_divisions')


@divisions.route('/<int:division_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(DivisionSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_division(division_id):
    """Get details of a division"""
    division = ensure_exists(Division, id=division_id)
    if division:
        return division.to_dict()


@divisions.route('', methods=['POST'])
@body(DivisionSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_division():
    """Create a new division"""
    data = request.get_json()

    required_fields = ['name', 'acronym', 'league']
    valid_fields = ['name', 'acronym', 'league_id', 'description']
    unique_fields = ['name', 'acronym']

    force_fields(data, required_fields)
    league_db = ensure_exists(League, join_method='or', id=data['league'], acronym=data['league'])
    data['league_id'] = league_db.id

    force_unique(Division, data, unique_fields, restrict_query={'league_id': league_db.id})

    cleaned_data = clean_data(data, valid_fields)

    division = Division()
    division.from_dict(cleaned_data)

    db.session.add(division)
    db.session.commit()

    return responses.create_success(f'{league_db.acronym} {division.name} added', 'api.divisions.get_division', division_id=division.id)


@divisions.route('/<int:division_id>', methods=['PUT'])
@body(UpdateDivisionSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_division(division_id):
    """Update an existing division"""
    data = request.get_json()

    division = ensure_exists(Division, id=division_id)

    unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'description']
    force_unique(Division, data, unique_fields, restrict_query={'league_id': division.league.id})
    cleaned_data = clean_data(data, valid_fields)

    division.from_dict(cleaned_data)

    db.session.commit()

    return responses.request_success(f'Division {division.name} updated', 'api.divisions.get_division', division_id=division.id)


@divisions.route('/<int:division_id>/seasons', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(SeasonsOfDivision())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_seasons_of_division(division_id):
    """Get a list of seasons the division has been part of"""

    division = ensure_exists(Division, id=division_id)

    seasons = []
    for season in division.seasons:
        data = {
            'id': season.id,
            'name': season.name,
            'acronym': season.acronym,
            '_links': {
                'self': url_for('api.seasons.get_season', season_id=season.id)
            }
        }
        seasons.append(data)

    response_json = {
        'division': division.name,
        'acronym': division.acronym,
        'league': division.league.acronym,
        'seasons': seasons,
        '_links': {
            'self': url_for('api.divisions.get_seasons_of_division', division_id=division_id),
            'league': url_for('api.leagues.get_league', league_id_or_acronym=division.league.id)
        }
    }

    return response_json
