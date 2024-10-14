# app/celery_app.py

from celery import Celery

celery_app = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

celery_app.conf.update(
    task_serializer='pickle',
    result_serializer='pickle',
    accept_content=['pickle'],
    timezone='UTC',
    enable_utc=True,
)

# Autodiscover tasks in specified modules
celery_app.autodiscover_tasks(['app.connectors'], force=True)
