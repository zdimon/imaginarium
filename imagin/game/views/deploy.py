from django.http import HttpResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def deploy(request):
    rc = subprocess.call("./deploy", shell=True)
    return HttpResponse('Ok')



