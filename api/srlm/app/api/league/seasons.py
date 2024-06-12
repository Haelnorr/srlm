"""Endpoints relating to Seasons"""
from datetime import datetime, timezone

from apifairy import arguments, body, response, authenticate, other_responses

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import Blueprint, jsonify

from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.errors import ResourceNotFound
from api.srlm.app.api.utils.functions import force_fields, clean_data, force_unique, ensure_exists
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, ReassignSeasonApplicationSchema, SeasonSchema, LinkSuccessSchema, SeasonCollection, \
    DivisionsInSeason, SeasonFilters, SeasonLookup, EditSeasonSchema, SeasonApplicationSchema, BasicSuccessSchema, \
    SeasonApplicationsList
from api.srlm.app.models import Season, League, SeasonDivision, Matchtype, SeasonRegistration, Division
from api.srlm.app.api.auth.utils import app_auth
import sqlalchemy as sa

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


seasons = Blueprint('seasons', __name__)
bp.register_blueprint(seasons, url_prefix='/seasons')


@seasons.route('', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(SeasonFilters())
@response(SeasonCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_seasons(search_filters):
    """Get a collection of seasons
    Specifying either `last` or `next` will return a paginated list with 1 per page. If multiple results for
    the query, will be ordered by relevant (i.e. `last` will be ordered by most-recent first).

    Specifying `start_date` or `end_date` will set the start/end window for the query (finals included). Must be
    in format "yyyy-mm-dd".

    `league` can be a leagues ID or acronym.
    """
    league_filter = search_filters.get('league', None)
    current_season = search_filters.get('current', None)
    last_season = search_filters.get('last', None)
    next_season = search_filters.get('next', None)
    start_date = search_filters.get('start_date', None)
    end_date = search_filters.get('end_date', None)
    order = search_filters['order']
    order_by = search_filters['order_by']
    page = search_filters['page']
    per_page = search_filters['per_page']

    query = db.session.query(Season)

    query = query.order_by(
        getattr(sa, order)(
            getattr(Season, order_by)
        ))

    now = datetime.now(timezone.utc)

    if current_season:
        query = query.filter(
            Season.start_date <= now,
            sa.or_(
                Season.finals_end >= now,
                Season.finals_end.is_(None)
            )
        )

    elif last_season:
        query = query.filter(
            Season.finals_end < now
        ).order_by(sa.desc(Season.finals_end))
        per_page = 1

    elif next_season:
        query = query.filter(
            Season.start_date > now
        ).order_by(sa.asc(Season.start_date))
        per_page = 1
    else:
        if start_date:
            query = query.filter(
                Season.start_date >= start_date
            )
        if end_date:
            query = query.filter(
                Season.finals_end <= end_date
            )

    if league_filter:
        league_filter = league_filter.upper()
        league = ensure_exists(League, return_none=True, join_method='or', id=league_filter, acronym=league_filter)
        query = query.filter(Season.league_id == league.id)

    return Season.to_collection_dict(query, page, per_page, 'api.seasons.get_seasons')


@seasons.route('/<season_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@arguments(SeasonLookup())
@response(SeasonSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_season(search, season_id):
    """Get details on a season.
    Can search by ID or acronym. If searching by acronym, league query is required."""
    league_filter = search.get('league', None)

    if not league_filter:
        season = ensure_exists(Season, id=season_id)
    else:
        league_filter = league_filter.upper()
        league = ensure_exists(League, return_none=True, acronym=league_filter)

        query = db.session.query(Season) \
            .filter(Season.league_id == league.id)
        try:
            season_id = int(season_id)
            season = query.filter(Season.id == season_id).first()
        except ValueError:
            season = query.filter(Season.acronym.ilike(season_id)).first()

        if not season:
            raise ResourceNotFound(f'No season found with the identifier {season_id}')

    return season.to_dict()


@seasons.route('', methods=['POST'])
@body(SeasonSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_season(data):
    """Create a new season"""

    unique_fields = ['name', 'acronym']
    required_fields = ['name', 'acronym', 'league', 'match_type']
    valid_fields = ['name', 'acronym', 'league_id', 'start_date', 'end_date', 'finals_start', 'finals_end',
                    'match_type_id', 'can_register']

    force_fields(data, required_fields)
    league_db = ensure_exists(League, join_method='or', id=data['league'], acronym=data['league'].upper())
    match_type = ensure_exists(Matchtype, join_method='or', id=data['match_type'], name=data['match_type'])
    data['league_id'] = league_db.id
    data['match_type_id'] = match_type.id

    force_unique(Season, data, unique_fields, restrict_query={'league_id': league_db.id})

    cleaned_data = clean_data(data, valid_fields)

    season = Season()
    season.from_dict(cleaned_data)

    db.session.add(season)
    db.session.commit()

    return responses.create_success(f'{season.league.acronym} {season.name} added', 'api.seasons.get_season', season_id=season.id)


@seasons.route('/<int:season_id>', methods=['PUT'])
@body(EditSeasonSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_season(data, season_id):
    """Update an existing season"""

    season = ensure_exists(Season, id=season_id)

    unique_fields = ['name', 'acronym']

    for field in unique_fields:
        if field in data:
            if data[field] == getattr(season, field):
                del data[field]

    force_unique(Season, data, unique_fields, restrict_query={'league_id': season.league.id})

    season.from_dict(data)

    db.session.commit()

    return responses.request_success(f'Season {season.name} updated', 'api.seasons.get_season', season_id=season.id)


@seasons.route('/<int:season_id>/divisions', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
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
        'league': season.league.acronym,
        'divisions': divisions
    }

    return response_json


@seasons.route('/apply', methods=['POST'])
@body(SeasonApplicationSchema())
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def action_application(data):
    """Action an application to join a season
    Accepting just marks application as accepted. To allocate to a division and complete the application
    use `action: "assign"` and provide a `division_id`.
    """
    application = ensure_exists(SeasonRegistration, id=data['application_id'])
    action = data['action']

    if action == 'accept':
        application.accept()

    elif action == 'reject':
        application.reject()

    elif action == 'assign':
        division = ensure_exists(Division, id=data['division_id'])
        application.allocate_to_division(division)

    return responses.request_success(f'Application {action}ed')


@seasons.route('/applications/reassign', methods=['POST'])
@body(ReassignSeasonApplicationSchema())
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def reassign_application(data):
    """Reassign a team that has been accepted into a division for a season"""
    application = ensure_exists(SeasonRegistration, id=data['application_id'])
    division = ensure_exists(Division, id=data['division_id'])
    if data['purge_data']:
        application.remove_from_division(reallocate=True)

    application.allocate_to_division(division)
    return responses.request_success('Application reassigned')


@seasons.route('/applications/<int:app_id>/remove', methods=['POST'])
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def remove_team_from_division(app_id):
    """Remove a team from the allocated division and withdraw their application"""
    application = ensure_exists(SeasonRegistration, id=app_id)
    application.remove_from_division()
    return responses.request_success('Application withdrawn')
    

@seasons.route('/applications', methods=['GET'])
@response(SeasonApplicationsList())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_applications():
    """Get a list of applications to register for a season"""
    applications_query = db.session.query(SeasonRegistration) \
        .filter(SeasonRegistration.status.in_(['Pending', 'Accepted']))
    completed_query = db.session.query(SeasonRegistration).filter(SeasonRegistration.status == 'Completed').limit(20)
    applications = applications_query.all() + completed_query.all()

    seasons_list = {}

    team_applications = []
    free_agent_applications = []
    recently_accepted = []

    for application in applications:
        app_dict = application.to_dict()
        if application.season_id not in seasons_list:
            seasons_list[application.season_id] = []
            for div in application.season.divisions:
                seasons_list[application.season_id].append({
                    'id': div.id,
                    'name': div.name
                })
        app_dict['divisions'] = seasons_list[application.season_id]
        if application.status == 'Completed':
            recently_accepted.append(app_dict)
        else:
            if application.type == 'team':
                team_applications.append(app_dict)
            else:
                free_agent_applications.append(app_dict)

    response_json = {
        'team_applications': team_applications,
        'free_agent_applications': free_agent_applications,
        'recently_accepted': recently_accepted
    }
    return response_json


@seasons.route('/applications/<int:season_id>', methods=['GET'])
@response(SeasonApplicationsList())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_applications_for_season(season_id):
    """Get a list of applications to register for a specific season"""

    applications_query = db.session.query(SeasonRegistration) \
        .filter(SeasonRegistration.status.in_(['Pending', 'Accepted', 'Completed'])) \
        .filter(SeasonRegistration.season_id == season_id)

    seasons_list = {}

    team_applications = []
    free_agent_applications = []

    for application in applications_query:
        app_dict = application.to_dict()
        if application.season_id not in seasons_list:
            seasons_list[application.season_id] = []
            for div in application.season.divisions:
                seasons_list[application.season_id].append({
                    'id': div.id,
                    'name': div.name
                })
        app_dict['divisions'] = seasons_list[application.season_id]
        if application.type == 'team':
            team_applications.append(app_dict)
        else:
            free_agent_applications.append(app_dict)

    response_json = {
        'team_applications': team_applications,
        'free_agent_applications': free_agent_applications
    }
    return response_json


# This is the 'I hate React' section. Fuck you React, fuck you
@seasons.route('/list', methods=['GET'])
def get_season_list():
    """Get a list of season ID's and names"""
    seasons_db = db.session.query(Season.id, Season.name).order_by(sa.desc(Season.id))
    season_dicts = [{
        'id': sid,
        'name': name
    } for sid, name in seasons_db]
    response_json = {
        'seasons': season_dicts
    }
    return response_json


@seasons.route('/<int:season_id>/divisions-list', methods=['GET'])
def get_divisions_in_season_list(season_id):
    """Get a list of season_division ID's and names for a given season"""
    season = ensure_exists(Season, id=season_id)

    divisions = [{
        'id': season_division.id,
        'name': season_division.division.name
    } for season_division in season.division_association]

    response_json = {
        'divisions': divisions
    }
    return response_json
