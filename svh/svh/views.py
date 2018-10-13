from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from svh.models import VideoFile

def index(request):
    return render(request, 'svh/index.html', {'videos': VideoFile.objects.all()})