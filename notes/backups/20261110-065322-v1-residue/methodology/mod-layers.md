# MOD-LAYERS — Spesifikasi Teknis Lapisan Segitiga Universal (theadvers v2.0)

Dokumen ini mendefinisikan spesifikasi teknis untuk setiap lapisan (*layer*) dalam arsitektur audit Segitiga. Seluruh lapisan dirancang secara Universal (Language & Runtime Agnostic): berlaku untuk sistem berbasis akun, objek, UTXO, state machine, sirkuit kriptografi, maupun layanan hibrida *on-chain/off-chain* pada bahasa pemrograman apa pun.

---

## 1. Kamus Abstraksi Universal

Agar tidak terikat pada satu bahasa atau ekosistem tertentu, seluruh catatan audit menggunakan lima abstraksi universal berikut:

| Istilah Universal | Cakupan Lintas-Ekosistem | Format Jangkar Wajib |
| :--- | :--- | :--- |
| Berkas Sumber (*Source Unit*) | Kontrak, program, modul runtime, sirkuit, pustaka, atau skrip layanan dalam *scope* (.sol, .vy, .rs, .move, .cairo, .go, .ts, .py, .circom, .nr, .fc, dll.). | Path/File.ext:Lxx-Lyy |
| Modul (*Module / Component*) | Unit logika yang membungkus state dan perilaku (Contract, Program, Pallet, Module, Circuit, Service, Relayer). | NamaModul |
| Titik Masuk / Fungsi (*Callable Unit*) | Fungsi publik/eksternal, instruksi, *extrinsic*, *message handler*, *entry function*, callback, hook, atau endpoint API/relayer. | NamaModul.namaFungsi |
| Nilai & State (*Value & State*) | Saldo token/koin native, share, hak klaim, objek bernilai, catatan utang/kolateral, bobot otoritas, atau kapasitas nilai laten. | NamaModul.namaState |
| Penjaga Kode (*Code Guard*) | Pemeriksaan kondisi yang membatasi eksekusi (require, assert, ensure, modifier, validasi *signer/authority/account/capability*, batas tipe data, atau constraint sirkuit). | Path/File.ext:Lxx-Lyy + ekspresi asli |

---

## 2. Lapisan 0: L-PART — Global Partitioning & Rekonsiliasi 100% Berkas (STAGE-0)

Lapisan L-PART dieksekusi satu kali di awal audit untuk menjamin 100% berkas dalam *scope* terdata tanpa memicu pembacaan kode acak (*code-first*).

### 2.1 Tabel Rekonsiliasi 100% Berkas & Klasifikasi 3-Tier
Setiap berkas sumber dalam *scope* wajib didaftarkan ke path-map.md dan diklasifikasikan ke dalam salah satu Tier berikut:

1. Tier 1 — `CORE-ASSET` (Pipa & Penyimpan Nilai Utama):
   - Kriteria: Modul yang secara langsung menyimpan, mencetak, membakar, mengunci, mengkliring, atau memindahkan aset/hak klaim bernilai.
   - Perlakuan: Wajib masuk ke dalam Wilayah Uang (R_i) dan dibedah penuh dari Tahap A sampai Tahap F.

2. Tier 2 — `VALUATION-CONTROL-LATENT` (Saraf Valuasi, Kontrol, Saldo 0 Berkapasitas, & Hibrida Off-Chain):
   - Kriteria:
     - Modul penentu harga, kurs tukar, indeks bunga/reward, pembagian share, atau adapter oracle.
     - Modul likuidasi, lelang, penyelesaian sengketa (*dispute*), atau *slashing*.
     - Modul otorisasi, tata kelola (*governance*), *timelock*, *pause/emergency*, atau pengelola *capability/authority*.
     - Modul yang saat inisialisasi atau di lingkungan uji memiliki Current Balance = 0, tetapi memiliki Intended Capacity > 0 (misal router transien, escrow baru, flash settlement, vault yang belum terisi).
     - Komponen verifikasi tanda tangan, bukti merkle/ZK, serta layanan *off-chain* (relayer, keeper, prover, sequencer) yang menyuplai input ke modul nilai.
   - Perlakuan: Wajib digabungkan ke Wilayah Uang (R_i) yang relevan atau dijadikan Wilayah tersendiri, lalu dibedah penuh dari Tahap A sampai Tahap F.

