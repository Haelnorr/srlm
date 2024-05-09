"""Provides endpoints for creating matches and retrieving match data"""
from datetime import datetime, timezone

from apifairy import body, response, authenticate, other_responses
from flask import request, Blueprint
import sqlalchemy as sa

from api.srlm.app.api.game.utils import period_from_log
from api.srlm.app.api.utils.cache import force_refresh
from api.srlm.app.spapi.lobby import get_lobby_matches
from api.srlm.app.task_manager.tasks import cancel_task
from api.srlm.app import db, cache
from api.srlm.app.api import bp
from api.srlm.app.api.utils import responses
from api.srlm.app.api.auth.utils import get_bearer_token, app_auth, dual_auth
from api.srlm.app.api.utils.errors import BadRequest
from api.srlm.app.api.utils.functions import force_fields, ensure_exists, clean_data, force_unique
from api.srlm.app.fairy.errors import unauthorized, bad_request, not_found
from api.srlm.app.fairy.schemas import LinkSuccessSchema, NewMatchSchema, ViewMatchSchema, MatchReviewSchema, \
    MatchtypeSchema, MatchStatsSchema, NewMatchFlag, LogsUploadSchema, GamemodeSchema, MatchtypeList
from api.srlm.app.models import SeasonDivision, Team, Match, MatchSchedule, MatchReview, MatchData, Matchtype, User, \
    PlayerMatchData, GameMode, Lobby
from api.srlm.app.spapi.lobby_manager import generate_lobby, validate_stats

match = Blueprint('match', __name__)
bp.register_blueprint(match, url_prefix='/match')


