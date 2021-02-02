from django.shortcuts import render
from .forms import GameuserForm
from game.utils import find_user, dial_cards_to_user, clear_table

def index(request):
    user = None
    if request.method == 'POST':
        form = GameuserForm(request.POST, request.FILES)
        login = request.POST['login']
        password = request.POST['password']
        user = find_user(login,password)
        if not user:
            if form.is_valid():
                user = form.save()
        clear_table()
    else:
        form = GameuserForm()
    
    return render(request, 'index.html', {"form": form, "user": user})



