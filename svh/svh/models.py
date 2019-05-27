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
            return os.path.splitext(self.path)[0]
        return self._name


class VideoFile(models.Model):
    path = models.CharField(max_length=2000, unique=True)
    sizeBytes = models.IntegerField(null=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.source.path + self.format

    def preview(self):
        Preview.objects.filter(videosource=self.source)


class Preview(models.Model):
    videosource = models.ForeignKey(VideoSource, on_delete=models.CASCADE)
    pos_seconds = models.IntegerField(null=True)
    image = models.ImageField(upload_to='previews')
