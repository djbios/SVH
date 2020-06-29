from django.core.management.base import BaseCommand
from svh.tasks import update_library


class Command(BaseCommand):
    help = 'Start library updating task'

    def handle(self, *args, **options):
        update_library()