3. Tier 3 — `ISOLATED-PERIPHERAL` (Periferal Terisolasi):
   - Kriteria: Definisi antarmuka/trait murni tanpa implementasi, kumpulan konstanta statis, kode tipe error, atau pustaka pembantu murni yang tidak memegang state dan tidak memindahkan nilai.
   - Perlakuan 1-Pass Lock: Wajib diperiksa 1-pass untuk memastikan tidak ada logika mutasi state/nilai atau delegasi eksekusi tersembunyi. Catat bukti baris kodenya (Path/File.ext:Lxx-Lyy) di path-map.md dan beri status `[LOCKED-TIER3]`.

### 2.2 Pembentukan Antrean Wilayah Uang (R_1 .. R_N)
- Kelompokkan berkas Tier 1 dan Tier 2 yang memiliki ikatan aliran nilai atau kontrol erat ke dalam Wilayah Uang (`R_1, R_2, ..., R_N`) (disarankan 2–5 berkas per wilayah agar fokus memori terjaga).
- Urutkan R_1 .. R_N berdasarkan Prioritas EV (`SOUL.md §3`) dan tuliskan ke STATE.md dengan status awal [OPEN].

---

## 3. Lapisan A: L-VALUE — Pemetaan Nilai Universal & Fakta Verbatim (STAGE-A)

Lapisan L-VALUE dijalankan di awal setiap Wilayah Aktif R_i untuk mengunci objek nilai dan aturan dasar sebelum menelusuri jalur.

### 3.1 Dua Dimensi Ukuran Nilai (Current vs Intended Capacity)
Pada path-map.md, setiap modul di Wilayah R_i wajib diukur menggunakan empat atribut:
1. Value Carrier: Jenis aset, hak klaim, objek, atau otoritas yang dikelola.
2. Current Balance / Initial State: Nilai saldo atau state saat kontrak/modul pertama kali di-deploy atau pada snapshot pengujian.
3. Intended Capacity & Latent Power: Kapasitas nilai maksimal yang dirancang mengalir/terkunci saat sistem beroperasi penuh, ditambah kekuasaan laten yang dimiliki modul tersebut (misal hak mencetak/membakar, hak memindahkan dana pengguna, hak mengubah kurs, atau hak membekukan sistem). Atribut ini mencegah modul bersaldo `0` diabaikan.
4. Core Value Invariant: Persamaan atau syarat mutlak yang menjamin kesetimbangan nilai di Wilayah R_i (misal: total klaim tidak boleh melebihi total aset pendukung).

### 3.2 Ekstraksi Fakta Verbatim & Peta Inversi Prasyarat (FACTS.md)
Setiap aturan teknis yang ditemukan pada kode Wilayah R_i wajib dicatat ke FACTS.md tanpa rangkuman kabur:
- Verbatim Anchor: Path/File.ext:Lxx-Lyy | NamaModul.namaSimbol.
- Exact Code Condition / Formula: Rumus matematika, skala desimal/presisi, batas parameter, atau syarat penjaga sebagaimana tertulis di kode.
- Prerequisite Inversion Hint: Jawaban atas pertanyaan adversarial: *"Kondisi ekstrem, manipulasi state eksternal, urutan eksekusi, atau input batas apa yang dapat membalikkan atau mematahkan fakta ini di Gelombang 2?"*

---

## 4. Lapisan B: L-PATH — Pemetaan Jalur 3-Edge Universal (STAGE-B)

Lapisan L-PATH memetakan anatomi pergerakan nilai dan kontrol di Wilayah R_i pada path-map.md menggunakan tiga jenis ikatan (*Edge*) wajib:

1. `[EDGE-ASSET]` (Pipa Pergerakan Aset):
   - Melacak setiap jalur di mana aset/klaim/objek masuk, berpindah antar-modul/akun, dicetak, dibakar, atau ditarik keluar.
   - Wajib mencantumkan: Titik Masuk (NamaModul.fungsi) -> Operasi Mutasi (Path/File.ext:Lxx-Lyy) -> Tujuan Akhir.

