from rest_framework import serializers
from svh.models import VideoFolder, Preview, VideoSource, Gif


class PreviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preview
        fields = ['id', 'url']


class VideoFolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoFolder
        fields = ['name', 'description', 'id', 'preview']

    preview = PreviewSerializer()


class VideoSourceSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = VideoSource
        fields = ['']