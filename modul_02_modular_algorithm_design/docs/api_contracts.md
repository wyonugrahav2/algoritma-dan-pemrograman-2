# API Contracts

Dokumen ini menetapkan kontrak input/output antar-modul, agar setiap
modul dapat dikembangkan dan diuji secara independen selama tetap
mematuhi kontrak yang disepakati di sini.

## 1. Kontrak `BaseModule`

Setiap modul WAJIB mengimplementasikan:

| Method             | Deskripsi                                                 |
| ------------------ | --------------------------------------------------------- |
| `initialize()`     | Dipanggil sekali sebelum eksekusi pertama.                |
| `execute(payload)` | Logika utama modul. Menerima & mengembalikan data.        |
| `cleanup()`        | Dipanggil setelah eksekusi selesai (sukses maupun gagal). |

## 2. Kontrak Payload per Modul

### `analytics`

- **Input**: `{"values": List[float]}`
- **Output**:
  ```json
  {
    "count": int,
    "mean": float,
    "median": float,
    "variance": float,
    "std_dev": float,
    "min": float,
    "max": float
  }
  ```

### `transformation`

- **Input** (salah satu):
  - `{"rows": List[Dict[str, Any]]}`
  - `{"values": List[Any]}`
- **Output**: struktur yang sama dengan input, namun sudah dibersihkan
  (whitespace di-strip, key dinormalisasi, nilai kosong dihapus).

### `validation`

- **Input**: `{"data": Any}`
- **Output**:
  ```json
  {
    "valid": bool,
    "errors": List[str]
  }
  ```

## 3. Kontrak Event Bus

Setiap kali sebuah modul selesai dieksekusi lewat `Dispatcher`, event
berikut dipublikasikan:

```
event_name: "module.<nama_modul>.completed"
payload:    <output modul tersebut>
```

Modul lain dapat `subscribe` ke event ini tanpa perlu mengetahui
detail implementasi modul yang mempublikasikannya.

## 4. Kontrak Error

Semua exception kustom aplikasi mewarisi `ModularAppError`
(`src/utils/error_handlers.py`). Modul TIDAK BOLEH melempar exception
generik Python tanpa membungkusnya, agar penanganan error di layer
atas (dispatcher/main) tetap konsisten.

## 5. Aturan Perubahan Kontrak

- Perubahan struktur input/output sebuah modul WAJIB diperbarui juga
  di dokumen ini.
- Perubahan yang bersifat _breaking_ (menghapus/mengubah tipe field)
  wajib menaikkan versi modul (lihat `base_algorithm.py -> version`).
