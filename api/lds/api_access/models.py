from api.lds.app import db
from datetime import datetime, timezone, timedelta
import secrets


class AuthorizedApp(db.Model):
    __bind_key__ = 'api_access'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    token = db.Column(db.String(34), index=True, unique=True)
    token_expiration = db.Column(db.DateTime, nullable=False)

    def get_new_token(self, expires_in=2592000):
        now = datetime.now(timezone.utc)
        self.token = secrets.token_hex(17)
        self.token_expiration = now + timedelta(seconds=min(expires_in, 2592000))
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        authorized_app = db.session.query(AuthorizedApp).filter(AuthorizedApp.token == token).first()
        if authorized_app is None or authorized_app.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return authorized_app
