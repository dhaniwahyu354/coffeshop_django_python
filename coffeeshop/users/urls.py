from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    # path('usersaccount/', views.usersaccount_view, name='usersaccount'),
    
    # crud roll
    # path('roles/', views.role_list, name='role_list'),
    # path('roles/add/', views.role_add, name='role_add'),
    # path('roles/edit/<int:pk>/', views.role_edit, name='role_edit'),
    # path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),
    
]