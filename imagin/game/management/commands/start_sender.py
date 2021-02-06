from django.core.management.base import BaseCommand, CommandError
from game.tasks import timer_task
import time

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('start sender')
        
        while True: 
            time.sleep(2)  
            timer_task.delay()  