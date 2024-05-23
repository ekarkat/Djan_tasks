from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "administration"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
