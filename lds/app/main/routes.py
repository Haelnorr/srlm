from flask import redirect, render_template, make_response, abort, current_app, url_for
from flask_login import login_required, current_user
from sqlalchemy import delete
from lds.app import db
from lds.app.models import Event
from lds.app.main import bp
from lds.logger import get_logger
from lds.app.auth.forms import ClearLogs
from lds.app.auth.functions import get_permissions
from lds.app.events import get_events
from lds.definitions import app_name


log = get_logger(__name__)


@bp.route('/index')
@bp.route('/dashboard')
def dash_redirect():
    log.debug('Redirecting to Dashboard')
    return redirect('/')


@bp.route('/')
@login_required
def dashboard():
    permissions = get_permissions(current_user.id)
    resp = make_response(render_template('dashboard.html', app_name=app_name, page='Dashboard', permissions=permissions))
    return resp


@login_required
@bp.route('/app_logs', methods=['GET', 'POST'])
def app_logs():
    form = None
    if current_app.debug:
        form = ClearLogs()

    if form is not None and form.validate_on_submit():
        db.session.execute(delete(Event).execution_options(synchronize_session='fetch'))
        db.session.commit()
        return redirect(url_for('main.app_logs'))

    events = get_events()
    permissions = get_permissions(current_user.id)
    if not permissions['admin']:
        abort(403)
    return make_response(render_template('app_logs.html', app_name=app_name, page='App Logs', permissions=permissions, events=events, form=form))
