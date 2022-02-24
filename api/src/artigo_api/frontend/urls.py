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
    path('resource/', views.ResourceView.as_view(), name='resource'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('reconcile/', views.ReconcileView.as_view(), name='reconcile'),
    path('game/', views.GameView.as_view(), name='game'),
    path('highscore/', views.HighscoreView.as_view(), name='highscore'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/registration/', views.RegisterView.as_view(), name='registration'),
    path('auth/user/', views.UserDetailsView.as_view(), name='user_details'),
    path('auth/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('auth/', include('dj_rest_auth.urls')),
]
