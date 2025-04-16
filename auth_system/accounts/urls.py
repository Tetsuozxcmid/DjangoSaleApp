from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('auth_login')),
    path('register/', views.register, name='auth_register'),
    path('login/', views.user_login, name='auth_login'),
    path('welcome/', views.welcome, name='auth_welcome'),
    path('logout/', views.logout_view, name='auth_logout'),
]