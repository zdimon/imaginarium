from django.contrib import admin
from game.models import Gameuser

@admin.register(Gameuser)
class GameuserAdmin(admin.ModelAdmin):
    list_display = ['login', 'sids', 'image', 'password']
