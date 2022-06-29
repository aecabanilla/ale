from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(r'', include('importaciones.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('importaciones.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
