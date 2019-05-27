from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start library updating task'

    def handle(self, *args, **options):
        from svh.tasks import folder_traverser, check_deleted_videosources, update_video_sizes
        folder_traverser()
        check_deleted_videosources()
        update_video_sizes() # todo this should be in VideFolder/Videosource model lazyattr
