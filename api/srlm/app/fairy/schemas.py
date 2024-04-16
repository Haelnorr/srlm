"""Provides marshmallow schemas for documentation support"""
from marshmallow import EXCLUDE
from marshmallow.validate import OneOf

from api.srlm.app import ma
from api.srlm.app.models import Permission, Match, Team, MatchResult, MatchReview, PlayerMatchData, MatchData, Discord, \
    Twitch, UserPermissions, User, Division, League, Season, SeasonDivision, Player, FreeAgent, Matchtype


class Links(ma.Schema):
    """Defines base Links schema"""
    self = ma.URL()


class UserLinks(Links):
    """Extends base Links to add User"""
    user = ma.URL()


class UserNoSelfLinks(ma.Schema):
    """Defines schema for only user link"""
    user = ma.URL()


class PaginationArgs(ma.Schema):
    """Defines pagination args"""
    page = ma.Int(missing=1)
    per_page = ma.Int(missing=10)
    total_pages = ma.Int(dump_only=True)
    total_items = ma.Int(dump_only=True)


class DateFilters(PaginationArgs):
    """Defines filters for dates"""
    start_date = ma.Date()
    end_date = ma.Date()


class SeasonFilters(DateFilters):
    """Filters for season lookup"""
    league = ma.Str()
    current = ma.Bool()
    last = ma.Bool()
    next = ma.Bool()
    order = ma.Str(missing="desc", validate=OneOf(['asc', 'desc']))
    order_by = ma.Str(missing="start_date", validate=OneOf(
        ['start_date', 'end_date', 'finals_start', 'finals_end', 'name', 'league']))


class PaginationLinks(Links):
    """Defines pagination links"""
    next = ma.URL()
    prev = ma.URL()


class Collection(ma.Schema):
    """Defines the meta structure of collections"""
    _meta = ma.Nested(PaginationArgs())
    _links = ma.Nested(PaginationLinks())


class CurrentFilterSchema(ma.Schema):
    """Defines filter arg for current"""
    current = ma.Bool()


class UnplayedFilterSchema(ma.Schema):
    """Defines filter arg for unplayed"""
    unplayed = ma.Bool()


class StatsFilterSchema(ma.Schema):
    """Defines filter arg for stats"""
    season = ma.Int()
    division = ma.Int()
    team = ma.Int()


class BasicAuthSchema(ma.Schema):
    """Defines the basic user auth login"""
    username = ma.Str(required=True)
    password = ma.Str(required=True)


class DiscordAuthSchema(ma.Schema):
    """Defines the scheme for auth via discord"""
    access_token = ma.Str(required=True)
    refresh_token = ma.Str(required=True)
    expires_in = ma.Int(required=True)


class TokenSchema(ma.Schema):
    """Defines Token responses"""
    token = ma.Str()
    expires = ma.DateTime()


class BasicSuccessSchema(ma.Schema):
    """Defines basic success responses"""
    result = ma.Str()
    message = ma.Str()


class LinkSuccessSchema(BasicSuccessSchema):
    """Defines success responses with a resource link provided"""
    location = ma.URL()


class UserVerifySchema(ma.Schema):
    """Defines the response for verifying a user token"""
    user = ma.Int()
    expires = ma.DateTime()
    _links = ma.Nested(UserLinks())


class PermissionSchema(ma.SQLAlchemySchema):
    """Defines the structure of Permissions requests"""
    class Meta:
        model = Permission
        ordered = True

    id = ma.auto_field(dump_only=True)
    key = ma.auto_field(required=True)
    description = ma.auto_field()
    users_count = ma.Int(dump_only=True)
    _links = ma.Nested(Links(), dump_only=True)


class PermissionCollection(Collection):
    """Defines the structure of the permissions collection"""
    items = ma.List(ma.Nested(PermissionSchema()))


