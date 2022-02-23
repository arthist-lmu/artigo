from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from drf_spectacular.views import (
	SpectacularAPIView,
	SpectacularRedocView,
	SpectacularSwaggerView,
)

urlpatterns = [
    path('get_user/', views.UserView.as_view(), name='user'),
    path('resource/', views.Resource.as_view(), name='resource'),
    path('search/', views.Search.as_view(), name='search'),
    path('reconcile/', views.Reconcile.as_view(), name='reconcile'),
    path('game/', views.Game.as_view(), name='game'),
    path('highscore/', views.Highscore.as_view(), name='highscore'),
    path(
    	'schema/',
    	SpectacularAPIView.as_view(),
    	name='schema',
    ),
    path(
    	'schema/swagger-ui/',
    	SpectacularSwaggerView.as_view(url_name='schema'),
    	name='swagger-ui',
    ),
    path(
    	'schema/redoc/',
    	SpectacularRedocView.as_view(url_name='schema'),
    	name='redoc',
    ),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
