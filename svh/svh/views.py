from django.conf import settings
from django.shortcuts import render, get_object_or_404
from svh.models import VideoFile, VideoFolder


def index(request):
    root = VideoFolder.objects.get(level=0)
    return page_from(request, root.pk)


def page_from(request, root):
    root_folder = get_object_or_404(VideoFolder, pk=root)
    children = root_folder.get_children()
    videos_ids = root_folder.videosource_set.values_list('videofile', flat=True)
    videos_ids = [i for i in videos_ids if not i == None]
    videos = [{
        'id': v,
        'preview': VideoFile.objects.get(pk=v).source.preview_set.order_by('pk').first().image.url
    }
        for v in videos_ids]

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
    pass #todo