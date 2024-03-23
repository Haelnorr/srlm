import jwt
from time import time
from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from api.lds.app import db, login


user_permissions = db.Table('user_permissions',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
                            )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    reset_pass = db.Column(db.Boolean)
    slap_id = db.relationship('Player', back_populates='user', lazy=True, uselist=False)
    discord_id = db.relationship('Discord', back_populates='user', lazy=True, uselist=False)
    streamed_matches = db.relationship('Match', back_populates='streamer', lazy=True)
    reviewed_matches = db.relationship('PlayerMatchData', back_populates='reviewed_by')
    permissions = db.relationship('Permission', secondary=user_permissions, back_populates='users', lazy=True)

    def __repr__(self):
        return f'<User {self.username} | ID: {self.id}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_password_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['reset_password']
        except jwt.exceptions.PyJWTError:
            # failed to decode, catches all jwt.exceptions
            return
        return load_user(user_id)

    @staticmethod
    def new(username=None, email=None, password=False, reset_pass=False):
        if username is None:
            username = input('Username: ')
        if email is None:
            email = input('Email: ')
        if password is False:
            password = input('Password:')
        user = User(username=username, email=email, reset_pass=reset_pass)
        if password is not None:
            user.set_password(password)
        return user

    def has_permission(self, key):
        for permission in self.permissions:
            if permission.key == key:
                return True
        else:
            return False

    """"# TO BE DEPRECIATED BY PERMISSIONS TABLE
    def add_permission(self, permission):
        self.permissions += permission

    # TO BE DEPRECIATED BY PERMISSIONS TABLE
    def remove_permission(self, permission):
        self.permissions -= permission

    # TO BE DEPRECIATED BY PERMISSIONS TABLE
    def get_permissions(self):
        none = True
        superuser = False
        if self.permissions is not PERMISSIONS.none:
            none = False
            if self.permissions & PERMISSIONS.superuser:
                superuser = True
        permissions = {
            'none': none,
            'superuser': superuser,
            'admin': bool(self.permissions & PERMISSIONS.admin | superuser),
            'unusedperm_1': bool(self.permissions & PERMISSIONS.unusedperm_1 | superuser),
            'unusedperm_2': bool(self.permissions & PERMISSIONS.unusedperm_2 | superuser),
            'unusedperm_3': bool(self.permissions & PERMISSIONS.unusedperm_3 | superuser),
            'unusedperm_4': bool(self.permissions & PERMISSIONS.unusedperm_4 | superuser),
            'unusedperm_5': bool(self.permissions & PERMISSIONS.unusedperm_5 | superuser),
            'unusedperm_6': bool(self.permissions & PERMISSIONS.unusedperm_6 | superuser),
            'unusedperm_7': bool(self.permissions & PERMISSIONS.unusedperm_7 | superuser)
        }
        return permissions

    # TO BE DEPRECIATED BY PERMISSIONS TABLE
    def list_permissions(self):
        perms = self.get_permissions()
        message = '<Permissions for user {}> Superuser: {}, Admin: {}, Unused1: {}, Unused2: {},' \
                  ' Unused3: {}, Unused4: {}, Unused5: {}, Unused6: {}, Unused7: {}'
        message = message.format(self.username, perms['superuser'], perms['admin'], perms['unusedperm_1'],
                                 perms['unusedperm_2'], perms['unusedperm_3'], perms['unusedperm_4'],
                                 perms['unusedperm_5'],
                                 perms['unusedperm_6'], perms['unusedperm_7'])
        return message"""


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, index=True, nullable=False)
    description = db.Column(db.String(128))
    additional_modifiers = db.Column(db.String(128))  # optional field for modifiers, like specifying which team a player is manager of, or which leagues LC's can manage


class Discord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_token = db.Column(db.String(64))
    refresh_token = db.Column(db.String(64))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slap_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_name = db.Column(db.String(64), nullable=False, unique=True)
    rookie = db.Column(db.Boolean, nullable=False, default=True)
    first_season = db.Column(db.Integer, db.ForeignKey('season_division.id'))
    next_name_change = db.Column(db.DateTime, nullable=False)
    team_association = db.relationship('PlayerTeam', back_populates='player')
    teams = association_proxy('team_association', 'team')
    season_association = db.relationship('FreeAgent', back_populates='player')
    seasons = association_proxy('season_association', 'season_division')
    match_data_assoc = db.relationship('PlayerMatchData', back_populates='player')
    match_data = association_proxy('player_data_assoc', 'match')
    awards_association = db.relationship('PlayerAward', back_populates='player', lazy=True)
    awards = association_proxy('awards_association', 'award')


