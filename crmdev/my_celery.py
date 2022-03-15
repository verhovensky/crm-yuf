from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crmdev.settings')

app = Celery('crmdev')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Moscow')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.task_routes = {
    'order.tasks.expire_order': {'queue': 'order'}
}