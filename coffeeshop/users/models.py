from django.contrib.auth.models import AbstractUser  # Kita pakai user bawaan Django tapi bisa ditambah field-nya
from django.db import models
from django.utils import timezone

# Fungsi untuk generate user_id unik seperti: 250601 (tahun 2025, bulan 06, urutan 01)
def generate_user_id():
    from datetime import datetime
    from django.db.models import Max

    now = datetime.now()
    prefix = now.strftime('%y%m')  # Ambil 2 digit tahun + 2 digit bulan, contoh: 2506

    # Hindari circular import (akan error kalau ditaruh di luar fungsi)
    from .models import User

    # Cari user terakhir yang dibuat bulan ini
    last_user = User.objects.filter(user_id__startswith=prefix).order_by('user_id').last()

    # Hitung nomor urut terakhir dan tambahkan 1
    if last_user:
        last_number = int(last_user.user_id[-2:]) + 1  # Ambil 2 digit terakhir
    else:
        last_number = 1

    # Gabungkan prefix + nomor urut → contoh hasil: 250601
    return f"{prefix}{last_number:02d}"

# Model Role untuk menyimpan jenis role user (Admin, Kasir, dll)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Tambahkan ini jika belum ada
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Hanya tambahkan field ini

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['name']
         # Opsional: Mengurutkan role berdasarkan nama

# Model User kustom, mewarisi semua fitur User Django
class User(AbstractUser):
    user_id = models.CharField(max_length=10, unique=True, editable=False)  # ID unik custom (YYMMnn)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal saat user dibuat
    updated_at = models.DateTimeField(auto_now=True)  # Tanggal saat terakhir user diperbarui

    REQUIRED_FIELDS = ['email']  # Email wajib saat register (selain username & password)

    def save(self, *args, **kwargs):
        # Saat user baru dibuat, generate user_id otomatis
        if not self.user_id:
            self.user_id = generate_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"  # Untuk tampilan di admin atau terminal
