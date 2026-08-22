# 🤝 Panduan Kontribusi

Terima kasih telah tertarik untuk berkontribusi pada repositori **Algoritma dan Pemrograman 2 (Advanced CLI & Algorithmic Systems)**!

Untuk menjaga kualitas kode, konsistensi arsitektur, dan kerapian riwayat Git, harap ikuti panduan berikut sebelum melakukan komit atau _Pull Request_.

---

## 🛠️ Alur Kerja & Git Branching

1. **Main Branch Protection**:
   - Branch `main` digunakan sebagai lini rilis utama yang stabil.
   - Setiap pengerjaan fitur baru wajib menggunakan _Feature Branch_ tersendiri.

2. **Penamaan Branch**:
   - Feature: `feat/modul-XX-nama-fitur`
   - Bugfix: `fix/modul-XX-deskripsi-issue`
   - Documentation: `docs/modul-XX-deskripsi`

---

## 📝 Format Conventional Commits

Setiap pesan komit wajib mengikuti standar **Conventional Commits**:

- `feat(...)`: Penambahan fitur baru (misal: `feat(domain): add data models`)
- `fix(...)`: Perbaikan bug/error
- `docs(...)`: Perubahan dokumentasi
- `test(...)`: Penambahan atau perbaikan unit/integration test
- `chore(...)`: Perubahan konfigurasi, perkakas, atau berkas build

---

## 🏗️ Standar Arsitektur Kode

Setiap modul dikembangkan menggunakan prinsip **Software Engineering Best Practices**:

- **Decoupled Architecture**: Pisahkan tugas tiap layer (_Domain_, _Input_, _Process_, _Output_, _Infrastructure_).
- **Type Hinting**: Gunakan type annotation Python secara konsisten pada setiap fungsi dan kelas.
- **Error Handling**: Manfaatkan hirarki _Custom Exception_ tanpa membiarkan aplikasi runtuh secara mendadak (_crash_).

---

## 👥 Tim Pengembang

- **Wyo Nugraha** ([@wyonugrahav2](https://github.com/wyonugrahav2)) - Lead Developer & Author
