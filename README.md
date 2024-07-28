# Telegram Bot with Groq API Integration

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Key Components](#key-components)
7. [GUI Interface](#gui-interface)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)

---

# Bahasa Indonesia

## 📜 Pendahuluan

Bot Telegram ini adalah chatbot canggih yang terintegrasi dengan Groq API untuk menyediakan percakapan yang didukung oleh AI. Fitur-fiturnya meliputi beberapa model AI, pemilihan karakter, dan antarmuka pengguna grafis (GUI) untuk manajemen yang mudah.

## 🛠️ Prasyarat

- Python 3.7+
- Perpustakaan `telebot`
- Perpustakaan `requests`
- Perpustakaan `PyQt6`
- Token Bot Telegram
- Kunci API Groq

## ⚙️ Pengaturan

1. Klon repositori atau unduh skrip.

2. Instal perpustakaan yang diperlukan:

   ```sh
   pip install pyTelegramBotAPI requests PyQt6
   ```

3. Buat file `api-bot-groq.json` di direktori yang sama dengan skrip dengan konten berikut:

   ```json
   {
       "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token_here",
       "GROQ_API_KEY": "your_groq_api_key_here"
   }
   ```

4. Buat file `characters.json` di direktori yang sama dengan definisi karakter (contoh disediakan di bagian [Konfigurasi](#konfigurasi)).

## 🛠️ Konfigurasi

### 🔑 Kunci API

Simpan kunci API Anda di file `api-bot-groq.json`:

```json
{
    "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token_here",
    "GROQ_API_KEY": "your_groq_api_key_here"
}
```

### 🎭 Karakter

Definisikan karakter dalam file `characters.json`:

```json
{
    "default": {
        "name": "Asisten Default",
        "description": "Asisten AI yang membantu."
    },
    "historian": {
        "name": "Pakar Sejarah",
        "description": "AI yang mengkhususkan diri dalam fakta dan peristiwa sejarah."
    }
}
```

## 🚀 Penggunaan

1. Jalankan skrip:

   ```sh
   python your_script_name.py
   ```

2. Gunakan GUI untuk memulai dan menghentikan bot.

3. Berinteraksi dengan bot di Telegram menggunakan perintah berikut:

   - `/start`: Memulai percakapan
   - `/menu`: Menampilkan menu utama
   - Gunakan tombol inline untuk mengganti model, karakter, atau mengakses fitur lainnya

## 🔍 Komponen Utama

### 💬 Fungsionalitas Bot

- Dukungan beberapa model AI
- Pemilihan karakter
- Manajemen konteks percakapan
- Transkripsi pesan suara
- Generasi saran untuk topik percakapan

### 📜 Penanganan Pesan

- `/start`: Mengirim pesan selamat datang
- `/menu`: Menampilkan menu utama
- Penanganan kueri callback untuk tombol inline
- Penanganan pesan suara untuk transkripsi
- Penanganan pesan umum untuk percakapan

## 🖥️ Antarmuka GUI

Antarmuka pengguna grafis menyediakan fitur berikut:

- Memulai Bot: Memulai operasi bot
- Menghentikan Bot: Menghentikan bot dengan baik
- Tampilan Log: Menampilkan aktivitas bot dan kesalahan

## 🔧 Kustomisasi

### 🔄 Menambahkan Model Baru

Tambahkan nama model baru ke daftar `AVAILABLE_MODELS` dalam skrip.

### 🎭 Menambahkan Karakter Baru

Tambahkan definisi karakter baru ke file `characters.json`.

### ⚙️ Memodifikasi Perilaku Bot

Sesuaikan fungsi `handle_message` untuk mengubah cara bot memproses dan merespons pesan.

## 🚑 Pemecahan Masalah

- **Bot Tidak Merespons**: Periksa koneksi internet Anda dan verifikasi Token Bot Telegram.
- **Kesalahan API**: Pastikan kunci API Groq Anda benar dan memiliki izin yang cukup.
- **GUI Tidak Berjalan**: Verifikasi bahwa PyQt6 telah diinstal dengan benar.
- **Masalah Karakter/Model**: Periksa file `characters.json` dan daftar `AVAILABLE_MODELS` untuk format yang benar.

Untuk masalah lainnya, periksa output konsol untuk pesan kesalahan dan rujuk dokumentasi perpustakaan yang bersangkutan untuk `telebot`, `requests`, dan `PyQt6`.
