from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

VIDEO_FORMATS = (
    ('default', '-vcodec libx264'),
)

class VideoSource(models.Model):
    path = models.CharField(max_length=2000,  unique=True)
    hash = models.CharField(max_length=200, unique=True)
    sizeBytes = models.IntegerField(null=True)
    deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return self.path


class VideoFile(models.Model):
    path = models.CharField(max_length=2000, unique=True)
    sizeBytes = models.IntegerField(null=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.source.path + self.format


class VideoFolder(MPTTModel):
    path = models.CharField(max_length=2000, unique=True)
    type = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    preview_path = models.CharField(max_length=2000, null=True)
    parent = TreeForeignKey('self',
                            related_name='folder_parent',
                            null=True, on_delete=models.DO_NOTHING)
