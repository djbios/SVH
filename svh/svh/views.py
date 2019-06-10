from django.conf import settings
from django.shortcuts import render, get_object_or_404
from svh.models import VideoFile, VideoFolder, VideoSource


def index(request):
    root = VideoFolder.objects.filter(level=0).first()  # workaround just for tests, in real life there is only 1 root
    return page_from(request, root.pk)


def page_from(request, root):
    root_folder = get_object_or_404(VideoFolder, pk=root)
    children = root_folder.get_children()
    videos= root_folder.videosource_set.all()

    return render(request, 'svh/index.html', {
        'folders': children,
        'videos': videos
    }) #todo preview - from description.yaml or random video + for videos


def play_video(request, id):
    videofile = get_object_or_404(VideoFile,id=id)
    neighbours = VideoFile.objects.filter(source__folder=videofile.source.folder)
    return render(request,'svh/videoplayer.html',{
        'videopath': videofile.path.replace(settings.MEDIA_ROOT,settings.MEDIA_URL),
        'neighbours': neighbours,
        'parent': videofile.source.folder,
    })


def page_by_type(request, type):
    folders = VideoFolder.objects.filter(type=type)
    return render(request, 'svh/index.html',{
        'folders': folders,
    })