# this is a helper table for recording which teams played in which season and in which division
season_division_team = db.Table('season_division_team',
                                db.Column('season_division_id', db.Integer, db.ForeignKey('season_division.id')),
                                db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
                                )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), index=True, unique=True, nullable=False)
    color = db.Column(db.String(7))
    logo = db.Column(db.String(128))
    founded_date = db.Column(db.DateTime)

    player_association = db.relationship('PlayerTeam', back_populates='team')
    players = association_proxy('player_association', 'player')
    season_divisions = db.relationship('SeasonDivision', secondary=season_division_team, back_populates='teams')
    matches_won = db.relationship('MatchResult', back_populates='winner', lazy=True)
    matches_lost = db.relationship('MatchResult', back_populates='loser', lazy=True)
    matches_home = db.relationship('Match', back_populates='home_team', lazy=True)
    matches_away = db.relationship('Match', back_populates='away_team', lazy=True)
    finals_won = db.relationship('FinalResult', back_populates='winner', lazy=True)
    finals_lost = db.relationship('FinalResult', back_populates='loser', lazy=True)
    finals_home = db.relationship('Final', back_populates='home_team', lazy=True)
    finals_away = db.relationship('Final', back_populates='away_team', lazy=True)
    player_match_data = db.relationship('PlayerMatchData', back_populates='team')
    awards_association = db.relationship('TeamAward', back_populates='team', lazy=True)
    awards = association_proxy('awards_association', 'award')
    match_availability = db.relationship('MatchAvailability', back_populates='team', lazy=True)


# this is a helper table for recording which players were a part of which team and when (aka 'roster')
class PlayerTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    player = db.relationship('Player', back_populates='teams')
    team = db.relationship('Team', back_populates='players')


# this is a helper table for recording which players were free agents, for which seasons and when
class FreeAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    season_division_id = db.Column(db.Integer, db.ForeignKey('season_division.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    player = db.relationship('Player', back_populates='seasons')
    season_division = db.relationship('Team', back_populates='players')


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), unique=True, nullable=False)
    seasons = db.relationship('Season', back_populates='league', lazy=True)
    divisions = db.relationship('Division', back_populates='league', lazy=True)


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    league = db.Column(db.Integer, db.ForeignKey('league.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    finals_start = db.Column(db.DateTime)
    finals_end = db.Column(db.DateTime)
    division_association = db.relationship('SeasonDivision', back_populates='season')
    divisions = association_proxy('division_association', 'division')
    match_type = db.Column(db.Integer, db.ForeignKey('matchtype.id'))


class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    league = db.Column(db.Integer, db.ForeignKey('league.id'), nullable=False)
    description = db.Column(db.String(128))
    season_association = db.relationship('SeasonDivision', back_populates='division')
    seasons = association_proxy('season_association', 'season')


class SeasonDivision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    teams = db.relationship('Team', secondary=season_division_team, back_populates='season_divisions')
    free_agent_association = db.relationship('FreeAgent', back_populates='season_division')
    free_agents = association_proxy('free_agent_association', 'player')

    season = db.relationship('Season', back_populates='divisions')
    division = db.relationship('Division', back_populates='season')
    matches = db.relationship('Match', back_populates='season_division', lazy=True)
    finals = db.relationship('Final', back_populates='season_division', lazy=True)
    team_awards = db.relationship('TeamAward', back_populates='season_division')
    player_awards = db.relationship('PlayerAward', back_populates='season_division')


# info of a match between two registered league teams
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_division = db.Column(db.Integer, db.ForeignKey('season_division.id'))
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    round = db.Column(db.Integer)
    match_week = db.Column(db.Integer)
    results = db.relationship('MatchResult', back_populates='match', lazy=True, uselist=False)  # null if not completed?
    cancelled = db.Column(db.String(32))  # cancelled reason
    schedule = db.relationship('MatchSchedule', back_populates='match', uselist=False)
    team_availability = db.relationship('MatchSchedule', back_populates='match')
    streamer = db.Column(db.Integer, db.ForeignKey('user.id'))
    final = db.Column(db.Integer, db.ForeignKey('final.id'))


# result of a match between two registered league teams, one-to-one relationship with match
class MatchResult(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('match.id'), primary_key=True)
    winner = db.Column(db.Integer, db.ForeignKey('team.id'))
    loser = db.Column(db.Integer, db.ForeignKey('team.id'))
    draw = db.Column(db.Boolean, default=False)
    score_winner = db.Column(db.Integer, nullable=False, default=0)
    score_loser = db.Column(db.Integer, nullable=False, default=0)
    overtime = db.Column(db.Boolean, nullable=False, default=False)
    forfeit = db.Column(db.Boolean, nullable=False, default=False)
    vod = db.Column(db.String(128))
    lobbies = db.relationship('Lobby', back_populates='match', lazy=True)


# presets for creating lobbies using different match types
class Matchtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(128))
    periods = db.Column(db.Boolean, nullable=False, default=True)
    arena = db.Column(db.String(32), nullable=False, default='Slapstadium')
    mercy_rule = db.Column(db.Integer, nullable=False, default=0)
    match_length = db.Column(db.Integer, nullable=False, default=300)
    game_mode = db.Column(db.String(32), nullable=False, default='hockey')
    seasons = db.relationship('Season', back_populates='match_type', lazy=True)


# stores data on an in game lobby for use with Slapshot Public API
class Lobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer, db.ForeignKey('match.id'))
    lobby_id = db.Column(db.String(64), nullable=False)
    match_data = db.relationship('MatchData', back_populates='lobby', lazy=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    password = db.Column(db.String(64), nullable=False)


# stores data on in game matches (periods of a match are separate entries)
class MatchData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lobby = db.Column(db.Integer, db.ForeignKey('lobby.id'))
    match_id = db.Column(db.String(64), nullable=False)
    player_data_assoc = db.relationship('PlayerMatchData', back_populates='match')
    player_data = association_proxy('player_data_assoc', 'player')


# stores match data of particular players (periods of a match are separate entries)
class PlayerMatchData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer, db.ForeignKey('match_data.id'))
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
    period = db.Column(db.Integer, default=0)
    source = db.Column(db.String(10)) # slap api, user, import
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    recorded_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    reviewed_date = db.Column(db.DateTime)
    valid = db.Column(db.Boolean, default=True)
    comments = db.Column(db.String(256))
    goals = db.Column(db.Integer, default=0)
    shots = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    saves = db.Column(db.Integer, default=0)
    primary_assists = db.Column(db.Integer, default=0)
    secondary_assists = db.Column(db.Integer, default=0)
    passes = db.Column(db.Integer, default=0)
    blocks = db.Column(db.Integer, default=0)
    takeaways = db.Column(db.Integer, default=0)
    turnovers = db.Column(db.Integer, default=0)
    possession_time = db.Column(db.Integer, default=0)
    game_winning_goals = db.Column(db.Integer, default=0)
    overtime_goals = db.Column(db.Integer, default=0)
    post_hits = db.Column(db.Integer, default=0)
    faceoffs_won = db.Column(db.Integer, default=0)
    faceoffs_lost = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)


