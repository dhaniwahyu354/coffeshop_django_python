from django.shortcuts import render, redirect, get_object_or_404
# menus/views.py
from .models import KategoriMenu
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Menu, GambarMenu, DetailTransaksi, Transaksi, KategoriMenu
from django.http import JsonResponse
from django.conf import settings
import os
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Transaksi
import uuid
from django.utils import timezone



# views.py kategori CRUD
@login_required(login_url='/auth/login/')
def kategori_list(request):
    kategori = KategoriMenu.objects.all()
    return render(request, 'menus/kategori_crud.html', {'kategori': kategori})

@login_required(login_url='/auth/login/')
def kategori_create(request):
    if request.method == 'POST':
        nama = request.POST.get('nama_kategori')
        if nama:
            KategoriMenu.objects.create(nama_kategori=nama)
            messages.success(request, 'Kategori berhasil ditambahkan!')
            return redirect('kategori_list')
    return redirect('kategori_list')

@login_required(login_url='/auth/login/')
def kategori_edit(request, pk):
    kategori = get_object_or_404(KategoriMenu, pk=pk)
    if request.method == 'POST':
        nama = request.POST.get('nama_kategori')
        kategori.nama_kategori = nama
        kategori.save()
        messages.success(request, 'Kategori berhasil diubah!')
        return redirect('kategori_list')
    return redirect('kategori_list')

@login_required(login_url='/auth/login/')
def kategori_delete(request, pk):
    kategori = get_object_or_404(KategoriMenu, pk=pk)
    kategori.delete()
    messages.success(request, 'Kategori berhasil dihapus!')
    return redirect('kategori_list')

# views.py untuk menus CRUD
def menus_crud(request):
    menus = Menu.objects.all()
    kategoris = KategoriMenu.objects.all()
    return render(request, 'menus/menus_crud.html', {
        'menus': menus,
        'kategoris': kategoris
    })

def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    kategoris = KategoriMenu.objects.all()
    if request.method == 'POST':
        # Update Menu
        menu.nama_menu = request.POST.get('nama_menu')
        menu.harga = request.POST.get('harga')
        menu.deskripsi = request.POST.get('deskripsi')
        menu.status = request.POST.get('status')
        kategori_id = request.POST.get('kategori')
        if kategori_id:
            menu.kategori = KategoriMenu.objects.get(id=kategori_id)
        menu.save()

        # Upload Gambar Baru dari input name="gambar[]"
        if request.FILES.getlist('gambar[]'):
            for img in request.FILES.getlist('gambar[]'):
                GambarMenu.objects.create(menu=menu, gambar=img)

        messages.success(request, 'Menu berhasil diperbarui!')
        return redirect('menu_detail', pk=menu.pk)

    return render(request, 'menus/menu_detail.html', {
        'menu': menu,
        'kategoris': kategoris
    })


def menu_create(request):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama_menu')
            harga = request.POST.get('harga')
            deskripsi = request.POST.get('deskripsi')
            status = request.POST.get('status')
            kategori_id = request.POST.get('kategori')

            menu = Menu.objects.create(
                nama_menu=nama,
                harga=harga,
                deskripsi=deskripsi,
                status=status,
                kategori=KategoriMenu.objects.get(id=kategori_id) if kategori_id else None
            )

            for img in request.FILES.getlist('gambar[]'):
                GambarMenu.objects.create(menu=menu, gambar=img)

            return JsonResponse({'success': True, 'message': 'Menu berhasil ditambahkan!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Permintaan tidak valid.'})

def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    messages.success(request, 'Menu berhasil dihapus!')
    return redirect('menus_crud')

def hapus_gambar_menu(request, id):
    gambar = get_object_or_404(GambarMenu, id=id)
    menu_id = gambar.menu.id  # untuk redirect kembali ke detail menu

    # Hapus file fisik dari media/
    file_path = os.path.join(settings.MEDIA_ROOT, gambar.gambar.name)
    if os.path.isfile(file_path):
        os.remove(file_path)

    # Hapus dari database
    gambar.delete()

    messages.success(request, f'Gambar berhasil dihapus!')
    return redirect('menu_detail', pk=menu_id)

# transaksi views
@login_required(login_url='/auth/login/')
def list_transaksi(request):
    query = request.GET.get('q', '')
    transaksi_list = Transaksi.objects.filter(
        Q(kode_transaksi__icontains=query) |
        Q(user__username__icontains=query)
    ).order_by('-waktu_transaksi')

    paginator = Paginator(transaksi_list, 10)  # 10 transaksi per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'transaksi/list_transaksi.html', context)

@login_required(login_url='/auth/login/')
def ubah_status_transaksi(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    if transaksi.status == 'complete':
        transaksi.status = 'cancel'
    else:
        transaksi.status = 'complete'
    transaksi.save()
    return redirect('list_transaksi')

@login_required(login_url='/auth/login/')
def tambah_transaksi(request):
    menus = Menu.objects.filter(status='tersedia').prefetch_related('gambar_menu')

    if request.method == 'POST':
        selected_menu_ids = request.POST.getlist('menu_id')
        quantities = request.POST.getlist('jumlah')

        if not selected_menu_ids:
            return render(request, 'transaksi/tambah_transaksi.html', {
                'menus': menus,
                'error': "Pilih setidaknya satu menu."
            })

        transaksi = Transaksi.objects.create(
            kode_transaksi=str(uuid.uuid4())[:8].upper(),
            user=request.user,
            waktu_transaksi=timezone.now(),
            jenis_pesanan=request.POST.get('jenis_pesanan', 'dine_in'),
            status='complete'
        )

        for idx, menu_id in enumerate(selected_menu_ids):
            try:
                menu = Menu.objects.get(id=menu_id)
                jumlah = int(quantities[idx])
                if jumlah < 1:
                    continue
                DetailTransaksi.objects.create(
                    transaksi=transaksi,
                    menu=menu,
                    jumlah=jumlah,
                    harga_satuan=menu.harga,
                    subtotal=menu.harga * jumlah
                )
            except (Menu.DoesNotExist, ValueError, IndexError):
                continue

        transaksi.update_total()
        return redirect('list_transaksi')

    return render(request, 'transaksi/tambah_transaksi.html', {'menus': menus})

@login_required(login_url='/auth/login/')
def detail_transaksi(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)

    if request.method == 'POST':
        jenis_pesanan = request.POST.get('jenis_pesanan')
        status = request.POST.get('status')

        if jenis_pesanan in dict(Transaksi.WAKTU_CHOICES) and status in dict(Transaksi.STATUS_CHOICES):
            transaksi.jenis_pesanan = jenis_pesanan
            transaksi.status = status
            transaksi.save()
            return redirect('detail_transaksi', pk=pk)

    return render(request, 'transaksi/detail_transaksi.html', {'transaksi': transaksi})