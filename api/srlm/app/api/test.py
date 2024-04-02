from flask import request, url_for

from api.srlm.app.api import bp
from api.srlm.app.spapi.lobby_manager import task_result, create_lobby, cancel_task


@bp.route('/start_task/<interval>')
def start_task(interval):

    task_id = create_lobby(1, interval)
    task_link = url_for('api.get_task', task_id=task_id)

    cancel_link = url_for('api.abort_task', task_id=task_id)

    response = f'<a href="{task_link}">Result</a> | <a href="{cancel_link}">Cancel</a>'

    return response


@bp.route('/get_task/<task_id>')
def get_task(task_id):
    return task_result(task_id)


@bp.route('/abort_task/<task_id>')
def abort_task(task_id):
    cancel_task(task_id)
    return f'Cancelled task {task_id} - <a href="{url_for("api.start_task", interval=80)}">start new task</a>: '
