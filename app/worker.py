# app/celery_py

from celery import Celery
from settings import get_settings

celery_app = Celery(
    __name__,
    broker=get_settings().CELERY_BROKER_URL,
    backend=get_settings().CELERY_RESULT_BACKEND,
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
celery_app.autodiscover_tasks(['tasks.handle_document','tasks.apply_chunking' ], force=True)
