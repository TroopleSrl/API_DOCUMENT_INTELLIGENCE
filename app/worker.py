# app/celery_py

from celery import Celery
from os import getenv

celery_app = Celery(
    __name__,
    broker=getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
)
celery_conf = celery_app.conf

celery_conf.update(
    # task_serializer='pickle',
    # result_serializer='pickle',
    # accept_content=['pickle'],
    timezone='UTC',
    enable_utc=True,
)

# Autodiscover tasks in specified modules
celery_app.autodiscover_tasks(['tasks.handle_document'], force=True)
