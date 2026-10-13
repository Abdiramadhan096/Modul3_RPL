import customtkinter as ctk
from tkinter import ttk, messagebox


class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Perpustakaan - Data Anggota")
        self.geometry("800x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ================= FRAME KIRI =================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota",
                     font=("Arial", 16, "bold")).pack(pady=15)

        self.entry_nama = ctk.CTkEntry(
            self.frame_kiri, placeholder_text="Masukkan Nama Anggota")
        self.entry_nama.pack(pady=10, padx=15, fill="x")

        self.entry_alamat = ctk.CTkEntry(
            self.frame_kiri, placeholder_text="Masukkan Alamat")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri, text="Simpan Data", fg_color="green",
            command=self.simpan_data)
        self.btn_simpan.pack(pady=10, padx=15, fill="x")

        self.btn_update = ctk.CTkButton(
            self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue",
            command=self.update_data)
        self.btn_update.pack(pady=10, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri, text="Hapus Data (Delete)", fg_color="red",
            command=self.hapus_data)
        self.btn_hapus.pack(pady=10, padx=15, fill="x")

        # ================= FRAME KANAN =================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Anggota Perpustakaan",
                     font=("Arial", 16, "bold")).pack(pady=15)

        kolom = ("nama", "alamat")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom,
                                  show="headings", height=15)
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")
        self.tabel.column("nama", width=180)
        self.tabel.column("alamat", width=250)
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        # Klik baris -> data tampil di form
        self.tabel.bind("<<TreeviewSelect>>", self.pilih_data)

    # ================= FUNGSI =================
    def bersihkan_form(self):
        self.entry_nama.delete(0, "end")
        self.entry_alamat.delete(0, "end")

    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        alamat = self.entry_alamat.get().strip()

        if not (nama and alamat):
            messagebox.showwarning("Peringatan", "Nama dan alamat harus diisi!")
            return

        self.tabel.insert("", "end", values=(nama, alamat))
        self.bersihkan_form()

    def pilih_data(self, event):
        terpilih = self.tabel.selection()
        if terpilih:
            nilai = self.tabel.item(terpilih[0], "values")
            self.bersihkan_form()
            self.entry_nama.insert(0, nilai[0])
            self.entry_alamat.insert(0, nilai[1])

    def update_data(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel dulu!")
            return
        self.tabel.item(terpilih[0], values=(
            self.entry_nama.get(), self.entry_alamat.get()))
        self.bersihkan_form()

    def hapus_data(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel dulu!")
            return
        self.tabel.delete(terpilih[0])
        self.bersihkan_form()


if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()