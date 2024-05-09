"""
Where all the models for the main league_manager database are defined
These models are used by both Alembic to create and migrate the database using Flask-Migrate and to interface with the
database using SQLAlchemy
"""
import jwt
import secrets
from time import time
from datetime import datetime, timedelta, timezone
import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from flask_login import UserMixin
from api.srlm.app import db, login


class LeagueManagerTable:
    __table_args__ = {"schema": "league_manager"}


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, UserMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reset_pass = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    steam_id = db.Column(db.String(32))

    player = db.relationship('Player', back_populates='user', lazy=True, uselist=False)
    discord = db.relationship('Discord', back_populates='user', lazy=True, uselist=False)
    twitch = db.relationship('Twitch', back_populates='user', lazy=True, uselist=False)
    streamed_matches = db.relationship('Match', back_populates='streamer', lazy=True)
    permission_assoc = db.relationship('UserPermissions', back_populates='user', lazy=True)
    permissions = association_proxy('permission_assoc', 'permission')

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

    def permissions_list(self):
        perms_list = []
        for permission in self.permissions:
            perms_list.append(permission.key)
        return perms_list

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'player': self.player.id if self.player is not None else None,
            'discord': self.discord.id if self.discord is not None else None,
            'permissions': self.permissions_list(),
            'matches_streamed': len(self.streamed_matches),
            'reset_pass': self.reset_pass,
            '_links': {
                'self': url_for('api.users.get_user', user_id=self.id),
                'player': url_for('api.players.get_player',
                                  player_id=self.player.id) if self.player is not None else None,
                'discord': url_for('api.users.discord.get_user_discord',
                                   user_id=self.id) if self.discord is not None else None,
                'permissions': url_for('api.users.permissions.get_user_permissions', user_id=self.id),
                'matches_streamed': url_for('api.users.get_user_matches_streamed', user_id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def has_permission(self, key):
        for perm in self.permission_assoc:
            if perm.permission.key == key:
                return perm.additional_modifiers if perm.permission.key == 'team_manager' else True
        else:
            return False

    def get_token(self, expires_in=604800):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=43200):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.query(User).filter(User.token == token).first()
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user

    def grant_permission(self, key, mods=None):
        perm = db.session.query(Permission).filter(Permission.key == key).first()
        if key == 'team_owner':
            user_perm = db.session.query(UserPermissions) \
                .filter(UserPermissions.user_id == self.id) \
                .filter(UserPermissions.permission_id == perm.id).first()
            if user_perm:
                user_perm.additional_modifiers = ','.join(mods + [user_perm.additional_modifiers])
                db.session.commit()
                return

        user_perm = UserPermissions()
        user_perm.user = self
        user_perm.permission = perm
        if mods:
            user_perm.additional_modifiers = ','.join(mods)
        db.session.add(user_perm)
        db.session.commit()


class Permission(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, index=True, nullable=False)
    description = db.Column(db.String(128))

    user_assoc = db.relationship('UserPermissions', back_populates='permission', lazy=True)
    users = association_proxy('user_assoc', 'user')

    def __repr__(self):
        return f'<Perm {self.key} | {self.description}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'key': self.key,
            'description': self.description,
            'users_count': len(self.users),
            '_links': {
                'self': url_for('api.auth.permissions.get_permission', perm_id_or_key=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['key', 'description']:
            if field in data:
                setattr(self, field, data[field])


class UserPermissions(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('league_manager.permission.id'))
    additional_modifiers = db.Column(db.String(
        128))  # optional field for modifiers, like specifying which team a player is manager of, or which leagues LC's can manage

    user = db.relationship('User', back_populates='permission_assoc')
    permission = db.relationship('Permission', back_populates='user_assoc')

    def __repr__(self):
        return f'<UserPerm {self.user.username} | {self.permission.key}>'

    def to_dict(self):
        data = {
            'permission_id': self.permission_id,
            'user': self.user.username,
            'key': self.permission.key,
            'description': self.permission.description,
            'additional_modifiers': self.additional_modifiers,
            '_links': {
                'self': url_for('api.auth.permissions.get_permission', perm_id_or_key=self.permission.id),
                'user': url_for('api.users.get_user', user_id=self.user_id),
            }
        }
        return data


class Discord(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    access_token = db.Column(db.String(64))
    refresh_token = db.Column(db.String(64))
    token_expiration = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='discord')

    def __repr__(self):
        return f'<Discord {self.user.username} | {self.discord_id}>'

    def to_dict(self, authenticated=False):
        data = {
            'user': self.user.username,
            'discord_id': self.discord_id,
            'token_expiration': self.token_expiration,
            '_links': {
                'self': url_for('api.users.discord.get_user_discord', user_id=self.user_id),
                'user': url_for('api.users.get_user', user_id=self.user_id)
            }
        }
        if authenticated:
            data['access_token'] = self.access_token
            data['refresh_token'] = self.refresh_token

        return data

    def from_dict(self, data):
        for field in ['discord_id', 'access_token', 'refresh_token']:
            if field in data:
                setattr(self, field, data[field])
        now = datetime.now(timezone.utc)
        self.token_expiration = now + timedelta(seconds=int(data['expires_in']))


class Twitch(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'), nullable=False)
    access_token = db.Column(db.String(64), nullable=False)
    refresh_token = db.Column(db.String(64), nullable=False)
    token_expiration = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='twitch')

    def __repr__(self):
        return f'<Twitch {self.user.username} | {self.twitch_id}>'

    def to_dict(self, authenticated=False):
        data = {
            'user': self.user.username,
            'twitch_id': self.twitch_id,
            'token_expiration': self.token_expiration,
            '_links': {
                'self': url_for('api.users.twitch.get_user_twitch', user_id=self.user_id),
                'user': url_for('api.users.get_user', user_id=self.user_id)
            }
        }
        if authenticated:
            data['access_token'] = self.access_token
            data['refresh_token'] = self.refresh_token

        return data

    def from_dict(self, data):
        for field in ['twitch_id', 'access_token', 'refresh_token']:
            if field in data:
                setattr(self, field, data[field])
        now = datetime.now(timezone.utc)
        self.token_expiration = now + timedelta(seconds=int(data['expires_in']))


class Player(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    slap_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    player_name = db.Column(db.String(64), nullable=False)
    rookie = db.Column(db.Boolean, nullable=False, default=True)
    first_season_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))
    next_name_change = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='player')
    first_season = db.relationship('SeasonDivision', back_populates='rookies')
    team_association = db.relationship('PlayerTeam', back_populates='player', lazy='dynamic')
    teams = association_proxy('team_association', 'team')
    season_association = db.relationship('FreeAgent', back_populates='player', lazy='dynamic')
    seasons = association_proxy('season_association', 'season_division')
    match_data_assoc = db.relationship('PlayerMatchData', back_populates='player')
    match_data = association_proxy('player_data_assoc', 'match')
    awards_association = db.relationship('PlayerAward', back_populates='player', lazy=True)
    awards = association_proxy('awards_association', 'award')

    def __repr__(self):
        return f'<Player {self.player_name} ({self.user.username if self.user else None})>'

    def to_dict(self):
        now = datetime.now(timezone.utc)
        current_team_q = self.team_association.filter(
            sa.and_(PlayerTeam.start_date < now, PlayerTeam.end_date.is_(None)))
        current_team = current_team_q.first()
        unique_teams = []
        for team in self.teams:
            if team.id not in unique_teams:
                unique_teams.append(team.id)
        data = {
            'id': self.id,
            'player_name': self.player_name,
            'user': self.user.username if self.user else None,
            'slap_id': self.slap_id,
            'rookie': self.rookie,
            'first_season': self.first_season.get_readable_name() if self.first_season else None,
            'next_name_change': self.next_name_change,
            'current_team': current_team.team.name if current_team else None,
            'teams': len(unique_teams),
            'free_agent_seasons': self.season_association.count(),
            'awards': len(self.awards_association),
            'stats': self.get_stats(),
            '_links': {
                'self': url_for('api.players.get_player', player_id=self.id),
                'user': url_for('api.users.get_user', user_id=self.user_id) if self.user else None,
                'first_season': url_for('api.season_division.get_season_division',
                                        season_division_id=self.first_season_id) if self.first_season else None,
                'current_team': url_for('api.teams.get_team', team_id=current_team.team.id) if current_team else None,
                'teams': url_for('api.players.get_player_teams', player_id=self.id),
                'free_agent_seasons': url_for('api.players.get_player_free_agent', player_id=self.id),
                'awards': url_for('api.players.get_player_awards', player_id=self.id)
            }
        }

        return data

    def to_simple_dict(self):
        now = datetime.now(timezone.utc)
        current_team_q = self.team_association.filter(
            sa.and_(PlayerTeam.start_date < now, PlayerTeam.end_date.is_(None)))
        current_team = current_team_q.first()
        data = {
            'player_name': self.player_name,
            'user': self.user.username if self.user else None,
            'slap_id': self.slap_id,
            'current_team': current_team.team.name if current_team else None,
            '_links': {
                'self': url_for('api.players.get_player', player_id=self.id),
                'user': url_for('api.users.get_user', user_id=self.user_id) if self.user else None,
                'current_team': url_for('api.teams.get_team', team_id=current_team.team.id) if current_team else None
            }
        }

        return data

    def from_dict(self, data):
        for field in ['player_name', 'slap_id', 'rookie', 'first_season_id', 'next_name_change']:
            if field in data:
                setattr(self, field, data[field])

    def current_team(self, season=None):
        now = datetime.now(timezone.utc)

        if season:
            start_filter = season.finals_end > PlayerTeam.start_date
            end_filter = sa.or_(
                season.start_date < PlayerTeam.end_date,
                PlayerTeam.end_date.is_(None)
            )

        else:
            start_filter = PlayerTeam.start_date < now
            end_filter = PlayerTeam.end_date.is_(None)

        current_team_q = self.team_association.filter(sa.and_(
            start_filter,
            end_filter
        ))
        return current_team_q.first()

    def get_stats(self, season_division=None, finals=None):
        player_data_query = db.session.query(PlayerMatchData) \
            .join(PlayerMatchData.match) \
            .join(MatchData.lobby) \
            .join(Lobby.match) \
            .filter(MatchData.accepted.is_(True)) \
            .filter(PlayerMatchData.player_id == self.id)

        start_date = None
        end_date = None
        if season_division:
            player_data_query = player_data_query.filter(
                Match.season_division_id == season_division.id)

            start_date, end_date = db.session.query(FreeAgent.start_date, FreeAgent.end_date) \
                .filter(sa.and_(
                    FreeAgent.season_division_id == season_division.id,
                    FreeAgent.player_id == self.id
                )).first()

        if finals:
            player_data_query = player_data_query.filter(Match.final_id.not_(None))
        else:
            player_data_query = player_data_query.filter(Match.final_id.is_(None))

        stat_totals = player_data_query.filter(PlayerMatchData.stat_total.is_(True))

        goals = 0
        shots = 0
        assists = 0
        saves = 0
        for record in stat_totals:
            goals += record.goals
            shots += record.shots
            assists += record.assists
            saves += record.saves

        return {
            'name': self.player_name,
            'id': self.id,
            'start_date': start_date,
            'end_date': end_date,
            'periods': player_data_query.count(),
            'goals': goals,
            'shots': shots,
            'assists': assists,
            'saves': saves
        }

    def join_team(self, team):
        player_team = PlayerTeam()
        player_team.player = self
        player_team.team = team
        player_team.start_date = datetime.now(timezone.utc)

        db.session.add(player_team)
        db.session.commit()

    def get_invites(self):
        invites = []
        for inv in self.invites:
            if inv.status == 'Pending':
                invites.append(inv.to_dict())
        return {
            'invites': invites
        }

    def accept_invite(self, invite):
        invite.accept()
        for inv in self.invites:
            if inv.status == 'Pending':
                inv.reject()


class SeasonDivisionTeam(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))

    team = db.relationship('Team', back_populates='season_division_assoc')
    season_division = db.relationship('SeasonDivision', back_populates='team_assoc')


