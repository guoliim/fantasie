from __future__ import absolute_import

import functools
import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.cache import cache

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasie.settings')
app = Celery('fantasie')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

logger = get_task_logger(__name__)


def single_instance_task(timeout):
    def task_exc(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_id = "celery-single-instance-" + func.__name__

            def acquire_lock():
                return cache.add(lock_id, "true", timeout)

            def release_lock():
                return cache.delete(lock_id)
            if acquire_lock():
                try:
                    func(*args, **kwargs)
                finally:
                    release_lock()
        return wrapper
    return task_exc
