from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps principais
    path("", include('pages.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('auditoria/', include('auditoria.urls')),
]
