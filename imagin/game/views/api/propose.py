from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from game.models import Gameuser, Card, Card2User, Propose
import json

@csrf_exempt
def propose(request):
    data = json.loads(request.body)
    user = Gameuser.objects.get(login=data['login'])
    card = Card.objects.get(pk=int(data['card_id']))
    c2u = Card2User.objects.get(card=card,position='table')
    try:
        p = Propose.objects.get(proposer=user)
        return HttpResponse('Error')
    except:
        p = Propose()
        p.owner = c2u.user
        p.proposer = user
        p.card = card
        if c2u.is_right:
            p.is_right = True
        p.save()
    return HttpResponse('OK')
    