from django.urls import path

from . import views

app_name = "taskmanager"

urlpatterns = [
    path('create/', views.create_workspace, name='create_workspace'),
]
