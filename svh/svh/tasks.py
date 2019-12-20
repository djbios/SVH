from django.conf import settings
import os
from django.dispatch import receiver
from svh.models import VideoSource, VideoFile, VideoFolder, Preview, Gif
from svh.rabbit.signals import synchronized_signal, video_converted_signal
from svh.utils import log_exception
from svh.celery import app

VIDEO_EXTENSIONS = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'avi', 'mov', 'wmv', 'yuv', 'rm', 'mp4', 'm4p',
                    'mpg', 'mpeg', 'mp2', 'mpv', 'mpe', 'm4v', '3gp', 'mts']


@receiver(synchronized_signal)
def update_library(sender, **kwargs):
    folder_traverser_fileservice()


def folder_traverser_fileservice():
    from svh.fileservice.proxy import get_files
    for f in get_files():
        filepath = f.get('fileName').replace(settings.FILESERVICE_SOURCES_FOLDER, '')
        dirpath = os.path.dirname(filepath)
        folder = VideoFolder.objects.get_or_create_with_hierarchy(dirpath)

        if os.path.splitext(filepath)[1] in ['.%s' % ex for ex in
                                      VIDEO_EXTENSIONS + [ext.upper() for ext in VIDEO_EXTENSIONS]]:
            hash = f.get('fileId')
            vs = None
            try:
                vs = VideoSource.objects.get_with_deleted(hash=hash)
                vs.deleted = False
                vs.path = filepath
                vs.folder = folder
                vs.save()
            except VideoSource.DoesNotExist:
                vs = VideoSource(path=filepath, hash=hash, folder=folder)
                vs.save()
            vf = VideoFile(source=vs, fileId=f.get('FileId'), format='source')
            vf.save()
            print(filepath, hash)


@log_exception
def download_torrent(magnet, target_path):
    from qbittorrentapi import Client
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents_add(urls=[magnet], save_path=target_path)


@app.task
def check_torrents():
    from qbittorrentapi import Client
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents.info()


@receiver(video_converted_signal)
def handle_converted_message(sender, source_file_id, result_file_id, format, **kwargs):
    VideoSource.objects.filter(videofile__fileId=source_file_id).first()
    source = VideoSource.objects.filter(videofile__fileId=source_file_id) or VideoSource.objects.get(hash=source_file_id)
    print(format)
    if format == 'preview':
        pr = Preview(videosource=source, fileId=result_file_id)
        pr.save()
    elif format == 'gif':
        gif = Gif(videosource=source, fileId=result_file_id)
        gif.save()
    else:
        vf = VideoFile(source=source, format=format, fileId=result_file_id)
        vf.save()
    print('Added %s for %s' % (result_file_id, source))

