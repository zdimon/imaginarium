from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from game.utils import put_card_on_table_json


@csrf_exempt
def guessing(request):
    data = json.loads(request.body)
    print(data)
    put_card_on_table_json(user, card)
    return HttpResponse('OK')

    