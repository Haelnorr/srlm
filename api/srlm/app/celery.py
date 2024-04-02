from celery import current_app as current_celery_app


def make_celery(app):
    celery = current_celery_app
    celery.conf.update(app.config["CELERY"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
