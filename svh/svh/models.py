from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import os

from svh.fileservice.proxy import get_file_url, start_conversion

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

    def get_or_create_with_hierarchy(self, folderPath, save=True):
        folder = self.get_queryset().filter(path=folderPath).first()
        if folder is None:
            folder = VideoFolder(path=folderPath)
            if folderPath is not '':
                parent_path = os.path.dirname(folderPath)
                parent = self.get_or_create_with_hierarchy(parent_path)
                parent.save()
                folder.parent=parent
            folder.save()

        return folder


class VideoFolder(MPTTModel):
    class Meta:
        ordering = ('path',)
    _name = models.CharField(max_length=500, null=True, db_column='name', blank=True)
    path = models.CharField(max_length=2000, unique=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    preview_path = models.CharField(max_length=2000, null=True, blank=True)
    parent = TreeForeignKey('self',
                            related_name='folder_parent',
                            null=True, on_delete=models.DO_NOTHING, blank=True)
    deleted = models.BooleanField(default=False)
    objects = VideoFolderManager()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self._name == None:
            return os.path.splitext(self.path)[0].replace(settings.SOURCE_VIDEOS_PATH,'')
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
        if not sources.exists():
            sources = VideoSource.objects.filter(folder__in=self.get_descendants()).exclude(preview=None)
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
            vf = VideoFile(format='default', source=self, fileId=self.hash)
            return vf
        return self.videofile_set.first()

    @property
    def preview(self):
        preview =  self.preview_set.first()
        if preview:
            return preview
        start_conversion(self.hash, 'preview')

    @property
    def gif_url(self):
        from svh.tasks import generate_gif_task
        if hasattr(self, 'gif'):
            return self.gif.image.url
        else:
            generate_gif_task.delay(self.id)
            if self.preview:
                return self.preview.image.url
            else:
                return None  # todo if no preview - return default img


class VideoFile(models.Model):
    fileId = models.CharField(max_length=2000, unique=True)
    sizeBytes = models.IntegerField(null=True)
    format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=VIDEO_FORMATS[0])
    source = models.ForeignKey(VideoSource, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.source.path + self.format

    @property
    def url(self):
        return get_file_url(self.fileId)


class Preview(models.Model): # todo delete file on model deletion
    videosource = models.ForeignKey(VideoSource, on_delete=models.CASCADE)
    fileId = models.CharField(max_length=2000, unique=False)


class Gif(models.Model): # todo delete file on model deletion
    videosource = models.OneToOneField(VideoSource, on_delete=models.CASCADE)
    fileId = models.CharField(max_length=2000, unique=True)
