from django.core.management.base import BaseCommand, CommandError
from game.models import Gameuser
from django.core.files import File
from imagin.settings import BASE_DIR

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('clear users')
        Gameuser.objects.all().delete()