2. `[EDGE-VALUATION]` (Saraf Perhitungan & Penilaian):
   - Melacak setiap jalur pembacaan dan perhitungan yang menentukan *"berapa nilai yang berhak diterima atau dibayar"*: rumus kurs tukar, rasio share/vault, pembacaan harga oracle, akumulasi indeks bunga/reward, serta operasi pembagian/pembulatan presisi.
   - Wajib mencantumkan sumber variabel yang dibaca (Path/File.ext:Lxx-Lyy) dan apakah variabel tersebut dapat dimanipulasi dalam transaksi/blok yang sama.
3. `[EDGE-CONTROL/LATENT]` (Jalur Kontrol, Likuidasi, Callback, & Input Off-Chain):
   - Melacak seluruh jalur yang mengubah aturan main atau berjalan pada kondisi khusus:
     - Pemeriksaan otorisasi, peran, kepemilikan akun/objek, atau tanda tangan kriptografis,
     - Jalur likuidasi, lelang paksa, *slashing*, atau penyelesaian sengketa (*dispute*),
     - Jalur darurat (*pause*, *unpause*, *emergency withdraw*, *upgrade*),
     - Panggilan keluar (*external call*, CPI, callback, hook) yang memberi kesempatan eksekusi balik,
     - Titik masuk data dari komponen off-chain (relayer, keeper, oracle pusher, prover ZK/merkle).

---

## 5. Lapisan C: L-HUNT — Perburuan Dua Gelombang & Antrean Kualitas (STAGE-C1 & STAGE-C2)

Lapisan L-HUNT memisahkan insting murni dari penggunaan katalog referensi agar agen tajam sekaligus sistematis.

### 5.1 Gelombang 1: STAGE-C1 (*Blind Adversarial Hunt*)
- Larangan: Dilarang membaca _ROUTER.md atau file plugin pada tahap ini.
- Tiga Output Wajib `C1` di Wilayah `R_i`:
  1. Jalur Terjaga -> `04-code-guarded.md`: Setiap jalur pada [EDGE-ASSET], [EDGE-VALUATION], atau [EDGE-CONTROL/LATENT] yang setelah diuji logikanya terbukti sudah tertutup rapat oleh penjaga kode eksak (Path/File.ext:Lxx-Lyy).
  2. Observasi Anomali Awal -> `05-raw-leads.md` (`[WAVE-1-BLIND]`): Dugaan celah yang ditemukan dari ketimpangan alur kode Wilayah R_i.
  3. Sinyal Lintas-Modul -> `RADAR.md` (`[TOUCHES: ...]`): Setiap efek samping, penulisan state bersama, atau asumsi lintas-modul wajib dicatat ke RADAR.md dengan tag `[TOUCHES: NamaModul.namaVariabelAtauFungsi]`.

### 5.2 Gelombang 2: STAGE-C2 (*Cross-Pollination & Pembentukan Antrean [QUEUED]*)
- Input Konteks (`--context-packet`): Fakta Wilayah R_i (FACTS.md), sinyal RADAR.md, dan indeks tipis _ROUTER.md.
- Tiga Operasi Penyilangan `C2`:
  1. Inversi `FACTS.md`: Menyerang Prerequisite Inversion Hint pada setiap fakta di Wilayah R_i.
  2. Perakitan Rantai `RADAR.md`: Menggabungkan dua atau lebih sinyal yang memiliki tag [TOUCHES: ...] pada state/fungsi yang sama menjadi skenario serangan berantai (*Chained Exploit*).
  3. Lazy-Load Bank Ilmu via `_ROUTER.md`: Membaca _ROUTER.md dan hanya memanggil read_file pada file plugin (M-xxx, AF-xx, DOM-xx, POV-xx, CHAIN-xx) yang Trigger Symptom-nya cocok dengan Wilayah R_i.
- Aturan Saringan Kualitas & Tabel `[QUEUED]` di `05-raw-leads.md`:
  - Kandidat yang gugur oleh FACTS.md dipindahkan ke `04-code-guarded.md`.
  - Seluruh kandidat yang lolos 3 syarat Segitiga (memiliki dampak L-VALUE, jalur L-PATH, dan tidak patah oleh FACTS.md) dimasukkan ke Tabel Antrean `[QUEUED]` di 05-raw-leads.md tanpa batas plafon total.
  - Kandidat di tabel [QUEUED] wajib diurutkan berdasarkan Prioritas EV (`SOUL.md §3`: P1 s/d P5) dan wajib memiliki pasangan Assigned M-xxx serta Assigned AF-xx.

