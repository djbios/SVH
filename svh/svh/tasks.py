from django.conf import settings
import os
from svh.models import VideoSource, VideoFile, VIDEO_FORMATS, VideoFolder, Preview
import imohash
from svh.utils import Protocol
from twisted.internet import reactor, defer
from crochet import wait_for
import yaml
import cv2
import random
from svh.utils import timeit
import io

VIDEO_EXTENSIONS = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'avi', 'mov', 'wmv', 'yuv', 'rm', 'mp4', 'm4p',
                    'mpg', 'mpeg', 'mp2', 'mpv', 'mpe', 'm4v', '3gp', 'mts']

@timeit
def folder_traverser():
    for path, dirs, files in os.walk(settings.SOURCE_VIDEOS_PATH):
        folder = VideoFolder.objects.filter(path=path).first()
        if not folder:
            folder = VideoFolder(path=path)
            parent_path = os.path.abspath(os.path.join(path, os.pardir))
            folder.parent = VideoFolder.objects.filter(path=parent_path).first()  # Get parent object or none

        if settings.DESCRIPTION_FILENAME in files:
            root_yaml = yaml.load(open(os.path.join(path, settings.DESCRIPTION_FILENAME)))
            folder.type = root_yaml.get('type')
            folder.description = root_yaml.get('description')
            folder.preview_path = root_yaml.get('preview_path')
        folder.save()
        for f in files:
            if os.path.splitext(f)[1] in ['.%s' % ex for ex in VIDEO_EXTENSIONS + [ext.upper() for ext in VIDEO_EXTENSIONS]]:
                filepath = os.path.join(path, f)
                hash = imohash.hashfile(filepath, hexdigest=True)
                try:
                    obj = VideoSource.objects.get(hash=hash)
                    obj.path = filepath
                    obj.folder = folder
                    obj.save()
                except VideoSource.DoesNotExist:
                    vs = VideoSource(path=filepath, hash=hash, folder=folder)
                    vs.save()
                print(filepath, hash)

        folder.save()


@timeit
def check_deleted_videosources():
    for vs in VideoSource.objects.filter(deleted=False):
        if not os.path.isfile(vs.path):
            vs.deleted=True
            print(vs.path,' was deleted.')
            vs.save()


@timeit
def update_video_sizes():
    for vs in VideoSource.objects.all():
        vs.sizeBytes = os.stat(vs.path).st_size
        vs.save()

    for vf in VideoFile.objects.all():
        vf.sizeBytes = os.stat(vf.path).st_size
        vf.save()


@timeit
def update_video_previews():
    for vs in VideoSource.objects.all():
        if not vs.preview_set.exists():
            generate_preview(vs)


@timeit
def generate_preview(videosource):
    smallestVideofile = videosource.videofile_set.order_by('sizeBytes').first()
    frames = get_random_frames(smallestVideofile.path, 20)
    for i, f in enumerate(frames):
        (h,w,s) = f.shape
        scale = settings.PREVIEW_HEIGHT / h
        nh, nw = h*scale, w*scale
        f = cv2.resize(f, (int(nw), int(nh)))
        is_success, buffer = cv2.imencode(".jpg", f)
        io_buf = io.BytesIO(buffer)
        filename = 'preview_%i_%i.jpg' % (videosource.pk, i) # todo replace with name after description adding
        pr = Preview()
        pr.videosource = videosource
        pr.image.save(filename, io_buf)


@timeit
def get_random_frames(video_path, count=1):
    cap = cv2.VideoCapture(video_path)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    targets = random.sample(range(min(video_length, 25*20)), count)
    frames = []
    if cap.isOpened() and video_length > 0:
        i = 0
        success, image = cap.read()
        while success and i <= max(targets):
            success, image = cap.read()
            if i in targets and cv2.countNonZero(image) > 30:
                frames.append(image)
            i += 1
    return frames


@timeit
def convert_video_in_format(input_path, output_path, format='default'):
    cmd = "ffmpeg"
    if os.name == 'nt':
        cmd = "C:\\\\Windows\\ffmpeg.exe" #todo magic path
    args = [cmd, "-i", input_path] + dict(VIDEO_FORMATS)[format].split()+ ["-y", output_path]
    pp = Protocol()
    reactor.spawnProcess(pp, cmd, args, {})
    return pp.deferred

# todo threads limit
#todo celery periodic
@timeit
@wait_for(timeout=3600)
def convert_videos(format='default'):
    deferreds = []
    for source in VideoSource.objects.filter(deleted=False):
        if not source.videofile_set.filter(format=format).exists():
            target_path = os.path.join(settings.MEDIA_ROOT, '%s.mp4' % source.hash)
            deferred = convert_video_in_format(source.path, target_path, format)

            def save_videofile(result, _source, _path):
                if result.get('code') == 0:
                    vf = VideoFile(path = _path, format=format, source=_source)
                    vf.save()
                else:
                    print("Some shit happens in conversion! %s" % result.get('logs'))

            deferred.addCallback(save_videofile, _source=source, _path=target_path)
            deferreds.append(deferred)

    return defer.DeferredList(deferreds)
