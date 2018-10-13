from django.db import models

VIDEO_FORMATS = (
    ('youtube', '-c:v libx264 -c:a aac -strict experimental -b:a 192k'),
)

class VideoSource(models.Model):
    path = models.CharField(max_length=200,  unique=True)
    hash = models.CharField(max_length=200, unique=True)


class VideoFile(models.Model):
    path = models.CharField(max_length=200, unique=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.OneToOneField(VideoSource, on_delete=models.CASCADE)