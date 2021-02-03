from django.contrib import admin
from game.models import Gameuser, Card, Card2User, Propose

@admin.register(Gameuser)
class GameuserAdmin(admin.ModelAdmin):
    list_display = ['login', 'sids', 'image', 'password', 'state', 'is_online', 'association']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'on_hand']

@admin.register(Card2User)
class Card2UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'position', 'is_right']

@admin.register(Propose)
class ProposeAdmin(admin.ModelAdmin):
    list_display = ['owner', 'proposer', 'card', 'is_right']