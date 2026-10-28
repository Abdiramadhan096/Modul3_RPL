import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        # Inisialisasi Model dan View
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menyimpan id_buku dari baris yang sedang dipilih
        self.id_terpilih = None

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)

        # Binding klik baris tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol simpan
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')

            # Bersihkan form input
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.id_terpilih = None
        # Hilangkan highlight di tabel
        self.view.tabel.selection_remove(self.view.tabel.selection())

    def pilih_baris(self,event):
        """Dipanggil saat pengguna mengklik baris di tabel."""
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return

        # Ambil nilai kolom dari baris yang diklik
        nilai = self.view.tabel.item(pilihan[0], "values")
        self.id_terpilih = nilai[0]  # id_buku

        # Isi form dengan data baris tersebut
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_judul.insert(0, nilai[1])

        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_penulis.insert(0, nilai[2])

        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_tahun.insert(0, nilai[3])

    def update_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin diperbarui!")
            return
    
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
    
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
    
        berhasil = self.model.update_buku(self.id_terpilih, judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")
    
    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
            return
    
        konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if not konfirmasi:
            return
    
        berhasil = self.model.delete_buku(self.id_terpilih)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")
    

    # Fungsi untuk menjalankan aplikasi
    def run(self):
        self.view.mainloop()