from celery_app import celery
import time

@celery.task
def long_running_task(x, y):
    time.sleep(10)   
    return x + y
