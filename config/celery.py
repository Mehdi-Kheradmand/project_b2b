import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')  # project name (my project name is config)
app.config_from_object('django.conf:settings', namespace='CELERY')

# # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='task.#'),
    Queue('high_priority', Exchange('high_priority'), routing_key='high.#'),
    Queue('low_priority', Exchange('low_priority'), routing_key='low.#'),
    Queue('koon', Exchange('koon'), routing_key='koon.#'),
)
