from . import views
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('get_user', views.UserView.as_view(), name='user'),

    # path('get_resource', views.ResourceView.as_view(), name='resource'),
    path('get_collection', views.CollectionView.as_view(), name='collection'),
    path('search', views.SearchView.as_view(), name='search'),

    path('gametype', views.GametypeView.as_view(), name='gametype'),
    path('gamesession', views.GamesessionView.as_view(), name='gamesession'),
    path('gameround', views.GameroundView.as_view(), name='gameround'),

    path('tagging', views.TaggingView.as_view(), name='tagging'),
    path('tag', views.TagView.as_view(), name='tag'),
    path('game_resource', views.GameResourceView.as_view(), name='game_resource'),
    path('game_resource_picture', views.GameResourceViewPicture.as_view(), name='game_resource_picture'),

    path('artigo_gametype', views.ARTigoGametypeView.as_view(), name='ARTigo_game'),
    path('gametype/gamesession', views.GametypeWithGamesessionView.as_view(), name='gametype_with_gamesession'),

    path('get_artigo_gameround/resource', views.GameroundWithResourceView.as_view(), name='ARTigo_gameround'),

    path('taboo_tags', views.TabooTagsView.as_view(), name='taboo_tags'),

]
