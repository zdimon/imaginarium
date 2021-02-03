from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def proposing(request):
    return HttpResponse('OK')
