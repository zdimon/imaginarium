from django.core.management.base import BaseCommand, CommandError
from game.models import Card
from django.core.files import File
from imagin.settings import BASE_DIR

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Load cards')
        Card.objects.all().delete()
        for i in range(1,70):
            card = Card()
            card.save()
            filepath = f'{BASE_DIR}/static/images/cards/{i}.jpg'
            with open(filepath, 'rb') as doc_file:
                card.image.save(f'{i}.jpg', File(doc_file), save=True)
            print(f'Creating card {i}')