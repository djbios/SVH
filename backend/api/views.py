from rest_framework import viewsets
from svh.models import VideoFolder
from api.serializers import VideoFolderSerializer


class VideoFolderViewSet(viewsets.ModelViewSet):
    queryset = VideoFolder.objects.all()
    serializer_class = VideoFolderSerializer
