from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from game.utils import put_card_on_table_json
from game.models import Gameuser, Card, Card2User
import socketio   
mgr = socketio.RedisManager('redis://localhost:6379/0', write_only=True)

@csrf_exempt
def gessing(request):
    data = json.loads(request.body)
    user = Gameuser.objects.get(login=data['login'])
    user.state = 'gessed'
    user.association = data['assoc']
    user.save()
    card = Card.objects.get(pk=int(data['card_id']))
    try:
        Card2User.objects.get(user=user,position='table')
        return HttpResponse('Error')
    except Exception as e:
        put_card_on_table_json(user,card, True)
        mgr.emit('show_table', data={})
        return HttpResponse('OK')
    