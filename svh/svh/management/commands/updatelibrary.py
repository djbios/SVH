from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start library updating task'

    def handle(self, *args, **options):
        from svh.tasks import folder_traverser, check_deleted_videosources, update_video_sizes, update_video_previews
        folder_traverser()
        check_deleted_videosources()
        update_video_sizes() # todo this should be in VideFolder/Videosource model lazyattr
        update_video_previews()
