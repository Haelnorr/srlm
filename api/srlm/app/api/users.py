import sqlalchemy as sa
from flask import request, url_for, abort
from api.srlm.app import db
from api.srlm.app.api import bp
from api.srlm.app.models import User
from api.srlm.app.api.errors import bad_request
from api.srlm.app.api.auth import user_auth, req_app_token
from api.srlm.app.auth.functions import check_username_exists, check_email_exists, get_bearer_token
from api.srlm.app.auth.email import send_password_reset_email

# create a new logger for this module
from api.srlm.logger import get_logger
log = get_logger(__name__)


@bp.route('/users/<int:user_id>', methods=['GET'])
@req_app_token
def get_user(user_id):
    user_token = get_bearer_token(request.headers)['user']
    user = User.check_token(user_token)
    print(user_token)
    print(user_id)

    include_email = False

    if user and user.id == user_id:
        include_email = True

    return User.query.get_or_404(user_id).to_dict(include_email=include_email)


@bp.route('/users', methods=['GET'])
@req_app_token
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(sa.select(User), page, per_page, 'api.get_users')


@bp.route('/users', methods=['POST'])
@req_app_token
def add_user():
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if check_username_exists(data['username']):
        return bad_request('please select a different username')
    if check_email_exists(data['email']):
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201, {'Location': url_for('api.get_user', user_id=user.id)}


@bp.route('/users/<int:user_id>', methods=['PUT'])
@req_app_token
@user_auth.login_required
def update_user(user_id):
    if user_auth.current_user().id != user_id:
        abort(403)
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and check_username_exists(data['username']):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and check_email_exists(data['email']):
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()


@bp.route('/users/<int:user_id>/new_password', methods=['POST'])
@req_app_token
@user_auth.login_required
def update_user_password(user_id):
    if user_auth.current_user().id != user_id:
        abort(403)
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'password' not in data:
        return bad_request('new password not supplied')

    user.set_password(data['password'])
    user.reset_pass = False
    user.revoke_token()
    token = user.get_token()
    db.session.commit()

    response = {
        'token': token,
        'expires': user.token_expiration
    }
    return response


@bp.route('/users/<int:user_id>/matches_streamed', methods=['GET'])
@req_app_token
def get_user_matches_streamed(user_id):
    pass


@bp.route('/users/<int:user_id>/matches_reviewed', methods=['GET'])
@req_app_token
def get_user_matches_reviewed(user_id):
    pass


@bp.route('/users/<int:user_id>/permissions', methods=['GET'])
@req_app_token
def get_user_permissions(user_id):
    pass


@bp.route('/users/<int:user_id>/discord', methods=['GET'])
@req_app_token
def get_user_discord(user_id):
    pass


@bp.route('/users/forgot_password', methods=['POST'])
@req_app_token
def request_password_reset():
    data = request.get_json()
    user = None
    if 'username' in data and check_username_exists(data['username']):
        user = db.session.query(User).filter(User.username == data['username']).first()
    elif 'email' in data and check_email_exists(data['email']):
        user = db.session.query(User).filter(User.email == data['email']).first()

    if user is not None:
        send_password_reset_email(user)
        return {
            'result': 'success',
            'user': user.id,
            '_links': {
                'user': url_for('api.get_user', user_id=user.id)
            }
        }
    else:
        return bad_request('failed to reset user - most likely username or email provided did not match')


@bp.route('/users/forgot_password/<reset_token>', methods=['GET'])
@req_app_token
def get_temp_token(reset_token):
    user = User.verify_reset_password_token(reset_token)
    if not user:
        return bad_request('Token is invalid or expired. Try again or contact an administrator')

    user.revoke_token()
    token = user.get_token(expires_in=300)
    user.reset_pass = True
    db.session.commit()
    return {'token': token, 'expires': user.token_expiration}
