# 📚 Soal E-Library

Proyek ini adalah soal no 2 berbasis Django yang digunakan untuk mengelola katalog buku digital.  
Fitur utama meliputi upload buku (PDF + cover), konversi PDF ke gambar, pencarian, filter berdasarkan genre/favorit, serta manajemen akun pengguna.

---

##  Fitur Utama
-  **Autentikasi User**
  - Register, login, logout
  - Proteksi halaman dengan `@login_required`

- 📚 **Bagian Buku**
  - Tambah / edit / hapus buku
  - Upload file PDF & cover
  - Auto hitung jumlah halaman PDF (pakai **PyMuPDF**)
  - Konversi PDF menjadi gambar halaman

-  **Favorit Buku**
  - Tandai atau hapus tanda favorit
  - Filter khusus favorit

-  **Pencarian & Filter**
  - Pencarian berdasarkan judul, penulis, deskripsi, tahun
  - Filter berdasarkan genre
  - Pagination

-  **Profil Pengguna**
  - Menampilkan buku yang diupload oleh user

---

## 🛠️ Teknologi yang Digunakan
- [Django](https://www.djangoproject.com/) – Backend framework
- [SQLite3](https://www.sqlite.org/) – Database default
- [Bootstrap 5](https://getbootstrap.com/) – UI framework
- [Font Awesome](https://fontawesome.com/) – Ikon
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – Membaca & menghitung halaman PDF, konversi ke gambar
- Python 3.11 – 3.13(disarankan)

---

## ⚙️ Instalasi & Menjalankan

1. **Clone Repository**
   ```bash
   git clone <https://github.com/Roy000000000/Soal2_elibrary.git>
   cd elibrary
2. **Buat Virtual Environment**
   ```bash
    python -m venv venv
    venv\Scripts\activate #Win
    source venv/bin/activate  # (Linux/Mac)
4. **Install Dependencies**
   ```bash
    pip install -r requirements.txt
6. **Jalankan Server**
   ```bash
    python manage.py runserver
8. **Login ke akun yang sudah ada**
   ```bash
     usn: elibrary
     pass: Adminku123!








