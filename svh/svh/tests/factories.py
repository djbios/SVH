import factory
from svh.models import VideoFolder, VideoSource


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
