from django.db import models

VIDEO_FORMATS = (
    ('default', '-vcodec libx264'),
)

class VideoSource(models.Model):
    path = models.CharField(max_length=200,  unique=True)
    hash = models.CharField(max_length=200, unique=True)
    deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return self.path


class VideoFile(models.Model):
    path = models.CharField(max_length=200, unique=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.source.path + self.format