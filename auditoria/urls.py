from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path('logs/', views.ActivityLogListView.as_view(), name='activity-logs'),
]