from django.core import management

from pokebattle.celery import app as celery_app


@celery_app.task
def clearsessions():
    management.call_command('clearsessions')