class UserPermissionsSchema(ma.SQLAlchemySchema):
    """Defines the structure of UserPermissions requests"""
    class Meta:
        model = UserPermissions
        ordered = True

    permission_id = ma.auto_field(dump_only=True)
    user = ma.Str(dump_only=True)
    key = ma.Str(required=True)
    description = ma.Str()
    additional_modifiers = ma.auto_field()
    _links = ma.Nested(UserLinks())


class UpdateUserPermissionsSchema(UserPermissionsSchema):
    """Extends UserPermissionsSchema for defining update requests"""
    additional_modifiers = ma.auto_field(required=True)


class RevokeUserPermission(ma.Schema):
    """Defines request body for revoking user permissions"""
    key = ma.Str(required=True)


class UserPermissionsCollection(ma.Schema):
    """Defines the structure of UserPermissions collections"""
    username = ma.Str(dump_only=True)
    permissions = ma.List(ma.Nested(UserPermissionsSchema()))
    _links = ma.Nested(Links())


class UpdatePermissionSchema(PermissionSchema):
    """Extends the PermissionSchema making the `key` field optional"""
    key = ma.auto_field(required=False)


class PermUsersSchema(ma.Schema):
    """Schema for defining the response listing users with a given permission"""

    class UsersWithPerm(ma.Schema):
        id = ma.Int()
        username = ma.String()
        _links = ma.Nested(Links())

    permission = ma.String()
    key = ma.String()
    users = ma.Nested(UsersWithPerm())
    _links = ma.Nested(Links())


class TeamSchema(ma.SQLAlchemySchema):
    """Defines the structure of Teams requests"""
    class Meta:
        model = Team
        ordered = True

    class TeamLinks(Links):
        logo = ma.URL()
        active_players = ma.URL()
        seasons_played = ma.URL()
        awards = ma.URL()

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    acronym = ma.auto_field(required=True)
    founded_date = ma.auto_field()
    color = ma.auto_field()
    logo = ma.auto_field()
    active_players = ma.Int(dump_only=True)
    seasons_played = ma.Int(dump_only=True)
    awards = ma.Int(dump_only=True)
    _links = ma.Nested(TeamLinks(), dump_only=True)


class EditTeamSchema(TeamSchema):
    """Overrides the team schema to make name and acronym optional"""
    name = ma.auto_field()
    acronym = ma.auto_field()


class SimpleTeamSchema(ma.SQLAlchemySchema):
    """Defines the structure of a simple team response"""
    class Meta:
        model = Team
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    acronym = ma.auto_field(required=True)
    color = ma.auto_field()
    _links = ma.Nested(Links())


class TeamCollection(Collection):
    """Defines the collection of teams"""
    items = ma.List(ma.Nested(TeamSchema()))


class MatchResultSchema(ma.SQLAlchemySchema):
    """Defines the structure of MatchResult requests"""
    class Meta:
        model = MatchResult
        ordered = True

    winner = ma.Str()
    loser = ma.Str()
    draw = ma.auto_field()
    score_winner = ma.auto_field()
    score_loser = ma.auto_field()
    overtime = ma.auto_field()
    forfeit = ma.auto_field()
    vod = ma.auto_field()
    _links = ma.Nested(Links())


class CurrentLobby(ma.Schema):
    id = ma.Int()
    password = ma.Str()


class TwitchSchema(ma.SQLAlchemySchema):
    """Defines the structure of Twitch requests"""
    class Meta:
        model = Twitch
        ordered = True

    user = ma.Str(dump_only=True)
    twitch_id = ma.auto_field(required=True)
    access_token = ma.auto_field(required=True)
    refresh_token = ma.auto_field(required=True)
    token_expiration = ma.auto_field(dump_only=True)
    expires_in = ma.Int(load_only=True, required=True)
    _links = ma.Nested(UserLinks())


class UpdateTwitchSchema(TwitchSchema):
    twitch_id = ma.auto_field()
    access_token = ma.auto_field()
    refresh_token = ma.auto_field()
    expires_in = ma.Int()


