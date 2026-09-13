# Memory-Efficient I/O: Generator & Iterator

## Generator vs List

```python
# Boros memori — seluruh hasil disimpan di list sekaligus
def load_all(path):
    return [json.loads(line) for line in open(path)]

# Hemat memori — satu baris pada satu waktu
def load_lazy(path):
    for line in open(path):
        yield json.loads(line)
```

Perbedaan intinya: `list comprehension` mengeksekusi seluruh isi sebelum
mengembalikan hasil apa pun, sementara `generator function` (memakai
`yield`) menghasilkan objek *generator* yang baru mengeksekusi kode
selangkah demi selangkah, tepat saat `next()` dipanggil oleh konsumen.

## Chunking

Untuk operasi yang tetap butuh sekelompok baris sekaligus (misalnya
batch-insert ke database), `read_chunks()` di `file_reader.py`
mengelompokkan aliran generator menjadi potongan berukuran tetap
(`CHUNK_SIZE`) tanpa pernah menahan lebih dari satu chunk di memori.

## Mengukur Penggunaan Memori

Modul ini memakai `tracemalloc` (`src/ui/metrics_presenter.py`) untuk
mencatat penggunaan memori puncak (*peak memory*) selama eksekusi
pipeline, sehingga efek dari pendekatan streaming dapat diverifikasi
secara empiris, bukan hanya diasumsikan secara teoritis.

## Kapan TIDAK Memakai Generator

- Ketika data harus diakses berkali-kali (generator hanya bisa
  di-iterasi sekali; setelah habis harus dibuat ulang).
- Ketika urutan pemrosesan memerlukan *random access* (indexing),
  bukan hanya iterasi berurutan.
- Ketika dataset memang kecil dan kesederhanaan kode lebih penting
  daripada efisiensi memori marjinal.
