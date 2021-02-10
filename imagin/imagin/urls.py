"""imagin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from game.views import *

from rest_framework import routers

from game.views.api.card_viewset import CardViewSet, TestView



router = routers.DefaultRouter()
router.register(r'card', CardViewSet)


urlpatterns = [

    path('api/', include(router.urls)),
    path('api/test', TestView.as_view()),


    path('', index),
    path('game', game, name='game'),
    path('logout/<slug:login>', logout),
    path('hello', hello),
    path('deploy', deploy),

    path('gessing', gessing),
    path('betting', betting),
    path('propose', propose),
    path('start', start),
    path('rosetta', include('rosetta.urls')),

    url(r'^admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
