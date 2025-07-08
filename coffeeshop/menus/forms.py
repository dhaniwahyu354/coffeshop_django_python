from django import forms
from .models import KategoriMenu

class KategoriMenuForm(forms.ModelForm):
    class Meta:
        model = KategoriMenu
        fields = ['nama_kategori']
        widgets = {
            'nama_kategori': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kategori'}),
        }