---

## 6. Lapisan D: L-PROVE — Mesin Pembuktian Rolling Batch (STAGE-D)

Lapisan L-PROVE mencegah kompresi konteks dengan membatasi meja operasi aktif.

### 6.1 Aturan Meja Operasi [ACTIVE-BATCH] (Maksimal 5 Kandidat)
- Dari daftar [QUEUED] Wilayah R_i di 05-raw-leads.md, tarik maksimal 5 kandidat dengan EV tertinggi ke blok `[ACTIVE-BATCH]` dan ubah statusnya menjadi `[ACTIVE]`.
- Baca file plugin M-xxx dan AF-xx yang ditugaskan pada ke-5 kandidat tersebut.
### 6.2 Standar Tiga Titik Bukti Segitiga Universal
Setiap kandidat [ACTIVE] wajib dilengkapi tiga bukti konkret di 05-raw-leads.md:
1. Titik 1 — Jejak Kode Eksak (*Exact Code Trace*):
   Urutan pemanggilan dari titik masuk hingga titik mutasi nilai/state lengkap dengan Path/File.ext:Lxx-Lyy dan bukti mengapa penjaga kode yang ada berhasil dilewati.
2. Titik 2 — Bukti Eksekusi / Jejak Matematika Konkret (*Concrete Execution or Math Trace*):
   - Hasil eksekusi nyata menggunakan *test runner* atau harness ekosistem target (forge test, cargo test, move test, snforge, pytest, go test, skrip simulasi), ATAU
   - Jejak perhitungan matematis langkah demi langkah dengan angka konkret pada setiap baris perubahan state.
3. Titik 3 — Delta Nilai & Kerusakan Invariant (*Value Delta & Broken Invariant*):
   Perbandingan terukur antara state/saldo sebelum vs sesudah serangan serta invariant spesifik yang dilanggar.

---

## 7. Lapisan E & F: L-VERDICT & L-DISCLOSURE — Pengadilan Bukti & Laporan Inkremental (STAGE-E & STAGE-F)

### 7.1 Pengadilan Batch Aktif (STAGE-E)
Setiap kandidat [ACTIVE] yang telah diuji di Tahap D wajib dipindahkan dari 05-raw-leads.md ke salah satu wadah kanonik berikut sesuai templates/VERDICT.md:
- `06-refuted-invalid.md`: Terbantahkan saat pembuktian (PoC gagal, hasil hitungan tidak menguntungkan/merugikan, atau tertahan penjaga kode yang baru terdeteksi saat uji). Wajib disertai alasan teknis dan Path/File.ext:Lxx-Lyy.
- `07-needs-next-step.md`: Logika serangan kuat tetapi membutuhkan verifikasi tambahan di luar kode yang tersedia (misal konfigurasi on-chain live atau layanan eksternal).
- `08-valid-not-eligible.md`: Valid secara teknis tetapi di luar kelayakan klaim (*out-of-scope*, *known issue*, atau asumsi peran terpercaya).
- `09-confirmed-findings.md`: Terbukti sahih memenuhi ketiga titik Bukti Segitiga.

Setelah blok [ACTIVE-BATCH] kosong ([ACTIVE] == 0):
- Jika masih ada `[QUEUED] > 0` untuk Wilayah R_i di 05-raw-leads.md, tarik batch berikutnya (maksimal 5 kandidat) dan ulangi Tahap D -> Tahap E.
- Jika `[ACTIVE] == 0` DAN `[QUEUED] == 0` untuk Wilayah R_i, lanjut ke Tahap F (`STAGE-F`).

### 7.2 Laporan Siap-Kirim Inkremental per Wilayah (STAGE-F)
- Sebelum meninggalkan Wilayah R_i, lengkapi seluruh temuan milik R_i di dalam `09-confirmed-findings.md` menjadi naskah Submission-Ready Disclosure yang utuh (Judul, Severity & EV, Ringkasan, Jejak Kode Path/File.ext:Lxx-Lyy, Langkah Reproduksi/PoC, dan Rekomendasi Mitigasi/Patch).
- Jalankan python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>, ubah status R_i menjadi [CLOSED] di STATE.md, lakukan *Hard Context Flush*, dan pindah ke Wilayah [OPEN] berikutnya (R_{i+1}).
