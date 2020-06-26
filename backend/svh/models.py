from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import os

from fileservice.proxy import start_conversion, get_file_url

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
        ordering = ('name',)
    name = models.CharField(max_length=500, null=False, blank=False)
    type = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=10000, null=True)
    parent = TreeForeignKey('self',
                            related_name='folder_parent',
                            null=True, on_delete=models.DO_NOTHING, blank=True)
    deleted = models.BooleanField(default=False)
    objects = VideoFolderManager()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def preview(self):
        sources = self.videofile_set.exclude(preview=None)
        if not sources.exists():
            sources = VideoFile.objects.filter(folder__in=self.get_descendants()).exclude(preview=None)
        return sources.first().preview if sources.exists() else None


class VideoFileManager(models.Manager):
    def get_queryset(self):
        return super(VideoFileManager, self).get_queryset().exclude(deleted=True)

    def get_with_deleted(self, **kwargs):
        return super(VideoFileManager, self).get_queryset().get(**kwargs)

    def all_with_deleted(self, **kwargs):
        return super(VideoFileManager, self).get_queryset().all()


class VideoFile(models.Model):
    folder = models.ForeignKey(VideoFolder,on_delete=models.SET_NULL, null=True)
    _name = models.CharField(max_length=500, null=True, db_column='name')
    hash = models.CharField(max_length=200, unique=True)
    deleted = models.BooleanField(default=False)
    objects = VideoFileManager()
    published = models.BooleanField(default=False)
    sourceHash = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=255, default='source')

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self._name == None:
            return f'{os.path.splitext(os.path.basename(self.folder.path))[0]}/{self.hash}'
        return self._name

    @property
    def preview(self):
        preview = self.preview_set.first()
        return preview or start_conversion(self.hash, 'preview')

    @property
    def gif_url(self):
        if hasattr(self, 'gif'):
            return self.gif.url
        else:
            start_conversion(self.hash, 'gif')
            if self.preview:
                return self.preview.url
            else:
                return None  # todo if no preview - return default img

class Preview(models.Model): # todo delete file on model deletion
    videosource = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
    fileId = models.CharField(max_length=2000, unique=False)

    @property
    def url(self):
        return get_file_url(self.fileId)


class Gif(models.Model): # todo delete file on model deletion
    videosource = models.OneToOneField(VideoFile, on_delete=models.CASCADE)
    fileId = models.CharField(max_length=2000, unique=True)

    @property
    def url(self):
        return get_file_url(self.fileId)
