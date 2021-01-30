from django.shortcuts import render

def logout(request):
    return render(request, 'logout.html')



