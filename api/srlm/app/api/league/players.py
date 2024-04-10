"""Endpoints relating to Players"""
from datetime import datetime, timezone

from apifairy import arguments, response, authenticate, other_responses, body
from flask import request, Blueprint, url_for
import sqlalchemy as sa
from sqlalchemy import func

from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import app_auth
from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, PlayerSchema, PlayerCollection, LinkSuccessSchema, \
    EditPlayerSchema, PlayerTeams, PlayerSeasons, CurrentFilterSchema, PlayerStatsSchema, StatsFilterSchema
from api.srlm.app.models import Player, SeasonDivision, Team, PlayerTeam, FreeAgent, PlayerMatchData, Match, Lobby, \
    MatchData, Season, Division
from api.srlm.logger import get_logger
log = get_logger(__name__)


players = Blueprint('players', __name__)
bp.register_blueprint(players, url_prefix='/players')


@players.route('/<int:player_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(PlayerSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_player(player_id):
    """Get details of a player"""
    player = ensure_exists(Player, id=player_id)
    return player.to_dict()


@players.route('', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(PaginationArgs())
@response(PlayerCollection())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_players(pagination):
    """Get the collection of all players"""
    page = pagination['page']
    per_page = pagination['per_page']
    return Player.to_collection_dict(sa.select(Player), page, per_page, 'api.players.get_players')


@players.route('', methods=['POST'])
@body(PlayerSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def new_player(data):
    """Create a new player"""

    required_fields = ['player_name']
    unique_fields = ['slap_id', 'player_name']
    valid_fields = ['slap_id', 'player_name', 'rookie', 'first_season_id']

    force_fields(data, required_fields)
    force_unique(Player, data, unique_fields)
    cleaned_data = clean_data(data, valid_fields)

    if 'first_season_id' in cleaned_data:
        ensure_exists(SeasonDivision, id=cleaned_data['first_season_id'])

    player = Player()
    player.from_dict(cleaned_data)

    db.session.add(player)
    db.session.commit()

    return responses.create_success(f"Player {player.player_name} created", 'api.players.get_player', player_id=player.id)


@players.route('/<int:player_id>', methods=['PUT'])
@body(EditPlayerSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def update_player(player_id):
    """Update an existing player"""
    data = request.get_json()

    player = ensure_exists(Player, id=player_id)

    unique_fields = ['slap_id', 'player_name']
    valid_fields = ['slap_id', 'player_name', 'rookie', 'first_season_id']

    force_unique(Player, data, unique_fields, self_id=player.id)
    cleaned_data = clean_data(data, valid_fields)

    if 'first_season_id' in cleaned_data:
        ensure_exists(SeasonDivision, id=cleaned_data['first_season_id'])

    player.from_dict(cleaned_data)
    db.session.commit()

    return responses.request_success(f"Player {player.player_name} updated", 'api.players.get_player', player_id=player.id)


@players.route('/<int:player_id>/teams', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(CurrentFilterSchema())
@response(PlayerTeams())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_player_teams(search_filter, player_id):
    """Get a list of teams the player has played on"""
    player = ensure_exists(Player, id=player_id)
    current = search_filter.get('current', False, bool)

    player_teams = PlayerTeam.get_teams_dict(player.id, current)

    if player_teams is None:
        raise ResourceNotFound('Player does not have a current team')

    return


@players.route('/<int:player_id>/stats', methods=['GET'])
@cache.cached(unless=force_refresh, query_string=True)
@arguments(StatsFilterSchema())
@response(PlayerStatsSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def get_player_stats(search_filters, player_id):
    """Get a players stats"""
    # get player
    player = ensure_exists(Player, id=player_id)

    season_id = search_filters.get('season', None)
    division_id = search_filters.get('division', None)

    season = None
    division = None
    team = None

    sd_filters = {}
    if season_id:
        season = ensure_exists(Season, id=season_id)
        sd_filters['season_id'] = season_id
    if division_id:
        division = ensure_exists(Division, id=division_id)
        sd_filters['division_id'] = division_id

    filters = {
        'player_id': player.id
    }
    if 'team_id' in search_filters:
        team = ensure_exists(Team, id=search_filters['team'])
        filters['team_id'] = search_filters['team']

    season_divisions = db.session.query(SeasonDivision).filter_by(**sd_filters)
    sd_ids = [sd.id for sd in season_divisions]

    sd_match_query = db.session.query(Match).filter(Match.season_division_id.in_(sd_ids))
    sd_matches = [sd.id for sd in sd_match_query]

    lobby_query = db.session.query(Lobby).filter(Lobby.match_id.in_(sd_matches))
    lobbies = [lb.id for lb in lobby_query]

    match_data_query = db.session.query(MatchData).filter(
        MatchData.accepted == True,
        MatchData.lobby_id.in_(lobbies)
    )
    filtered_matches = [match.id for match in match_data_query]

    stats = db.session.query(PlayerMatchData).with_entities(
        func.sum(PlayerMatchData.goals).label("goals"),
        func.max(PlayerMatchData.shots).label("shots"),
        func.max(PlayerMatchData.assists).label("assists"),
        func.max(PlayerMatchData.saves).label("saves"),
        func.max(PlayerMatchData.primary_assists).label("primary_assists"),
        func.max(PlayerMatchData.secondary_assists).label("secondary_assists"),
        func.max(PlayerMatchData.passes).label("passes"),
        func.max(PlayerMatchData.blocks).label("blocks"),
        func.max(PlayerMatchData.takeaways).label("takeaways"),
        func.max(PlayerMatchData.turnovers).label("turnovers"),
        func.max(PlayerMatchData.game_winning_goals).label("game_winning_goals"),
        func.max(PlayerMatchData.overtime_goals).label("overtime_goals"),
        func.max(PlayerMatchData.post_hits).label("post_hits"),
        func.max(PlayerMatchData.faceoffs_won).label("faceoffs_won"),
        func.max(PlayerMatchData.faceoffs_lost).label("faceoffs_lost"),
        func.max(PlayerMatchData.score).label("score"),
        func.max(PlayerMatchData.possession_time_sec).label("possession_time_sec")
    ).filter_by(
        **filters
    ).filter(
        PlayerMatchData.match_id.in_(filtered_matches)
    ).first()

    response_json = {
        'player': player.to_dict(),
        'stats': {
            'goals': stats.goals,
            'shots': stats.shots,
            'assists': stats.assists,
            'saves': stats.saves,
            'primary_assists': stats.primary_assists,
            'secondary_assists': stats.secondary_assists,
            'passes': stats.passes,
            'blocks': stats.blocks,
            'takeaways': stats.takeaways,
            'turnovers': stats.turnovers,
            'game_winning_goals': stats.game_winning_goals,
            'overtime_goals': stats.overtime_goals,
            'post_hits': stats.post_hits,
            'faceoffs_won': stats.faceoffs_won,
            'faceoffs_lost': stats.faceoffs_lost,
            'score': stats.score,
            'possession_time_sec': stats.goals
        },
        'season': season.name if season else None,
        'division': division.name if division else None,
        'team': team.name if team else None,
        '_links': {
            'self': url_for('api.players.get_player_stats', player_id=player_id),
            'player': url_for('api.players.get_player', player_id=player_id),
            'season': url_for('api.seasons.get_season', season_id=season_id) if season else None,
            'division': url_for('api.divisions.get_division', division_id=division_id) if division else None,
            'team': url_for('api.teams.get_team', team_id=team.id) if team else None
        }
    }
    return response_json


@players.route('/<int:player_id>/teams', methods=['POST'])
@body(PlayerTeams())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def register_player_team(data, player_id):
    """Register a player to a team"""
    # get the player
    player = ensure_exists(Player, id=player_id)
    current_team = player.current_team()

    # check if player has current team
    if player.current_team():
        raise BadRequest(f'Player already registered to {current_team.team.name} - cannot be registered to multiple teams at once.')

    # validate the data
    force_fields(data, ['team'])

    # get the team
    team = ensure_exists(Team, join_method='or', id=data['team'], acronym=data['team'])

    # register the player to the team
    player_team = PlayerTeam()
    player_team.player = player
    player_team.team = team
    player_team.start_date = datetime.now(timezone.utc)

    db.session.add(player_team)
    db.session.commit()

    return responses.request_success(f'Player {player.player_name} registered to team {team.name}', 'api.players.get_team', team_id=team.id)


@players.route('/<int:player_id>/teams', methods=['DELETE'])
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def deregister_player_team(player_id):
    """De-register a player from a team"""
    # get the player
    player = ensure_exists(Player, id=player_id)

    # check if player has current team
    current_team = player.current_team()

    if not current_team:
        raise BadRequest('Player is not registered to a team')

    # de-register the player from the team (add end date)
    current_team.end_date = datetime.now(timezone.utc)

    db.session.commit()

    return responses.request_success(f'Player {player.player_name} de-registered from team '
                                     f'{current_team.team.name}', 'api.players.get_player', player_id=player.id)


@players.route('/<int:player_id>/free_agent', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(PlayerSeasons())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_player_free_agent(player_id):
    """Get a list of seasons a player has been a free agent in"""
    player = ensure_exists(Player, id=player_id)

    player_seasons = FreeAgent.get_free_agent_seasons(player.id)

    if player_seasons is None:
        raise ResourceNotFound('Player has not been a free agent in any season')
    else:
        return player_seasons


@players.route('/<int:player_id>/free_agent', methods=['POST'])
@body(PlayerSeasons())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found | bad_request)
def register_player_free_agent(data, player_id):
    """Register a player to a season as a free agent"""
    player = ensure_exists(Player, id=player_id)

    force_fields(data, ['season_division_id'])

    season_division = ensure_exists(SeasonDivision, id=data['season_division_id'])

    # check if player isnt already a free agent in that season
    already_registered = ensure_exists(FreeAgent, return_none=True, player_id=player.id, season_division_id=season_division.id)
    if already_registered:
        raise BadRequest('Player already registered as a free agent to that season')

    start_date = None
    end_date = None
    if 'start_date' in data:
        start_date = data['start_date']
    if 'end_date' in data:
        end_date = data['end_date']

    free_agent = FreeAgent()
    free_agent.player = player
    free_agent.season_division = season_division
    free_agent.start_date = start_date
    free_agent.end_date = end_date

    db.session.add(free_agent)
    db.session.commit()

    return responses.request_success(f"Player {player.player_name} registered as a Free Agent to "
                                     f"{season_division.get_readable_name()} ({season_division.season.league.acronym})",
                                     'api.season_division.get_season_division', season_division_id=season_division.id)


@players.route('/<int:player_id>/awards', methods=['GET'])
@cache.cached(unless=force_refresh)
def get_player_awards(player_id):  # TODO
    pass


@players.route('/<int:player_id>/awards', methods=['POST'])
def give_player_award(player_id):  # TODO
    pass
