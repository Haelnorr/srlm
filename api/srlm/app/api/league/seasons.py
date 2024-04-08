"""Endpoints relating to Seasons"""
from apifairy import arguments, body, response, authenticate, other_responses

from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import request, Blueprint
from api.srlm.app.api.utils.functions import force_fields, clean_data, force_unique, ensure_exists, \
    force_date_format
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, SeasonSchema, LinkSuccessSchema, SeasonCollection, \
    DivisionsInSeason
from api.srlm.app.models import Season, League, SeasonDivision, Matchtype
from api.srlm.app.api.auth.utils import app_auth
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


seasons = Blueprint('seasons', __name__)
bp.register_blueprint(seasons, url_prefix='/seasons')


@seasons.route('/', methods=['GET'])
@arguments(PaginationArgs())
@response(SeasonCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_seasons(pagination):
    """Get the collection of all seasons"""
    page = pagination['page']
    per_page = pagination['per_page']
    return Season.to_collection_dict(sa.select(Season), page, per_page, 'api.seasons.get_seasons')


@seasons.route('/<int:season_id>', methods=['GET'])
@response(SeasonSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_season(season_id):
    """Get details on a season"""
    season = ensure_exists(Season, id=season_id)
    if season:
        return season.to_dict()


@seasons.route('/', methods=['POST'])
@body(SeasonSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_season():
    """Create a new season"""
    data = request.get_json()

    unique_fields = ['name', 'acronym']
    required_fields = ['name', 'acronym', 'league', 'match_type']
    valid_fields = ['name', 'acronym', 'league_id', 'start_date', 'end_date', 'finals_start', 'finals_end', 'match_type_id']

    force_fields(data, required_fields)
    league_db = ensure_exists(League, join_method='or', id=data['league'], acronym=data['league'])
    match_type = ensure_exists(Matchtype, join_method='or', id=data['match_type'], name=data['match_type'])
    data['league_id'] = league_db.id
    data['match_type_id'] = match_type.id

    force_unique(Season, data, unique_fields, restrict_query={'league_id': league_db.id})

    date_fields = ['start_date', 'end_date', 'finals_start', 'finals_end']
    force_date_format(data, date_fields)

    cleaned_data = clean_data(data, valid_fields)

    season = Season()
    season.from_dict(cleaned_data)

    db.session.add(season)
    db.session.commit()

    return responses.create_success(f'{season.league.acronym} {season.name} added', 'api.seasons.get_season', season_id=season.id)


@seasons.route('/<int:season_id>', methods=['PUT'])
@body(SeasonSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_season(season_id):
    """Update an existing season"""
    data = request.get_json()

    season = ensure_exists(Season, id=season_id)

    unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'start_date', 'end_date', 'finals_start', 'finals_end']
    force_unique(Season, data, unique_fields, restrict_query={'league_id': season.league.id})

    date_fields = ['start_date', 'end_date', 'finals_start', 'finals_end']
    force_date_format(data, date_fields)

    cleaned_data = clean_data(data, valid_fields)

    season.from_dict(cleaned_data)

    db.session.commit()

    return responses.request_success(f'Season {season.name} updated', 'api.seasons.get_season', season_id=season.id)


@seasons.route('/<int:season_id>/divisions', methods=['GET'])
@arguments(PaginationArgs())
@response(DivisionsInSeason())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_divisions_in_season(pagination, season_id):
    """Get a list of divisions in a season"""
    page = pagination['page']
    per_page = pagination['per_page']

    season = ensure_exists(Season, id=season_id)

    divisions = SeasonDivision.to_collection_dict(season.division_association, page, per_page, 'api.seasons.get_divisions_in_season', season_id=season_id)

    response_json = {
        'season': season.name,
        'acronym': season.acronym,
        'league': season.league.acronym
    }
    response_json.update(divisions)

    return response_json
