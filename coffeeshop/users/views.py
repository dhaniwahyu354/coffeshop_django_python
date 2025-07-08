import random
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import User, Role
from usersprofile.models import ProfileUser

from .forms import CustomUserCreationForm, RoleForm

# View untuk registrasi user baru
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('login')
        else:
            messages.error(request, 'Terjadi kesalahan, cek form kembali.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

# View untuk login user
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')  # perbaikan di sini
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Username atau password salah.')
#     return render(request, 'auth/login.html')

def login_view(request):
    context = {}

    # AJAX captcha refresh
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        angka1 = random.randint(1, 10)
        angka2 = random.randint(1, 10)
        request.session['captcha_answer'] = angka1 + angka2
        captcha_text = f"{angka1} + {angka2}"
        return JsonResponse({'captcha': captcha_text})

    # POST request (login)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        captcha_answer = request.POST.get('captcha', '').strip()
        captcha_correct = request.session.get('captcha_answer')

        errors = {}

        if not username:
            errors['username'] = 'Username wajib diisi.'
        if not password:
            errors['password'] = 'Password wajib diisi.'
        if not captcha_answer:
            errors['captcha'] = 'Captcha wajib diisi.'
        elif str(captcha_answer) != str(captcha_correct):
            errors['captcha'] = 'Captcha salah.'

        if errors:
            context['errors'] = errors
            context['form_data'] = {
                'username': username,
                'password': password,
                'captcha': captcha_answer
            }
            angka1 = random.randint(1, 10)
            angka2 = random.randint(1, 10)
            request.session['captcha_answer'] = angka1 + angka2
            context['captcha'] = f"{angka1} + {angka2}"
            return render(request, 'auth/login.html', context)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            errors['password'] = 'Username atau password salah.'
            context['errors'] = errors
            context['form_data'] = {
                'username': username,
                'password': '',
                'captcha': ''
            }
            angka1 = random.randint(1, 10)
            angka2 = random.randint(1, 10)
            request.session['captcha_answer'] = angka1 + angka2
            context['captcha'] = f"{angka1} + {angka2}"
            return render(request, 'auth/login.html', context)

    # GET request: tampilkan form awal
    angka1 = random.randint(1, 10)
    angka2 = random.randint(1, 10)
    request.session['captcha_answer'] = angka1 + angka2
    context['captcha'] = f"{angka1} + {angka2}"
    return render(request, 'auth/login.html', context)

# View untuk logout user
def logout_view(request):
    logout(request)
    return redirect('login')

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

# def usersaccount_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')  # atau render login.html jika ingin langsung ditampilkan

#     users = User.objects.all()  # Ambil semua user
#     context = {
#         'users': users,
#     }
#     return render(request, 'core/usersaccountpage.html', context)

def user_detail_view(request, user_id):
    user_detail = get_object_or_404(User, user_id=user_id)
    all_roles = Role.objects.all()

    # Jika profile belum ada, buat dulu agar tidak error saat template render
    profile, created = ProfileUser.objects.get_or_create(user=user_detail)

    if request.method == 'POST':
        # Update data user
        user_detail.email = request.POST.get('email')
        user_detail.username = request.POST.get('username')
        role_id = request.POST.get('role')
        if role_id:
            user_detail.role = Role.objects.get(id=role_id)
        user_detail.save()

        # Update data profil
        profile.nama_lengkap = request.POST.get('nama_lengkap')
        profile.no_telp = request.POST.get('no_telp')
        profile.alamat = request.POST.get('alamat')
        profile.jenis_kelamin = request.POST.get('jenis_kelamin')
        profile.tanggal_lahir = request.POST.get('tanggal_lahir')

        if request.FILES.get('foto_user'):
            profile.foto_user = request.FILES.get('foto_user')

        profile.save()

        return redirect('user_detail', user_id=user_detail.user_id)

    return render(request, 'core/useraccount_detail.html', {
        'user_detail': user_detail,
        'all_roles': all_roles
    })

# menampilkan users account page
# def usersaccount_view(request):
    
#     users = User.objects.all()  # Ambil semua user
#     context = {
#         'users': users,
#     }
#     return render(request, 'core/base_users_account.html', {
#         'active_tab': 'users'
#     }, context)

# def role_list_view(request):
#     return render(request, 'core/base_users_account.html', {
#         'active_tab': 'roles'
#     })

# # Optional: untuk future connections tab
# def connections_view(request):
#     return render(request, 'core/base_users_account.html', {
#         'active_tab': 'connections'
#     })

# CRUD Role Management

# def role_list(request):
#     roles = Role.objects.all()
#     return render(request, 'users/role_list.html', {'roles': roles})

# def role_add(request):
#     if request.method == 'POST':
#         form = RoleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('role_list')
#     else:
#         form = RoleForm()
#     return render(request, 'users/role_form.html', {'form': form, 'is_edit': False})

# def role_edit(request, pk):
#     role = get_object_or_404(Role, pk=pk)
#     if request.method == 'POST':
#         form = RoleForm(request.POST, instance=role)
#         if form.is_valid():
#             form.save()
#             return redirect('role_list')
#     else:
#         form = RoleForm(instance=role)
#     return render(request, 'users/role_form.html', {'form': form, 'is_edit': True})

# def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    return render(request, 'users/role_confirm_delete.html', {'role': role})