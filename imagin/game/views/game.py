from django.shortcuts import render
from imagin.settings import SOCKET_SERVER
from game.models import Gameuser, Card
from game.utils import dial_cards_to_user, put_card_on_table_json
import json

def game(request):
    for u in Gameuser.objects.filter(is_online=True):
        dial_cards_to_user(u)
    return render(request, 'game.html', {'socket_server': SOCKET_SERVER})

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
@csrf_exempt
def put_card_on_table(request):
    data = json.loads(request.body)
    user = Gameuser.objects.get(login=data['login'])
    card = Card.objects.get(pk=data['card_id'])
    put_card_on_table_json(user,card)
    return HttpResponse('OK')



