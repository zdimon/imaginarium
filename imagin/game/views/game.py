from django.shortcuts import render
from imagin.settings import SOCKET_SERVER, BROWSER_STORAGE
from game.models import Gameuser, Card
from game.utils import dial_cards_to_user, put_card_on_table_json
import json

def game(request):
    return render(request, 'game.html', {'socket_server': SOCKET_SERVER, 'storage': BROWSER_STORAGE})







