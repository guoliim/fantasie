import os
import re
import sys

import django

# Setup Django Project
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 可以自己用绝对路径定义,目的是工程目录下
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasie.settings")
django.setup()

from musiclib.models import MusicLibrary


def get_country(artist, title, genre):
    jp_artist_list = ['前田愛', '和田光司', '宮崎歩', '大黒摩季', '太田美知彦', '若草恵']
    cn_artist_list = ['Hei Bao (Black Panther)']
    cn_range = "[\u4e00-\u9fa5]+"
    jp_range0 = "[\u30A0-\u30FF]+"
    jp_range1 = "[\u3040-\u309F]+"
    kr_range = "[\uac00-\ud7ff]+"
    s = re.sub('\'', '', artist + title)

    if genre == 'Classical':
        return 'Others'
    if artist in jp_artist_list:
        return 'Japanese'
    if artist in cn_artist_list:
        return 'Chinese'
    if re.search(kr_range,s):
        return 'Korea'
    if re.search(jp_range0,s) or re.search(jp_range1,s):
        return 'Japanese'
    if re.search(cn_range,s):
        return 'Chinese'
    else:
        return 'Others'


def get_composer(title, album):
    album_split = album.split(':')
    title_split = title.split(':')
    composer = ''
    if len(album_split) > 1:
        composer = album_split[0]
    if len(title_split) > 1:
        composer = title_split[0]
    return composer

if __name__ == "__main__":
    for meta in MusicLibrary.objects.all():
        if meta.genre == 'Classical':
            meta.composer = get_composer(meta.title, meta.album)
        meta.country = get_country(meta.artist, meta.title, meta.genre)
        meta.save()
    print("Create or update success!")