class ViewMatchSchema(ma.SQLAlchemySchema):
    """Defines the structure of Matches requests"""
    class Meta:
        model = Match
        ordered = True

    class MatchLinks(Links):
        season_division = ma.URL()
        home_team = ma.URL()
        away_team = ma.URL()
        steamer = ma.URL()

    id = ma.auto_field()
    season_division = ma.Str()
    home_team = ma.Nested(SimpleTeamSchema())
    away_team = ma.Nested(SimpleTeamSchema())
    round = ma.auto_field()
    match_week = ma.auto_field()
    cancelled = ma.auto_field()
    streamer = ma.Nested(TwitchSchema())
    final = ma.Bool()
    scheduled_time = ma.DateTime()
    current_lobby = ma.Nested(CurrentLobby())
    results = ma.Nested(MatchResultSchema())
    _links = ma.Nested(MatchLinks())


class SimpleMatchSchema(ma.SQLAlchemySchema):
    """Defines the structure of simple match response"""
    class Meta:
        model = Match
        ordered = True

    class SimpleMatchLinks(Links):
        season_division = ma.URL()
        home_team = ma.URL()
        away_team = ma.URL()

    id = ma.auto_field()
    home_team = ma.Nested(SimpleTeamSchema())
    away_team = ma.Nested(SimpleTeamSchema())
    result = ma.Str()
    round = ma.auto_field()
    match_week = ma.auto_field()
    final = ma.Bool()
    scheduled_time = ma.DateTime()
    current_lobby = ma.Nested(CurrentLobby())
    _links = ma.Nested(SimpleMatchLinks())


class NewMatchSchema(ma.SQLAlchemySchema):
    """Defines the structure for editing a match"""
    class Meta:
        model = Match
        ordered = True

    season_division_id = ma.auto_field(required=True)
    home_team_id = ma.auto_field(required=True)
    away_team_id = ma.auto_field(required=True)
    round = ma.auto_field()
    match_week = ma.auto_field()


class PlayerMatchDataSchema(ma.SQLAlchemySchema):
    """Defines the structure of player match data"""
    class Meta:
        model = PlayerMatchData
        ordered = True

    class PlayerDataLinks(ma.Schema):
        player = ma.URL()
        team = ma.URL()

    id = ma.auto_field(required=True)
    player = ma.Str(dump_only=True)
    team = ma.Str(dump_only=True)
    goals = ma.auto_field()
    shots = ma.auto_field()
    assists = ma.auto_field()
    saves = ma.auto_field()
    primary_assists = ma.auto_field()
    secondary_assists = ma.auto_field()
    passes = ma.auto_field()
    blocks = ma.auto_field()
    takeaways = ma.auto_field()
    turnovers = ma.auto_field()
    possession_time_sec = ma.auto_field()
    game_winning_goals = ma.auto_field()
    post_hits = ma.auto_field()
    faceoffs_won = ma.auto_field()
    faceoffs_lost = ma.auto_field()
    score = ma.auto_field()
    _links = ma.Nested(PlayerDataLinks(), dump_only=True)


class MatchDataSchema(ma.SQLAlchemySchema):
    """Defines the structure for match data requests"""
    class Meta:
        model = MatchData
        ordered = True

    id = ma.auto_field(required=True)
    lobby_id = ma.auto_field(dump_only=True)
    processed = ma.auto_field(dump_only=True)
    accepted = ma.auto_field(required=True)
    match_id = ma.auto_field(dump_only=True)
    region = ma.auto_field(dump_only=True)
    gamemode = ma.auto_field(dump_only=True)
    created = ma.auto_field(dump_only=True)
    arena = ma.auto_field(dump_only=True)
    home_score = ma.auto_field()
    away_score = ma.auto_field()
    winner = ma.auto_field()
    current_period = ma.auto_field()
    periods_enabled = ma.auto_field()
    custom_mercy_rule = ma.auto_field()
    end_reason = ma.auto_field()
    source = ma.auto_field(dump_only=True)


