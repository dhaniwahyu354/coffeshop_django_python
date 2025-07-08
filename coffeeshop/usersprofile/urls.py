from django.urls import path
from . import views

urlpatterns = [
    path('', views.usersprofiles_view, name='usersprofile'),
    path('ubah-password/', views.ubah_password_view, name='ubah_password'),
    
]