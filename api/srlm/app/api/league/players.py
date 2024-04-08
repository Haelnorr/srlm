"""Endpoints relating to Players"""
from datetime import datetime, timezone

from apifairy import arguments, response, authenticate, other_responses, body
from flask import request, Blueprint
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import req_app_token, user_auth
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.fairy.errors import unauthorized, not_found, bad_request
from api.srlm.app.fairy.schemas import PaginationArgs, PlayerSchema, PlayerCollection, LinkSuccessSchema, \
    EditPlayerSchema, PlayerTeams, PlayerSeasons
from api.srlm.app.models import Player, SeasonDivision, Team, PlayerTeam, FreeAgent
from api.srlm.logger import get_logger
log = get_logger(__name__)


players = Blueprint('players', __name__)
bp.register_blueprint(players, url_prefix='/players')


@players.route('/<int:player_id>', methods=['GET'])
@req_app_token
@response(PlayerSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found)
def get_player(player_id):
    """Get details of a player"""
    player = ensure_exists(Player, id=player_id)
    return player.to_dict()


@players.route('/', methods=['GET'])
@req_app_token
@arguments(PaginationArgs())
@response(PlayerCollection())
@authenticate(user_auth)
@other_responses(unauthorized)
def get_players(pagination):
    """Get the collection of all players"""
    page = pagination['page']
    per_page = pagination['per_page']
    return Player.to_collection_dict(sa.select(Player), page, per_page, 'api.players.get_players')


@players.route('/', methods=['POST'])
@req_app_token
@body(PlayerSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(user_auth)
@other_responses(unauthorized | bad_request)
def new_player():
    """Create a new player"""
    data = request.get_json()

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
@req_app_token
@body(EditPlayerSchema())
@response(LinkSuccessSchema())
@authenticate(user_auth)
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
@req_app_token
@response(PlayerTeams())
@authenticate(user_auth)
@other_responses(unauthorized | not_found)
def get_player_teams(player_id):
    """Get a list of teams the player has played on"""
    player = ensure_exists(Player, id=player_id)
    current = request.args.get('current', False, bool)  # TODO

    player_teams = PlayerTeam.get_teams_dict(player.id, current)

    if player_teams is None:
        raise ResourceNotFound('Player does not have a current team')

    return


@players.route('/<int:player_id>/stats', methods=['GET'])
@req_app_token
def get_player_stats(player_id):  # TODO
    pass


@players.route('/<int:player_id>/teams', methods=['POST'])
@req_app_token
@body(PlayerTeams())
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def register_player_team(player_id):
    """Register a player to a team"""
    # get the player
    player = ensure_exists(Player, id=player_id)
    current_team = player.current_team()

    # check if player has current team
    if player.current_team():
        raise BadRequest(f'Player already registered to {current_team.team.name} - cannot be registered to multiple teams at once.')

    # validate the data
    data = request.get_json()
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
@req_app_token
@response(LinkSuccessSchema())
@authenticate(user_auth)
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
@req_app_token
@response(PlayerSeasons())
@authenticate(user_auth)
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
@req_app_token
@body(PlayerSeasons())
@response(LinkSuccessSchema())
@authenticate(user_auth)
@other_responses(unauthorized | not_found | bad_request)
def register_player_free_agent(player_id):
    """Register a player to a season as a free agent"""
    player = ensure_exists(Player, id=player_id)

    data = request.get_json()
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
@req_app_token
def get_player_awards(player_id):  # TODO
    pass


@players.route('/<int:player_id>/awards', methods=['POST'])
@req_app_token
def give_player_award(player_id):  # TODO
    pass
