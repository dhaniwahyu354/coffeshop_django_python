# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('kategori/', views.kategori_list, name='kategori_list'),
    path('kategori/tambah/', views.kategori_create, name='kategori_create'),
    path('kategori/edit/<int:pk>/', views.kategori_edit, name='kategori_edit'),
    path('kategori/hapus/<int:pk>/', views.kategori_delete, name='kategori_delete'),

    path('', views.menus_crud, name='menus_crud'),
    path('menus/tambah/', views.menu_create, name='menu_create'),
    path('menus/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('menus/<int:pk>/hapus/', views.menu_delete, name='menu_delete'),
    path('gambar/<int:id>/hapus/', views.hapus_gambar_menu, name='hapus_gambar_menu'),

    # Tambahkan URL untuk transaksi
    path('transaksi/', views.list_transaksi, name='list_transaksi'),
    path('transaksi/ubah-status/<int:pk>/', views.ubah_status_transaksi, name='ubah_status_transaksi'),
    path('transaksi/tambah/', views.tambah_transaksi, name='tambah_transaksi'),
    path('transaksi/detail/<int:pk>/', views.detail_transaksi, name='detail_transaksi'),

]
