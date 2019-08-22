from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from qbittorrentapi import Client
from svh.tasks import update_library
from svh import settings


def torrent_finished(request, torrent_hash):
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents_delete(False,[torrent_hash])
    update_library.delay()
    return HttpResponse()


@csrf_exempt
def is_superuser(request):
    if request.user.is_staff:
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@staff_member_required
def update_library_cmd(request):
    update_library().delay()
    return HttpResponse("OK")
