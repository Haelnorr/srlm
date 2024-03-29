from flask import request, url_for
from api.srlm.api_access.models import AuthorizedApp
from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.api.auth import basic_auth, req_app_token, user_auth
from api.srlm.app.api.responses import request_success
from api.srlm.app.auth.functions import get_bearer_token
from api.srlm.app.models import User


@bp.route('/tokens/user', methods=['POST'])
@basic_auth.login_required
def get_user_token():
    token = basic_auth.current_user().get_token()
    expires = basic_auth.current_user().token_expiration
    db.session.commit()
    return {'token': token, 'expires': expires}


@bp.route('/tokens/user', methods=['DELETE'])
@req_app_token
@user_auth.login_required
def revoke_user_token():
    user_auth.current_user().revoke_token()
    db.session.commit()
    return request_success('User token revoked')


@bp.route('/tokens/user/validate', methods=['POST'])
@req_app_token
@user_auth.login_required
def validate_user_token():
    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)

    response = {
        'user': user.id,
        'expires': user.token_expiration,
        '_links': {
            'user': url_for('api.get_user', user_id=user.id)
        }
    }
    return response


@bp.route('/tokens/app', methods=['POST'])
@req_app_token
def request_new_app_token():
    app_token = get_bearer_token(request.headers)['app']

    authorized_app = AuthorizedApp.check_token(app_token)
    token = authorized_app.get_new_token()
    db.session.commit()
    response = {
        'token': token,
        'expiry': authorized_app.token_expiration
    }
    return response


@bp.route('/tokens/app', methods=['GET'])
@req_app_token
def get_app_token():
    app_token = get_bearer_token(request.headers)['app']

    authorized_app = AuthorizedApp.check_token(app_token)
    response = {
        'token': authorized_app.token,
        'expiry': authorized_app.token_expiration
    }
    return response
