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
    return render(request, 'svh/index.html', {'folders': children, 'videos_ids': videos_ids}) #todo preview

def play_video(request, id):
    videofile = get_object_or_404(VideoFile,id=id)

    return render(request,'svh/videoplayer.html',{'videopath': videofile.path.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)})