class MatchFlag(ma.SQLAlchemySchema):
    """Defines structure of match flags"""
    class Meta:
        model = MatchReview
        ordered = True

    id = ma.auto_field(required=True)
    type = ma.auto_field(dump_only=True)
    reason = ma.auto_field(dump_only=True)
    raised_by = ma.auto_field(dump_only=True)
    comments = ma.auto_field()
    resolved = ma.auto_field()
    resolved_by = ma.auto_field(dump_only=True)
    resolved_on = ma.auto_field(dump_only=True)


class NewMatchFlag(MatchFlag):
    """Defines structure for creating a new match flag"""
    class NewLobby(ma.Schema):
        class InitialScore(ma.Schema):
            home = ma.Int(required=True)
            away = ma.Int(required=True)

        current_period = ma.Int()
        stats_carryover = ma.Boolean()
        initial_score = ma.Nested(InitialScore(), optional=True)

    id = ma.auto_field(dump_only=True)
    type = ma.auto_field(required=True)
    reason = ma.auto_field(required=True)
    comments = ma.auto_field(required=True)
    resolved = ma.auto_field(dump_only=True)
    new_lobby = ma.Nested(NewLobby(), optional=True)


class MatchPlayerDataSchema(MatchDataSchema):
    """Extends MatchDataSchema adding player data"""
    player_data = ma.List(ma.Nested(PlayerMatchDataSchema()))


class MatchStatsSchema(ma.Schema):
    """Defines response when requesting match stats"""
    match_id = ma.Int(dump_only=True)
    match_details = ma.Nested(SimpleMatchSchema(), dump_only=True)
    periods = ma.List(ma.Nested(MatchPlayerDataSchema()))


class MatchReviewSchema(MatchStatsSchema):
    """Defines structure of MatchReview requests"""
    flags = ma.List(ma.Nested(MatchFlag()), required=True)


class GenerateLobbySchema(ma.Schema):
    """Defines input for generating lobbies"""
    match_id = ma.Int(required=True)


class LinkSteamSchema(ma.Schema):
    """Defines input for linking steam account"""
    steam_id = ma.String(required=True)


class DiscordSchema(ma.SQLAlchemySchema):
    """Defines structure of Discord requests"""
    class Meta:
        model = Discord
        ordered = True

    class DiscordLinks(Links):
        user = ma.URL()

    user = ma.Str(dump_only=True)
    discord_id = ma.auto_field(required=True)
    access_token = ma.auto_field(required=True)
    refresh_token = ma.auto_field(required=True)
    token_expiration = ma.auto_field(dump_only=True)
    expires_in = ma.Int(required=True, load_only=True)
    _links = ma.Nested(DiscordLinks())


class UpdateDiscordSchema(DiscordSchema):
    """Extends DiscordSchema for defining updates requests"""
    discord_id = ma.auto_field()
    access_token = ma.auto_field()
    refresh_token = ma.auto_field()
    expires_in = ma.Int(load_only=True)


class ChangePasswordSchema(ma.Schema):
    """Defines request body for changing password"""
    password = ma.Str()


class PasswordResetSchema(ma.Schema):
    """Defines structure for password reset requests"""

    username = ma.Str(load_only=True)
    password = ma.Str(load_only=True)
    user = ma.Int(dump_only=True)
    reset_token = ma.Str(dump_only=True)
    _links = ma.Nested(UserNoSelfLinks(), dump_only=True)


class UserSchema(ma.SQLAlchemySchema):
    """Defines the structure of user requests"""
    class Meta:
        model = User
        ordered = True

    class UserSchemaLinks(Links):
        player = ma.URL()
        discord = ma.URL()
        permissions = ma.URL()
        matches_streamed = ma.URL()

    id = ma.auto_field()
    username = ma.auto_field(required=True)
    email = ma.auto_field()
    password = ma.Str(load_only=True, required=True)
    player = ma.Int(dump_only=True)
    discord = ma.Int(dump_only=True)
    permissions = ma.List(ma.Str(), dump_only=True)
    matches_streamed = ma.Int(dump_only=True)
    reset_pass = ma.Bool(dump_only=True)
    _links = ma.Nested(UserSchemaLinks(), dump_only=True)


class UpdateUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    username = ma.auto_field()
    email = ma.auto_field()


class UserCollection(ma.Schema):
    """Defines the structure of the users collection"""
    items = ma.List(ma.Nested(UserSchema()))


class LeagueLink(Links):
    """Extends Links class to provide league link"""
    league = ma.URL()


class LeagueSchema(ma.SQLAlchemySchema):
    """Defines the structure for League requests"""
    class Meta:
        model = League
        ordered = True

    class LeagueLinks(Links):
        seasons = ma.URL()
        divisions = ma.URL()

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    acronym = ma.auto_field(required=True)
    seasons_count = ma.Int(dump_only=True)
    divisions_count = ma.Int(dump_only=True)
    _links = ma.Nested(LeagueLinks, dump_only=True)


class EditLeagueSchema(LeagueSchema):
    """Overrides the LeagueSchema to make name and acronym optional"""
    name = ma.auto_field()
    acronym = ma.auto_field()


class LeagueCollection(Collection):
    """Defines the collection of Leagues"""
    items = ma.List(ma.Nested(LeagueSchema))


class SeasonSchema(ma.SQLAlchemySchema):
    """Defines the structure for Season requests"""
    class Meta:
        model = Season
        ordered = True

    class SeasonLinks(Links):
        league = ma.URL()
        match_type = ma.URL()
        divisions = ma.URL()

    class DivisionLink(ma.Schema):
        name = ma.Str()
        acronym = ma.Str()
        _link = ma.URL()

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    acronym = ma.auto_field(required=True)
    league = ma.Str(required=True)
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    finals_start = ma.auto_field()
    finals_end = ma.auto_field()
    match_type = ma.Str(required=True)
    divisions = ma.List(ma.Nested(DivisionLink()))
    _links = ma.Nested(SeasonLinks())


class EditSeasonSchema(SeasonSchema):
    """Overrides the SeasonSchema to make league and match_type dump_only"""
    league = ma.Str(dump_only=True)
    match_type = ma.Str(dump_only=True)


class SeasonCollection(Collection):
    """Defines the structure for the collection of Seasons"""
    items = ma.List(ma.Nested(SeasonSchema))


class DivisionSchema(ma.SQLAlchemySchema):
    """Defines the structure for Division requests"""
    class Meta:
        model = Division
        ordered = True

    class DivisionLinks(Links):
        league = ma.URL()
        seasons = ma.URL()

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    acronym = ma.auto_field(required=True)
    league = ma.Str(required=True)
    description = ma.auto_field()
    seasons_count = ma.Int(dump_only=True)
    _links = ma.Nested(DivisionLinks(), dump_only=True)


class UpdateDivisionSchema(ma.SQLAlchemySchema):
    """Defines the structure for updating Divisions"""
    class Meta:
        model = Division
        ordered = True

    name = ma.auto_field()
    acronym = ma.auto_field()
    description = ma.auto_field()


class DivisionCollection(Collection):
    """Defines the structure for Divisions collection"""
    items = ma.List(ma.Nested(DivisionSchema()))


class SeasonsOfDivision(ma.Schema):
    """Defines the response structure when requesting a list of seasons the division is in"""
    class SeasonOfDivision(ma.Schema):
        id = ma.Int()
        name = ma.Str()
        acronym = ma.Str()
        _links = ma.Nested(Links())

    division = ma.Str()
    acronym = ma.Str()
    league = ma.Str()
    seasons = ma.List(ma.Nested(SeasonOfDivision))
    _links = ma.Nested(LeagueLink())


class SeasonsInLeague(ma.Schema):
    """Defines the response for the list of seasons in a league"""
    league = ma.Str()
    acronym = ma.Str()
    seasons = ma.Nested(SeasonCollection())


class DivisionsInLeague(ma.Schema):
    """Defines the response for the list of divisions in a league"""
    league = ma.Str()
    acronym = ma.Str()
    divisions = ma.Nested(DivisionCollection())