class Team(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), index=True, unique=True, nullable=False)
    color = db.Column(db.String(7))
    logo = db.Column(db.String(128))
    founded_date = db.Column(db.DateTime)

    player_association = db.relationship('PlayerTeam', back_populates='team', lazy='dynamic')
    players = association_proxy('player_association', 'player')
    season_division_assoc = db.relationship('SeasonDivisionTeam', back_populates='team', lazy='dynamic')
    season_divisions = association_proxy('season_division_assoc', 'season_division')
    player_match_data = db.relationship('PlayerMatchData', back_populates='team')
    awards_association = db.relationship('TeamAward', back_populates='team', lazy='dynamic')
    awards = association_proxy('awards_association', 'award')
    match_availability = db.relationship('MatchAvailability', back_populates='team', lazy='dynamic')
    invites = db.relationship('TeamInvites', back_populates='team', lazy='dynamic')
    applications = db.relationship('SeasonRegistration', back_populates='team', lazy='dynamic')

    def __repr__(self):
        return f'<Team {self.name} ({self.acronym})>'

    def to_dict(self):
        now = datetime.now(timezone.utc)
        active_players = self.player_association.filter(
            sa.and_(PlayerTeam.start_date < now, PlayerTeam.end_date.is_(None)))
        data = {
            'id': self.id,
            'name': self.name,
            'acronym': self.acronym,
            'founded_date': self.founded_date,
            'color': self.color,
            'logo': True if self.logo else False,
            'active_players': active_players.count(),
            'seasons_played': self.season_division_assoc.count(),
            'awards': self.awards_association.count(),
            '_links': {
                'self': url_for('api.teams.get_team', team_id=self.id),
                'logo': self.logo,
                'active_players': url_for('api.teams.get_team_players', team_id=self.id, current=True),
                'seasons_played': url_for('api.teams.get_team_seasons', team_id=self.id),
                'awards': url_for('api.teams.get_team_awards', team_id=self.id)
            }
        }

        return data

    def to_simple_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'acronym': self.acronym,
            'color': self.color,
            '_links': {
                'self': url_for('api.teams.get_team', team_id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'acronym', 'color', 'logo', 'founded_date']:
            if field in data:
                setattr(self, field, data[field])

    def get_stats(self, season_division=None, finals=None, current=False):
        matches = db.session.query(Match).filter(
            sa.and_(
                sa.or_(
                    Match.home_team_id == self.id,
                    Match.away_team_id == self.id
                ),
                Match.results != None  # noqa
            )
        )
        players_query = self.player_association
        if season_division:
            player_data_query = season_division.get_player_data_query()

            matches = matches.filter(Match.season_division_id == season_division.id)

            if finals:
                players_query = players_query \
                    .filter(PlayerTeam.start_date < season_division.season.finals_end) \
                    .filter(sa.or_(
                        PlayerTeam.end_date > season_division.season.finals_start,
                        PlayerTeam.end_date.is_(None)
                    ))
            else:
                players_query = players_query \
                    .filter(PlayerTeam.start_date < season_division.season.end_date) \
                    .filter(sa.or_(
                        PlayerTeam.end_date > season_division.season.start_date,
                        PlayerTeam.end_date.is_(None)
                    ))
        else:
            player_data_query = db.session.query(PlayerMatchData) \
                .join(PlayerMatchData.match) \
                .join(MatchData.lobby) \
                .join(Lobby.match) \
                .filter(MatchData.accepted.is_(True))
            if current:
                now = datetime.now(timezone.utc)
                players_query = players_query \
                    .filter(PlayerTeam.start_date < now) \
                    .filter(
                        PlayerTeam.end_date.is_(None)
                    )

        player_data_query = player_data_query.filter(sa.or_(
            Match.home_team_id == self.id,
            Match.away_team_id == self.id
        ))
        if finals:
            player_data_query = player_data_query.filter(Match.final_id.not_(None))
        else:
            player_data_query = player_data_query.filter(Match.final_id.is_(None))
        self_player_data_query = player_data_query \
            .filter(PlayerMatchData.team_id == self.id)
        versus_player_data_query = player_data_query \
            .filter(PlayerMatchData.team_id != self.id)

        wins = matches.filter(Match.results.has(winner_id=self.id, overtime=False)).count()
        ot_wins = matches.filter(Match.results.has(winner_id=self.id, overtime=True)).count()
        losses = matches.filter(Match.results.has(loser_id=self.id, overtime=False)).count()
        ot_losses = matches.filter(Match.results.has(loser_id=self.id, overtime=True)).count()
        goals_for = 0
        for record in self_player_data_query.filter(PlayerMatchData.stat_total.is_(True)):
            goals_for += record.goals
        goals_against = 0
        for record in versus_player_data_query.filter(PlayerMatchData.stat_total.is_(True)):
            goals_against += record.goals

        players = []
        for player_assoc in players_query:
            added = any(player_dict['id'] == player_assoc.player.id for player_dict in players)
            if not added:
                periods = self_player_data_query \
                    .filter(PlayerMatchData.player_id == player_assoc.player.id)

                stat_totals = periods.filter(PlayerMatchData.stat_total.is_(True))

                goals = 0
                shots = 0
                assists = 0
                saves = 0
                for record in stat_totals:
                    goals += record.goals
                    shots += record.shots
                    assists += record.assists
                    saves += record.saves

                player = {
                    'name': player_assoc.player.player_name,
                    'id': player_assoc.player_id,
                    'start_date': player_assoc.start_date,
                    'end_date': player_assoc.end_date,
                    'periods': periods.count(),
                    'goals': goals,
                    'shots': shots,
                    'assists': assists,
                    'saves': saves
                }
                players.append(player)

        return {
            'name': self.name,
            'id': self.id,
            'color': self.color,
            'acronym': self.acronym,
            'logo': self.logo,
            'founded': self.founded_date,
            'matches': matches.count(),
            'wins': wins,
            'ot_wins': ot_wins,
            'losses': losses,
            'ot_losses': ot_losses,
            'points': (wins * 3) + (ot_wins * 2) + ot_losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'players': players
        }

    def get_upcoming_matches(self):
        query = db.session.query(Match).filter(
            sa.or_(
                Match.home_team_id == self.id,
                Match.away_team_id == self.id
            )
        ).filter(
            Match.results == None  # noqa
        )
        return [match.to_dict() for match in query]

    def get_completed_matches(self, limit=10):
        query = db.session.query(Match).filter(
            sa.or_(
                Match.home_team_id == self.id,
                Match.away_team_id == self.id
            )
        ).filter(
            Match.results != None  # noqa
        ).join(
            Match.results
        ).order_by(
            sa.desc(MatchResult.completed_date)
        ).limit(limit)
        return [match.to_dict() for match in query]

    def get_manager_details(self):
        players = [{
            'id': pa.player.id,
            'user_id': pa.player.user_id,
            'name': pa.player.player_name,
            'manager': pa.player.user.has_permission('team_manager') if pa.player.user else False
        } for pa in self.player_association.filter(PlayerTeam.end_date.is_(None))]

        owner = db.session.query(User) \
            .join(User.permission_assoc) \
            .join(UserPermissions.permission) \
            .filter(Permission.key == 'team_owner') \
            .filter(UserPermissions.additional_modifiers.contains(str(self.id))) \
            .first()

        seasons = db.session.query(Season).filter(Season.can_register)

        invites = self.invites.filter_by(status='Pending')
        applications = self.applications.filter(SeasonRegistration.status != 'Withdrawn').order_by(sa.desc(SeasonRegistration.id))

        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'logo': self.logo,
            'acronym': self.acronym,
            'founded': self.founded_date,
            'owner': owner.username if owner else None,
            'players': players,
            'invites': [inv.to_dict() for inv in invites],
            'applications': [app.to_dict() for app in applications],
            'open_seasons': [season.to_dict() for season in seasons],
            'upcoming_matches': self.get_upcoming_matches(),
            'recent_matches': self.get_completed_matches(limit=10)
        }

    def invite_player(self, invited_player, inviting_player):
        invite = TeamInvites()
        invite.from_dict({
            'team': self,
            'invited_player': invited_player,
            'inviting_player': inviting_player
        })
        db.session.add(invite)
        db.session.commit()

    def apply_to_season(self, season):
        application = SeasonRegistration()
        application.from_dict({
            'team_id': self.id,
            'season_id': season.id
        })
        db.session.add(application)
        db.session.commit()


