from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('usuarios/', include('usuarios.urls')),
    
    # Logout padrão do Django - aceita apenas POST
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
