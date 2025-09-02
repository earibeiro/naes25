from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.ActivityLogListView.as_view(), name='activity-logs'),
]