from rest_framework import serializers

from .models import MusicLibrary


class MusicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLibrary
        fields = ('rawhash',
                  )


class MusicMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLibrary
        fields = ('title', 'artist', 'album', 'year', 'genre',
                  'grouping', 'track_n', 'track_t', 'disk_n',
                  'disk_t', 'fileurl', 'coverurl',
                  'rawhash', 'length', 'bitrate', 'codec',
                  'country', 'composer', 'cache'
                  )