class SeasonDivisionSchema(ma.SQLAlchemySchema):
    """Defines the structure for SeasonDivision requests"""
    class Meta:
        model = SeasonDivision
        ordered = True

    class SeasonDivisionLinks(LeagueLink):
        season = ma.URL()
        division = ma.URL()
        teams = ma.URL()
        free_agents = ma.URL()
        rookies = ma.URL()
        matches = ma.URL()
        finals = ma.URL()

    season_id = ma.auto_field(required=True, load_only=True)
    division_id = ma.auto_field(required=True, load_only=True)
    id = ma.auto_field(dump_only=True)
    season = ma.Nested(SeasonSchema(), dump_only=True)
    division = ma.Nested(DivisionSchema(), dump_only=True)
    league = ma.Str(dump_only=True)
    teams_count = ma.Int(dump_only=True)
    free_agents_count = ma.Int(dump_only=True)
    rookies_count = ma.Int(dump_only=True)
    matches_count = ma.Int(dump_only=True)
    finals_count = ma.Int(dump_only=True)
    _links = ma.Nested(SeasonDivisionLinks(), dump_only=True)


class PlayerSchema(ma.SQLAlchemySchema):
    """Defines the structure for Player requests"""
    class Meta:
        model = Player
        ordered = True

    class PlayerLinks(Links):
        user = ma.URL()
        first_season = ma.URL()
        current_team = ma.URL()
        teams = ma.URL()
        free_agent_seasons = ma.URL()
        awards = ma.URL()

    id = ma.auto_field(dump_only=True)
    player_name = ma.auto_field(required=True)
    user = ma.Str(dump_only=True)
    slap_id = ma.auto_field()
    rookie = ma.auto_field()
    first_season = ma.Str(dump_only=True)
    first_season_id = ma.auto_field(load_only=True)
    next_name_change = ma.auto_field(dump_only=True)
    current_team = ma.Str(dump_only=True)
    teams = ma.Int(dump_only=True)
    free_agent_seasons = ma.Int(dump_only=True)
    awards = ma.Int(dump_only=True)
    _links = ma.Nested(PlayerLinks(), dump_only=True)


class EditPlayerSchema(PlayerSchema):
    """Overrides PlayerSchema making player_name optional"""
    player_name = ma.auto_field()


class PlayerCollection(Collection):
    """Defines the collection of Players"""
    items = ma.List(ma.Nested(PlayerSchema()))


class SimplePlayerSchema(ma.SQLAlchemySchema):
    """Defines a simplified version of the PlayerSchema"""
    class Meta:
        model = Player
        ordered = True

    class SimplePlayerLinks(Links):
        user = ma.URL()
        current_team = ma.URL()

    player_name = ma.auto_field(required=True)
    user = ma.Str(dump_only=True)
    slap_id = ma.auto_field(dump_only=True)
    current_team = ma.Str(dump_only=True)
    _links = ma.Nested(SimplePlayerLinks(), dump_only=True)


class PlayerLink(ma.Schema):
    player = ma.URL()


class FreeAgentSchema(ma.SQLAlchemySchema):
    """Defines the structure for free agent requests"""
    class Meta:
        model = FreeAgent
        ordered = True

    player = ma.Str()
    player_id = ma.auto_field(load_only=True, required=True)
    season_division_id = ma.auto_field(load_only=True, required=True)
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    _links = ma.Nested(PlayerLink())


class SeasonDivisionLink(Links):
    """Extends the base Links class adding season_division"""
    season_division = ma.URL()
    league = ma.URL()


class SimpleSeasonDivision(ma.Schema):
    """Base class for other season division requests"""
    id = ma.Int(dump_only=True)
    season = ma.Str(dump_only=True)
    division = ma.Str(dump_only=True)
    league = ma.Str(dump_only=True)
    _links = ma.Nested(SeasonDivisionLink())


class StartEndDates(ma.Schema):
    start = ma.DateTime()
    end = ma.DateTime()


