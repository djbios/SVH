from django.conf import settings
import os
from svh.models import VideoSource, VideoFile, VIDEO_FORMATS
from imohash import hashfile
from svh.utils import Protocol
from twisted.internet import reactor, defer
from crochet import wait_for

VIDEO_EXTENSIONS = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'avi', 'mov', 'wmv', 'yuv', 'rm', 'mp4', 'm4p',
                    'mpg', 'mpeg', 'mp2', 'mpv', 'mpe', 'm4v', '3gp', 'mts']

def update_library():
    scan_new_videos()
    check_deleted_videosources()


def scan_new_videos():
    paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(settings.SOURCE_VIDEOS_PATH)
              for f in filenames if
              os.path.splitext(f)[1] in ['.%s' % ex for ex in VIDEO_EXTENSIONS + [ext.upper() for ext in VIDEO_EXTENSIONS]]]
    for path in paths:
        hash = hashfile(path, hexdigest=True)
        try:
            obj = VideoSource.objects.get(hash=hash)
            obj.path = path
            obj.save()
        except VideoSource.DoesNotExist:
            vs = VideoSource(path=path, hash=hash)
            vs.save()
        print(path, hash)

    return len(paths)

def check_deleted_videosources():
    for vs in VideoSource.objects.filter(deleted=False):
        if not os.path.isfile(vs.path):
            vs.deleted=True
            print(vs.path,' was deleted.')
            vs.save()

def convert_video_in_format(input_path, output_path, format='default'):
    cmd = "ffmpeg"
    if os.name == 'nt':
        cmd = "C:\\\\Windows\\ffmpeg.exe"
    args = [cmd, "-i", input_path, "-vcodec", "libx264", "-y", output_path]
    pp = Protocol()
    reactor.spawnProcess(pp, cmd, args, {})
    return pp.deferred


@wait_for(timeout=3600)
def convert_videos(format='default'):
    deferreds = []
    for source in VideoSource.objects.filter(deleted=False):
        if not VideoFile.objects.filter(source=source).filter(format=format).exists():
            target_path = os.path.join(settings.MEDIA_ROOT, '%s.mp4' % source.hash)
            deferred = convert_video_in_format(source.path, target_path, format)

            def save_videofile(result, _source):
                if result.get('code') == 0:
                    vf = VideoFile(path = target_path, format=format, source=_source)
                    vf.save()
                    pass
                else:
                    print("Some shit happens in conversion! %s" % result.get('logs'))

            deferred.addCallback(save_videofile, _source=source)
            deferreds.append(deferred)

    return defer.DeferredList(deferreds)
