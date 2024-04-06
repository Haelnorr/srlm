from api.srlm.app import db
from api.srlm.app.api import bp
from flask import request, url_for
from api.srlm.app.api.utils import responses
from api.srlm.app.api.utils.functions import force_fields, clean_data, ensure_exists, force_unique
from api.srlm.app.models import Division, League
from api.srlm.app.api.auth.utils import req_app_token
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/divisions', methods=['GET'])
@req_app_token
def get_divisions():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Division.to_collection_dict(sa.select(Division), page, per_page, 'api.get_divisions')


@bp.route('/divisions/<int:division_id>', methods=['GET'])
@req_app_token
def get_division(division_id):
    division = ensure_exists(Division, id=division_id)
    if division:
        return division.to_dict()


@bp.route('/divisions', methods=['POST'])
@req_app_token
def add_division():
    data = request.get_json()

    required_fields = ['name', 'acronym', 'league']
    valid_fields = ['name', 'acronym', 'league_id', 'description']
    unique_fields = ['name', 'acronym']

    force_fields(data, required_fields)
    league = ensure_exists(League, join_method='or', id=data['league'], acronym=data['league'])
    data['league_id'] = league.id

    force_unique(Division, data, unique_fields, restrict_query={'league_id': league.id})

    cleaned_data = clean_data(data, valid_fields)

    division = Division()
    division.from_dict(cleaned_data)

    db.session.add(division)
    db.session.commit()

    return responses.create_success(f'{league.acronym} {division.name} added', 'api.get_division', division_id=division.id)


@bp.route('/divisions/<int:division_id>', methods=['PUT'])
@req_app_token
def update_division(division_id):
    data = request.get_json()

    division = ensure_exists(Division, id=division_id)

    unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'description']
    force_unique(Division, data, unique_fields, restrict_query={'league_id': division.league.id})
    cleaned_data = clean_data(data, valid_fields)

    division.from_dict(cleaned_data)

    db.session.commit()

    return responses.request_success(f'Division {division.name} updated', 'api.get_division', division_id=division.id)


@bp.route('/divisions/<int:division_id>/seasons', methods=['GET'])
@req_app_token
def get_seasons_of_division(division_id):

    division = ensure_exists(Division, id=division_id)

    seasons = []
    for season in division.seasons:
        data = {
            'id': season.id,
            'name': season.name,
            'acronym': season.acronym,
            '_links': {
                'self': url_for('api.get_season', season_id=season.id)
            }
        }
        seasons.append(data)

    response = {
        'division': division.name,
        'acronym': division.acronym,
        'league': division.league.acronym,
        'seasons': seasons,
        '_links': {
            'self': url_for('api.get_seasons_of_division', division_id=division_id),
            'league': url_for('api.get_league', league_id_or_acronym=division.league.id)
        }
    }

    return response
