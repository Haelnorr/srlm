from celery.contrib.abortable import AbortableAsyncResult
from celery.result import AsyncResult


def task_result(task_id):
    result = AsyncResult(task_id)
    return {
        'ready': result.ready(),
        'successful': result.successful(),
        'value': result.result if result.ready() else None
    }


def cancel_task(task_id):
    task = AbortableAsyncResult(task_id)
    task.abort()

