from .views import *
from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('game/', GameView.as_view(), name='game'),
    path('home/', HomeView.as_view(), name='home'),
    path('resource/', ResourceView.as_view(), name='resource'),
    path('reconcile/', ReconcileView.as_view(), name='reconcile'),
    path('reconcile/add/', ReconcileAddView.as_view(), name='reconcile_add'),
    path('reconcile/remove/', ReconcileRemoveView.as_view(), name='reconcile_remove'),
    path('search/', SearchView.as_view(), name='search'),
    path('scores/', ScoresView.as_view(), name='scores'),
    path('session/', SessionView.as_view(), name='session'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/registration/', RegisterView.as_view(), name='registration'),
    path('auth/user/', UserDetailsView.as_view(), name='user_details'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('auth/', include('dj_rest_auth.urls')),
]
