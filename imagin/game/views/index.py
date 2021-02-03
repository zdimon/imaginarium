from django.shortcuts import render
from .forms import GameuserForm
from game.utils import find_user, dial_cards_to_user, clear_table
from imagin.settings import BROWSER_STORAGE

def index(request):
    user = None
    if request.method == 'POST':
        form = GameuserForm(request.POST, request.FILES)
        login = request.POST['login']
        user = find_user(login)
        if not user:
            if form.is_valid():
                user = form.save()
        clear_table()
    else:
        form = GameuserForm()
    
    return render(request, 'index.html', {"form": form, "user": user, "storage": BROWSER_STORAGE})



