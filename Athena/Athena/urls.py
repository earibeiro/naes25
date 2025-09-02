from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirecionamento de Login
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', include('usuarios.urls')),
    
    # Apps principais
    path("", include('pages.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('auditoria/', include('auditoria.urls')),
]
