"""Endpoints Relating to SeasonDivisions"""
from apifairy import authenticate, other_responses, response, arguments, body

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import Blueprint
import sqlalchemy as sa
from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.errors import ResourceNotFound, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import SeasonDivisionSchema, SeasonDivisionLookup, LinkSuccessSchema, \
    SeasonDivisionTeams, SeasonDivisionRookies, SeasonDivisionFreeAgents, UnplayedFilterSchema, SeasonDivisionMatches
from api.srlm.app.models import SeasonDivision, FreeAgent, Season, Division, League
from api.srlm.app.api.auth.utils import app_auth

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


season_division = Blueprint('season_division', __name__)
bp.register_blueprint(season_division, url_prefix='/season_division')


@season_division.route('/<int:season_division_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(SeasonDivisionSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_season_division(season_division_id):
    """Get details of a SeasonDivision"""
    season_division_db = ensure_exists(SeasonDivision, id=season_division_id)
    return season_division_db.to_dict()


@season_division.route('', methods=['GET'])
@arguments(SeasonDivisionLookup())
@cache.cached(unless=force_refresh)
@response(SeasonDivisionSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def season_division_lookup(filters):
    """Get details of a SeasonDivision"""
    league_filter = filters['league']
    season_filter = filters['season']
    division_filter = filters['division']

    league = ensure_exists(League, join_method='or', id=league_filter, acronym=league_filter)

    season = db.session.query(Season).filter(sa.and_(
        sa.or_(
            Season.acronym == season_filter,
            Season.id == season_filter
        ),
        Season.league == league
    )).first()

    if not season:
        raise ResourceNotFound(f'No season matching {season_filter} in league {league.acronym}')

    division = db.session.query(Division).filter(
        sa.or_(
            Division.name.contains(division_filter),
            Division.acronym == division_filter
        ),
        Division.league == league
    ).first()

    if not division:
        raise ResourceNotFound(f'No division matching {division_filter} in league {league.name}')

    season_division_db = db.session.query(SeasonDivision).filter(
        SeasonDivision.season == season,
        SeasonDivision.division == division
    ).first()
    if not season_division_db:
        raise ResourceNotFound('No SeasonDivision found')
    return season_division_db.to_dict()


@season_division.route('', methods=['POST'])
@body(SeasonDivisionSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_season_division(data):
    """Create a new SeasonDivision
    Season must be specified by ID. Division can be specified by ID, or by combination of
    league acronym and division acronym.
    """
    season = ensure_exists(Season, id=data['season_id'])
    if 'league' and 'division_acronym' in data:
        division = db.session.query(Division).filter(
            sa.and_(
                Division.acronym == data['division_acronym'],
                Division.league.has(acronym=data['league'])
            )
        ).first()
    elif 'division_id' in data:
        division = ensure_exists(Division, id=data['division_id'])
    else:
        raise BadRequest('Missing division identifier')

    season_division_exists = ensure_exists(SeasonDivision, return_none=True, season_id=season.id, division_id=division.id)

    if season_division_exists:
        raise BadRequest('SeasonDivision already exists')

    season_division_db = SeasonDivision()
    season_division_db.season = season
    season_division_db.division = division
    db.session.add(season_division_db)
    db.session.commit()

    return responses.create_success(f'{season_division_db.get_readable_name()} created.',
                                    'api.season_division.get_season_division', season_division_id=season_division_db.id)


@season_division.route('/<int:season_division_id>/teams', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(SeasonDivisionTeams())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_teams_in_season_division(season_division_id):
    """Get a list of teams in a SeasonDivision
    Includes a list of players on each team that season
    """
    # check season_division exists
    season_division_db = ensure_exists(SeasonDivision, id=season_division_id)
    # get list of teams
    teams = SeasonDivision.get_teams_dict(season_division_db.id)

    return teams


@season_division.route('/<int:season_division_id>/rookies', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(SeasonDivisionRookies())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_rookies_in_season_division(season_division_id):
    """Get a list of rookies in a SeasonDivision"""
    # check season_division exists
    season_division_db = ensure_exists(SeasonDivision, id=season_division_id)

    return season_division_db.get_rookies_dict()


@season_division.route('/<int:season_division_id>/free_agents', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(SeasonDivisionFreeAgents())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_free_agents_in_season_division(season_division_id):
    """Get a list of free agents in a SeasonDivision"""
    season_division_db = ensure_exists(SeasonDivision, id=season_division_id)

    free_agents = FreeAgent.get_season_free_agents(season_division_db.id)

    if free_agents is None:
        raise ResourceNotFound('No free agents in the specified season')

    return free_agents


@season_division.route('/<int:season_division_id>/matches', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(UnplayedFilterSchema())
@response(SeasonDivisionMatches())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_matches_in_season_division(search_filter, season_division_id):
    """Get a list of matches in a Season Division"""
    season_division_db = ensure_exists(SeasonDivision, id=season_division_id)
    unplayed = search_filter.get('unplayed', False)

    matches = season_division_db.get_matches_dict(unplayed)

    return matches


@season_division.route('/<int:season_division_id>/finals', methods=['GET'])
@cache.cached(unless=force_refresh)
def get_finals_in_season_division(season_division_id):  # noqa TODO
    pass
