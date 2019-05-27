from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start video conversion task'

    def handle(self, *args, **options):
        from svh.tasks import convert_videos, update_video_previews, update_video_sizes
        convert_videos()
        update_video_previews()
        update_video_sizes()