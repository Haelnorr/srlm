"""Provides marshmallow schemas for documentation support"""
from api.srlm.app import ma
from api.srlm.app.models import Permission, Match, Team, MatchResult, MatchReview, PlayerMatchData, MatchData, Discord, \
    Twitch, UserPermissions, User


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


class PaginationLinks(Links):
    """Defines pagination links"""
    next = ma.URL()
    prev = ma.URL()


class FilterSchema(ma.Schema):
    """Defines filter arg"""
    f = ma.Str()


class BasicAuthSchema(ma.Schema):
    """Defines the basic user auth login"""
    username = ma.Str(required=True)
    password = ma.Str(required=True)


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


class PermissionCollection(ma.Schema):
    """Defines the structure of the permissions collection"""
    items = ma.List(ma.Nested(PermissionSchema()))
    _meta = ma.Nested(PaginationArgs())
    _links = ma.Nested(PaginationLinks())


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
    founded_date = ma.auto_field(dump_only=True)
    color = ma.auto_field()
    logo = ma.auto_field()
    active_players = ma.Int(dump_only=True)
    seasons_played = ma.Int(dump_only=True)
    awards = ma.Int(dump_only=True)
    _links = ma.Nested(TeamLinks())


class SimpleTeamSchema(ma.SQLAlchemySchema):
    """Defines the structure of a simple team response"""
    class Meta:
        model = Team
        ordered = True

    name = ma.auto_field()
    acronym = ma.auto_field(required=True)
    color = ma.auto_field()
    _links = ma.Nested(Links())


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

    id = ma.auto_field()
    player = ma.Str()
    team = ma.Str()
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
    _links = ma.Nested(PlayerDataLinks())


class MatchDataSchema(ma.SQLAlchemySchema):
    """Defines the structure for match data requests"""
    class Meta:
        model = MatchData
        ordered = True

    lobby_id = ma.auto_field()
    processed = ma.auto_field()
    accepted = ma.auto_field()
    match_id = ma.auto_field()
    region = ma.auto_field()
    gamemode = ma.auto_field()
    created = ma.auto_field()
    arena = ma.auto_field()
    home_score = ma.auto_field()
    away_score = ma.auto_field()
    winner = ma.auto_field()
    current_period = ma.auto_field()
    periods_enabled = ma.auto_field()
    custom_mercy_rule = ma.auto_field()
    end_reason = ma.auto_field()
    source = ma.auto_field()


class MatchReviewSchema(ma.Schema):
    """Defines structure of MatchReview requests"""
    class MatchFlag(ma.SQLAlchemySchema):
        class Meta:
            model = MatchReview
            ordered = True

        type = ma.auto_field()
        reason = ma.auto_field()
        raised_by = ma.auto_field()
        comments = ma.auto_field()
        resolved = ma.auto_field()
        resolved_by = ma.auto_field()
        resolved_on = ma.auto_field()

    class MatchReviewDataSchema(MatchDataSchema):
        player_data = ma.List(ma.Nested(PlayerMatchDataSchema()))

    match_id = ma.Int()
    match_details = ma.Nested(SimpleMatchSchema())
    periods = ma.List(ma.Nested(MatchReviewDataSchema()))
    flags = ma.List(ma.Nested(MatchFlag()))


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
    email = ma.auto_field(required=True)
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
    _meta = ma.Nested(PaginationArgs())
    _links = ma.Nested(PaginationLinks())
