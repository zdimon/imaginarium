from django.http import HttpResponse
import subprocess

def deploy(request):
    rc = subprocess.call("./deploy", shell=True)
    return HttpResponse('Ok')



