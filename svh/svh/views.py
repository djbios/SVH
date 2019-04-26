import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader, RequestContext
from svh.models import  VideoFile

def index(request):
    root = 'D:\\\\'
    paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(settings.SOURCE_VIDEOS_PATH) for f in filenames]
    dct = {}
    for item in paths:
        p = dct
        for x in item.split('\\'):
            p = p.setdefault(x, {})


    return render(request, 'svh/index.html', {'videos': VideoFile.objects.all()})

def play_video(request, id):
    videofile = get_object_or_404(VideoFile,id=id)

    return render(request,'svh/videoplayer.html',{'videopath': videofile.path})