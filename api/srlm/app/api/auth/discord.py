from apifairy import body, authenticate, response, other_responses
from flask import Blueprint

from api.srlm.app import db
from api.srlm.app.api.auth import auth_bp
from api.srlm.app.api.auth.utils import app_auth, get_discord_info
from api.srlm.app.api.utils.errors import UserAuthError
from api.srlm.app.api.utils.functions import ensure_exists
from api.srlm.app.fairy.errors import unauthorized
from api.srlm.app.fairy.schemas import DiscordAuthSchema, TokenSchema
from api.srlm.app.models import User, Discord

discord = Blueprint('discord', __name__)
auth_bp.register_blueprint(discord, url_prefix='/discord')


@discord.route('', methods=['POST'])
@body(DiscordAuthSchema())
@response(TokenSchema())
@authenticate(app_auth)
@other_responses(unauthorized)
def auth_by_discord(data):
    """Authenticates a user by their discord access token.
    If no user exists matching the discord account provided, a new user will be created."""
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    token_expiration = data.get('token_expiration', None)

    discord_request = get_discord_info(access_token)

    if discord_request.status_code == 200:
        data = discord_request.json()
        discord_db = ensure_exists(Discord, return_none=True, discord_id=data['id'])
        if not discord_db:
            discord_db = Discord()
            discord_db.access_token = access_token
            discord_db.refresh_token = refresh_token
            discord_db.token_expiration = token_expiration
            discord_db.discord_id = data['id']

            user = User()
            user.username = data['global_name']
            user.discord = discord_db
            user.get_token()
            db.session.add(user)
            db.session.add(discord_db)
            db.session.commit()
    else:
        raise UserAuthError()

    response_json = {
        'token': discord_db.user.token,
        'expires': discord_db.user.token_expiration
    }

    return response_json

