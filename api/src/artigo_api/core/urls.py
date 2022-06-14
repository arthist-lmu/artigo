from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from .utils import login_required

admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('', include('frontend.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
