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


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from schema_graph.views import Schema

schema_view = get_schema_view(
   openapi.Info(
      title="Miya taxi API",
      default_version='v1',
      description=''' 

          Documentation `ReDoc` view can be found [here](/doc).

            The Model graph can be found [here](/schema) .

          Authors: zdimon77@gmail.com;

      ''',
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



router = routers.DefaultRouter()
router.register(r'card', CardViewSet)


urlpatterns = [

    path('api/', include(router.urls)),
    path('api/test', TestView.as_view()),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0)), 
    path("schema/", Schema.as_view(),name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
