from django.core.management.base import BaseCommand, CommandError
from game.models import Gameuser
from imagin.settings import BASE_DIR
import threading
import socketio
import eventlet
eventlet.monkey_patch()
mgr = socketio.RedisManager('redis://localhost:6379/0')
sio = socketio.Server(cors_allowed_origins='*',async_mode='eventlet',client_manager=mgr)

app = socketio.WSGIApp(sio)

def add_user_task(sid,data):
    user = Gameuser.objects.get(login=data['login'])
    user.add_sid(sid)

def remove_user_task(sid):
    Gameuser.remove_sid(sid)

@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def login(sid, data):
    thread = threading.Thread(target=add_user_task, args=(sid,data))
    thread.start()


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    thread = threading.Thread(target=remove_user_task, args=(sid,))
    thread.start()

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Statrting socket server')
        eventlet.wsgi.server(eventlet.listen(('', 5001)), app)

        