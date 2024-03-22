from flask import render_template, make_response
from flask_login import login_required, current_user
from lds.app import db
from lds.app.errors import bp
from lds.app.auth.functions import get_permissions


@bp.app_errorhandler(403)
@login_required
def forbidden(error):
    permissions = get_permissions(current_user.id)
    return make_response(render_template('errors/403.html', page='403', permissions=permissions), 403)


@bp.app_errorhandler(404)
@login_required
def not_found_error(error):
    permissions = get_permissions(current_user.id)
    return make_response(render_template('errors/404.html', page='404', permissions=permissions), 404)


@bp.app_errorhandler(500)
@login_required
def internal_error(error):
    permissions = get_permissions(current_user.id)
    db.session.rollback()
    return make_response(render_template('errors/500.html', page='500', permissions=permissions), 500)
