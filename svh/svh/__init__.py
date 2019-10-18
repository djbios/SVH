from __future__ import absolute_import, unicode_literals
from svh.celery import app as celery_app
from svh.rabbit.rabbit import rabbit_consumer

__all__ = ('celery_app', 'rabbit_consumer')
