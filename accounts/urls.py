from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_login, name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]
