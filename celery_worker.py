from app import celery

# Start Celery worker
if __name__ == '__main__':
    celery.worker_main()
