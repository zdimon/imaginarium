from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def betting(request):
    return HttpResponse('OK')