@match.route('', methods=['POST'])
@body(NewMatchSchema())
@response(LinkSuccessSchema(), 201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def create_match(data):
    """Create a new match"""

    required_fields = ['season_division_id', 'home_team_id', 'away_team_id']
    force_fields(data, required_fields)

    season_division = ensure_exists(SeasonDivision, id=data['season_division_id'])
    if data['home_team_id'] == data['away_team_id']:
        raise BadRequest('Team cannot play itself')
    home_team = ensure_exists(Team, id=data['home_team_id'])
    away_team = ensure_exists(Team, id=data['away_team_id'])
    # ensure they are registered to the season
    if season_division not in home_team.season_divisions:
        raise BadRequest(f'Team {home_team.name} not registered to {season_division.get_readable_name()}')
    if season_division not in away_team.season_divisions:
        raise BadRequest(f'Team {away_team.name} not registered to {season_division.get_readable_name()}')

    # create match
    valid_fields = ['season_division_id', 'home_team_id', 'away_team_id', 'round', 'match_week']
    cleaned_data = clean_data(data, valid_fields)
    match_db = Match()
    match_db.from_dict(cleaned_data)

    # create match_schedule entry
    match_db.schedule = MatchSchedule()

    db.session.add(match_db)
    db.session.commit()

    return responses.create_success(f'Match between {match_db.home_team.name} and {match_db.away_team.name} created', 'api.match.get_match', match_id=match_db.id)


@match.route('/<int:match_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(ViewMatchSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_match(match_id):
    """Get details of a match"""
    match_db = ensure_exists(Match, id=match_id)
    response_json = match_db.to_dict()
    return response_json


@match.route('/<int:match_id>/review', methods=['GET'])
@response(MatchReviewSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_match_review(match_id):
    """Get the flags and match data of a match"""
    match_db = ensure_exists(Match, id=match_id)

    flags = db.session.query(MatchReview).filter_by(match_id=match_id)

    flags_data = []
    for flag in flags:
        flags_data.append(flag.to_dict())

    lobby_ids = []
    for lobby in match_db.lobbies:
        lobby_ids.append(lobby.id)

    period_query = db.session.query(MatchData).filter(MatchData.lobby_id.in_(lobby_ids)).order_by(sa.asc(MatchData.created))
    periods = []
    for period in period_query:
        period_data = period.to_dict()
        period_data['player_data'] = []
        for player in period.player_data_assoc:
            period_data['player_data'].append(player.to_dict())
        periods.append(period_data)

    response_json = {
        'match_id': match_db.id,
        'match_details': match_db.to_simple_dict(),
        'periods': periods,
        'flags': flags_data,
    }

    return response_json


@match.route('/<int:match_id>/review', methods=['PUT'])
@body(MatchReviewSchema())
@response(LinkSuccessSchema())
@authenticate(dual_auth)
@other_responses(unauthorized | bad_request | not_found)
def update_match_review(match_id):
    """Updates a match review. Requires user token"""

    match_db = ensure_exists(Match, id=match_id)
    if match_db.results:
        raise BadRequest('Match results already confirmed. Unable to submit review')

    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)

    data = request.get_json()

    if 'flags' not in data or type(data['flags']) is not list:
        raise BadRequest('Flags field missing or invalid format. Must be a list/array')

    if 'periods' in data and type(data['periods']) is not list:
        raise BadRequest('Periods field in invalid format. Must be a list/array')

    for flag_data in data['flags']:
        if 'id' not in flag_data:
            raise BadRequest('One or more flags are missing ID tags')
        flag = ensure_exists(MatchReview, id=flag_data['id'])
        valid_fields = ['comments', 'resolved']
        flag.from_dict(clean_data(flag_data, valid_fields))
        if flag.resolved:
            flag.resolved_by = user.id
            flag.resolved_on = datetime.now(timezone.utc)

    if 'periods' in data:
        for period_data in data['periods']:
            if 'id' not in period_data:
                raise BadRequest('One or more period data entries are missing ID tags')
            period = ensure_exists(MatchData, id=period_data['id'])
            valid_fields = ['home_score', 'away_score', 'winner', 'current_period', 'periods_enabled',
                            'custom_mercy_rule', 'end_reason', 'accepted']
            period.from_dict(clean_data(period_data, valid_fields))
            if 'player_data' in period_data:
                for player_data in period_data['player_data']:
                    if 'id' not in player_data:
                        raise BadRequest('One or more player data entries are missing ID tags')
                    player_match_data = ensure_exists(PlayerMatchData, id=player_data['id'])
                    player_match_data.from_dict(player_data)

    db.session.commit()

    match_db = db.session.get(Match, match_db.id)
    lobby_ids = [lb.id for lb in match_db.lobbies]
    accepted_periods = db.session.query(MatchData).filter(MatchData.lobby_id.in_(lobby_ids)).count()
    flags = db.session.query(MatchReview).filter_by(match_id=match_db.id, resolved=False).count()

    if accepted_periods == (1 + (match_db.season_division.season.match_type.periods * 2)) and flags == 0:
        validate_stats.delay(match_db.id)

    return responses.request_success(f'Updated review of match {match_db.id}', 'api.match.get_match', match_id=match_id)


@match.route('/<int:match_id>/stats', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(MatchStatsSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_match_stats(match_id):
    """Get the accepted match stats"""
    match_db = ensure_exists(Match, id=match_id)

    lobby_ids = []
    for lobby in match_db.lobbies:
        lobby_ids.append(lobby.id)

    period_query = db.session.query(MatchData).filter(
        sa.and_(
            MatchData.accepted.is_(True),
            MatchData.lobby_id.in_(lobby_ids)
        )
    ).order_by(sa.asc(MatchData.current_period))

    period_ids = []
    for period in period_query:
        period_ids.append(period.id)

    teams = {
        match_db.home_team_id: 'home',
        match_db.away_team_id: 'away'
    }
    periods = {}
    totals = {
        'home': [],
        'away': []
    }
    for period in period_query:
        period_data = period.to_dict()
        period_data['player_data'] = {
            'home': [],
            'away': []
        }
        for player in period.player_data_assoc:
            period_data['player_data'][teams[player.team_id]].append(player.to_dict())
        periods[f'period{period.current_period}'] = period_data

        final_player_data = period.player_data_assoc.filter_by(stat_total=True)

        for player in final_player_data:
            final_player_data = player.to_dict()
            periods_played = db.session.query(PlayerMatchData).filter(
                sa.and_(
                    PlayerMatchData.player_id == player.player_id,
                    PlayerMatchData.match.has(accepted=True),
                    PlayerMatchData.match_id.in_(period_ids)
                )
            ).count()
            final_player_data['periods_played'] = periods_played
            totals[teams[player.team_id]].append(final_player_data)

    response_json = {
        'match_id': match_db.id,
        'match_details': match_db.to_simple_dict(),
        'periods': periods,
        'stat_totals': totals
    }
    return response_json


@match.route('/<int:match_id>/review', methods=['POST'])
@body(NewMatchFlag())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(dual_auth)
@other_responses(unauthorized | not_found | bad_request)
def report_issue(data, match_id):
    """Reports an issue with a match. Requires user token
    Valid values for `type` are: "Technical", "Forfeit", "Report"
    """
    match_db = ensure_exists(Match, id=match_id)
    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)

    required_fields = valid_fields = ['type', 'reason', 'comments']
    force_fields(data, required_fields)

    flag = MatchReview()
    flag.from_dict(clean_data(data, valid_fields))
    flag.raised_by = user.username

    db.session.add(flag)
    db.session.commit()

    # Check if the issue reported was technical and if a new lobby was requested
    if data['type'] == 'Technical' and 'new_lobby' in data:

        new_lobby = {
            'match': match_db,
        }

        # check for an existing active lobby
        existing_lobby = match_db.current_lobby()
        if existing_lobby:

            # active lobby found, tell the monitor to destroy it
            cancel_task(existing_lobby.task_id)

            # check if a stats carryover was requested
            if data['new_lobby']['stats_carryover']:

                # recover the stats from the old lobby
                recovered_stats_req = get_lobby_matches(existing_lobby.lobby_id)

                # make sure the request was successful
                if recovered_stats_req.status_code == 200:

                    # get the recovered stats
                    recovered_stats = recovered_stats_req.json()

                    # order the results by time created to ensure we can grab the most recent period
                    ordered_periods = sorted(recovered_stats, key=lambda t: t['created'])
                    # grab the 'players' field from the most recent period
                    # this is what the slap api expects as the initial_stats input
                    new_lobby['initial_stats'] = ordered_periods[-1]['game_stats']['players']

        if 'current_period' in data['new_lobby']:
            new_lobby['current_period'] = int(data['new_lobby']['current_period'])

        if 'initial_score' in data['new_lobby']:
            new_lobby['initial_score']['home'] = int(data['new_lobby']['initial_score']['home'])
            new_lobby['initial_score']['away'] = int(data['new_lobby']['initial_score']['away'])

        generate_lobby(**new_lobby)

    return responses.create_success(f'Report submitted for match {match_db.id}', 'api.match.get_match', match_id=match_db.id)


@match.route('/type/<int:match_type_id>', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(MatchtypeSchema())
@authenticate(app_auth)
@other_responses(unauthorized | not_found)
def get_match_type(match_type_id):
    """Get the details of a match type"""
    match_type = ensure_exists(Matchtype, id=match_type_id)
    return match_type.to_dict()


@match.route('/type', methods=['GET'])
@cache.cached(unless=force_refresh)
@response(MatchtypeList())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_match_types():
    """Get the list of match types"""
    query = db.session.query(Matchtype)
    match_types = [mt.to_dict() for mt in query]
    return {'matchtypes': match_types}


@match.route('/type', methods=['POST'])
@body(MatchtypeSchema())
@response(LinkSuccessSchema(), status_code=201)
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def add_match_type(data):
    """Create a new match type"""
    required_fields = valid_fields = ['name', 'description', 'periods', 'arena', 'mercy_rule',
                                      'match_length', 'game_mode', 'num_players']
    unique_fields = ['name']
    force_fields(data, required_fields)
    force_unique(Matchtype, data, unique_fields)

    cleaned_data = clean_data(data, valid_fields)

    match_type = Matchtype()
    match_type.from_dict(cleaned_data)
    db.session.add(match_type)
    db.session.commit()

    return responses.create_success(f'Match type {match_type.name} created.', 'api.match.get_match_type', match_type_id=match_type.id)


@match.route('/logs', methods=['POST'])
@body(LogsUploadSchema())
@response(LinkSuccessSchema())
@authenticate(app_auth)
@other_responses(unauthorized | bad_request)
def upload_from_logs(data):
    """Upload match data from log files"""
    match_db = ensure_exists(Match, id=data['match_id'])
    region = data['region']
    gamemode = data['gamemode']

    lobby = Lobby()
    lobby.match_id = match_db.id
    lobby.lobby_id = 'Offline - no lobby ID'
    lobby.active = False
    lobby.password = ''
    db.session.add(lobby)
    db.session.commit()

    for period in data['periods']:
        uploaded = period_from_log(period['log_json'], match_db.id, region, period['created'], gamemode, lobby.id)
        if not uploaded:
            raise BadRequest('Upload failed')

    validate_stats.delay(match_db.id)

    return responses.request_success('Log data uploaded successfully', 'api.match.get_match_stats', match_id=match_db.id)


@match.route('/gamemodes', methods=['GET'])
@response(GamemodeSchema())
@authenticate(app_auth)
@other_responses(unauthorized)
def get_gamemodes():
    """Get a list of accepted gamemodes"""
    query = db.session.query(GameMode)

    gamemodes = []
    for gamemode in query:
        gamemodes.append(gamemode.to_dict())

    return {'items': gamemodes}
