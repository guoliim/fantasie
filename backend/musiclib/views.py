import random
from unicodedata import normalize
from urllib.parse import quote

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import MusicLibrary
from .serializers import MusicListSerializer, MusicMetaSerializer
from .utils import convert_aac, is_ua_safari


# 如果不把list和meta的获取方式分离,那么若ALAC转换未完成,list就拿不到应有的cacheurl值
@api_view(['GET'])
def api_list(request):
    if request.method == 'GET':
        data = request.query_params
        try:
            context = get_list(request=request, req_dict=data, is_safari=is_ua_safari(request))
        except MusicLibrary.DoesNotExist:
            return JsonResponse([], safe=False)
        if settings.DEBUG:
            serializer = MusicMetaSerializer(context, many=True)
        else:
            serializer = MusicListSerializer(context, many=True)
        return JsonResponse(serializer.data, safe=False)  # JSON array need safe=False


@api_view(['GET'])
def api_song_album_list(request):
    if request.method == 'GET':
        data = request.query_params
        try:
            coverhash = MusicLibrary.objects.get(rawhash=data['rawhash']).coverhash
            meta_list = get_song_meta_list(request, coverhash)
        except MusicLibrary.DoesNotExist:
            return JsonResponse([], safe=False)
        serializer = MusicListSerializer(meta_list, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def api_song_meta(request):
    def convert_for_no_safari(meta):
        if meta.codec == 'alac':
            if settings.ALAC_CONVERTIBLE:
                convert_aac.delay(settings.MEDIA_ROOT + meta.filepath, meta.rawhash)
            meta.fileurl = meta.cacheurl
        return meta

    if request.method == 'GET':
        data = request.query_params
        try:
            meta = MusicLibrary.objects.get(rawhash=data['rawhash'])
        except MusicLibrary.DoesNotExist:
            return JsonResponse({}, safe=True)
        if not is_ua_safari(request):
            meta = convert_for_no_safari(meta)
        serializer = MusicMetaSerializer(meta)
        return JsonResponse(serializer.data)


def api_recommendation(request):
    result = [
        {"name": "Popular", "refer": "/api/list?type=Popular"},
        {"name": "Classical", "refer": "/api/list?type=Classical"},
        {"name": "All", "refer": "/api/list"},
        {"name": "Soundtrack", "refer": "/api/list?type=Soundtrack"},
        {"name": "Chinese", "refer": "/api/list?country=Chinese"},
    ]
    return JsonResponse(result, safe=False)


def get_song_meta_list(request, coverhash):
    meta_list = MusicLibrary.objects.filter(coverhash=coverhash).order_by('disk_n', 'disk_t', 'track_n', 'track_t')
    return meta_list


def get_list(request, req_dict, is_safari):
    meta = MusicLibrary.objects

    meta = meta.type_filter(**req_dict)
    meta = meta.custom_filter(**{
        'field_list': ['title', 'artist', 'album'],
        'req_dict': req_dict,
        'mode': 'contains'
    })
    meta = meta.custom_filter(**{
        'field_list': ['codec', 'composer', 'genre', 'year', 'grouping', 'country'],
        'req_dict': req_dict,
        'mode': 'equal'
    })

    if req_dict.get("method") == "album":
        coverhash_list = meta.get_distinct_album_coverhash_list()
        return get_song_meta_list(request, coverhash=random.choice(coverhash_list))

    if not is_safari and req_dict == {}:
        aac_meta = meta.filter(codec='aac')
        meta_list = aac_meta.get_random_song_list(5) + meta.get_random_song_list(5)
    else:
        meta_list = meta.get_random_song_list(10)
    return meta_list


def get_song_meta(req_dict):
    meta_list = get_list(req_dict)
    context = meta_list
    for e in context:
        e['filepath'] = os.path.join(settings.MEDIA_URL, quote(normalize('NFC', str(e['filepath']))))
        e['coverpath'] = os.path.join(settings.STATIC_URL, e['coverhash'] + '.jpg')
        if not settings.DEBUG:
            keys_list = list(e.keys())
            for key in keys_list:
                if not key == 'rawhash':
                    e.pop(key, None)
    return context


def index(request):
    return render(request, 'index.html')

