import subprocess

from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import os

VIDEO_FORMATS = (
    ('default', '-vcodec libx264'),
)


class VideoFolderManager(models.Manager):
    def all_types(self):
        return self.exclude(type=None).order_by().values_list('type', flat=True).distinct()


class VideoFolder(MPTTModel):
    class Meta:
        ordering = ('path',)
    _name = models.CharField(max_length=500, null=True, db_column='name')
    path = models.CharField(max_length=2000, unique=True)
    type = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    preview_path = models.CharField(max_length=2000, null=True)
    parent = TreeForeignKey('self',
                            related_name='folder_parent',
                            null=True, on_delete=models.DO_NOTHING)
    objects = VideoFolderManager()

    @property
    def name(self):
        if self._name == None:
            return os.path.splitext(self.path)[0]
        return self._name

    @property
    def first_video(self):
        return self.videosource_set.first()


class VideoSource(models.Model):
    _name = models.CharField(max_length=500, null=True, db_column='name')
    path = models.CharField(max_length=2000,  unique=True)
    hash = models.CharField(max_length=200, unique=True)
    sizeBytes = models.IntegerField(null=True)
    deleted = models.BooleanField(default=False)
    folder = models.ForeignKey(VideoFolder,on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.path

    @property
    def name(self):
        if self._name == None:
            return os.path.splitext(os.path.basename(self.path))[0]
        return self._name

    @property
    def videofile(self):
        if settings.AS_IS_BY_DEFAULT and not self.videofile_set.exists():
            linkpath = os.path.join(settings.MEDIA_ROOT, self.hash)
            if not os.path.exists(linkpath):
                os.symlink(self.path, linkpath)  # on windows needs Administrator
            return VideoFile(path=linkpath,format='default',source=self)
        return self.videofile_set.first()

class VideoFile(models.Model): # todo delete file on model deletion
    path = models.CharField(max_length=2000, unique=True)
    sizeBytes = models.IntegerField(null=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.source.path + self.format

    @property
    def one_preview(self):
        return self.source.preview_set.first()

    @property
    def url(self):
        return self.path.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)


class Preview(models.Model): # todo delete file on model deletion
    videosource = models.ForeignKey(VideoSource, on_delete=models.CASCADE)
    pos_seconds = models.IntegerField(null=True)
    image = models.ImageField(upload_to='previews')


class Gif(models.Model): # todo delete file on model deletion
    videosource = models.OneToOneField(VideoSource, on_delete=models.CASCADE)
    image = models.FileField(upload_to='gifs')

#todo https://pypi.org/project/watchdog/ filesystem monitoring