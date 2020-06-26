from django.contrib.auth.models import User, Group
from rest_framework import serializers

from fileservice.proxy import get_file_url
from svh.models import VideoFolder, VideoFile


class VideoFolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoFolder
        fields = ['id', 'name', 'description', 'parent', 'deleted', 'published']


class VideoFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoFile
        fields = ['id', 'name', 'hash', 'deleted', 'published', 'media_url']

    media_url = serializers.SerializerMethodField()

    def get_media_url(self, vf):
        return get_file_url(vf.hash)
