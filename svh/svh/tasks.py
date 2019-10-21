from django.conf import settings
import os
from django.dispatch import receiver
from svh.models import VideoSource, VideoFile, VIDEO_FORMATS, VideoFolder, Preview, Gif

from svh.rabbit.signals import synchronized_signal, video_converted_signal
from svh.utils import timeit, log_exception
import io
from svh.celery import app
from svh.ffmpeg_helper import convert_video_to_format

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
            try:
                obj = VideoSource.objects.get_with_deleted(hash=hash)
                obj.deleted = False
                obj.path = filepath
                obj.folder = folder
                obj.save()
            except VideoSource.DoesNotExist:
                vs = VideoSource(path=filepath, hash=hash, folder=folder)
                vs.save()
            print(filepath, hash)


@log_exception
def download_torrent(magnet, target_path):
    from qbittorrentapi import Client
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents_add(urls=[magnet], save_path=target_path)


@app.task
def convert_videosource_task(video_source_id, format):
    vs = VideoSource.objects.get(id=video_source_id)
    if vs.videofile_set.filter(format=format).exists(): #todo test it
        print("Video is already converted.")

    vf = VideoFile(source=vs, format=format)
    vf.path = os.path.join(settings.MEDIA_ROOT, '%s_%s.mp4' % (vs.hash, format))
    convert_video_to_format(vs.path, vf.path, format)
    vf.sizeBytes = os.stat(vf.path).st_size
    vf.save()


@app.task
def check_torrents():
    from qbittorrentapi import Client
    client = Client(host=settings.TORRENT_SERVICE_URL, username='admin', password='adminadmin')
    client.torrents.info()

@receiver(video_converted_signal)
def handle_converted_message(sender, source_file_id, result_file_id, format):
    source = VideoSource.objects.filter(file_id=)
    if format == 'preview':
        pr = Preview()