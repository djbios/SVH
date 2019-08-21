from django.http import HttpResponse
from qbittorrentapi import Client
from svh.tasks import update_library
from svh import settings


def torrent_finished(request, torrent_hash):
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents_delete(False,[torrent_hash])
    update_library.delay()
    return HttpResponse()