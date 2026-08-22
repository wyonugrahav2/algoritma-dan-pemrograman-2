# IPO Specification — Advanced IPO Problem Analysis

## 1. Tujuan
Dokumen ini memetakan komponen **Input, Process, dan Output** untuk sistem CLI
Advanced IPO, mendefinisikan syarat batas (boundary conditions), tipe data
yang diizinkan, serta kontrak antar layer.

## 2. Input

| Aspek | Ketentuan |
|---|---|
| Tipe data diizinkan | `integer`, `float`, `string`, `list[float]` |
| Sumber input | CLI flag (`--values`), mode interaktif (stdin) |
| Panjang maksimum string | 500 karakter (`Settings.max_input_length`) |
| Batas nilai numerik | `MIN_VALUE_THRESHOLD` s.d. `MAX_VALUE_THRESHOLD` (±1.000.000) |
| Delimiter list | koma (`,`), whitespace di sekitar elemen diabaikan |
| Kondisi ditolak | input kosong, tipe tidak sesuai, nilai di luar rentang, gagal parsing |

## 3. Process

| Tahap | Fungsi | Deskripsi |
|---|---|---|
| 1 | `filter_outliers` | Membuang nilai yang menyimpang > N standar deviasi dari rata-rata |
| 2 | `sort_values` | Mengurutkan nilai (ascending secara default) |
| 3 | `normalize_values` | Min-max scaling ke rentang [0, 1] |

Pipeline bersifat **berurutan (sequential)** dan berhenti pada tahap pertama
yang gagal (`stop_on_error=True` secara default), melempar
`PipelineBrokenError` yang membungkus exception asli.

## 4. Output

| Format | Ekstensi | Penggunaan |
|---|---|---|
| `table` | — | Tampilan default di terminal |
| `json` | `.json` | Struktur data lengkap, cocok untuk integrasi/API |
| `plain` | `.txt`, `.log` | Ringkasan teks polos |
| `csv` | `.csv` | Ekspor tabular untuk spreadsheet |

## 5. Kontrak Antar Layer

```
RawInput → (validators) → ValidatedInput → (parsers)
        → Pipeline (transformers) → PipelineReport
        → (formatters) → representasi format
        → (presenters / exporters) → terminal / file
```

Setiap layer **hanya** boleh berkomunikasi melalui objek domain yang
didefinisikan di `src/domain/models.py`. Tidak ada layer yang mengakses
detail implementasi layer lain secara langsung (mis. `output_layer` tidak
boleh membaca `sys.argv` dari `input_layer`).

## 6. Kode Galat

Lihat `config/constants.py` → `ErrorCode` untuk daftar lengkap kode galat
kustom (`E1xxx` untuk Input, `E2xxx` untuk Process, `E3xxx` untuk Output).
