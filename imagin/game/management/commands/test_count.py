from django.core.management.base import BaseCommand, CommandError
from game.utils import try_to_count

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Count')
        try_to_count()