from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

from svh.models import VideoFolder, VideoSource
from svh.tasks import folder_traverser
from svh.tests.factories import *
import os


class CoreTests(TestCase):
    @patch('os.walk')
    @patch('imohash.hashfile')
    def test_traverser(self, hashfile, oswalk):
        hashfile.return_value = '123'
        oswalk.return_value = [('/tmp', ['dir1'], ['file1.avi']), ('/tmp/dir1', [], [])]
        folder_traverser()
        self.assertTrue(VideoFolder.objects.filter(path='/tmp').count() == 1)
        self.assertTrue(VideoSource.objects.filter(hash='123').count() == 1)
        self.assertTrue(VideoFolder.objects.filter(path=os.path.join('/tmp/dir1')).count() == 1)

        oswalk.return_value = [('/tmp', ['dir1'], ['file1.avi']), ('/tmp/dir1', [], [])]

    def test_video_folder_name_if_null(self):
        vf = VideoFolderFactory(_name=None)
        self.assertIsNotNone(vf.name)

    def test_video_source_name_if_null(self):
        vs = VideoSourceFactory(_name=None)
        self.assertIsNotNone(vs.name)

    def test_video_folder_types(self):
        vfs = VideoFolderFactory.create_batch(10)
        VideoFolderFactory(type=vfs[0].type)
        types = VideoFolder.objects.all_types()
        for vf in VideoFolder.objects.all():
            self.assertEqual(1, list(types).count(vf.type))

    def test_videosource_before_conversion(self):
        vs = VideoSourceFactory()
        self.client.get('/')
        response = self.client.get(reverse('page',args=[vs.folder.id]))
        self.assertNotIn(vs.name, response.body)


    def test_videofolder_without_files(self):
        vf = VideoFolderFactory()
        response = self.client.get('/')
        self.assertNotIn(vf.name, response.body)