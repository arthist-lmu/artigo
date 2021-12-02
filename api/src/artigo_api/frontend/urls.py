from . import views
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('get_user', views.UserView.as_view(), name='user'),

    path('get_resource', views.ResourceView.as_view(), name='resource'),
    path('get_collection', views.CollectionView.as_view(), name='collection'),
    path('search', views.SearchView.as_view(), name='search'),

    path('get_gametype', views.GametypeView.as_view(), name='gametype'),
    path('get_tagging', views.TaggingView.as_view(), name='tagging'),
    path('get_tag', views.TagView.as_view(), name='tag'),
    path('game/resource', views.GameResourceView.as_view(), name='game_resource'),

]
