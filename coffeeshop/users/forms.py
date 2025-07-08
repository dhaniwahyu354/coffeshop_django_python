# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Role

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# class RoleForm(forms.ModelForm):
#     class Meta:
#         model = Role
#         fields = ['name']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name'] # Hanya field 'name'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Role'}),
        }
        labels = {
            'name': 'Nama Role',
        }

# Form baru untuk menambah/mengedit Pengguna
class UserAddForm(forms.ModelForm):
    # Field password dan konfirmasi password, karena AbstractUser tidak menyediakannya secara langsung
    # dan kita ingin input terpisah untuk konfirmasi
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Kata Sandi'}),
        label="Kata Sandi",
        min_length=8 # Opsional: Tambahkan validasi panjang minimum password
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Kata Sandi'}),
        label="Konfirmasi Kata Sandi",
        min_length=8 # Opsional: Tambahkan validasi panjang minimum password
    )

    class Meta:
        model = User
        # Fields yang akan ditampilkan di form. user_id tidak disertakan karena di-generate otomatis.
        fields = ('username', 'email', 'password', 'role')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Email'}),
            'role': forms.Select(attrs={'class': 'form-control'}), # Ini akan menjadi dropdown untuk memilih role
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'role': 'Role Pengguna',
        }

    def clean(self):
        """Metode ini digunakan untuk validasi custom, terutama untuk mencocokkan password."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Memastikan password dan konfirmasi password cocok
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Kata sandi tidak cocok. Mohon ulangi.")
        return cleaned_data

    def save(self, commit=True):
        """
        Menyimpan objek user dan mengenkripsi password sebelum disimpan ke database.
        """
        user = super().save(commit=False) # Mengambil objek user tanpa menyimpannya ke DB dulu
        user.set_password(self.cleaned_data["password"]) # Mengenkripsi password
        if commit:
            user.save() # Menyimpan objek user ke database
        return user