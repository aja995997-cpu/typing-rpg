Tentu, berikut adalah draft README.md yang profesional dan lengkap untuk repositori GitHub kamu. File ini mencakup deskripsi proyek, fitur, cara instalasi, dan penjelasan struktur data.

Salin kode di bawah ini dan simpan sebagai file bernama README.md di folder proyek kamu.

code
Markdown
download
content_copy
expand_less
# 🚗 Python TypeRacer - Multi User RPG Edition

**Python TypeRacer** adalah game mengetik cepat (typing game) berbasis desktop yang dibangun menggunakan Python dan **CustomTkinter**. Game ini menggabungkan latihan mengetik dengan elemen RPG ringan, sistem ekonomi, dan manajemen akun multi-user.

![Status Proyek](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![UI](https://img.shields.io/badge/UI-CustomTkinter-orange)

## 📸 Screenshots
*(Disarankan untuk menambahkan screenshot aplikasi di sini agar repo terlihat menarik)*
> ![Halaman Login](link_gambar_login_kamu.png)
> ![Gameplay](link_gambar_gameplay_kamu.png)

## ✨ Fitur Utama

### 🔐 Sistem Multi-User
*   **Login & Register:** Buat akun baru atau masuk ke akun yang sudah ada.
*   **Fitur "Ingat Saya":** Auto-login saat aplikasi dibuka kembali.
*   **Keamanan Data:** Progres (koin, skin, achievement) disimpan terpisah untuk setiap pengguna.

### 🎮 Mode Permainan
1.  **Arcade Mode:** Pilih tingkat kesulitan (level) dan lawan bot dengan kecepatan bervariasi.
2.  **Story Mode (Mode Cerita):** Ikuti alur cerita motivasi per chapter. Selesaikan chapter untuk membuka achievement.

### 🏆 Progres & Ekonomi
*   **Toko Kendaraan (Shop):** Gunakan koin yang didapat dari balapan untuk membeli skin kendaraan baru (Mobil, UFO, Roket, Naga, dll).
*   **Sistem Mata Uang:** Dapatkan koin berdasarkan kecepatan (WPM) dan kemenangan.
*   **Achievements:** Klaim hadiah koin setelah menamatkan cerita.
*   **Target List:** Lacak bot mana saja yang sudah berhasil kamu kalahkan.

### 📊 Statistik & Peringkat
*   **Leaderboard Global:** Bandingkan kekayaan koinmu dengan pemain lain. Top 3 mendapat warna khusus (Emas, Perak, Perunggu).
*   **Riwayat Pertandingan:** Catatan detail setiap balapan (Lawan, WPM, Akurasi, Tanggal) dengan sistem paginasi halaman.
*   **Live WPM & Akurasi:** Statistik real-time saat mengetik.

### 🎨 Antarmuka Modern
*   Menggunakan tema "Dark Mode" yang elegan.
*   Animasi balapan visual menggunakan Canvas.
*   Update UI instan (tanpa reload window) saat membeli item atau klaim hadiah.

## 🛠️ Prasyarat

Pastikan kamu sudah menginstal **Python 3.x**.
Pustaka eksternal yang dibutuhkan hanyalah **CustomTkinter**.

```bash
pip install customtkinter

Jika kamu belum memiliki tkinter (biasanya sudah bawaan Python), instal sesuai OS kamu:

Windows: Sudah terinstall saat install Python.

Linux (Ubuntu/Debian): sudo apt-get install python3-tk

🚀 Cara Menjalankan

Clone repositori ini:

code
Bash
download
content_copy
expand_less
git clone https://github.com/username-kamu/nama-repo-kamu.git
cd nama-repo-kamu

Jalankan file utama:

code
Bash
download
content_copy
expand_less
python main.py
# Atau sesuaikan dengan nama file kode kamu
📂 Struktur File Data

Game ini akan secara otomatis membuat file JSON berikut jika belum ada:

users.json: Menyimpan data akun, password (simulasi), koin, skin yang dimiliki, dan progres achievement.

history.json: Menyimpan log riwayat pertandingan semua user.

story_mode.json: Berisi teks dan judul untuk Mode Cerita.

typing_texts.json: Berisi database kata/kalimat untuk Mode Arcade.

Contoh isi typing_texts.json agar game lebih seru:
Kamu bisa mengedit file ini manual untuk menambah variasi kata.

code
JSON
download
content_copy
expand_less
{
    "level_data": {
        "Level 1 (Mudah)": [
            "kucing lari kencang",
            "buku baru saya"
        ],
        "Level 2 (Sedang)": [
            "pemrograman python sangat menyenangkan",
            "konsistensi adalah kunci kesuksesan"
        ]
    }
}
🤝 Kontribusi

Kontribusi sangat diterima! Jika kamu ingin menambah fitur baru atau memperbaiki bug:

Fork repo ini.

Buat branch fitur baru (git checkout -b fitur-keren).

Commit perubahan kamu (git commit -m 'Menambah fitur keren').

Push ke branch (git push origin fitur-keren).

Buat Pull Request.

📝 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan portofolio. Silakan gunakan dan modifikasi dengan bebas.

Dibuat dengan ❤️ menggunakan Python.
