from frontend import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('get_user', views.GetUser.as_view(), name='get_user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('get_resource', views.get_resource, name='get_resource'),
    path('get_collection', views.get_collection, name='get_collection'),
]
