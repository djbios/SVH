from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader, RequestContext
from svh.models import  VideoFile

def index(request):
    return render(request, 'svh/index.html', {'videos': VideoFile.objects.all()})

def play_video(request, id):
    videofile = get_object_or_404(VideoFile,id=id)

    return render(request,'svh/videoplayer.html',{'videopath': videofile.path})