from django.shortcuts import render
from imagin.settings import SOCKET_SERVER

def game(request):
    return render(request, 'game.html', {'socket_server': SOCKET_SERVER})



