# User Experience Specification

## Tata Warna (Theme)

| Peran     | Warna default | Digunakan untuk                          |
|-----------|----------------|-------------------------------------------|
| primary   | Cyan           | Judul, header tabel, prompt aktif          |
| success   | Green          | Pesan sukses, status "OK"                  |
| warning   | Yellow         | Peringatan non-fatal                       |
| error     | Red            | Pesan galat / kegagalan eksekusi           |
| muted     | Grey           | Teks sekunder, footer, hint                |

Tema dapat diganti melalui variabel lingkungan `CLI_THEME` (`default` atau `mono`),
lihat `config/settings.py`.

## Prinsip Tampilan

1. **Konsistensi**: setiap command output selalu memiliki header, isi, dan
   footer status (durasi eksekusi / jumlah hasil).
2. **Feedback instan**: proses yang berjalan lebih dari beberapa ratus
   milidetik wajib menampilkan spinner (`src/components/spinners.py`).
3. **Table-first**: hasil data tabular dirender dengan `tables.py`,
   bukan dicetak baris demi baris secara manual.
4. **Graceful pada non-TTY**: ketika output diarahkan ke file/pipe,
   warna ANSI otomatis dinonaktifkan (fallback ke tema `mono`).
5. **Prompt interaktif** (`prompts.py`) hanya dipicu jika argumen wajib
   tidak disediakan lewat flag — CLI tetap bisa dijalankan non-interaktif
   untuk kebutuhan scripting/automation.
