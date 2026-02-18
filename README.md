# 🌿 GitHub Auto Contribute

Program Python untuk otomatis membuat kontribusi di GitHub contribution graph.

## 📋 Cara Penggunaan

### 1. Persiapan (lakukan sekali saja)

Pastikan folder ini sudah terhubung ke GitHub:

```bash
git init
git remote add origin https://github.com/username/nama-repo.git
```

Pastikan git user sudah dikonfigurasi:

```bash
git config --global user.name "Nama Kamu"
git config --global user.email "email@kamu.com"
```

### 2. Jalankan Program

```bash
python auto_contribute.py
```

### 3. Ikuti Instruksi

Program akan:
1. ✅ Mengecek apakah folder terhubung ke git
2. ✅ Mengecek remote (origin) dan konfigurasi user
3. 🔢 Meminta input jumlah contribute yang diinginkan
4. 🚀 Melakukan commit sebanyak yang dipilih
5. 📤 Menawarkan push ke GitHub

## 📁 File

| File | Keterangan |
|------|------------|
| `auto_contribute.py` | Script utama |
| `data.txt` | File yang dimodifikasi setiap commit |

## ⚠️ Catatan

- Setiap commit memodifikasi `data.txt` dengan timestamp unik
- Contribution graph GitHub diperbarui setelah push berhasil
- Pastikan repo GitHub sudah dibuat sebelum push
