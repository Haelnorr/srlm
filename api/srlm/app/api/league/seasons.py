from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import request
from api.srlm.app.api.utils.functions import force_fields, clean_data, force_unique, ensure_exists, \
    force_date_format
from api.srlm.app.models import Season, League, SeasonDivision, Matchtype
from api.srlm.app.api.auth.utils import req_app_token
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/seasons', methods=['GET'])
@req_app_token
def get_seasons():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Season.to_collection_dict(sa.select(Season), page, per_page, 'api.get_seasons')


@bp.route('/seasons/<int:season_id>', methods=['GET'])
@req_app_token
def get_season(season_id):
    season = ensure_exists(Season, id=season_id)
    if season:
        return season.to_dict()


@bp.route('/seasons', methods=['POST'])
@req_app_token
def add_season():
    data = request.get_json()

    unique_fields = ['name', 'acronym']
    required_fields = ['name', 'acronym', 'league', 'match_type']
    valid_fields = ['name', 'acronym', 'league_id', 'start_date', 'end_date', 'finals_start', 'finals_end', 'match_type_id']

    force_fields(data, required_fields)
    league = ensure_exists(League, join_method='or', id=data['league'], acronym=data['league'])
    match_type = ensure_exists(Matchtype, join_method='or', id=data['match_type'], name=data['match_type'])
    data['league_id'] = league.id
    data['match_type_id'] = match_type.id

    force_unique(Season, data, unique_fields, restrict_query={'league_id': league.id})

    date_fields = ['start_date', 'end_date', 'finals_start', 'finals_end']
    force_date_format(data, date_fields)

    cleaned_data = clean_data(data, valid_fields)

    season = Season()
    season.from_dict(cleaned_data)

    db.session.add(season)
    db.session.commit()

    return responses.create_success(f'{season.league.acronym} {season.name} added', 'api.get_season', season_id=season.id)


@bp.route('/seasons/<int:season_id>', methods=['PUT'])
@req_app_token
def update_season(season_id):
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

    return responses.request_success(f'Season {season.name} updated', 'api.get_season', season_id=season.id)


@bp.route('/seasons/<int:season_id>/divisions', methods=['GET'])
@req_app_token
def get_divisions_in_season(season_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    season = ensure_exists(Season, id=season_id)

    divisions = SeasonDivision.to_collection_dict(season.division_association, page, per_page, 'api.get_divisions_in_season', season_id=season_id)

    response = {
        'season': season.name,
        'acronym': season.acronym,
        'league': season.league.acronym
    }
    response.update(divisions)

    return response
