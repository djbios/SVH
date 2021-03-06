import uuid
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.urls import reverse
from svh.tasks import folder_traverser
from svh.tests.factories import *
import os


@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_TASK_ALWAYS_EAGER=True)
class CoreTests(TestCase):
    def test_empty_homepage(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

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
        vs = VideoSourceFactory(_name=None, path='some/test/path')
        self.assertEqual(vs.name, 'path')

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
        self.assertNotIn(vs.name, str(response.content))

    def test_videofolder(self):
        vf = VideoFolderFactory()
        response = self.client.get(reverse('page', args=[vf.id]))
        self.assertEqual(response.status_code, 200)

    def test_videofolder_without_files(self):
        vf = VideoFolderFactory()
        response = self.client.get('/')
        self.assertNotIn(vf.name, str(response.content))

    def test_play_video(self):
        vfile = VideoFileFactory()
        response = self.client.get(reverse('play_video', args=[vfile.source.id]))
        self.assertEqual(response.status_code, 200)

    def test_videofile_without_preview(self):
        vfile = VideoFileFactory()
        response = self.client.get(reverse('page', args=[vfile.source.folder.id]))
        self.assertEqual(response.status_code, 200)

    def test_types_header(self):
        vfs = VideoFolderFactory.create_batch(5)
        response = self.client.get('/')
        for vf in vfs:
            self.assertIn(vf.type, str(response.content))

    def test_page_by_type(self):
        type='testtype'
        vfs = [VideoFolderFactory(type=type) for i in range(5)]
        response = self.client.get(reverse('by_type', args=[type]))
        for vf in vfs:
            self.assertIn(vf.name, str(response.content))

    def test_fill_attributes(self):
        vf = VideoFolderFactory()
        yaml = {
            'description': 'some description',
            'name': 'some name'
        }
        vf.fill(yaml)
        self.assertEqual(yaml['description'], vf.description)
        self.assertEqual(yaml['name'], vf._name)

    def test_admin_features_admin(self):
        admin = AdminFactory()
        VideoSourceFactory()
        self.client.force_login(admin)
        response = self.client.get('/')
        self.assertIn('form id="updateLibraryForm"', str(response.content))

    def test_admin_features_user(self):
        admin = UserFactory()
        VideoSourceFactory()
        self.client.force_login(admin)
        response = self.client.get('/')
        self.assertNotIn('form id="updateLibraryForm"', str(response.content))

    def test_not_published_videosource(self):
        vf = VideoFileFactory()
        self.client.get('/')
        response = self.client.get(reverse('page', args=[vf.source.folder.id]))
        self.assertNotIn(vf.source.name, str(response.content))

        self.client.force_login(AdminFactory())
        response = self.client.get(reverse('page', args=[vf.source.folder.id]))
        self.assertIn(vf.source.name, str(response.content))

    def test_published_videosource(self):
        vs = VideoSourceFactory(published=True)
        vf = VideoFileFactory(source=vs)

        self.client.get('/')

        response = self.client.get(reverse('page', args=[vs.folder.id]))
        self.assertIn(vs.name, str(response.content))

    def test_deleted_videosource(self):
        vs = VideoSourceFactory(deleted=True)
        vf = VideoFileFactory(source=vs)

        self.client.get('/')
        response = self.client.get(reverse('page', args=[vf.source.folder.id]))
        self.assertNotIn(vf.source.name, str(response.content))

        self.client.force_login(AdminFactory())
        response = self.client.get(reverse('page', args=[vf.source.folder.id]))
        self.assertNotIn(vf.source.name, str(response.content))

    @override_settings(MEDIA_ROOT = '/tmp')
    def test_preview(self):
        vf1 = VideoFolderFactory()
        preview = PreviewFactory()
        vf2 = preview.videosource.folder
        vf2.parent = vf1
        vf2.save()
        response = self.client.get(reverse('page', args=[vf1.id]))
        self.assertIn(preview.image.url, str(response.content))

    @override_settings(MEDIA_ROOT='/tmp')
    def test_included_preview(self):
        vf0 = VideoFolderFactory()
        vf1 = VideoFolderFactory()
        vf1.parent = vf0
        vf1.save()

        preview = PreviewFactory()
        vf2 = preview.videosource.folder
        vf2.parent = vf1
        vf2.save()

        response = self.client.get(reverse('page', args=[vf0.id]))
        self.assertIn(preview.image.url, str(response.content))

    def batch_rename(self):
        find = 'str to find'
        replace = 'str to replace'
        self.client.force_login(AdminFactory())
        vs_list = VideoSourceFactory.create_batch(10)
        for vs in vs_list:
            vs._name=vs._name + find
            vs.save()

        response = self.client.get(reverse('rename')+'?ids='+','.join(str(x.id) for x in vs_list))

        self.assertEqual(response.status_code, 200)
        for vs in vs_list:
            self.assertIn(vs.name, str(response.content))

        response = self.client.post(reverse('rename'), {
            'ids': ','.join(str(x.id) for x in vs_list),
            'find': find,
            'replace': replace
        })

        self.assertEqual(response.status_code, 200)
        for vs in VideoSource.objects.all():
            self.assertNotIn(find, vs.name)
            self.assertIn(replace, vs.name)