class SeasonDivisionTeams(SimpleSeasonDivision):
    """Defines the response for the list of teams in a SeasonDivision"""
    class SeasonTeamSchema(SimpleTeamSchema):
        class CurrentPlayers(ma.Schema):
            id = ma.Int()
            name = ma.Str()
            start_date = ma.Date()
            end_date = ma.Date()
            _links = ma.Nested(Links())
        players = ma.List(ma.Nested(CurrentPlayers()))
    teams = ma.List(ma.Nested(SeasonTeamSchema()))


class SeasonDivisionRookies(SimpleSeasonDivision):
    """Defines the response for the list of rookies in a SeasonDivision"""
    rookies = ma.List(ma.Nested(SimplePlayerSchema()))


class SeasonDivisionFreeAgents(SimpleSeasonDivision):
    """Defines the response for the list of free agents in a SeasonDivision"""
    free_agents = ma.List(ma.Nested(FreeAgentSchema()))


class SeasonDivisionMatches(SimpleSeasonDivision):
    """Defines the response for the list of matches in a SeasonDivision"""
    matches = ma.List(ma.Nested(SimpleMatchSchema()))


class PlayerTeams(ma.Schema):
    """Defines the response for the list of teams a player has been on"""
    class TeamList(ma.Schema):
        name = ma.Str()
        acronym = ma.Str()
        color = ma.Str()
        dates = ma.List(ma.Nested(StartEndDates()))
        _links = ma.Nested(Links())

    player = ma.Str(dump_only=True)
    teams = ma.List(ma.Nested(TeamList()), dump_only=True)
    current_team = ma.Nested(TeamList())
    _links = ma.Nested(PlayerLink(), dump_only=True)
    team = ma.Str(required=True, load_only=True)


class TeamLink(Links):
    team = ma.URL()


class TeamPlayers(ma.Schema):
    """Defines the response for the list of players a team has"""
    class PlayerList(ma.Schema):
        id = ma.Int()
        name = ma.Str()
        dates = ma.List(ma.Nested(StartEndDates()))
        _links = ma.Nested(Links())

    team = ma.Str()
    acronym = ma.Str()
    color = ma.Str()
    players = ma.List(ma.Nested(PlayerList()))
    _links = ma.Nested(TeamLink())


class TeamSeasonPlayers(ma.Schema):
    """Defines the response for the list of players in a team during a given season"""
    class CurrentPlayer(ma.Schema):
        id = ma.Int()
        name = ma.Str()
        dates = ma.List(ma.Nested(StartEndDates()))
        _links = ma.Nested(Links())

    season_division = ma.Str()
    team = ma.Str()
    acronym = ma.Str()
    color = ma.Str()
    players = ma.List(ma.Nested(CurrentPlayer()))
    _links = ma.Nested(TeamLink())


class TeamSeasons(SimpleTeamSchema):
    """Defines the response for the list of seasons a team has played in"""
    season_divisions = ma.List(ma.Nested(SimpleSeasonDivision()), dump_only=True)
    _links = ma.Nested(TeamLink(), dump_only=True)
    season_division_id = ma.Int(required=True, load_only=True)


class PlayerSeasons(ma.Schema):
    """Defines the response for the list of seasons a player has been a free agent in"""
    player = ma.Str(dump_only=True)
    free_agent_seasons = ma.List(ma.Nested(SimpleSeasonDivision()), dump_only=True)
    _links = ma.Nested(Links() and PlayerLink(), dump_only=True)
    season_division_id = ma.Int(load_only=True, required=True)


class MatchtypeSchema(ma.SQLAlchemySchema):
    """Defines the structure for Matchtype requests"""
    class Meta:
        model = Matchtype
        ordered = True

    name = ma.auto_field(required=True)
    description = ma.auto_field(required=True)
    periods = ma.auto_field(required=True)
    arena = ma.auto_field(required=True)
    mercy_rule = ma.auto_field(required=True)
    match_length = ma.auto_field(required=True)
    game_mode = ma.auto_field(required=True)
    num_players = ma.auto_field(required=True)
    _links = ma.Nested(Links(), dump_only=True)


