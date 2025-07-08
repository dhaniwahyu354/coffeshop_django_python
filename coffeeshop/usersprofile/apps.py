from django.apps import AppConfig


class UsersprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersprofile'

# userprofile/apps.py

from django.apps import AppConfig

class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userprofile'


def ready(self):
    import usersprofile.signals  # ⬅️ Import signals agar aktif saat aplikasi dijalankan
