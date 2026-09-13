# Streaming Architecture: Stream Processing vs Batch Loading

## 1. Batch Loading (Pendekatan Tradisional)

Pada pendekatan batch, seluruh dataset dimuat penuh ke memori sebelum
diproses:

```python
data = json.load(open("huge_file.json"))  # seluruh file masuk RAM
for row in data:
    process(row)
```

**Kelemahan**: penggunaan memori tumbuh linear terhadap ukuran berkas.
Berkas berukuran 10GB membutuhkan (kurang lebih) 10GB+ RAM sebelum baris
pertama sempat diproses.

## 2. Stream Processing (Pendekatan Modul Ini)

Dengan generator, data mengalir satu rekaman (atau satu chunk kecil) pada
satu waktu:

```python
def read_lazy(path):
    with open(path) as f:
        for line in f:
            yield json.loads(line)
```

Memori yang digunakan pada dasarnya konstan (`O(1)` terhadap N baris),
karena hanya baris yang sedang diproses yang berada di RAM.

## 3. Lazy Evaluation dalam Pipeline

`StreamChain` (lihat `src/pipeline/stream_chain.py`) menyusun beberapa
generator menjadi satu rangkaian. Tidak ada komputasi yang terjadi saat
`chain.add_stage(...)` dipanggil — eksekusi baru dimulai ketika consumer
(sink) mulai menarik data lewat iterasi (`for row in chain.run(): ...`).

```
source --(yield)--> cleanser --(yield)--> enricher --(yield)--> sink
```

Setiap tahap adalah generator function; Python hanya mengeksekusi kode di
dalamnya sampai baris `yield` berikutnya diminta oleh consumer.

## 4. Backpressure

Jika `source` menghasilkan data lebih cepat daripada `sink` mampu
menulisnya, buffer internal bisa membengkak. `BackpressureController`
menyisipkan bounded buffer dan menerapkan jeda (`throttle`) otomatis saat
buffer mendekati kapasitas maksimum (`high watermark`), lalu melepas jeda
saat buffer kembali turun (`low watermark`).

## 5. Trade-off

| Aspek              | Batch Loading        | Stream Processing        |
|--------------------|-----------------------|---------------------------|
| Memori              | O(N)                  | O(1) / O(chunk_size)      |
| Latensi hasil pertama | Tinggi (tunggu load penuh) | Rendah (langsung mengalir) |
| Kompleksitas kode   | Sederhana             | Perlu desain generator    |
| Cocok untuk         | Dataset kecil–menengah | Dataset raksasa / real-time |
