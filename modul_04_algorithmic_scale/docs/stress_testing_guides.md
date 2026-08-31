# Panduan Metodologi Stress Testing

Dokumen ini menjelaskan alur kerja `stress testing engine` pada modul
Algorithmic Scale, mulai dari pembuatan data sintetis hingga
pembacaan laporan akhir.

## 1. Tujuan

Menguji daya tahan (skalabilitas) sebuah fungsi/algoritma terhadap
kenaikan ukuran data (N), dan secara otomatis:

- Mengukur waktu eksekusi pada tiap tingkatan skala.
- Mengukur puncak penggunaan memori (peak memory usage).
- Mendeteksi **bottleneck** — titik di mana waktu eksekusi melonjak
  tidak proporsional terhadap kenaikan N.
- Menebak kelas kompleksitas Big-O yang paling mendekati perilaku nyata.

## 2. Alur Kerja (Pipeline)

1. **Pilih target algoritma** dari `src/algorithms/`.
2. **Tentukan tingkatan skala** yang ingin diuji (`config/scale_levels.py`),
   contohnya dari Tiny hingga Huge.
3. **Bangkitkan data sintetis** melalui `src/datasets/generators.py`
   dan/atau skenario Best/Average/Worst Case dari `data_cases.py`.
4. **Jalankan profiler**:
   - `time_profiler.py` mencatat durasi eksekusi (dengan pengulangan
     untuk mengurangi noise, lihat `REPEATS_PER_MEASUREMENT`).
   - `memory_profiler.py` mencatat puncak alokasi memori selama
     eksekusi berlangsung.
5. **Bandingkan terhadap ambang batas** (`EXECUTION_TIMEOUT_SECONDS`,
   `MAX_MEMORY_MB`). Jika terlampaui, level skala tersebut ditandai
   sebagai **timeout** atau **memory-exceeded**, dan pengujian ke
   skala yang lebih besar dihentikan otomatis untuk skenario tsb.
6. **Analisis kompleksitas** lewat `complexity_analyzer.py`, yang
   membandingkan rasio pertumbuhan waktu terhadap pertumbuhan N.
7. **Visualisasi & pelaporan**:
   - `ascii_plotter.py` menampilkan grafik tren pertumbuhan di terminal.
   - `report_exporter.py` mengekspor hasil ke Markdown atau JSON.

## 3. Deteksi Bottleneck

Sebuah level skala dianggap **bottleneck** apabila salah satu kondisi
berikut terpenuhi:

- Waktu eksekusi naik lebih dari 4x lipat dibanding prediksi linear
  saat N hanya naik 2x lipat (indikasi kompleksitas superlinear tak
  terduga).
- Penggunaan memori naik melewati `MAX_MEMORY_MB` sebelum mencapai
  level skala target.
- Eksekusi melebihi `EXECUTION_TIMEOUT_SECONDS`.

## 4. Rekomendasi Praktik Baik

- Selalu gunakan `RANDOM_SEED` yang tetap agar hasil dapat direproduksi.
- Uji minimal skenario Average Case; tambahkan Best/Worst Case untuk
  algoritma yang sensitif terhadap urutan data (mis. sorting, searching).
- Jalankan pengujian pada mesin yang tidak sedang dibebani proses lain
  agar hasil pengukuran waktu lebih stabil.
- Naikkan skala secara bertahap (Tiny → Small → Medium → Large → Huge)
  agar bottleneck dapat terdeteksi lebih awal sebelum menghabiskan
  waktu pada skala raksasa.
