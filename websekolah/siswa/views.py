from django.shortcuts import render, redirect
from django.db import connection

def ambil_satu_siswa(id_siswa):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir FROM siswa WHERE id = %s", [id_siswa])
        if cursor.description is None:
            return None
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if row:
            data = dict(zip(columns, row))
            
            if data['tgl_lahir']:
                try:
                    data['tgl_lahir'] = data['tgl_lahir'].strftime('%Y-%m-%d')
                except AttributeError:
                    pass
            
            data['status_hadir'] = "Hadir" if data['status_hadir'] else "Tidak Hadir"
            return data
    return None

def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir FROM siswa ORDER BY id DESC")
        columns = [col[0] for col in cursor.description]
        data_siswa = []
        for row in cursor.fetchall():
            siswa_dict = dict(zip(columns, row))
            
            siswa_dict['status_hadir'] = "Hadir" if siswa_dict['status_hadir'] else "Tidak Hadir"
            data_siswa.append(siswa_dict)

    search_text = "BEKASI"
    return render(request, 'list.html', {
        'keyword': search_text,
        'data': data_siswa
    })

def siswa_detail(request, id):
    siswa = ambil_satu_siswa(id)
    return render(request, 'detail.html', {'siswa': siswa})

def siswa_create(request):
    if request.method == 'POST':     
        nama = request.POST.get('nama', '').strip()
        umur = request.POST.get('umur')
        tgl_lahir = request.POST.get('tgl_lahir') or None
        status_hadir = True if request.POST.get('status_hadir') == 'Hadir' else False
        nilai_akhir = request.POST.get('nilai_akhir') or 0

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO siswa (nama, umur, tgl_lahir, status_hadir, nilai_akhir)
                VALUES (%s, %s, %s, %s, %s)
            """, [nama, umur, tgl_lahir, status_hadir, nilai_akhir])

        return redirect('siswa_list')

    return render(request, 'form.html')

def siswa_update(request, id):
    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        umur = request.POST.get('umur')
        tgl_lahir = request.POST.get('tgl_lahir') or None
        status_hadir = True if request.POST.get('status_hadir') == 'Hadir' else False
        nilai_akhir = request.POST.get('nilai_akhir') or 0

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa 
                SET nama = %s, umur = %s, tgl_lahir = %s, status_hadir = %s, nilai_akhir = %s 
                WHERE id = %s
            """, [nama, umur, tgl_lahir, status_hadir, nilai_akhir, id])

        return redirect('siswa_list')

    siswa = ambil_satu_siswa(id)
    if siswa:
        return render(request, 'form.html', {'siswa': siswa})
    return redirect('siswa_list')


def siswa_delete(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM siswa WHERE id = %s", [id])
        return redirect('siswa_list')

    siswa = ambil_satu_siswa(id)
    if siswa:
        return render(request, 'delete.html', {'siswa': siswa})
    return redirect('siswa_list')