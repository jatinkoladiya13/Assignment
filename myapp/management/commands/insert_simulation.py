from django.core.management.base import BaseCommand
from myapp.tasks import run_insertions

class Command(BaseCommand):
    help = 'Simulates insertions into different models across multiple databases'

    def handle(self, *args, **options):
        run_insertions()
        self.stdout.write(self.style.SUCCESS('Successfully simulated insertions over multiple models'))
        