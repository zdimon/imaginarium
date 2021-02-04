from django.shortcuts import render
from game.models import Gameuser
from imagin.settings import BROWSER_STORAGE

def logout(request,login):
    try:
        user = Gameuser.objects.get(login=login)
        user.delete()
        return render(request, 'logout.html',{"storage": BROWSER_STORAGE})
    except:
        return render(request, 'logout.html',{"storage": BROWSER_STORAGE, "delete": True})



