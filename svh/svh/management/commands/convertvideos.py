from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start video conversion task'

    def handle(self, *args, **options):
        from svh.tasks import convert_videos
        convert_videos()