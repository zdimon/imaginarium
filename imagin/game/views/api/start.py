from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from game.models import Gameuser, Card, Card2User, Propose
import json
from game.utils import update_online_users_in_json

@csrf_exempt
def start(request):
    data = json.loads(request.body)
    user = Gameuser.objects.get(login=data['login'])
    user.state = 'gessor'
    user.save()
    update_online_users_in_json()
    return HttpResponse('OK')