from datetime import datetime, timezone
from flask import request
import sqlalchemy as sa
from api.srlm.app import db
from api.srlm.app.api.league import league_bp as league
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import req_app_token
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound
from api.srlm.app.api.utils.functions import ensure_exists, force_fields, force_unique, clean_data
from api.srlm.app.models import Player, SeasonDivision, Team, PlayerTeam, FreeAgent
from api.srlm.logger import get_logger
log = get_logger(__name__)


@league.route('/players/<int:player_id>', methods=['GET'])
@req_app_token
def get_player(player_id):
    player = ensure_exists(Player, id=player_id)
    return player.to_dict()


@league.route('/players', methods=['GET'])
@req_app_token
def get_players():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Player.to_collection_dict(sa.select(Player), page, per_page, 'api.league.get_players')


@league.route('/players', methods=['POST'])
@req_app_token
def new_player():
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

    return responses.create_success(f"Player {player.player_name} created", 'api.league.get_player', player_id=player.id)


@league.route('/players/<int:player_id>', methods=['PUT'])
@req_app_token
def update_player(player_id):
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

    return responses.request_success(f"Player {player.player_name} updated", 'api.league.get_player', player_id=player.id)


@league.route('/players/<int:player_id>/teams', methods=['GET'])
@req_app_token
def get_player_teams(player_id):
    player = ensure_exists(Player, id=player_id)
    current = request.args.get('current', False, bool)

    player_teams = PlayerTeam.get_teams_dict(player_id, current)

    if player_teams is None:
        raise ResourceNotFound('Player does not have a current team')

    return


@league.route('/players/<int:player_id>/stats', methods=['GET'])
@req_app_token
def get_player_stats(player_id):
    pass


@league.route('/players/<int:player_id>/teams', methods=['POST'])
@req_app_token
def register_player_team(player_id):
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

    return responses.request_success(f'Player {player.player_name} registered to team {team.name}', 'api.league.get_team', team_id=team.id)


@league.route('/players/<int:player_id>/teams', methods=['DELETE'])
@req_app_token
def deregister_player_team(player_id):
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
                                     f'{current_team.team.name}', 'api.league.get_player', player_id=player.id)


@league.route('/players/<int:player_id>/free_agent', methods=['GET'])
@req_app_token
def get_player_free_agent(player_id):
    player = ensure_exists(Player, id=player_id)

    player_seasons = FreeAgent.get_free_agent_seasons(player.id)

    if player_seasons is None:
        raise ResourceNotFound('Player has not been a free agent in any season')
    else:
        return player_seasons


@league.route('/players/<int:player_id>/free_agent', methods=['POST'])
@req_app_token
def register_player_free_agent(player_id):
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
                                     'api.league.get_season_division', season_division_id=season_division.id)


@league.route('/players/<int:player_id>/awards', methods=['GET'])
@req_app_token
def get_player_awards(player_id):
    pass


@league.route('/players/<int:player_id>/awards', methods=['POST'])
@req_app_token
def give_player_award(player_id):
    pass
