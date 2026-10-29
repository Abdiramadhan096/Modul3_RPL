# Sistem Manajemen Perpustakaan

Aplikasi desktop untuk mengelola data perpustakaan, dibangun dengan **Python** dan **CustomTkinter**, menggunakan pola arsitektur **MVC (Model-View-Controller)** dan basis data **MySQL**.

## Deskripsi Singkat

Aplikasi ini membantu petugas perpustakaan mengelola koleksi buku dan data anggota melalui antarmuka grafis. Fitur utama:

- **Login dengan hash SHA-256.** Kata sandi tidak disimpan sebagai teks biasa, tetapi sebagai hash 64 karakter heksadesimal di tabel `users`.
- **Otorisasi berbasis role.** Pengguna dengan role `admin` dapat menambah, memperbarui, dan menghapus data buku. Pengguna dengan role `anggota` hanya dapat melihat data, sedangkan form input dan tombol aksi dikunci.
- **Manajemen data buku (CRUD).** Simpan, perbarui, dan hapus data buku dengan memilih baris pada tabel.
- **Manajemen data anggota (CRUD).** Simpan, perbarui, dan hapus data anggota.
- **Registrasi pengguna.** Metode `register_user` pada `UserModel` otomatis mengubah kata sandi menjadi hash SHA-256 sebelum disimpan.
- **Pengujian dan CI otomatis.** Unit test dengan `pytest` dan pemeriksaan kode dengan `flake8` dijalankan otomatis oleh GitHub Actions pada setiap push.

## Teknologi

| Komponen | Keterangan |
|---|---|
| Bahasa | Python 3.11 atau lebih baru |
| Antarmuka | CustomTkinter |
| Basis data | MySQL (dijalankan melalui Laragon) |
| Driver database | mysql-connector-python |
| Pengujian | pytest |
| Linter | flake8 |
| CI | GitHub Actions |

## Struktur Direktori MVC

```
Modul3_RPL/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml       # Konfigurasi CI (flake8 + pytest)
├── config/
│   └── database.py               # Koneksi ke MySQL
├── models/                       # MODEL: logika data dan query SQL
│   ├── buku_model.py
│   ├── anggota_model.py
│   └── user_model.py             # Autentikasi dan registrasi (SHA-256)
├── views/                        # VIEW: tampilan antarmuka (CustomTkinter)
│   ├── login_view.py
│   ├── buku_view.py
│   └── anggota_view.py
├── controllers/                  # CONTROLLER: penghubung Model dan View
│   ├── auth_controller.py
│   ├── buku_controller.py
│   └── anggota_controller.py
├── tests/                        # Unit test (pytest)
│   ├── test_buku.py
│   └── test_auth.py
├── main.py                       # Titik masuk aplikasi
├── requirements.txt              # Daftar dependensi
└── README.md
```

Peran tiap lapisan:

| Lapisan | Tanggung jawab |
|---|---|
| **Model** | Berkomunikasi dengan database: menjalankan query SELECT, INSERT, UPDATE, dan DELETE. |
| **View** | Menampilkan form, tombol, dan tabel. Tidak berisi logika bisnis. |
| **Controller** | Menerima aksi pengguna dari View, memprosesnya lewat Model, lalu memperbarui View. |

## Panduan Instalasi dan Konfigurasi Database MySQL

### 1. Prasyarat

