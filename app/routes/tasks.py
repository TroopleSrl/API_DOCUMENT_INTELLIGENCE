from fastapi import APIRouter
from celery.result import AsyncResult
from app.celery_app import celery_app

router = APIRouter()

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        # Task is waiting for execution
        response = {
            'task_id': task_id,
            'status': task_result.state,
            'result': None
        }
    elif task_result.state != 'FAILURE':
        # Task is either executed or being executed
        response = {
            'task_id': task_id,
            'status': task_result.state,
            'result': task_result.result  # Can be None if not completed
        }
    else:
        # Something went wrong in the background job
        response = {
            'task_id': task_id,
            'status': task_result.state,
            'result': str(task_result.result),  # Exception details
        }
    return response
