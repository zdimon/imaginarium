from django.contrib import admin
from game.models import *

@admin.register(Gameuser)
class GameuserAdmin(admin.ModelAdmin):
    list_display = ['login', 'sids', 'image', 'password']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'on_hand']

@admin.register(Card2User)
class Card2UserAdmin(admin.ModelAdmin):
    list_display = ['card', 'user', 'position']

@admin.register(Propose)
class ProposeAdmin(admin.ModelAdmin):
    list_display = ['owner', 'proposer', 'card', 'is_right']