- [Python](https://www.python.org/downloads/) 3.11 atau lebih baru
- [Laragon](https://laragon.org/) (menyediakan MySQL)
- [Git](https://git-scm.com/)

### 2. Unduh proyek

```bash
git clone <URL-repositori-Anda>
cd Modul3_RPL
```

### 3. Buat dan aktifkan virtual environment

```bash
python -m venv env
env\Scripts\activate
```

> Pada Linux atau macOS gunakan `source env/bin/activate`.

### 4. Pasang dependensi

```bash
pip install -r requirements.txt
```

### 5. Siapkan database MySQL

1. Buka **Laragon**, lalu klik **Mulai Semua** agar layanan MySQL berjalan.
2. Buka terminal MySQL (menu **Terminal** di Laragon, atau phpMyAdmin), lalu jalankan:

```sql
CREATE DATABASE perpustakaan;
USE perpustakaan;

CREATE TABLE buku (
    id_buku INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(150) NOT NULL,
    penulis VARCHAR(100) NOT NULL,
    tahun_terbit INT NOT NULL
);

CREATE TABLE anggota (
    id_anggota INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    alamat VARCHAR(255) NOT NULL
);

CREATE TABLE peminjaman (
    id_pinjam INT AUTO_INCREMENT PRIMARY KEY,
    id_buku INT NOT NULL,
    id_anggota INT NOT NULL,
    tanggal_pinjam DATE NOT NULL,
    tanggal_kembali DATE,
    FOREIGN KEY (id_buku) REFERENCES buku(id_buku),
    FOREIGN KEY (id_anggota) REFERENCES anggota(id_anggota)
);

CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL,
    role ENUM('admin','anggota') NOT NULL DEFAULT 'anggota'
);
```

3. Tambahkan dua akun uji coba. Kata sandi disimpan dalam bentuk hash SHA-256 menggunakan fungsi `SHA2(..., 256)` milik MySQL:

```sql
INSERT INTO users (username, password, role) VALUES
('petugas',   SHA2('admin123', 256), 'admin'),
('mahasiswa', SHA2('user123', 256),  'anggota');
```

4. Pastikan hasilnya benar. Kolom `password` harus berisi 64 karakter acak, bukan teks asli:

```sql
SELECT * FROM users;
```

| Username | Kata sandi (untuk login) | Role |
|---|---|---|
| `petugas` | `admin123` | admin |
| `mahasiswa` | `user123` | anggota |

> Akun di atas hanya untuk uji coba. Ganti atau hapus akun tersebut pada penggunaan sebenarnya.

### 6. Sesuaikan konfigurasi koneksi (jika perlu)

Pengaturan koneksi berada di `config/database.py`. Nilai bawaan sesuai Laragon:

| Pengaturan | Nilai bawaan |
|---|---|
| Host | `localhost` |
| Database | `perpustakaan` |
| Username | `root` |
| Password | *(kosong)* |

Jika MySQL Anda memakai username atau password lain, ubah nilainya di file tersebut.

## Cara Menjalankan Aplikasi

1. Pastikan layanan **MySQL di Laragon** sudah berjalan.
2. Aktifkan virtual environment (`env\Scripts\activate`).
3. Jalankan dari folder utama proyek:

```bash
python main.py
```

4. Jendela **Login** akan muncul. Masuk menggunakan akun uji coba:

| Login sebagai | Hasil |
|---|---|
| `petugas` / `admin123` (admin) | Semua tombol aktif: Simpan, Perbarui, dan Hapus |
| `mahasiswa` / `user123` (anggota) | Form input dan tombol aksi terkunci. Hanya dapat melihat data. |

5. Untuk memperbarui atau menghapus data buku (admin): klik satu baris pada tabel, lalu tekan **Perbarui Data** atau **Hapus Data**.

> Untuk membuka halaman data anggota secara langsung, ubah isi `main.py` agar memanggil `AnggotaController` (`AnggotaController().run()`).

## Menjalankan Pengujian

Jalankan dari folder utama proyek:

```bash
python -m pytest -v
```

Pemeriksaan kualitas kode dengan flake8 (sama dengan yang dijalankan di CI):

```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Continuous Integration

Setiap `git push` atau pull request ke branch `main` memicu workflow GitHub Actions di `.github/workflows/ci_pipeline.yml` dengan urutan:

1. Mengambil kode dari repositori
2. Menyiapkan Python 3.11
3. Menginstal dependensi dari `requirements.txt`
4. Memeriksa kode dengan **flake8**
5. Menjalankan unit test dengan **pytest**

## Membuat Berkas Eksekusi (.exe)

Aplikasi dapat dipaketkan menjadi satu berkas `.exe` dengan PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Hasilnya ada di folder `dist/`. MySQL harus tetap berjalan saat aplikasi dibuka.

## Pembuat

Moh Abdi Ramadhan