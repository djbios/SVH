from django.http import Http404
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters
from svh.models import VideoFolder, VideoFile
from svh.serializers import VideoFolderSerializer, VideoFileSerializer


class VideoFolderViewSet(mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = VideoFolder.objects.all()
    serializer_class = VideoFolderSerializer

    @action(methods=['get'], detail=False)
    def root(self, request):
        root = self.queryset.get(parent=None)
        return Response(VideoFolderSerializer(root).data)


class VideoFileViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer
    filterset_fields = ('folder','format')

    def get_queryset(self):
        return self.queryset.filter(sourceHash=None)

    def retrieve(self, request, pk=None, *args, **kwargs):
        file = self.queryset.filter(pk=pk)
        if not file:
            raise Http404
        files = self.queryset.filter(sourceHash=file.first().hash)
        files |= file

        serializer = VideoFileSerializer(files, many=True)
        return Response(serializer.data)
