from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import os

VIDEO_FORMATS = (
    ('default', '-vcodec libx264'),
)

BIRTH_PLACES = ('user', 'torrent', 'upload')


class VideoFolderManager(models.Manager):
    def all_types(self):
        return self.exclude(type=None).order_by().values_list('type', flat=True).distinct()

    def get_queryset(self):
        return super(VideoFolderManager, self).get_queryset().exclude(deleted=True)

    def all_with_deleted(self, **kwargs):
        return super(VideoFolderManager, self).get_queryset().all()


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
    deleted = models.BooleanField(default=False)
    objects = VideoFolderManager()

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self._name == None:
            return os.path.splitext(self.path)[0]
        return self._name

    @property
    def first_video(self):
        return self.videosource_set.first()

    def fill(self, yaml_dict: dict):
        self.description = yaml_dict.get('description')
        self.preview_path = yaml_dict.get('preview_path')
        self.type = yaml_dict.get('type')
        self._name = yaml_dict.get('name')

    @property
    def preview(self):
        sources = self.videosource_set.exclude(preview=None)
        return sources.first().preview if sources.exists() else None


class VideoSourceManager(models.Manager):
    def get_queryset(self):
        return super(VideoSourceManager, self).get_queryset().exclude(deleted=True)

    def get_with_deleted(self, **kwargs):
        return super(VideoSourceManager, self).get_queryset().get(**kwargs)

    def all_with_deleted(self, **kwargs):
        return super(VideoSourceManager, self).get_queryset().all()


class VideoSource(models.Model):
    _name = models.CharField(max_length=500, null=True, db_column='name')
    path = models.CharField(max_length=2000,  unique=True)
    hash = models.CharField(max_length=200, unique=True)
    sizeBytes = models.IntegerField(null=True)
    deleted = models.BooleanField(default=False)
    folder = models.ForeignKey(VideoFolder,on_delete=models.SET_NULL, null=True)
    objects = VideoSourceManager()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self._name == None:
            return os.path.splitext(os.path.basename(self.path))[0]
        return self._name

    @property
    def videofile(self):
        if settings.ALLOW_SOURCE_SERVING and not self.videofile_set.exists():
            vf = VideoFile(path=self.path, format='default', source=self)
            return vf
        return self.videofile_set.first()

    @property
    def preview(self):
        return self.videofile.preview


class VideoFile(models.Model): # todo deletion logic
    path = models.CharField(max_length=2000, unique=True)
    sizeBytes = models.IntegerField(null=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.source.path + self.format

    @property
    def preview(self):
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