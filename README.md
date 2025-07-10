# Scripts Perbandingan Data Mahasiswa

**Author:** Denni Septiyaji

## Deskripsi

Proyek ini berisi script Python untuk membandingkan data ID mahasiswa dan ID calon mahasiswa dari berbagai file CSV. Script akan menganalisis konsistensi data antar file dan menghasilkan laporan perbandingan dalam format Markdown dan HTML.

## Fitur

- ✅ **Analisis Multi-file**: Membandingkan data dari beberapa file CSV sekaligus
- ✅ **Resume Statistik**: Menampilkan ringkasan analisis di awal laporan
- ✅ **Deteksi Anomali**: Mengidentifikasi ID yang tidak konsisten antar file
- ✅ **Dual Output**: Menghasilkan laporan dalam format Markdown dan HTML
- ✅ **Konfigurasi Fleksibel**: Mudah dikonfigurasi untuk berbagai struktur file CSV

## Struktur Proyek

```
scripts/
├── data/                   # Folder berisi file CSV yang akan dianalisis
│   ├── file1.csv
│   ├── file2.csv
│   └── file3.csv
├── result/                 # Folder output hasil analisis
│   ├── comparison.md       # Laporan dalam format Markdown
│   └── comparison.html     # Laporan dalam format HTML
├── src/                    # Source code
│   ├── compare_ids.py      # Script utama
│   ├── config.py           # Konfigurasi file yang akan dianalisis
│   └── config-backup.py    # Backup konfigurasi
└── README.md              # Dokumentasi proyek
```

## Instalasi dan Penggunaan

### Prasyarat

- Python 3.7 atau lebih baru
- Module standar Python (csv, pathlib, collections)

### Langkah-langkah

1. **Clone atau download proyek ini**
   ```bash
   git clone <repository-url>
   cd scripts
   ```

2. **Siapkan file CSV** di folder `data/`

3. **Konfigurasi file yang akan dianalisis** di `src/config.py`:
   ```python
   to_be_checked = [
       {
           "filename": "point1.csv",
           "delimiter": ";",
           "idcalonmahasiswa": 1,    # Index kolom ID calon mahasiswa
           "idmahasiswa": 6          # Index kolom ID mahasiswa
       },
       # ... file lainnya
   ]
   ```

4. **Jalankan script**:
   ```bash
   cd src
   python compare_ids.py
   ```

5. **Lihat hasil** di folder `result/`:
   - `comparison.md` - Laporan format Markdown
   - `comparison.html` - Laporan format HTML

## Format Konfigurasi

Setiap file dalam konfigurasi memiliki format sebagai berikut:

```python
{
    "filename": "nama_file.csv",     # Nama file di folder data/
    "delimiter": ";",                # Delimiter CSV (;, ,, \t, dll)
    "idcalonmahasiswa": 1,          # Index kolom ID calon mahasiswa (0-based)
    "idmahasiswa": 6                # Index kolom ID mahasiswa (0-based)
}
```

**Catatan:** 
- Index kolom dimulai dari 0
- Jika file tidak memiliki salah satu jenis ID, set nilai ke `None`

## Format Output

### Resume (di awal laporan)
- **Total ID unik**: Jumlah total ID yang ditemukan
- **ID yang ada di semua file**: ID yang konsisten di semua file
- **ID yang janggal**: ID yang tidak ada di semua file (beserta daftar file yang tidak memiliki ID tersebut)

### Tabel Perbandingan
Tabel yang menunjukkan keberadaan setiap ID di setiap file dengan simbol:
- ✔️ = ID ada di file
- ❌ = ID tidak ada di file

## Contoh Output

```markdown
# RESUME PERBANDINGAN

## ID Calon Mahasiswa
- **Total ID unik**: 150
- **ID yang ada di semua file**: 120
- **ID yang janggal (tidak lengkap)**: 30

### ID Janggal ID Calon Mahasiswa:
- **12345** tidak ada di file: point2.csv, point3.csv
- **67890** tidak ada di file: point1.csv

# DAFTAR PERBANDINGAN

## ID Calon Mahasiswa
| idcalonmahasiswa | point1.csv | point2.csv | point3.csv |
|------------------|------------|------------|------------|
| 12345           | ✔️          | ❌          | ❌          |
| 67890           | ❌          | ✔️          | ✔️          |
```

## Troubleshooting

### Error: File tidak ditemukan
- Pastikan file CSV ada di folder `data/`
- Periksa nama file di `config.py` sudah sesuai

### Error: Index out of range
- Periksa index kolom di `config.py`
- Pastikan index tidak melebihi jumlah kolom di file CSV

### Encoding Error
- Pastikan file CSV menggunakan encoding UTF-8
- Jika menggunakan Excel, save as CSV dengan encoding UTF-8

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini:

1. Fork repository
2. Buat branch fitur baru
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

## Lisensi

Proyek ini dibuat untuk keperluan analisis data internal.

---

**Author:** Denni Septiyaji  
**Created:** 2025  
**Last Updated:** July 2025
