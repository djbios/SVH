from rest_framework import serializers

from fileservice.proxy import get_file_url
from svh.models import VideoFolder, VideoFile


class VideoFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFolder
        fields = ['id', 'name', 'description', 'parent', 'children']
        read_only_fields = ['children']

    children = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, vfol):
        return vfol.name or vfol.path or 'Root'

    def get_children(self, vfol):
        return VideoFolderSerializer(vfol.get_children(), many=True).data


class VideoFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoFile
        fields = ['id', 'name', 'hash', 'folder', 'media_url']

    folder = serializers.PrimaryKeyRelatedField(read_only=True)
    media_url = serializers.SerializerMethodField()

    def get_media_url(self, vf):
        return get_file_url(vf.hash)
