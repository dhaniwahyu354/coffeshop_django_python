from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from users.models import Role
from users.forms import RoleForm, UserAddForm # Pastikan Anda mengimpor RoleForm dari aplikasi 'users'
from usersprofile.models import ProfileUser
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

User = get_user_model()
# landing page view
def landingpage_view(request):
    return render(request, 'landingpage/index.html')


# dashboard view
@login_required(login_url='/auth/login/')
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

# users account view
@login_required(login_url='/auth/login/')
def usersaccount_view(request):
    users = User.objects.select_related('role', 'profileuser').all()
    user_add_form = UserAddForm() # Kirim instance form kosong untuk di-render di template
    return render(request, 'core/base_users_account.html', {
        'active_tab': 'users',
        'users': users,
        'user_add_form': user_add_form, # <-- Pastikan ini dilewatkan ke base_users_account.html
    })

@login_required(login_url='/auth/login/')
def user_add_view(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Pengguna berhasil ditambahkan!')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat menambahkan pengguna: {e}')
        else:
            messages.error(request, 'Formulir tidak valid. Mohon periksa input Anda.')
    # Selalu redirect kembali ke daftar pengguna setelah POST, baik sukses maupun gagal
    return redirect('usersaccount')

# Anda bisa menambahkan user_edit_view dan user_delete_view serupa di sini
# Misalnya:
# @login_required(login_url='/auth/login/')
# def user_edit_view(request, user_id):
#     user_obj = get_object_or_404(User, id=user_id)
#     if request.method == 'POST':
#         form = UserAddForm(request.POST, instance=user_obj) # Gunakan UserAddForm, atau buat UserEditForm terpisah tanpa password
#         # ... (logic edit)
#     else:
#         form = UserAddForm(instance=user_obj)
#     return render(request, 'core/users/aksi_user.html', {
#         'form': form,
#         'action_type': 'edit',
#         'modal_title': f'Edit Pengguna: {user_obj.username}',
#         'user_obj': user_obj
#     })

# @login_required(login_url='/auth/login/')
# def user_delete_view(request, user_id):
#     user_obj = get_object_or_404(User, id=user_id)
#     # ... (logic delete)
#     return redirect('user_list')


# roles management view
@login_required(login_url='/auth/login/')
def role_list_view(request):
    roles = Role.objects.all()
    return render(request, 'core/base_users_account.html', {
        'active_tab': 'roles',
        'roles': roles
    })

# add role view
@login_required(login_url='/auth/login/')
def role_add_view(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Role berhasil ditambahkan!')
                return redirect('role_list') # Redirect ke daftar role setelah sukses
            except Exception as e:
                # Tangkap error saat menyimpan ke database
                messages.error(request, f'Terjadi kesalahan saat menyimpan role: {e}')
                # Render ulang form dengan data yang sudah diisi dan error (jika ada)
                return render(request, 'core/roles/aksi_role.html', {
                    'form': form,
                    'action_type': 'add',
                    'modal_title': 'Tambah Role Baru'
                })
        else:
            # Formulir tidak valid, tampilkan error pada formulir
            messages.error(request, 'Formulir tidak valid. Mohon periksa input Anda.')
            return render(request, 'core/roles/aksi_role.html', {
                'form': form, # Kirim form yang tidak valid kembali ke template agar error ditampilkan
                'action_type': 'add',
                'modal_title': 'Tambah Role Baru'
            })
    else:
        form = RoleForm()
    return render(request, 'core/roles/aksi_role.html', {
        'form': form,
        'action_type': 'add',
        'modal_title': 'Tambah Role Baru'
    })

# edit role view
@login_required(login_url='/auth/login/')
def role_edit_view(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Role berhasil diperbarui!')
                return redirect('role_list') # Redirect ke daftar role setelah sukses
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat menyimpan perubahan role: {e}')
                return render(request, 'core/roles/aksi_role.html', {
                    'form': form,
                    'action_type': 'edit',
                    'modal_title': f'Edit Role: {role.name}',
                    'role': role # <-- PENTING: Kirim objek role ke template
                })
        else:
            messages.error(request, 'Formulir tidak valid. Mohon periksa input Anda.')
            return render(request, 'core/roles/aksi_role.html', {
                'form': form, # Kirim form yang tidak valid kembali ke template agar error ditampilkan
                'action_type': 'edit',
                'modal_title': f'Edit Role: {role.name}',
                'role': role # <-- PENTING: Kirim objek role ke template
            })
    else:
        form = RoleForm(instance=role)
    return render(request, 'core/roles/aksi_role.html', {
        'form': form,
        'action_type': 'edit',
        'modal_title': f'Edit Role: {role.name}',
        'role': role # <-- PENTING: Kirim objek role ke template
    })

# delete role view
@login_required(login_url='/auth/login/')
def role_delete_view(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    # Anda bisa menambahkan logika untuk mengecek apakah role ini sedang digunakan oleh user
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # if User.objects.filter(role=role).exists():
    #     messages.error(request, f'Role "{role.name}" tidak dapat dihapus karena masih digunakan oleh beberapa pengguna.')
    #     return redirect('role_list')

    if request.method == 'POST':
        role_name = role.name # Simpan nama sebelum dihapus
        try:
            role.delete()
            messages.success(request, f'Role "{role_name}" berhasil dihapus.')
        except Exception as e:
            messages.error(request, f'Gagal menghapus role "{role_name}". Terjadi kesalahan: {e}')
        return redirect('role_list')
    # Jika request bukan POST (misal langsung akses URL), arahkan kembali
    messages.error(request, 'Aksi penghapusan role tidak diizinkan tanpa konfirmasi.')
    return redirect('role_list')

# detail users views
@login_required(login_url='/auth/login/')
def user_detail_view(request, user_id):
    user_detail = get_object_or_404(User, user_id=user_id)
    all_roles = Role.objects.all()

    if request.method == 'POST':
        # Update user fields
        user_detail.username = request.POST.get('username')
        user_detail.email = request.POST.get('email')
        user_detail.role_id = request.POST.get('role')
        user_detail.updated_at = timezone.now()
        user_detail.save()

        # Update profile fields
        profile = user_detail.profileuser
        profile.nama_lengkap = request.POST.get('nama_lengkap')
        profile.no_telp = request.POST.get('no_telp')
        profile.alamat = request.POST.get('alamat')
        profile.jenis_kelamin = request.POST.get('jenis_kelamin')
        profile.tanggal_lahir = request.POST.get('tanggal_lahir')
        if request.FILES.get('foto_user'):
            profile.foto_user = request.FILES['foto_user']
        profile.updated_at = timezone.now()
        profile.save()

        messages.success(request, 'Data pengguna berhasil diperbarui.')
        return redirect('user_detail', user_id=user_id)

    return render(request, 'core/users_account/useraccount_detail.html', {
        'user_detail': user_detail,
        'all_roles': all_roles
    })

@login_required(login_url='/auth/login/')
def user_delete_view(request, user_id):
    user = get_object_or_404(User, user_id=user_id)

    if user == request.user:
        messages.error(request, '⚠️ Anda tidak dapat menghapus akun Anda sendiri.')
    else:
        user.delete()
        messages.success(request, f'✅ Pengguna "{user.username}" berhasil dihapus.')

    return redirect('usersaccount')

def page_not_found_view(request, exception=None):
    return render(request, 'core/404.html', status=404)
