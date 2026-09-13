# Modul 11 — Modern Data Pipelines

CLI Modern Data Pipeline & Stream Processor: membaca, memfilter,
mentransformasi, dan mengalirkan data berukuran besar (CSV/JSON/log)
secara efisien tanpa membuat RAM penuh, menggunakan pendekatan
**Lazy Evaluation** berbasis generator Python.

## Instalasi

```bash
cd modul_11_modern_data_pipelines
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

`ijson` (opsional, untuk streaming JSON array besar) dapat dipasang lewat:

```bash
pip install -e ".[streaming-json]"
```

## Penggunaan Cepat

Membaca CSV, membersihkan & memperkaya data, lalu menulis ke JSONL:

```bash
python main.py --input data.csv --format csv \
    --output result.jsonl --output-format jsonl
```

Menghitung agregat (sum/avg/min/max) per grup selama streaming:

```bash
python main.py --input data.csv --agg-field value --group-by category
```

Membaca dari stdin (JSON Lines) — cocok untuk pipe dari proses lain:

```bash
cat events.jsonl | python main.py --stdin --output out.jsonl
```

Tanpa `--output`, hasil ditampilkan sebagai preview di terminal (default
5 baris pertama, dapat diatur lewat `--preview`).

## Menjalankan Test

```bash
pytest
```

Tiga suite pengujian utama:

- `test_generator_pipeline.py` — memverifikasi bahwa pipeline benar-benar
  lazy (tidak ada eksekusi sebelum dikonsumsi).
- `test_chunking_memory.py` — memverifikasi konsumsi RAM tetap konstan
  saat memproses berkas berukuran besar (20.000 baris).
- `test_data_integrity.py` — memverifikasi tidak ada baris yang hilang
  atau terduplikasi dari input hingga output.

## Struktur Proyek

```
modul_11_modern_data_pipelines/
├── config/            # Pengaturan chunk size, buffer, skema data
├── docs/              # Dokumentasi arsitektur streaming & memory I/O
├── src/
│   ├── sources/       # file_reader.py, stream_reader.py (Generator-based)
│   ├── transformers/  # data_cleanser.py, enricher.py, aggregator.py
│   ├── sinks/         # file_writer.py, console_sink.py
│   ├── pipeline/      # stream_chain.py, backpressure.py
│   └── ui/            # progress_tracker.py, metrics_presenter.py
├── tests/
├── main.py            # Entry point CLI
└── pyproject.toml
```

## Arsitektur Singkat

```
source (generator) -> cleanser -> enricher -> backpressure -> [aggregator] -> sink
```

Setiap panah adalah generator yang meneruskan `yield` ke tahap
berikutnya — lihat `docs/streaming_architecture.md` untuk penjelasan
lebih dalam tentang Lazy Evaluation dan `docs/memory_efficient_io.md`
untuk perbandingan generator vs list.
