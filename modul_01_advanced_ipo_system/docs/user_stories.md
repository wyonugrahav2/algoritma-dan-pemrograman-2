# User Stories — Advanced IPO CLI System

## US-01: Analisis Dataset Cepat via CLI Flag
**Sebagai** seorang analis data,
**saya ingin** menjalankan `python main.py --values "10,2,8,4,99"`,
**agar** saya langsung mendapatkan statistik dan hasil normalisasi tanpa
mode interaktif.

**Kriteria Penerimaan:**
- Sistem mem-parsing daftar nilai yang dipisahkan koma.
- Outlier (99) difilter sebelum normalisasi.
- Hasil ditampilkan dalam format tabel di terminal.

## US-02: Input Interaktif Bertahap
**Sebagai** pengguna baru,
**saya ingin** memasukkan nilai satu per satu melalui prompt interaktif,
**agar** saya bisa memvalidasi setiap nilai sebelum diproses lebih lanjut.

**Kriteria Penerimaan:**
- Sistem menampilkan pesan galat yang jelas untuk input non-numerik.
- Pengguna dapat mengetik `selesai` untuk mengakhiri sesi input.
- Program tidak berhenti paksa (crash) akibat satu input yang salah.

## US-03: Ekspor Hasil ke Berkas
**Sebagai** manajer proyek,
**saya ingin** mengekspor hasil analisis ke file `.csv` atau `.json`,
**agar** saya dapat membagikannya ke tim lain di luar terminal.

**Kriteria Penerimaan:**
- Flag `--export hasil.csv` menghasilkan berkas CSV yang valid.
- Direktori tujuan dibuat otomatis jika belum ada.
- Kegagalan penulisan berkas menghasilkan pesan galat yang informatif,
  bukan traceback mentah.

## US-04: Audit Trail & Observabilitas
**Sebagai** developer yang melakukan debugging,
**saya ingin** setiap tahap pipeline tercatat di log dengan durasi eksekusi,
**agar** saya dapat mengidentifikasi bottleneck performa dengan cepat.

**Kriteria Penerimaan:**
- Setiap tahap pipeline mencatat durasi dalam milidetik.
- Log tersimpan baik di konsol maupun di berkas `logs/ipo_system.log`.
- Kegagalan sistem tercatat dengan level `ERROR` beserta kode galat.

## US-05: Validasi Batas Nilai
**Sebagai** administrator sistem,
**saya ingin** sistem menolak nilai numerik yang berada di luar batas
ambang batas yang wajar,
**agar** data anomali tidak mencemari hasil analisis bisnis.

**Kriteria Penerimaan:**
- Nilai di luar rentang `[MIN_VALUE_THRESHOLD, MAX_VALUE_THRESHOLD]` ditolak
  dengan `ValueOutOfRangeError`.
- Pesan galat menyebutkan nilai yang ditolak dan batas yang berlaku.
