from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView  # ✅ ADICIONAR
from django.conf.urls.static import static  # ✅ ADICIONAR

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps principais
    path("", include('pages.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('auditoria/', include('auditoria.urls')),
    
    # ✅ FAVICON (redireciona para arquivo estático ou retorna 204 No Content)
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
]

# ✅ DJANGO DEBUG TOOLBAR - APENAS EM DEBUG
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    # ✅ SERVIR ARQUIVOS ESTÁTICOS EM DESENVOLVIMENTO
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
