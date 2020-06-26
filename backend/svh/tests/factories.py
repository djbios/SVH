import factory.fuzzy
from svh.models import VideoFolder, VideoFile, VideoFile, Preview
from django.contrib.auth.models import User


class VideoFolderFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFolder

    _name = factory.Faker('name')
    path = factory.Faker('file_path')
    type = factory.Faker('word')
    description = factory.Faker('text')
    published = True


class VideoSourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFile

    _name = factory.Faker('name')
    path = factory.Faker('file_path')
    hash = factory.Faker('pystr')
    sizeBytes = factory.Faker('pyint')
    folder = factory.SubFactory(VideoFolderFactory)
    deleted = False


class PreviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = Preview

    videosource = factory.SubFactory(VideoSourceFactory)
    fileId = factory.Faker('word')


class VideoFileFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFile

    fileId = factory.Faker('word')
    format = factory.Faker('word')
    source = factory.SubFactory(VideoSourceFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.LazyAttribute(lambda o: o.email)


class AdminFactory(UserFactory):
    @factory.post_generation
    def make_superuser(obj, create, extracted):
        obj.is_staff = True
        obj.is_admin = True
        obj.is_superuser = True
        obj.save()
