from celery import Celery 

broker_url="redis://localhost:6379/0"
backend_url="redis://localhost:6379/1"

app = Celery('tasks', broker_url, backend_url)

app.conf.timezone = 'UTC'

app.conf.result_serializer = 'json'