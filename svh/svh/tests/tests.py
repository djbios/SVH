from unittest.mock import patch
from django.test import TestCase
from svh.models import VideoFolder, VideoSource
from svh.tasks import folder_traverser
import os


class CoreTests(TestCase):
    @patch('os.walk')
    @patch('imohash.hashfile')
    def testSync(self, hashfile, oswalk):
        hashfile.return_value = '123'
        oswalk.return_value = [('/tmp', ['dir1'], ['file1.avi']), ('/tmp/dir1', [], [])]
        folder_traverser()
        self.assertTrue(VideoFolder.objects.filter(path='/tmp').count() == 1)
        self.assertTrue(VideoSource.objects.filter(hash='123').count() == 1)
        self.assertTrue(VideoFolder.objects.filter(path=os.path.join('/tmp/dir1')).count() == 1)

        oswalk.return_value = [('/tmp', ['dir1'], ['file1.avi']), ('/tmp/dir1', [], [])]
