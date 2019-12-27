from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start library updating task'

    def handle(self, *args, **options):
        from svh.tasks import update_library
        update_library.delay()
