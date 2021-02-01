from django.contrib import admin
from game.models import Gameuser, Card

@admin.register(Gameuser)
class GameuserAdmin(admin.ModelAdmin):
    list_display = ['login', 'sids', 'image', 'password']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'on_hand']