class Final(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_division = db.Column(db.Integer, db.ForeignKey('season_division.id'))
    best_of = db.Column(db.Integer, nullable=False, default=1)
    elimination = db.Column(db.Boolean, nullable=False, default=True)
    round = db.Column(db.String(20), nullable=False)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    matches = db.relationship('Match', back_populates='final', lazy=True)
    results = db.relationship('FinalResults', back_populates='final', lazy=True, uselist=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)


class FinalResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    final = db.Column(db.Integer, db.ForeignKey('final.id'))
    winner = db.Column(db.Integer, db.ForeignKey('team.id'))
    loser = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_team_score = db.Column(db.Integer, nullable=False, default=0)
    away_team_score = db.Column(db.Integer, nullable=False, default=0)


class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    description = db.Column(db.String(128), nullable=False)
    teams_association = db.relationship('TeamAward', back_populates='award', lazy=True)
    teams = association_proxy('teams_association', 'team')
    players_association = db.relationship('PlayerAward', back_populates='award', lazy=True)
    players = association_proxy('players_association', 'player')


class TeamAward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
    award = db.Column(db.Integer, db.ForeignKey('award.id'))
    season_division = db.Column(db.Integer, db.ForeignKey('season_division.id'))


class PlayerAward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    award = db.Column(db.Integer, db.ForeignKey('award.id'))
    season_division = db.Column(db.Integer, db.ForeignKey('season_division.id'))


class MatchSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer, db.ForeignKey('match.id'))
    scheduled_time = db.Column(db.DateTime)
    home_team_accepted = db.Column(db.Boolean, default=False, nullable=False)
    away_team_accepted = db.Column(db.Boolean, default=False, nullable=False)


class MatchAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer, db.ForeignKey('match.id'))
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)


class ServerRegion(db.Model):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class Arena(db.Model):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class EndReason(db.Model):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class GameMode(db.Model):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module = db.Column(db.String(50), index=True)
    message = db.Column(db.String(200))


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
