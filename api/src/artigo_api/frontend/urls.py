from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    path('get_user', views.UserView.as_view(), name='user'),
    path('resource', views.Resource.as_view(), name='resource'),
    path('search', views.Search.as_view(), name='search'),
    path('reconcile', views.Reconcile.as_view(), name='reconcile'),
    path('game', views.Game.as_view(), name='game'),
    path('highscore', views.Highscore.as_view(), name='highscore'),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
