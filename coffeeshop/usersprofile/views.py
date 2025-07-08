# usersprofile/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProfileUser
from django.contrib import messages

@login_required(login_url='/auth/login/')
def usersprofiles_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # atau render login.html jika ingin langsung ditampilkan

    user = request.user

    try:
        profile = user.profileuser  # relasi OneToOne
    except ProfileUser.DoesNotExist:
        profile = ProfileUser(user=user)

    if request.method == 'POST':
        profile.nama_lengkap = request.POST.get('nama_lengkap', '')
        profile.no_telp = request.POST.get('no_telp', '')
        profile.alamat = request.POST.get('alamat', '')
        profile.jenis_kelamin = request.POST.get('jenis_kelamin', '')
        tanggal_lahir = request.POST.get('tanggal_lahir', '')
        if tanggal_lahir:
            profile.tanggal_lahir = tanggal_lahir

        # ⚠️ Ambil foto dari FILES, bukan POST!
        if 'foto_user' in request.FILES:
            profile.foto_user = request.FILES['foto_user']

        profile.save()

        return redirect('usersprofile')  # nama url sesuai dengan name di urls.py

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def ubah_password_view(request):
    # logika ubah password
    return render(request, 'auth/ubah_password.html')

