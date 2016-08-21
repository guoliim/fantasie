import os
from random import randint
from unicodedata import normalize
from urllib.parse import quote

from django.conf import settings
from django.db import models
from django.db.models.aggregates import Count


class MusicLibraryQuerySet(models.QuerySet):

    def custom_filter(self, **kwargs):
        mode = kwargs['mode']
        req_dict = kwargs['req_dict']
        result = self
        for field in kwargs['field_list']:
            if mode == 'equal':
                if req_dict.get(field):
                    result = result.filter(**{field + '__iexact': req_dict.get(field)})
            if mode == 'contains':
                if req_dict.get(field):
                    result = result.filter(**{field + '__icontains': req_dict.get(field)})
        return result

    def type_filter(self, **kwargs):
        if not kwargs.get('type'):
            return self
        req_type = kwargs['type'][0]
        if req_type in ['Classical', 'Soundtrack']:
            return self.filter(genre=req_type)
        elif req_type == 'Light':
            return self.filter(grouping=req_type)
        elif req_type == 'Popular':
            return self.exclude(genre='Classical').exclude(genre='Soundtrack').exclude(grouping='Light')
        else:
            return self

    def get_random_song_list(self, n):
        # 形成结果为n个QueryObject列表,不是QuerySet
        # 为了性能不使用order_by('?')
        result = []
        count = self.aggregate(count=Count('id'))['count']
        for _ in range(n):
            try:
                random_index = randint(0, count - 1)
            except ValueError:
                raise MusicLibrary.DoesNotExist
            result.append(self.all()[random_index])
        return result

    def get_distinct_album_coverhash_list(self):
        result_list = []
        for d in self.values("coverhash").distinct():
            result_list.append(d["coverhash"])
        return result_list


class MusicLibrary(models.Model):
    rawhash = models.CharField(max_length=32, default='', unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    album = models.CharField(max_length=200, blank=True, null=True)
    artist = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    grouping = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    track_n = models.IntegerField(blank=True, null=True)
    track_t = models.IntegerField(blank=True, null=True)
    disk_n = models.IntegerField(blank=True, null=True)
    disk_t = models.IntegerField(blank=True, null=True)
    filepath = models.CharField(max_length=300, default='')
    coverhash = models.CharField(max_length=32, default='')
    length = models.IntegerField()
    bitrate = models.IntegerField()
    codec = models.CharField(max_length=10, default='')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    cache = models.BooleanField(default=False)
    country = models.CharField(max_length=20, blank=True, null=True)
    composer = models.CharField(max_length=100, blank=True, null=True)

    def fileurl(self):
        return os.path.join(settings.MEDIA_URL, quote(normalize('NFC', self.filepath)))

    def cacheurl(self):
        return os.path.join(settings.CACHE_URL, self.rawhash + '.m4a')

    def coverurl(self):
        return os.path.join(settings.COVERS_URL, self.coverhash + '.jpg')

    objects = MusicLibraryQuerySet.as_manager()
