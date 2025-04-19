from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('auth_login')),

    path('register/', views.register, name='auth_register'),
    path('login/', views.user_login, name='auth_login'),
    path('welcome/', views.welcome, name='auth_welcome'),
    path('logout/', views.logout_view, name='auth_logout'),

    path('posts/create/',views.create_post,name='create_post'),
    path('posts/delete/<int:post_id>',views.delete_post,name='delete_post'),
    path('posts/edit/<int:post_id>',views.edit_post,name='edit_post'),
    path('post/<int:post_id>/exchange/',views.create_exchange_offer,name='create_exchange'),

    path('my-offers/', views.user_offers, name='user_offers'),
    path('my-offers/accept/<int:offer_id>/', views.accept_offer, name='accept_offer'),
    path('my-offers/reject/<int:offer_id>/', views.reject_offer, name='reject_offer'),

    path('search/',views.searching,name='search')
]