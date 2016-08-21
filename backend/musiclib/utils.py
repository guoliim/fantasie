import os
import subprocess

from django.conf import settings

from fantasie.celery import app, single_instance_task, logger
from .models import MusicLibrary


@app.task
@single_instance_task(60*10)
def convert_aac(filepath, rawhash):
    # 由于Celery使用Redis,所有参数必须能够序列化存储,因而只能将rawhash作为参数而不是meta
    meta = MusicLibrary.objects.filter(rawhash=rawhash).first()
    directory = settings.CACHE_ROOT
    if not os.path.exists(directory):
        os.makedirs(directory)
    temp_filepath = os.path.join(directory, meta.rawhash + '.m4a')
    if not os.path.exists(temp_filepath) and not meta.cache:
        if settings.PLATFORM == 'darwin':
            retcode = subprocess.call(["ffmpeg", "-i", filepath, "-map", "0:0", "-b:a", "256k", temp_filepath])
        else:
            retcode = subprocess.call(["ffmpeg", "-i", filepath, "-map", "0:0", "-strict", "-2", "-b:a", "256k", temp_filepath])
        if retcode == 0:
            meta.cache = True
            meta.save()
            logger.debug("Convert Successful.")
        else:
            logger.debug("Convert Failed.")


def is_ua_safari(request):
    try:
        return False if "chrome" in request.META["HTTP_USER_AGENT"].lower() else True
    except AttributeError:
        return True
