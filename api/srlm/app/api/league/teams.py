"""Endpoints relating to Teams"""
from datetime import datetime, timezone

from apifairy import arguments, response, authenticate, other_responses, body

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from flask import url_for, Blueprint, request
import sqlalchemy as sa

from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.errors import ResourceNotFound, BadRequest
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import TeamCollection, TeamSchema, LinkSuccessSchema, EditTeamSchema, \
    TeamPlayers, TeamSeasonPlayers, TeamSeasons, CurrentFilterSchema, TeamsListSchema, \
    TeamStatsFilter, TeamStatsMatchesSchema, TeamManageSchema, TeamFilters, SendInviteSchema, BasicSuccessSchema, \
    SendApplicationSchema
from api.srlm.app.models import Team, SeasonDivision, PlayerTeam, UserPermissions, Permission, TeamAward, Player, User, \
    TeamInvites, Season, SeasonRegistration
from api.srlm.app.api.auth.utils import app_auth, user_auth, get_bearer_token

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


teams = Blueprint('teams', __name__)
bp.register_blueprint(teams, url_prefix='/teams')


@teams.route('', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(TeamFilters())
@response(TeamCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_teams(filters):
    """Get the collection of all teams"""
    page = filters['page']
    per_page = filters['per_page']
    owner = filters['owner']
    order = filters['order']
    order_by = filters['order_by']

    if order_by == 'seasons_played':
        query = db.session.query(Team, sa.func.count(SeasonDivision.id).label('count')) \
            .outerjoin(Team.season_division_assoc) \
            .group_by(Team) \
            .order_by(getattr(sa, order)('count'))
    elif order_by == 'active_players':
        query = db.session.query(Team, sa.func.count(PlayerTeam.id).label('count')) \
            .outerjoin(PlayerTeam,
                       (Team.id == PlayerTeam.team_id) & (PlayerTeam.end_date.is_(None))) \
            .group_by(Team) \
            .order_by(getattr(sa, order)('count'))
    elif order_by == 'awards':
        query = db.session.query(Team, sa.func.count(TeamAward.id).label('count')) \
            .outerjoin(Team.awards_association) \
            .group_by(Team) \
            .order_by(getattr(sa, order)('count'))
    else:
        query = sa.select(Team)

        if owner:
            team_ids_q = db.session.query(UserPermissions) \
                .filter(UserPermissions.user_id == owner) \
                .join(UserPermissions.permission) \
                .filter(Permission.key == 'team_owner').first()
            team_ids = []
            if team_ids_q:
                team_ids = team_ids_q.additional_modifiers.split(',')
            query = db.session.query(Team).filter(Team.id.in_(team_ids))

        query = query.order_by(getattr(sa, order)(getattr(Team, order_by)))

    return Team.to_collection_dict(query, page, per_page, 'api.teams.get_teams')


@teams.route('/list', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@response(TeamsListSchema())  # yeah i didn't feel like making a new schema, sue me
@authenticate(app_auth)
@other_responses(unauthorized)
def get_teams_list():
    """Get a simple list of all teams"""
    query = db.session.query(Team).order_by(Team.name)
    teams_list = [
        {
            'id': team.id,
            'name': team.name,
            'acronym': team.acronym
        }
        for team in query
    ]
    return {'teams': teams_list}


@teams.route('/<int:team_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(TeamSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team(team_id):
    """Get details of a team"""
    team = ensure_exists(Team, id=team_id)
    return team.to_dict()


@teams.route('', methods=['POST'])
@body(TeamSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_team(data):
    """Create a new team"""

    required_fields = unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'color', 'logo', 'founded_date']

    force_fields(data, required_fields)
    force_unique(Team, data, unique_fields)

    cleaned_data = clean_data(data, valid_fields)

    if cleaned_data['color'] == "":
        cleaned_data['color'] = None

    team = Team()
    team.from_dict(cleaned_data)

    db.session.add(team)
    db.session.commit()

    user = User.check_token(get_bearer_token(request.headers)['user'])
    if user:
        user.grant_permission('team_owner', mods=[str(team.id)])
        user.grant_permission('team_manager', mods=[str(team.id)])
        user.player.join_team(team)

    return responses.create_success(f'Team {team.name} created', 'api.teams.get_team', team_id=team.id)


@teams.route('/<int:team_id>', methods=['PUT'])
@body(EditTeamSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_team(data, team_id):
    """Update an existing team"""

    team = ensure_exists(Team, id=team_id)

    unique_fields = ['name', 'acronym']
    valid_fields = ['name', 'acronym', 'color', 'logo', 'founded_date']

    force_unique(Team, data, unique_fields, self_id=team.id)

    cleaned_data = clean_data(data, valid_fields)
    team.from_dict(cleaned_data)
    db.session.commit()

    return responses.request_success(f'Team {team.name} updated', 'api.teams.get_team', team_id=team.id)


@teams.route('/<int:team_id>/players', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(CurrentFilterSchema())
@response(TeamPlayers())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team_players(search_filter, team_id):
    """Get a list of the teams players"""
    team = ensure_exists(Team, id=team_id)
    current = search_filter.get('current', False)

    team_players = PlayerTeam.get_players_dict(team.id, current)

    return team_players


@teams.route('/<int:team_id>/players/season/<int:season_division_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(TeamSeasonPlayers())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team_players_in_season(team_id, season_division_id):
    """Get a list of players on the team in a given season"""
    # get team
    team = ensure_exists(Team, id=team_id)
    # get season_division
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    # query the teams playerlist for players active during the season
    # uses (player_start_date is earlier than season_end) and (player_end_date is later than season_start)
    season_start = datetime.combine(season_division.season.start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    season_end = datetime.combine(season_division.season.finals_end, datetime.min.time()).replace(tzinfo=timezone.utc)

    players = []
    for player_assoc in team.player_association:
        player_start_date = player_assoc.start_date.replace(tzinfo=timezone.utc)
        player_end_date = player_assoc.end_date.replace(tzinfo=timezone.utc) if player_assoc.end_date is not None else None
        if player_start_date < season_end and (player_end_date is None or player_end_date > season_start):
            player = {
                'player_name': player_assoc.player.player_name,
                'start_date': player_assoc.start_date,
                'end_date': player_assoc.end_date,
                '_links': {
                    'self': url_for('api.players.get_player', player_id=player_assoc.player.id)
                }
            }
            players.append(player)

    response_json = {
        'season_division': f'{season_division.get_readable_name()} ({season_division.season.league.acronym})',
        'team': team.name,
        'acronym': team.acronym,
        'color': team.color,
        'players': players,
        '_links': {
            'self': url_for('api.teams.get_team_players_in_season', team_id=team.id, season_division_id=season_division.id),
            'team': url_for('api.teams.get_team', team_id=team.id)
        }
    }
    return response_json


@teams.route('/<int:team_id>/seasons', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(TeamSeasons())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team_seasons(team_id):
    """Get a list of seasons the team has played in"""
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    if team.season_divisions.count() == 0:
        raise ResourceNotFound('Team has not played in any seasons')

    # return list of seasons
    seasons = SeasonDivision.get_seasons_dict(team.id)
    return seasons


@teams.route('/<int:team_id>/seasons', methods=['POST'])
@body(TeamSeasons())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def register_team_season(data, team_id):
    """Register a team to a season"""
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    # validate input
    force_fields(data, ['season_division_id'])

    # ensure season exists
    season_division = ensure_exists(SeasonDivision, id=data['season_division_id'])

    team_registered = team.season_divisions.filter_by(id=season_division.id).first()

    if team_registered:
        raise BadRequest(f'Team {team.name} already registered to {season_division.get_readable_name()}')

    # register team
    team.season_divisions.append(season_division)
    db.session.commit()

    return responses.request_success(f'Team {team.name} registered to {season_division.get_readable_name()}',
                                     'api.season_division.get_season_division', season_division_id=season_division.id)


@teams.route('/<int:team_id>/seasons/<int:season_division_id>', methods=['DELETE'])
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def deregister_team_season(team_id, season_division_id):
    """De-register a team from a season"""
    # ensure team exists
    team = ensure_exists(Team, id=team_id)

    # ensure season exists
    season_division = ensure_exists(SeasonDivision, id=season_division_id)

    team_registered = team.season_divisions.filter_by(id=season_division.id).first()

    if not team_registered:
        raise BadRequest(f'Team {team.name} not registered to {season_division.get_readable_name()}')

    team.season_divisions.remove(season_division)
    db.session.commit()

    return responses.request_success(f'Team {team.name} de-registered from {season_division.get_readable_name()}',
                                     'api.season_division.get_season_division', season_division_id=season_division.id)


@teams.route('/<int:team_id>/stats', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(TeamStatsFilter())
@response(TeamStatsMatchesSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team_stats(filters, team_id):
    """Get a teams stats
    Can filter by season_division, or by current player roster
    """
    team = ensure_exists(Team, id=team_id)

    season_division_id = filters.get('season_division', 0)
    season_division = ensure_exists(SeasonDivision, return_none=True, id=season_division_id)

    current = filters.get('current', False)

    response_json = team.get_stats(season_division=season_division, current=current)

    response_json['upcoming_matches'] = team.get_upcoming_matches()
    response_json['completed_matches'] = team.get_completed_matches()

    return response_json


@teams.route('/<int:team_id>/invite', methods=['POST'])
@body(SendInviteSchema())
@response(BasicSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def send_invite(data, team_id):
    """Invite a player to join a team
    Requires user token"""
    team = ensure_exists(Team, id=team_id)
    invited_player = ensure_exists(Player, id=data['player_id'])
    inviting_user = User.check_token(get_bearer_token(request.headers)['user'])
    team.invite_player(invited_player, inviting_user.player)
    return responses.request_success(f'Invite to {team.name} sent to {invited_player.player_name}')


@teams.route('/invite/<int:invite_id>', methods=['DELETE'])
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def withdraw_invite(invite_id):
    """Withdraw a players invite to the team"""
    invite = ensure_exists(TeamInvites, id=invite_id)
    invite.withdraw()
    return responses.request_success('Invite withdrawn')


@teams.route('/<int:team_id>/apply', methods=['POST'])
@body(SendApplicationSchema())
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | bad_request | not_found)
def apply_to_season(data, team_id):
    """Apply for a team to join a season"""
    team = ensure_exists(Team, id=team_id)
    season = ensure_exists(Season, id=data['season_id'])
    if not season.can_register:
        raise BadRequest('Season not open for registration')
    team.apply_to_season(season)
    return responses.request_success(f'Application to join season {season.name} submitted')


@teams.route('/apply/<int:application_id>', methods=['DELETE'])
@response(BasicSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def cancel_application(application_id):
    """Cancel an application to join a season"""
    application = ensure_exists(SeasonRegistration, id=application_id)
    application.withdraw()
    return responses.request_success('Application withdrawn')


@teams.route('/<int:team_id>/manage', methods=['GET'])
@response(TeamManageSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_team_manager_details(team_id):
    """Get the management details of a team"""
    team = ensure_exists(Team, id=team_id)
    return team.get_manager_details()


@teams.route('/<int:team_id>/awards', methods=['GET'])
@cache.cached(unless=force_refresh)
def get_team_awards(team_id):  # noqa TODO
    pass


@teams.route('/<int:team_id>/awards', methods=['POST'])
@cache.cached(unless=force_refresh)
def give_team_award(team_id):  # noqa TODO
    pass
