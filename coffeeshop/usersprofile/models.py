from django.db import models
from django.conf import settings

class ProfileUser(models.Model):
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=20, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    foto_user = models.ImageField(upload_to='users/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_lengkap
