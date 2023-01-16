from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('auth/', views.auth_page, name='auth'),
    path('auth resend/', views.resend_token, name='resend_token')
]