from django.urls import path
from . import views
from .views import dashboard_view


urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # users accout management
    path('usersaccount/', views.usersaccount_view, name='usersaccount'),
    path('usersaccount/add/', views.user_add_view, name='user_add'), # URL untuk menambah pengguna
    path('usersaccount/<str:user_id>/', views.user_detail_view, name='user_detail'),
    path('usersaccount/delete/<str:user_id>/', views.user_delete_view, name='user_delete'),
    
    # role management
    path('roles/', views.role_list_view, name='role_list'),
    path('roles/add/', views.role_add_view, name='role_add'),
    path('roles/edit/<int:role_id>/', views.role_edit_view, name='role_edit'),
    path('roles/delete/<int:role_id>/', views.role_delete_view, name='role_delete'),
    # path('connections/', views.connections_view, name='connections'),

    # path menambahkan users untuk admin
    # path psge not found
    path('404/', views.page_not_found_view, name='page_not_found'),
]

# urlpatterns = [
#     path('', views.landingpage_view, name='landingpage'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),

#     # --- Pengelolaan Akun Pengguna & Role ---
#     # Pola URL Pengguna (Lebih spesifik dulu, baru umum)
#     path('usersaccount/add/', views.user_add_view, name='user_add'), # URL untuk menambah pengguna
#     path('usersaccount/edit/<str:user_id>/', views.user_edit_view, name='user_edit'), # Asumsi Anda akan menambah ini
#     path('usersaccount/delete/<str:user_id>/', views.user_delete_view, name='user_delete'), # Asumsi Anda akan menambah ini
#     path('usersaccount/<str:user_id>/', views.user_detail_view, name='user_detail'), # Detail/profil pengguna (pola umum)
#     path('usersaccount/', views.usersaccount_view, name='usersaccount'), # Daftar/manajemen utama pengguna (pola paling umum di bawah)


#     # Pola URL Role (Jalur terpisah, jadi urutan internalnya saja yang penting)
#     path('roles/add/', views.role_add_view, name='role_add'), # Pola spesifik dulu
#     path('roles/edit/<int:role_id>/', views.role_edit_view, name='role_edit'),
#     path('roles/delete/<int:role_id>/', views.role_delete_view, name='role_delete'),
#     path('roles/', views.role_list_view, name='role_list'), # Daftar/manajemen role (pola umum di bawah)
# ]