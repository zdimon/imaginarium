from django.core.management.base import BaseCommand, CommandError
from game.models import Gameuser, Card
from django.core.files import File
from imagin.settings import BASE_DIR

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('clear users')
        Gameuser.objects.all().delete()
        for c in Card.objects.all():
            c.on_hand = False
            c.save()