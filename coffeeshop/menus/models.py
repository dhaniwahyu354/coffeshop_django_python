from django.db import models
# from django.contrib.auth.models import User
# diubah
from django.conf import settings
from django.utils import timezone

class KategoriMenu(models.Model):
    nama_kategori = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Kategori Menu" # Opsional: Untuk nama yang lebih baik di admin
        
    def __str__(self):
        return self.nama_kategori

class Menu(models.Model):
    STATUS_MENU_CHOICES = [
        ('tersedia', 'Tersedia'),
        ('habis', 'Habis'),
        ('belum', 'Belum Tersedia'),
    ]

    nama_menu = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(blank=True, null=True)
    kategori = models.ForeignKey(KategoriMenu, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=10,
        choices=STATUS_MENU_CHOICES,
        default='tersedia'
    )

    def __str__(self):
        return f"{self.nama_menu} - {self.get_status_display()}"

class GambarMenu(models.Model):
    menu = models.ForeignKey(Menu, related_name='gambar_menu', on_delete=models.CASCADE)
    gambar = models.ImageField(upload_to='menu/')

    def __str__(self):
        return f"Gambar untuk: {self.menu.nama_menu}"
    

class Transaksi(models.Model):
    WAKTU_CHOICES = [
        ('dine_in', 'Dine In'),
        ('takeaway', 'Takeaway'),
        ('online', 'Online'),
    ]

    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('cancel', 'Cancel'),
    ]

    kode_transaksi = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    waktu_transaksi = models.DateTimeField(default=timezone.now)
    jenis_pesanan = models.CharField(max_length=10, choices=WAKTU_CHOICES, default='dine_in')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='complete')

    def __str__(self):
        return f"Transaksi #{self.kode_transaksi} - {self.get_status_display()}"

    def update_total(self):
        total = sum(detail.subtotal for detail in self.details.all())
        self.total = total
        self.save()

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, related_name='details', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.menu.nama_menu} x {self.jumlah}"

    def save(self, *args, **kwargs):
        self.harga_satuan = self.menu.harga
        self.subtotal = self.harga_satuan * self.jumlah
        super().save(*args, **kwargs)
        self.transaksi.update_total()


# saya mau saat transaksi, masuk menu transaksi nanti tampil tabel yang menampilkan data transaksi, tambahkan transaksi akan menuju ke halaman tambah transaksi(halaman tambah transaksi akan menggantikan halaman transaksi), muncul data yang perlu di masukkan untuk menu muncul dalam bentuk card denan kolon check list