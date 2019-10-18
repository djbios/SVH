from django.conf import settings
import os
from django.core.files.base import ContentFile
from svh.models import VideoSource, VideoFile, VIDEO_FORMATS, VideoFolder, Preview, Gif
import imohash
import yaml
import cv2
import random
from svh.utils import timeit, log_exception
import io
from svh.celery import app
from svh.ffmpeg_helper import convert_video_to_format

VIDEO_EXTENSIONS = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'avi', 'mov', 'wmv', 'yuv', 'rm', 'mp4', 'm4p',
                    'mpg', 'mpeg', 'mp2', 'mpv', 'mpe', 'm4v', '3gp', 'mts']

@app.task
def update_library():
    folder_traverser_fileservice()
    update_video_previews()


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


@timeit
def update_video_previews():
    for vs in VideoSource.objects.all():
        if not vs.preview_set.exists():
            generate_preview(vs)

@timeit
def generate_preview(videosource):
    def get_random_frames(video_path, count=1):  # todo slow
        cap = cv2.VideoCapture(video_path)
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        targets = random.sample(range(min(video_length, 25 * 20)), count)
        frames = []
        if cap.isOpened() and video_length > 0:
            i = 0
            success, image = cap.read()
            while success and i <= max(targets):
                success, image = cap.read()
                if i in targets and image.mean() > 10:
                    frames.append(image)
                i += 1
        return frames

    smallestVideofile = videosource.videofile
    if smallestVideofile == None:
        return
    frames = get_random_frames(smallestVideofile.path, 5)
    for i, f in enumerate(frames):
        (h,w,s) = f.shape
        scale = settings.PREVIEW_HEIGHT / h
        nh, nw = h*scale, w*scale
        f = cv2.resize(f, (int(nw), int(nh)))
        is_success, buffer = cv2.imencode(".jpg", f)
        io_buf = io.BytesIO(buffer)
        filename = 'preview_%s_%i.jpg' % (videosource.name, i)
        pr = Preview()
        pr.videosource = videosource
        pr.image.save(filename, io_buf)


@log_exception
@timeit
def generate_gif(videosource):
    from moviepy.editor import VideoFileClip
    smallestVideofile = videosource.videofile
    if smallestVideofile == None:
        return
    filename = '%s.gif' % videosource.id
    clip = VideoFileClip(smallestVideofile.path)
    scale = settings.PREVIEW_HEIGHT / clip.size[1]
    gif = Gif(videosource=videosource)
    gif.image.save(filename, ContentFile(''))
    clip.subclip(clip.duration/2, clip.duration/2 + min(clip.duration*0.1, 5)).resize(scale).write_gif(gif.image.path) # todo gif length in settings
    gif.save()


@app.task
def generate_gif_task(vs_id):
    generate_gif(VideoSource.objects.get(id=vs_id))

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