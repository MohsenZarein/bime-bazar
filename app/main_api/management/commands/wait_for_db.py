from time import sleep
from django.db import connections
from django.core.management import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """ Django command to pause execution until database is available """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database ...')
        conn = None
        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write(self.style.ERROR('Database unavailable, waiting 1 second ...'))
                sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database available'))
            