class StatsSchema(ma.SQLAlchemySchema):
    """Defines structure of stats output"""
    class Meta:
        model = PlayerMatchData
        ordered = True

    goals = ma.auto_field()
    shots = ma.auto_field()
    assists = ma.auto_field()
    saves = ma.auto_field()
    primary_assists = ma.auto_field()
    secondary_assists = ma.auto_field()
    passes = ma.auto_field()
    blocks = ma.auto_field()
    takeaways = ma.auto_field()
    turnovers = ma.auto_field()
    possession_time_sec = ma.auto_field()
    game_winning_goals = ma.auto_field()
    post_hits = ma.auto_field()
    faceoffs_won = ma.auto_field()
    faceoffs_lost = ma.auto_field()
    score = ma.auto_field()


class PlayerStatsSchema(ma.Schema):
    """Defines response for retreiving player stats"""
    class PlayerStatsLinks(Links):
        player = ma.URL()
        season = ma.URL()
        division = ma.URL()
        team = ma.URL()

    player = ma.Nested(PlayerSchema())
    season = ma.Str()
    division = ma.Str()
    team = ma.Str()
    stats = ma.Nested(StatsSchema())
    _links = ma.Nested(PlayerStatsLinks())


class SeasonDivisionCollection(Collection):
    """Defines the collection of season divisions"""
    items = ma.List(ma.Nested(SeasonDivisionSchema()))


class DivisionsInSeason(ma.Schema):
    """Defines the response for the list of divisions in a season"""
    season = ma.Str()
    acronym = ma.Str()
    divisions = ma.Nested(SeasonDivisionCollection())


class SeasonDivisionLookup(ma.Schema):
    """Defines filters for the season division lookup"""
    season = ma.Str(required=True)
    division = ma.String(required=True)
    league = ma.String(required=True)


class SeasonLookup(ma.Schema):
    """Defines filter for league lookup"""
    league = ma.Str()


class LogsUploadSchema(ma.Schema):
    """Format for match data from log file uploads"""
    class Period(ma.Schema):
        class PeriodData(ma.Schema):
            class LogPlayer(ma.Schema):
                class Stats(ma.Schema):
                    class Meta:
                        unknown = EXCLUDE
                    goals = ma.Float()
                    shots = ma.Float()
                    assists = ma.Float()
                    saves = ma.Float()
                    primary_assists = ma.Float()
                    secondary_assists = ma.Float()
                    passes = ma.Float()
                    blocks = ma.Float()
                    takeaways = ma.Float()
                    turnovers = ma.Float()
                    possession_time_sec = ma.Float()
                    game_winning_goals = ma.Float()
                    post_hits = ma.Float()
                    faceoffs_won = ma.Float()
                    faceoffs_lost = ma.Float()
                    score = ma.Float()

                game_user_id = ma.Str(required=True)
                team = ma.Str(required=True)
                username = ma.Str(required=True)
                stats = ma.Nested(Stats(), required=True)

            class Score(ma.Schema):
                home = ma.Int(required=True)
                away = ma.Int(required=True)

            class Meta:
                unknown = EXCLUDE

            winner = ma.Str(required=True)
            arena = ma.Str(required=True)
            periods_enabled = ma.Str(required=True)
            current_period = ma.Str(required=True)
            custom_mercy_rule = ma.Str(required=True)
            end_reason = ma.Str(required=True)
            score = ma.Nested(Score(), required=True)
            players = ma.List(ma.Nested(LogPlayer()), required=True)

        log_json = ma.Nested(PeriodData(), required=True)
        created = ma.DateTime(required=True)

    periods = ma.List(ma.Nested(Period()), required=True)
    match_id = ma.Int(required=True)
    region = ma.Str(required=True)
    gamemode = ma.Str(required=True)


class GamemodeSchema(ma.Schema):
    class Gamemode(ma.Schema):
        value = ma.Str()
        label = ma.Str()
        info = ma.Str()

    items = ma.List(ma.Nested(Gamemode()))
