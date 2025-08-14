from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msg_service.settings')

app = Celery('msg_service', broker=f'amqp://{settings.RMQ_USER}:{settings.RMQ_PASSWORD}@{settings.RMQ_HOST}:{settings.RMQ_PORT}/%2F')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()