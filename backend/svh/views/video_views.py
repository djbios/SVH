from django.http import Http404
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from svh.models import VideoFolder, VideoFile
from svh.serializers import VideoFolderSerializer, VideoFileSerializer


class VideoFolderViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = VideoFolder.objects.all()
    serializer_class = VideoFolderSerializer


class VideoFileViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):

    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(sourceHash=None)
        serializer = VideoFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        file = self.queryset.filter(pk=pk)
        if not file:
            raise Http404
        files = self.queryset.filter(sourceHash=file.first().hash)
        files |= file

        seralizer = VideoFileSerializer(files, many=True)
        return Response(seralizer.data)
