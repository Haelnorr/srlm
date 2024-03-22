import jwt
from time import time
from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from api.lds.app import db, login
from api.lds.definitions import PERMISSIONS


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    permissions = db.Column(db.Integer, nullable=False, default=0)
    reset_pass = db.Column(db.Boolean)
    slap_id = db.relationship('Player', backref='user', lazy=True, uselist=False)
    discord_id = db.relationship('Discord', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return '<User {}> ID: {}, Email: {}, Permissions: {}, Reset Pass: {}' \
            .format(self.username, self.id, self.email, self.permissions, self.permissions)

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
    def new(username=None, email=None, password=False, reset_pass=False, permissions=0):
        if username is None:
            username = input('Username: ')
        if email is None:
            email = input('Email: ')
        if password is False:
            password = input('Password:')
        user = User(username=username, email=email, reset_pass=reset_pass, permissions=permissions)
        if password is not None:
            user.set_password(password)
        return user

    def add_permission(self, permission):
        self.permissions += permission

    def remove_permission(self, permission):
        self.permissions -= permission

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

    def list_permissions(self):
        perms = self.get_permissions()
        message = '<Permissions for user {}> Superuser: {}, Admin: {}, Unused1: {}, Unused2: {},' \
                  ' Unused3: {}, Unused4: {}, Unused5: {}, Unused6: {}, Unused7: {}'
        message = message.format(self.username, perms['superuser'], perms['admin'], perms['unusedperm_1'],
                                 perms['unusedperm_2'], perms['unusedperm_3'], perms['unusedperm_4'],
                                 perms['unusedperm_5'],
                                 perms['unusedperm_6'], perms['unusedperm_7'])
        return message


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


season_division_team = db.Table('season_division_team',
                                db.Column('season_division_id', db.Integer, db.ForeignKey('SeasonDivision')),
                                db.Column('team_id', db.Integer, db.ForeignKey('Team'))
                                )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), unique=True, nullable=False)
    color = db.Column(db.String(7))
    logo = db.Column(db.String(128))
    founded_date = db.Column(db.DateTime)
    player_association = db.relationship('PlayerTeam', back_populates='team')
    players = association_proxy('player_association', 'player')
    season_divisions = db.relationship('SeasonDivision', secondary=season_division_team, backref='teams')


class PlayerTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    player = db.relationship('Player', back_populates='teams')
    team = db.relationship('Team', back_populates='players')


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), unique=True, nullable=False)
    seasons = db.relationship('Season', backref='league', lazy=True)
    divisions = db.relationship('Division', backref='league', lazy=True)


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
    # type =


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
    teams = db.relationship('Team', secondary=season_division_team, backref='season_divisions')

    season = db.relationship('Season', back_populates='divisions')
    division = db.relationship('Division', back_populates='season')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module = db.Column(db.String(50), index=True)
    message = db.Column(db.String(200))


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
