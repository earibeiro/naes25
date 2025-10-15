from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps principais
    path("", include('pages.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('auditoria/', include('auditoria.urls')),
]

# ✅ DJANGO DEBUG TOOLBAR - APENAS EM DEBUG
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
