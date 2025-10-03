from celery import Celery 

broker_url = "redis://localhost:6379/0"
backend_url = "redis://localhost:6379/1"

app = Celery('app', 
             broker=broker_url,  
             backend=backend_url) 

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    include=['app.tasks'],
    worker_pool='solo'  
)