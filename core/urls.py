from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('', views.homepage, name='home'),
]