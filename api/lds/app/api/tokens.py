from api.lds.app import db
from api.lds.app.api import bp
from api.lds.app.api.auth import basic_auth, req_app_token


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required()
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}


def revoke_token():
    pass
