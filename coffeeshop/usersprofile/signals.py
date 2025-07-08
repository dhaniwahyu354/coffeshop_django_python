from django.db.models.signals import post_save  # Trigger saat model disimpan
from django.dispatch import receiver  # Untuk menangkap sinyal
from django.conf import settings  # Mengakses model user kustom dari settings
from .models import ProfileUser  # Model profil yang akan dibuat

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Jika user baru dibuat, otomatis buat profilnya
        ProfileUser.objects.create(user=instance, nama_lengkap=instance.username)
    else:
        # Kalau user di-update (misalnya ganti password), update juga profilnya
        instance.profileuser.save()
