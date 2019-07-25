from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from svh.forms import AddFolderForm
from svh.models import VideoFolder, VideoSource
from svh.tasks import download_torrent, update_library
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    root = VideoFolder.objects.filter(level=0).first()
    if not root:
        return HttpResponse("No video content")
    return page_from(request, root.pk)


def page_from(request, root):
    root_folder = get_object_or_404(VideoFolder, pk=root)
    if request.method == "POST":
        add_folder_form = AddFolderForm(request.POST) # todo validation
        if (add_folder_form.is_valid()):
            download_torrent(add_folder_form['magnet'].value(), root_folder.path)
    else:
        add_folder_form = AddFolderForm()

    children = root_folder.get_children()
    videos= root_folder.videosource_set.all()

    return render(request, 'svh/index.html', {
        'parent': root_folder.parent,
        'folders': children,
        'videosources': videos,
        'add_folder_form': add_folder_form
    }) #todo preview - from description.yaml or random video + for videos


def play_video(request, id, format='default'):
    videosource = get_object_or_404(VideoSource, id=id)
    neighbours = VideoSource.objects.filter(folder=videosource.folder)
    return render(request,'svh/videoplayer.html',{
        'videosource': videosource,
        'videosources_near': neighbours,
    })

def page_by_type(request, type):
    folders = VideoFolder.objects.filter(type=type)
    return render(request, 'svh/index.html',{
        'folders': folders,
    })


@staff_member_required
def update_library_cmd(request):
    update_library.delay()
    return HttpResponse()
