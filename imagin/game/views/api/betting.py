from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from game.utils import put_card_on_table_json
from game.models import Gameuser, Card, Card2User

@csrf_exempt
def betting(request):
    data = json.loads(request.body)
    user = Gameuser.objects.get(login=data['login'])
    card = Card.objects.get(pk=int(data['card_id']))
    try:
        Card2User.objects.get(user=user,position='table')
        return HttpResponse('Error')
    except Exception as e:
        put_card_on_table_json(user,card, False)
        return HttpResponse('OK')
    