# this is a helper table for recording which players were a part of which team and when (aka 'roster')
class PlayerTeam(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    player = db.relationship('Player', back_populates='team_association')
    team = db.relationship('Team', back_populates='player_association')

    def __repr__(self):
        return f'<PlayerTeam {self.player.player_name} | {self.team.name}>'

    def player_to_dict(self):
        data = {
            'id': self.player.id,
            'name': self.player.player_name,
            'dates': [
                {
                    'start': self.start_date,
                    'end': self.end_date
                }
            ],
            '_links': {
                'self': url_for('api.players.get_player', player_id=self.player.id)
            }
        }
        return data

    def team_to_dict(self):
        team_owner = db.session.query(UserPermissions).filter(
            sa.and_(
                UserPermissions.permission.has(key='team_owner'),
                UserPermissions.additional_modifiers == str(self.team.id)
            )
        ).first()
        team_managers_q = db.session.query(UserPermissions).filter(
            sa.and_(
                UserPermissions.permission.has(key='team_manager'),
                UserPermissions.additional_modifiers == str(self.team.id)
            )
        )
        team_managers = [tm.user.username for tm in team_managers_q]
        data = {
            'id': self.team.id,
            'name': self.team.name,
            'acronym': self.team.acronym,
            'color': self.team.color,
            'owner': team_owner.user.username if team_owner else None,
            'managers': team_managers,
            'dates': [
                {
                    'start': self.start_date,
                    'end': self.end_date
                }
            ],
            '_links': {
                'self': url_for('api.teams.get_team', team_id=self.team.id)
            }
        }
        return data

    @staticmethod
    def get_players_dict(team_id, current=False):
        team = db.session.get(Team, team_id)
        players = []
        if current:
            for player_assoc in team.player_association:
                now = datetime.now(timezone.utc)
                if player_assoc.start_date.replace(tzinfo=timezone.utc) < now and (
                        player_assoc.end_date is None or player_assoc.end_date.replace(tzinfo=timezone.utc) > now):
                    players.append(player_assoc.player_to_dict())

        else:
            for player_assoc in team.player_association:
                index = next((i for i, player, in enumerate(players) if player['id'] == player_assoc.player.id), None)
                if index:
                    dates = {
                        'start': player_assoc.start_date,
                        'end': player_assoc.end_date
                    }

                    players[index]['dates'].append(dates)
                else:
                    players.append(player_assoc.player_to_dict())

        response = {
            'team': team.name,
            'acronym': team.acronym,
            'color': team.color,
            'players': players,
            '_links': {
                'self': url_for('api.teams.get_team_players', team_id=team.id, current=current),
                'team': url_for('api.teams.get_team', team_id=team.id)
            }
        }
        return response

    @staticmethod
    def get_teams_dict(player_id, current=False):
        player = db.session.get(Player, player_id)
        if current:
            response = None
            for team_assoc in player.team_association:
                now = datetime.now(timezone.utc)
                if team_assoc.start_date.replace(tzinfo=timezone.utc) < now and (
                        team_assoc.end_date is None or team_assoc.end_date.replace(tzinfo=timezone.utc) > now):
                    response = {
                        'player': player.player_name,
                        'current_team': team_assoc.team_to_dict(),
                        '_links': {
                            'self': url_for('api.players.get_player_teams', player_id=player.id, current=True),
                            'player': url_for('api.players.get_player', player_id=player.id)
                        }
                    }
                    break
            return response

        else:
            teams = {}
            for team_assoc in player.team_association:
                if team_assoc.team.id not in teams:
                    teams[team_assoc.team.id] = team_assoc.team_to_dict()
                else:
                    dates = {
                        'start': team_assoc.start_date,
                        'end': team_assoc.end_date
                    }
                    teams[team_assoc.team.id]['dates'].append(dates)

            response = {
                'player': player.player_name,
                'teams': teams,
                '_links': {
                    'self': url_for('api.players.get_player_teams', player_id=player.id),
                    'player': url_for('api.players.get_player', player_id=player.id)
                }
            }
            return response


# this is a helper table for recording which players were free agents, for which seasons and when
class FreeAgent(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'))
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    player = db.relationship('Player', back_populates='season_association')
    season_division = db.relationship('SeasonDivision', back_populates='free_agent_association')

    def to_dict(self, parent):
        if parent == 'player':
            return self.season_division.to_simple_dict()
        elif parent == 'season_division':
            data = {
                'player': self.player.player_name,
                'start_date': self.start_date,
                'end_date': self.end_date,
                '_links': {
                    'player': url_for('api.players.get_player', player_id=self.player_id)
                }
            }
        else:
            raise ValueError("parent arg should be either 'player' or 'season_division'")
        return data

    def from_dict(self, data):
        valid_fields = ['start_date', 'end_date']
        for field in valid_fields:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def get_free_agent_seasons(player_id):
        player = db.session.get(Player, player_id)
        season_query = db.session.query(FreeAgent).filter_by(player_id=player_id).order_by(
            sa.desc(FreeAgent.season_division_id))

        if season_query.count() == 0:
            return None

        seasons = []
        for free_agent_record in season_query:
            seasons.append(free_agent_record.to_dict(parent='player'))

        response = {
            'player': player.player_name,
            'free_agent_seasons': seasons,
            '_links': {
                'self': url_for('api.players.get_player_free_agent', player_id=player.id),
                'player': url_for('api.players.get_player', player_id=player.id)
            }
        }
        return response

    @staticmethod
    def get_season_free_agents(season_division_id):
        # get season/division
        season_division = db.session.get(SeasonDivision, season_division_id)
        # query free agents
        player_query = db.session.query(FreeAgent).filter_by(season_division_id=season_division.id)
        # return none if no players
        if player_query.count() == 0:
            return None
        # get players
        players = []
        for free_agent_record in player_query:
            players.append(free_agent_record.to_dict(parent='season_division'))
        # build response
        response = {
            'id': season_division_id,
            'season': season_division.season.name,
            'division': season_division.division.name,
            'league': season_division.season.league.acronym,
            'free_agents': players,
            '_links': {
                'self': url_for('api.season_division.get_free_agents_in_season_division',
                                season_division_id=season_division.id),
                'season_division': url_for('api.season_division.get_season_division',
                                           season_division_id=season_division.id),
                'league': url_for('api.leagues.get_league', league_id_or_acronym=season_division.season.league.id)
            }
        }
        return response


"""
class PlayerTeamRegistrations(PlayerTeam):
    pass


class PlayerSeasonRegistrations(FreeAgent):
    pass"""


class League(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    acronym = db.Column(db.String(5), unique=True, nullable=False)
    server_region_value = db.Column(db.String(32), db.ForeignKey('league_manager.server_region.value'))

    seasons = db.relationship('Season', back_populates='league', lazy='dynamic')
    divisions = db.relationship('Division', back_populates='league', lazy='dynamic')
    server_region = db.relationship('ServerRegion', back_populates='leagues')

    def __repr__(self):
        return f'<League {self.name} | {self.acronym}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'acronym': self.acronym,
            'seasons_count': self.seasons.count(),
            'divisions_count': self.divisions.count(),
            '_links': {
                'self': url_for('api.leagues.get_league', league_id_or_acronym=self.id),
                'seasons': url_for('api.leagues.get_league_seasons', league_id_or_acronym=self.id),
                'divisions': url_for('api.leagues.get_league_divisions', league_id_or_acronym=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'acronym']:
            if field in data:
                setattr(self, field, data[field])
        self.acronym = self.acronym.upper()


class Season(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    acronym = db.Column(db.String(5), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league_manager.league.id'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    finals_start = db.Column(db.Date)
    finals_end = db.Column(db.Date)
    match_type_id = db.Column(db.Integer, db.ForeignKey('league_manager.matchtype.id'))
    can_register = db.Column(db.Boolean, default=False)

    league = db.relationship('League', back_populates='seasons')
    division_association = db.relationship('SeasonDivision', back_populates='season', lazy='dynamic')
    divisions = association_proxy('division_association', 'division')
    match_type = db.relationship('Matchtype', back_populates='seasons')

    def __repr__(self):
        return f'<Season {self.name} | {self.league.acronym}>'

    def get_divisions(self):
        divisions = []
        for division in self.divisions:
            season_division = db.session.query(SeasonDivision).filter_by(
                season_id=self.id,
                division_id=division.id
            ).first()
            data = {
                'name': division.name,
                'acronym': division.acronym,
                '_link': url_for('api.season_division.get_season_division', season_division_id=season_division.id)
            }
            divisions.append(data)
        return divisions

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'acronym': self.acronym,
            'league': self.league.acronym,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'finals_start': self.finals_start,
            'finals_end': self.finals_end,
            'match_type': self.match_type.name,
            'divisions': self.get_divisions(),
            'can_register': self.can_register,
            '_links': {
                'self': url_for('api.seasons.get_season', season_id=self.id),
                'league': url_for('api.leagues.get_league', league_id_or_acronym=self.league_id),
                'match_type': url_for('api.match.get_match_type', match_type_id=self.match_type_id),
                'divisions': url_for('api.seasons.get_divisions_in_season', season_id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'acronym', 'league_id', 'start_date', 'end_date', 'finals_start', 'finals_end',
                      'match_type_id', 'can_register']:
            if field in data:
                setattr(self, field, data[field])


class Division(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league_manager.league.id'), nullable=False)
    acronym = db.Column(db.String(5), nullable=False)
    description = db.Column(db.String(128))

    league = db.relationship('League', back_populates='divisions')
    season_association = db.relationship('SeasonDivision', back_populates='division', lazy='dynamic')
    seasons = association_proxy('season_association', 'season')

    def __repr__(self):
        return f'<Division {self.name} | {self.acronym} | {self.league.acronym}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'acronym': self.acronym,
            'league': self.league.acronym,
            'description': self.description,
            'seasons_count': self.season_association.count(),
            '_links': {
                'self': url_for('api.divisions.get_division', division_id=self.id),
                'league': url_for('api.leagues.get_league', league_id_or_acronym=self.league_id),
                'seasons': url_for('api.divisions.get_seasons_of_division', division_id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'acronym', 'league_id', 'description']:
            if field in data:
                setattr(self, field, data[field])


class SeasonDivision(PaginatedAPIMixin, db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('league_manager.season.id'))
    division_id = db.Column(db.Integer, db.ForeignKey('league_manager.division.id'))

    team_assoc = db.relationship('SeasonDivisionTeam', back_populates='season_division', lazy='dynamic')
    teams = association_proxy('team_assoc', 'team')
    free_agent_association = db.relationship('FreeAgent', back_populates='season_division')
    free_agents = association_proxy('free_agent_association', 'player')
    season = db.relationship('Season', back_populates='division_association')
    division = db.relationship('Division', back_populates='season_association')
    matches = db.relationship('Match', back_populates='season_division', lazy=True)
    finals = db.relationship('Final', back_populates='season_division', lazy=True)
    team_awards = db.relationship('TeamAward', back_populates='season_division')
    player_awards = db.relationship('PlayerAward', back_populates='season_division')
    rookies = db.relationship('Player', back_populates='first_season')

    def __repr__(self):
        return f'<SeasonDivision | {self.season.name} | Division: {self.division.name} | {self.season.league.acronym}>'

    def get_readable_name(self):
        return self.season.name + ' ' + self.division.name

    def get_acronym(self):
        return self.season.acronym + self.division.acronym

    def to_dict(self):
        data = {
            'id': self.id,
            'season': self.season.to_dict(),
            'division': self.division.to_dict(),
            'league': self.season.league.acronym,
            'teams_count': self.team_assoc.count(),
            'free_agents_count': len(self.free_agents),
            'rookies_count': len(self.rookies),
            'matches_count': len(self.matches),
            'finals_count': len(self.finals),
            '_links': {
                'self': url_for('api.season_division.get_season_division', season_division_id=self.id),
                'league': url_for('api.leagues.get_league', league_id_or_acronym=self.season.league_id),
                'season': url_for('api.seasons.get_season', season_id=self.season_id),
                'division': url_for('api.divisions.get_division', division_id=self.division_id),
                'teams': url_for('api.season_division.get_teams_in_season_division', season_division_id=self.id),
                'free_agents': url_for('api.season_division.get_free_agents_in_season_division',
                                       season_division_id=self.id),
                'rookies': url_for('api.season_division.get_rookies_in_season_division', season_division_id=self.id),
                'matches': url_for('api.season_division.get_matches_in_season_division', season_division_id=self.id),
                'finals': url_for('api.season_division.get_finals_in_season_division', season_division_id=self.id)
            }
        }
        return data

    def to_simple_dict(self):
        data = {
            'id': self.id,
            'season': self.season.name,
            'division': self.division.name,
            'league': self.season.league.acronym,
            '_links': {
                'self': url_for('api.season_division.get_season_division', season_division_id=self.id),
                'season': url_for('api.seasons.get_season', season_id=self.season.id),
                'division': url_for('api.divisions.get_division', division_id=self.division.id),
                'league': url_for('api.leagues.get_league', league_id_or_acronym=self.season.league.id)
            }
        }
        return data

    @staticmethod
    def get_teams_dict(season_division_id):
        season_division = db.session.get(SeasonDivision, season_division_id)
        teams = []

        for team in season_division.teams:
            team_data = team.to_simple_dict()

            if season_division.season.start_date and season_division.season.finals_end:
                season_start = datetime.combine(season_division.season.start_date, datetime.min.time()).replace(
                    tzinfo=timezone.utc)
                season_end = datetime.combine(season_division.season.finals_end, datetime.min.time()).replace(
                    tzinfo=timezone.utc)
                players = []
                for player_assoc in team.player_association:
                    player_start_date = player_assoc.start_date.replace(tzinfo=timezone.utc)
                    player_end_date = player_assoc.end_date.replace(
                        tzinfo=timezone.utc) if player_assoc.end_date is not None else None
                    if player_start_date < season_end and (player_end_date is None or player_end_date > season_start):
                        player = {
                            'id': player_assoc.player.id,
                            'name': player_assoc.player.player_name,
                            'start_date': player_assoc.start_date,
                            'end_date': player_assoc.end_date,
                            '_links': {
                                'self': url_for('api.players.get_player', player_id=player_assoc.player.id)
                            }
                        }
                        players.append(player)
                team_data['players'] = players
            teams.append(team_data)
        response = season_division.to_simple_dict()
        response['teams'] = teams
        links = {
            'self': url_for('api.season_division.get_teams_in_season_division', season_division_id=season_division.id),
            'season_division': url_for('api.season_division.get_season_division',
                                       season_division_id=season_division.id),
            'league': url_for('api.leagues.get_league', league_id_or_acronym=season_division.season.league.id)
        }
        response['_links'] = links
        return response

    @staticmethod
    def get_seasons_dict(team_id):
        team = db.session.get(Team, team_id)
        seasons = []
        for season in team.season_divisions:
            seasons.append(season.to_simple_dict())
        response = team.to_simple_dict()
        response['season_divisions'] = seasons
        links = {
            'self': url_for('api.teams.get_team_seasons', team_id=team.id),
            'team': url_for('api.teams.get_team', team_id=team.id)
        }
        response['_links'] = links
        return response

    def get_rookies_dict(self):
        rookies = []
        for rookie in self.rookies:
            rookies.append(rookie.to_simple_dict())

        response = self.to_simple_dict()
        response['rookies'] = rookies
        links = {
            'self': url_for('api.season_division.get_rookies_in_season_division', season_division_id=self.id),
            'season_division': url_for('api.season_division.get_season_division', season_division_id=self.id),
            'league': url_for('api.leagues.get_league', league_id_or_acronym=self.season.league.id)
        }
        response['_links'] = links
        return response

    def get_matches_dict(self, unplayed=False):
        matches = []
        for match in self.matches:
            if unplayed:
                if match.results is None:
                    matches.append(match.to_simple_dict())
            else:
                if match.results:
                    matches.append(match.to_simple_dict())

        response = self.to_simple_dict()
        response['matches'] = matches
        links = {
            'self': url_for('api.season_division.get_rookies_in_season_division', season_division_id=self.id),
            'season_division': url_for('api.season_division.get_season_division', season_division_id=self.id),
            'league': url_for('api.leagues.get_league', league_id_or_acronym=self.season.league.id)
        }
        response['_links'] = links
        return response

    def top_players(self, stat, secondary_stat, secondary_sort_reverse=False):
        query = db.session.query(
            PlayerMatchData.player_id,
            sa.func.sum(getattr(PlayerMatchData, stat)).label('goals'),
            sa.func.sum(getattr(PlayerMatchData, secondary_stat)).label('goals')
        ) \
            .filter(PlayerMatchData.stat_total.is_(True)) \
            .join(PlayerMatchData.match) \
            .join(MatchData.lobby) \
            .filter(Lobby.match.has(season_division_id=self.id)) \
            .group_by(PlayerMatchData.player_id) \
            .limit(10)

        data = []
        for row in query:
            player = db.session.get(Player, row[0])
            current_team = player.current_team(season=self.season)
            periods_played = self.get_player_data_query().filter(PlayerMatchData.player_id == player.id).count()
            player_data = {
                'id': player.id,
                'name': player.player_name,
                'team_id': current_team.team.id if current_team else None,
                'team': current_team.team.name if current_team else 'Free Agent',
                stat: int(row[1]),
                secondary_stat: int(row[2]),
                'periods': periods_played
            }
            data.append(player_data)
        if secondary_sort_reverse:
            sorted_data = sorted(data, key=lambda p: (p[stat], -p['periods'], -p[secondary_stat]), reverse=True)
        else:
            sorted_data = sorted(data, key=lambda p: (p[stat], -p['periods'], p[secondary_stat]), reverse=True)
        return sorted_data

    def leaderboard(self):
        team_data = []
        for team in self.teams:
            team_data.append(team.get_stats(season_division=self))

        sorted_teams = sorted(team_data, key=lambda t: (t['points'], (t['goals_for'] - t['goals_against']), t['goals_for']), reverse=True)

        free_agents = []
        for free_agent in self.free_agents:
            free_agents.append(free_agent.get_stats(season_division=self))

        return {
            'id': self.id,
            'season': self.season.to_dict(),
            'division': self.division.to_dict(),
            'teams': sorted_teams,
            'free_agents': free_agents,
            'most_goals': self.top_players('goals', 'shots', True),
            'most_assists': self.top_players('assists', 'primary_assists'),
            'most_saves': self.top_players('saves', 'blocks')
        }

    def get_match_data_query(self):
        return db.session.query(MatchData) \
            .join(MatchData.lobby) \
            .join(Lobby.match) \
            .join(Match.season_division) \
            .filter(SeasonDivision.id == self.id) \
            .filter(MatchData.accepted.is_(True))

    def get_player_data_query(self):
        return db.session.query(PlayerMatchData) \
            .join(PlayerMatchData.match) \
            .join(MatchData.lobby) \
            .join(Lobby.match) \
            .join(Match.season_division) \
            .filter(SeasonDivision.id == self.id) \
            .filter(MatchData.accepted.is_(True))


# info of a match between two registered league teams
class Match(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))
    home_team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    round = db.Column(db.Integer)
    match_week = db.Column(db.Integer)
    cancelled = db.Column(db.String(32))  # cancelled reason
    streamer_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    final_id = db.Column(db.Integer, db.ForeignKey('league_manager.final.id'))

    season_division = db.relationship('SeasonDivision', back_populates='matches')
    home_team = db.relationship('Team', backref='matches_home', foreign_keys=home_team_id)
    away_team = db.relationship('Team', backref='matches_away', foreign_keys=away_team_id)
    streamer = db.relationship('User', back_populates='streamed_matches')
    final = db.relationship('Final', back_populates='matches')
    results = db.relationship('MatchResult', back_populates='match', lazy=True, uselist=False)
    schedule = db.relationship('MatchSchedule', back_populates='match', uselist=False)
    team_availability = db.relationship('MatchAvailability', back_populates='match')
    lobbies = db.relationship('Lobby', back_populates='match', lazy='dynamic')
    match_reviews = db.relationship('MatchReview', back_populates='match', lazy='dynamic')

    def from_dict(self, data):
        for field in ['season_division_id', 'home_team_id', 'away_team_id', 'round', 'match_week']:
            if field in data:
                setattr(self, field, data[field])

    def current_lobby(self):
        current_lobby = self.lobbies.filter_by(active=True).first()
        return {'id': current_lobby.id, 'password': current_lobby.password} if current_lobby else None

    def to_dict(self):
        data = {
            'id': self.id,
            'season_division': self.season_division.to_dict(),
            'home_team': self.home_team.to_simple_dict(),
            'away_team': self.away_team.to_simple_dict(),
            'round': self.round,
            'match_week': self.match_week,
            'cancelled': self.cancelled,
            'streamer': self.streamer.twitch.to_dict() if self.streamer else None,
            'final': bool(self.final_id),
            'scheduled_time': self.schedule.scheduled_time,
            'current_lobby': self.current_lobby(),
            'results': self.results.to_dict() if self.results else None,
            'has_review': bool(self.match_reviews.filter_by(resolved=False).count()),
            '_links': {
                'self': url_for('api.match.get_match', match_id=self.id),
                'season_division': url_for('api.season_division.get_season_division',
                                           season_division_id=self.season_division_id),
                'home_team': url_for('api.teams.get_team', team_id=self.home_team_id),
                'away_team': url_for('api.teams.get_team', team_id=self.away_team_id),
                'streamer': url_for('api.users.twitch.get_user_twitch',
                                    user_id=self.streamer_id) if self.streamer else None
            }
        }
        return data

    def to_simple_dict(self):
        data = {
            'id': self.id,
            'home_team': self.home_team.to_dict(),
            'away_team': self.away_team.to_dict(),
            'result': self.results.get_result() if self.results else None,
            'round': self.round,
            'match_week': self.match_week,
            'final': bool(self.final_id),
            'scheduled_time': self.schedule.scheduled_time,
            'current_lobby': self.current_lobby(),
            '_links': {
                'self': url_for('api.match.get_match', match_id=self.id),
                'home_team': url_for('api.teams.get_team', team_id=self.home_team_id),
                'away_team': url_for('api.teams.get_team', team_id=self.away_team_id),
            }
        }
        return data


# result of a match between two registered league teams, one-to-one relationship with match
class MatchResult(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, db.ForeignKey('league_manager.match.id'), primary_key=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    draw = db.Column(db.Boolean, default=False)
    score_winner = db.Column(db.Integer, nullable=False, default=0)
    score_loser = db.Column(db.Integer, nullable=False, default=0)
    overtime = db.Column(db.Boolean, nullable=False, default=False)
    forfeit = db.Column(db.Boolean, nullable=False, default=False)
    vod = db.Column(db.String(128))
    completed_date = db.Column(db.DateTime)

    match = db.relationship('Match', back_populates='results', uselist=False)
    winner = db.relationship('Team', backref='matches_won', foreign_keys=winner_id)
    loser = db.relationship('Team', backref='matches_lost', foreign_keys=loser_id)

    def get_result(self):
        return f"{self.winner.name} {self.score_winner}-{self.score_loser} {self.loser.name}"

    def from_dict(self, data):
        for field in ['winner_id', 'loser_id', 'draw', 'score_winner', 'score_loser', 'overtime', 'forfeit', 'vod']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'winner': self.winner.name,
            'loser': self.loser.name,
            'draw': self.draw,
            'score_winner': self.score_winner,
            'score_loser': self.score_loser,
            'overtime': self.overtime,
            'forfeit': self.forfeit,
            'vod': self.vod,
            '_links': {
                'self': url_for('api.match.get_match', match_id=self.id)
            }
        }
        return data


# presets for creating lobbies using different match types
class Matchtype(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(128))
    periods = db.Column(db.Boolean, nullable=False, default=True)
    arena = db.Column(db.String(32), db.ForeignKey('league_manager.arena.value'), nullable=False)
    mercy_rule = db.Column(db.Integer, nullable=False, default=0)
    match_length = db.Column(db.Integer, nullable=False, default=300)
    game_mode = db.Column(db.String(32), db.ForeignKey('league_manager.game_mode.value'), nullable=False)
    num_players = db.Column(db.Integer, nullable=False, default=3)

    seasons = db.relationship('Season', back_populates='match_type', lazy=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'periods': self.periods,
            'arena': self.arena,
            'mercy_rule': self.mercy_rule,
            'match_length': self.match_length,
            'game_mode': self.game_mode,
            'num_players': self.num_players,
            '_links': {
                'self': url_for('api.match.get_match_type', match_type_id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'description', 'periods', 'arena', 'mercy_rule', 'match_length', 'game_mode',
                      'num_players']:
            if field in data:
                setattr(self, field, data[field])


# stores data on an in game lobby for use with Slapshot Public API
class Lobby(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('league_manager.match.id'))
    lobby_id = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    password = db.Column(db.String(64), nullable=False)
    task_id = db.Column(db.String(64))

    match = db.relationship('Match', back_populates='lobbies')
    match_data = db.relationship('MatchData', back_populates='lobby', lazy='dynamic')


# stores data on in game matches (periods of a match are separate entries)
class MatchData(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.Integer, db.ForeignKey('league_manager.lobby.id'))
    processed = db.Column(db.Boolean, nullable=False, default=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    match_id = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(16), nullable=False)
    gamemode = db.Column(db.String(16), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    arena = db.Column(db.String(16), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.String(10), nullable=False)
    current_period = db.Column(db.Integer, nullable=False)
    periods_enabled = db.Column(db.Boolean, nullable=False)
    custom_mercy_rule = db.Column(db.String(16), nullable=False)
    end_reason = db.Column(db.String(32), nullable=False)
    source = db.Column(db.String(10))  # e.g. slap api, user, import

    lobby = db.relationship('Lobby', back_populates='match_data')
    player_data_assoc = db.relationship('PlayerMatchData', back_populates='match', lazy='dynamic')
    player_data = association_proxy('player_data_assoc', 'player')

    def from_dict(self, data):
        for field in ['lobby_id', 'processed', 'match_id', 'region', 'gamemode', 'created', 'arena', 'home_score',
                      'away_score', 'winner', 'current_period', 'periods_enabled', 'custom_mercy_rule', 'end_reason',
                      'source', 'accepted']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'lobby_id': self.lobby_id,
            'processed': self.processed,
            'accepted': self.accepted,
            'match_id': self.match_id,
            'region': self.region,
            'gamemode': self.gamemode,
            'created': self.created,
            'arena': self.arena,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'winner': self.winner,
            'current_period': self.current_period,
            'periods_enabled': self.periods_enabled,
            'custom_mercy_rule': self.custom_mercy_rule,
            'end_reason': self.end_reason,
            'source': self.source
        }
        return data


# stores match data of particular players (periods of a match are separate entries)
class PlayerMatchData(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('league_manager.match_data.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
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
    possession_time_sec = db.Column(db.Integer, default=0)
    game_winning_goals = db.Column(db.Integer, default=0)
    overtime_goals = db.Column(db.Integer, default=0)
    post_hits = db.Column(db.Integer, default=0)
    faceoffs_won = db.Column(db.Integer, default=0)
    faceoffs_lost = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    current_period = db.Column(db.Integer, nullable=False)
    stat_total = db.Column(db.Boolean, nullable=False, default=False)

    match = db.relationship('MatchData', back_populates='player_data_assoc')
    player = db.relationship('Player', back_populates='match_data_assoc')
    team = db.relationship('Team', back_populates='player_match_data')

    def from_dict(self, data):
        for field in ['match_id', 'player_id', 'team_id', 'goals', 'shots', 'assists', 'saves', 'primary_assists',
                      'secondary_assists', 'passes', 'blocks', 'takeaways', 'turnovers', 'possession_time_sec',
                      'game_winning_goals', 'post_hits', 'faceoffs_won', 'faceoffs_lost', 'score', 'current_period']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.match_id,
            'player': self.player.player_name,
            'team': self.team.name,
            'goals': self.goals,
            'shots': self.shots,
            'assists': self.assists,
            'saves': self.saves,
            'primary_assists': self.primary_assists,
            'secondary_assists': self.secondary_assists,
            'passes': self.passes,
            'blocks': self.blocks,
            'takeaways': self.takeaways,
            'turnovers': self.turnovers,
            'possession_time_sec': self.possession_time_sec,
            'game_winning_goals': self.game_winning_goals,
            'post_hits': self.post_hits,
            'faceoffs_won': self.faceoffs_won,
            'faceoffs_lost': self.faceoffs_lost,
            'score': self.score,
            '_links': {
                'player': url_for('api.players.get_player', player_id=self.player_id),
                'team': url_for('api.teams.get_team', team_id=self.team_id)
            }
        }
        return data


class Final(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))
    best_of = db.Column(db.Integer, nullable=False, default=1)
    elimination = db.Column(db.Boolean, nullable=False, default=True)
    round = db.Column(db.String(20), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    completed = db.Column(db.Boolean, nullable=False, default=False)

    season_division = db.relationship('SeasonDivision', back_populates='finals')
    home_team = db.relationship('Team', backref='finals_home', foreign_keys=home_team_id)
    away_team = db.relationship('Team', backref='finals_away', foreign_keys=away_team_id)
    matches = db.relationship('Match', back_populates='final', lazy=True)
    results = db.relationship('FinalResults', back_populates='final', lazy=True, uselist=False)


class FinalResults(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    final_id = db.Column(db.Integer, db.ForeignKey('league_manager.final.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    home_team_score = db.Column(db.Integer, nullable=False, default=0)
    away_team_score = db.Column(db.Integer, nullable=False, default=0)

    final = db.relationship('Final', back_populates='results')
    winner = db.relationship('Team', backref='finals_won', foreign_keys=winner_id)
    loser = db.relationship('Team', backref='finals_lost', foreign_keys=loser_id)


class Award(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    description = db.Column(db.String(128), nullable=False)

    teams_association = db.relationship('TeamAward', back_populates='award', lazy=True)
    teams = association_proxy('teams_association', 'team')
    players_association = db.relationship('PlayerAward', back_populates='award', lazy=True)
    players = association_proxy('players_association', 'player')


class TeamAward(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    award_id = db.Column(db.Integer, db.ForeignKey('league_manager.award.id'))
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))

    team = db.relationship('Team', back_populates='awards_association')
    award = db.relationship('Award', back_populates='teams_association')
    season_division = db.relationship('SeasonDivision', back_populates='team_awards')


class PlayerAward(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'))
    award_id = db.Column(db.Integer, db.ForeignKey('league_manager.award.id'))
    season_division_id = db.Column(db.Integer, db.ForeignKey('league_manager.season_division.id'))

    player = db.relationship('Player', back_populates='awards_association')
    award = db.relationship('Award', back_populates='players_association')
    season_division = db.relationship('SeasonDivision', back_populates='player_awards')


class MatchSchedule(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('league_manager.match.id'))
    scheduled_time = db.Column(db.DateTime)
    home_team_accepted = db.Column(db.Boolean, default=False, nullable=False)
    away_team_accepted = db.Column(db.Boolean, default=False, nullable=False)

    match = db.relationship('Match', back_populates='schedule')


class MatchAvailability(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('league_manager.match.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)

    match = db.relationship('Match', back_populates='team_availability')
    team = db.relationship('Team', back_populates='match_availability')


class ServerRegion(db.Model, LeagueManagerTable):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))
    utc_offset = db.Column(db.String(7))

    leagues = db.relationship('League', back_populates='server_region')


class Arena(db.Model, LeagueManagerTable):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class EndReason(db.Model, LeagueManagerTable):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))


class GameMode(db.Model, LeagueManagerTable):
    value = db.Column(db.String(32), primary_key=True)
    label = db.Column(db.String(32), unique=True, nullable=False)
    info = db.Column(db.String(64))

    def to_dict(self):
        data = {
            'value': self.value,
            'label': self.label,
            'info': self.info
        }
        return data


class Event(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    module = db.Column(db.String(50), index=True)
    message = db.Column(db.String(200))


class MatchReview(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('league_manager.match.id'))
    type = db.Column(db.String(16), nullable=False)
    reason = db.Column(db.String(256), nullable=False)
    raised_by = db.Column(db.String(32))
    comments = db.Column(db.String(256))
    resolved = db.Column(db.Boolean, nullable=False, default=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('league_manager.user.id'))
    resolved_on = db.Column(db.Integer)

    reviewer = db.relationship('User', backref='match_review')
    match = db.relationship('Match', back_populates='match_reviews')

    def from_dict(self, data):
        for field in ['match_id', 'type', 'raised_by', 'reason', 'comments', 'resolved', 'resolved_by', 'resolved_on']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'type': self.type,
            'reason': self.reason,
            'raised_by': self.raised_by,
            'comments': self.comments,
            'resolved': self.resolved,
            'resolved_by': self.resolved_by,
            'resolved_on': self.resolved_on
        }
        return data


class SeasonRegistration(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'))
    season_id = db.Column(db.Integer, db.ForeignKey('league_manager.season.id'), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('league_manager.division.id'))
    status = db.Column(db.String(16), default='Pending', nullable=False)
    type = db.Column(db.String(10), nullable=False)

    team = db.relationship('Team', back_populates='applications')
    player = db.relationship('Player', backref='applications')
    season = db.relationship('Season', backref='applications')
    division = db.relationship('Division', backref='applications')

    def to_dict(self):
        return {
            'id': self.id,
            'team': self.team.to_dict() if self.team else None,
            'player': self.player.to_dict() if self.player else None,
            'season': self.season.to_dict(),
            'division': self.division.to_dict() if self.division else None,
            'status': self.status,
            'type': self.type
        }

    def from_dict(self, data):
        fields = ['player_id', 'team_id', 'season_id', 'division_id']
        for field in fields:
            if field in data:
                setattr(self, field, data[field])
                if field == 'team_id':
                    self.type = 'team'
                elif field == 'player_id':
                    self.type = 'player'

    def accept(self):
        self.status = 'Accepted'
        db.session.commit()

    def reject(self):
        self.status = 'Rejected'
        db.session.commit()

    def withdraw(self):
        self.status = 'Withdrawn'
        db.session.commit()

    def allocate_to_division(self, division):
        self.division = division
        sd = db.session.query(SeasonDivision)\
            .filter_by(
                season_id=self.season_id,
                division_id=self.division_id)\
            .first()
        if self.team:
            self.team.season_divisions.append(sd)
        elif self.player:
            now = datetime.now(timezone.utc)
            free_agent = FreeAgent()
            free_agent.player = self.player
            free_agent.season_division = sd
            free_agent.start_date = now
            db.session.add(free_agent)
        self.status = 'Completed'
        db.session.commit()


class TeamInvites(db.Model, LeagueManagerTable):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('league_manager.team.id'), nullable=False)
    invited_player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'), nullable=False)
    inviting_player_id = db.Column(db.Integer, db.ForeignKey('league_manager.player.id'), nullable=False)
    status = db.Column(db.String(16), default='Pending', nullable=False)

    team = db.relationship('Team', back_populates='invites')
    invited_player = db.relationship('Player', backref='invites', foreign_keys=invited_player_id)
    inviting_player = db.relationship('Player', foreign_keys=inviting_player_id)

    def to_dict(self):
        return {
            'id': self.id,
            'team': self.team.to_dict(),
            'invited_player': self.invited_player.to_dict(),
            'inviting_player': self.inviting_player.to_dict(),
            'status': self.status
        }

    def from_dict(self, data):
        fields = ['team', 'invited_player', 'inviting_player']
        for field in fields:
            if field in data:
                setattr(self, field, data[field])

    def accept(self):
        self.status = 'Accepted'
        player_team = PlayerTeam()
        player_team.player = self.invited_player
        player_team.team = self.team
        player_team.start_date = datetime.now(timezone.utc)

        db.session.add(player_team)
        db.session.commit()

    def reject(self):
        self.status = 'Rejected'
        db.session.commit()

    def withdraw(self):
        self.status = 'Withdrawn'
        db.session.commit()


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
