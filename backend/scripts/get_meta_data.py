import datetime
import hashlib
import os
import sys
import time

import django
import pydub
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4Cover

# Setup Django Project
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 可以自己用绝对路径定义,目的是工程目录下
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasie.settings")
django.setup()

from django.conf import settings
from musiclib.models import MusicLibrary


def get_mp4_metadata(filepath, covers_root):
    meta_raw = MP4(filepath)
    data_bin = pydub.AudioSegment.from_file(filepath)
    meta = {
        'rawhash': hashlib.md5(data_bin.raw_data).hexdigest(),
        'title': meta_raw.get('\xa9nam'),
        'album': meta_raw.get('\xa9alb'),
        'artist': meta_raw.get('\xa9ART'),
        'year': meta_raw.get('\xa9day'),
        'grouping': meta_raw.get('\xa9grp'),
        'genre': meta_raw.get('\xa9gen'),
        'track': meta_raw.get('trkn'),  # n/t
        'disk': meta_raw.get('disk'),  # n/t
        'filepath': filepath[len(media_root):],
        'length': meta_raw.info.length,
        'bitrate': meta_raw.info.bitrate,
        'codec': meta_raw.info.codec,
    }
    # Clear outside []
    for key in iter(meta):
        if isinstance(meta[key], list):
            meta[key] = meta[key][0]
    # Normalize data
    # meta['country'] = get_country(meta)
    if meta['codec'] != 'alac':
        meta['codec'] = 'aac'
    if len(meta['year']) > 4:
        meta['year'] = meta['year'][:4]
    if meta['track']:
        meta['track_n'] = meta['track'][0]
        meta['track_t'] = meta['track'][1]
    if meta['disk']:
        meta['disk_n'] = meta['disk'][0]
        meta['disk_t'] = meta['disk'][1]
    meta.pop('track', None)
    meta.pop('disk', None)

    cover_raw = meta_raw.get('covr')
    if cover_raw:
        cover_bin = MP4Cover(cover_raw[0])
        meta['coverhash'] = hashlib.md5(cover_bin).hexdigest()
        coverpath = os.path.join(covers_root, meta['coverhash']) + '.jpg'
        if not os.path.exists(coverpath):
            with open(coverpath, "wb") as fp:
                fp.write(cover_bin)
    return meta


if __name__ == "__main__":
    media_root = settings.MEDIA_ROOT
    static_root = settings.STATIC_ROOT
    covers_root = settings.COVERS_ROOT
    time_threshold = 5 * 365 * 24 * 60 * 60

    if not os.path.exists(covers_root):
        os.makedirs(covers_root)

    for dirpath, dirnames, filenames in os.walk(media_root):
        for filename in filenames:
            if filename.split('.')[-1] == 'm4a' and (
                        time.mktime(datetime.datetime.now().timetuple()) - os.path.getctime(
                        os.path.join(dirpath, filename))) < time_threshold:
                meta = get_mp4_metadata(os.path.join(dirpath, filename), covers_root)
                s = MusicLibrary.objects.filter(rawhash=meta['rawhash'])
                nowtime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if s:
                    s.update(**meta)
                    print("UPDATED:" + nowtime_str + str(meta))
                else:
                    s = MusicLibrary(**meta)
                    try:
                        s.save()
                        print("CREATED:" + nowtime_str + str(meta))
                    except Exception as e:
                        print("FAILED:" + nowtime_str + e + str(meta))
                        raise e

    print("All Things Done")
