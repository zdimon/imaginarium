from django.shortcuts import render
from imagin.settings import SOCKET_SERVER
from game.models import Gameuser, Card
from game.utils import dial_cards_to_user, put_card_on_table_json
import json

def game(request):
    #for u in Gameuser.objects.filter(is_online=True):
    #    dial_cards_to_user(u)
    return render(request, 'game.html', {'socket_server': SOCKET_SERVER})







