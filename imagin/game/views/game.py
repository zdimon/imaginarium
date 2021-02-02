from django.shortcuts import render
from imagin.settings import SOCKET_SERVER

from game.models import Gameuser

def game(request):
    from game.utils import dial_cards_to_user
    for user in Gameuser.objects.filter(is_online=True):
        dial_cards_to_user(user)
    return render(request, 'game.html', {'socket_server': SOCKET_SERVER})



