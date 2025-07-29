from celery import Celery, Task


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, include=["app.tasks"])
    celery_app.config_from_object(app.config, namespace="CELERY")
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
