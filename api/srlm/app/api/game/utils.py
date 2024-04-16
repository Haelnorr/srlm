from api.srlm.app import db
from api.srlm.app.api.utils.functions import ensure_exists
from api.srlm.app.models import MatchData, Lobby, Match, Player, PlayerMatchData


def period_from_log(log_json, match_id, region, created, gamemode, lobby_id):

    match = ensure_exists(Match, return_none=True, id=match_id)

    if match is None:
        return None

    period = MatchData()
    period.current_period = log_json['current_period']
    period.winner = log_json['winner']
    period.periods_enabled = bool(log_json['periods_enabled'])
    period.current_period = int(log_json['current_period'])
    period.custom_mercy_rule = log_json['custom_mercy_rule']
    period.end_reason = log_json['end_reason']
    period.home_score = int(log_json['score']['home'])
    period.away_score = int(log_json['score']['away'])
    period.arena = log_json['arena']
    period.region = region
    period.created = created
    period.gamemode = gamemode
    period.lobby_id = lobby_id
    period.match_id = 'Offline - no match ID'
    period.source = 'LogUpload'
    db.session.add(period)
    db.session.commit()

    teams = {
        'home': match.home_team_id,
        'away': match.away_team_id
    }

    for player in log_json['players']:
        player_db = ensure_exists(Player, return_none=True, slap_id=player['game_user_id'])
        if player_db is None:
            player_db = Player()
            player_db.player_name = player['username']
            player_db.slap_id = int(player['game_user_id'])
            player_db.first_season_id = match.season_division_id
            db.session.add(player_db)
            db.session.commit()

        valid_stats = ['goals', 'shots', 'assists', 'saves', 'primary_assists', 'secondary_assists', 'passes', 'blocks',
                       'takeaways', 'turnovers', 'possession_time_sec', 'game_winning_goals', 'post_hits',
                       'faceoffs_won', 'faceoffs_lost', 'score']

        player_data = PlayerMatchData()
        player_data.match_id = period.id
        player_data.player_id = player_db.id
        player_data.team_id = teams[player['team']]
        for stat in player['stats']:
            if stat in valid_stats:
                setattr(player_data, stat, player['stats'][stat])
        db.session.add(player_data)
        db.session.commit()

    return True
