import factory.fuzzy
from svh.models import VideoFolder, VideoSource, VideoFile, VIDEO_FORMATS
from django.contrib.auth.models import User

class VideoFolderFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFolder

    _name = factory.Faker('word')
    path = factory.Faker('file_path')
    type = factory.Faker('word')
    description = factory.Faker('text')
    preview_path = factory.Faker('file_path')

class VideoSourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoSource

    _name = factory.Faker('word')
    path = factory.Faker('file_path')
    hash = factory.Faker('pystr')
    sizeBytes = factory.Faker('pyint')
    folder = factory.SubFactory(VideoFolderFactory)

class VideoFileFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFile

    path = factory.Faker('file_path')
    sizeBytes = factory.Faker('pyint')
    format = factory.fuzzy.FuzzyChoice(dict(VIDEO_FORMATS).keys())
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
