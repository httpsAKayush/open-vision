from celery import Celery

app = Celery('open_vision')
app.conf.task_always_eager = True
