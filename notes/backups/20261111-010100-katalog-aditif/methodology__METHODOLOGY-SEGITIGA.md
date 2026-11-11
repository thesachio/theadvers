# METHODOLOGY-SEGITIGA — Mesin Alur Vertikal Lintas-Bahasa, Slicing Konteks, & Arsitektur Plugin (theadvers v2.0)

Dokumen ini adalah Mesin Alur Operasional dari Metode Segitiga (Nilai `L-VALUE` -> Jalur `L-PATH` -> Bukti `L-PROVE`) yang bersifat Language-Agnostic (Lintas Bahasa & Ekosistem): berlaku penuh untuk proyek berbasis Solidity (.sol), Vyper (.vy), Rust/Solana/CosmWasm/Stylus/Substrate (.rs), Move Sui/Aptos (.move), Cairo Starknet (.cairo), Go/Cosmos SDK/Node L1-L2 (.go), sirkuit ZK (.circom, .nr), FunC/Tolk (.fc, .tolk), hingga layanan hibrida off-chain/relayer/keeper/sequencer (.ts, .js, .py).

Dokumen ini dirancang bukan sebagai bacaan pasif sekali lewat, melainkan sebagai Sumber Potongan Konteks Aktif (*Executable Methodology Slices*) yang disuntikkan ulang ke memori kerja agen di setiap tahap melalui python3 tools/verify_segitiga.py --context-packet <audit-dir>.

---

## 1. Peta Wadah Kanonik & Aliran Status Kandidat

Seluruh proses audit hanya menggunakan berkas kerja kanonik berikut:
1. `STATE.md`: Kursor posisi aktif (Active Region R_i, Current Stage, Batch Number, Queued/Active Count) dan *Write-Ahead Checkpoint*.
2. `FACTS.md`: Bank fakta verbatim (Path/File.ext:Lxx-Lyy) beserta kolom Prerequisite Inversion Hint (cara mematahkan prasyarat di Gelombang 2).
3. `RADAR.md`: Radar sinyal lintas-kontrak/lintas-modul dengan tag wajib `[TOUCHES: KontrakAtauModul.variabelAtauFungsi]`.
4. `path-map.md`: Tabel Rekonsiliasi 100% File Kode Sumber dalam *Scope* (Tier 1/2/3), pembagian Wilayah Uang (R_1 .. R_N), tabel kapasitas nilai (Current Balance + Intended Capacity), dan peta 3-Edge ([EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT]).
5. `04-code-guarded.md`: Wadah jalur/hipotesis yang gugur di Tahap C (C1/C2) karena sudah dijaga rapat oleh kode (require, assert!, ensure!, modifier, pengecekan *signer/account constraint*, batas state, atau fakta di FACTS.md).
6. `05-raw-leads.md`: Wadah kerja Wilayah Aktif R_i yang terbagi menjadi:
   - Tabel `[QUEUED]`: Menampung seluruh kandidat kuat hasil saringan Tahap C tanpa batas plafon jumlah, diurutkan menurut Prioritas EV (`SOUL.md §3`).
   - Blok `[ACTIVE-BATCH]`: Menampung maksimal 3 kandidat `[ACTIVE]` yang ditarik dari [QUEUED] untuk dibuktikan dan diadili dalam satu putaran Batch D -> E.
7. `06-refuted-invalid.md`: Wadah kandidat dari 05-raw-leads.md yang patah/terbantahkan saat pembuktian Tahap D/E beserta bukti eksak penyebab kegagalannya.
8. `07-needs-next-step.md`: Wadah kandidat yang logikanya belum patah tetapi membutuhkan verifikasi lanjutan (state on-chain live, parameter deployment eksternal, atau komponen off-chain tertutup).
9. `08-valid-not-eligible.md`: Wadah perilaku/risiko yang secara teknis valid tetapi tidak memenuhi syarat kelayakan klaim (*out-of-scope*, *known issue*, asumsi kepercayaan admin resmi, atau di bawah ambang kebijakan).
10. `09-confirmed-findings.md`: Wadah temuan sahih yang lulus Bukti Segitiga penuh di Tahap E, dan langsung dilengkapi naskah Submission-Ready Disclosure pada Tahap F di akhir setiap wilayah.

---

## 2. Potongan Tahapan Eksekusi (*Executable Stage Slices*)

Setiap blok di bawah ini dibatasi oleh penanda @SLICE agar dapat diekstrak secara otomatis oleh verify_segitiga.py --context-packet.

<!-- @SLICE:STAGE-0:START -->
### TAHAP 0 — Global Partitioning & Rekonsiliasi 100% Berkas Sumber (STAGE-0)
- Tujuan: Mencegah ada satu pun berkas kode sumber dalam *scope* (baik kontrak on-chain, modul runtime, sirkuit, maupun komponen off-chain) yang terlewat, sekaligus mencegah agen membedah seluruh repositori secara acak (*code-first*).
- Input Wajib: Daftar seluruh berkas kode sumber dalam *scope* proyek target pada bahasa apa pun (.sol, .vy, .rs, .move, .cairo, .go, .ts, .py, .circom, .nr, .fc, dll.).
- Prosedur Eksekusi:
  1. Daftarkan 100% berkas kode sumber dalam *scope*** ke **Tabel Rekonsiliasi 100% File di path-map.md.
  2. Klasifikasikan setiap berkas ke dalam salah satu dari 3 Tier:
     - Tier 1 (`CORE-ASSET`): Kontrak/modul/program yang menyimpan, mencetak, membakar, mengunci, mengkliring, atau memindahkan aset/token/koin/state saldo.
     - Tier 2 (`VALUATION-CONTROL-LATENT`): Kontrak/modul penentu harga/kurs/share/oracle, modul likuidasi/lelang/dispute, pengatur otorisasi/governance/timelock/pause/account-constraint, kontrak/akun dengan Current Balance = 0 namun memiliki Intended Capacity > 0, sirkuit verifikasi, serta jembatan input off-chain/relayer/keeper/signature.
     - Tier 3 (`ISOLATED-PERIPHERAL`): Interface/trait/header tipe data murni (misal I*.sol, definisi trait/struct tanpa logika mutasi, konstanta statis, atau helper terisolasi tanpa akses state/nilai). Lakukan pemeriksaan 1-pass, buktikan ketiadaan mutasi nilai/state/kontrol dengan jangkar baris kode (Path/File.ext:Lxx-Lyy), lalu beri status [LOCKED-TIER3].
  3. Kelompokkan seluruh berkas Tier 1 dan Tier 2 yang saling berikatan ke dalam Wilayah Uang (`R_1, R_2, ..., R_N`).
  4. Urutkan antrean Wilayah R_1 .. R_N berdasarkan Prioritas EV (`SOUL.md §3`) dan tuliskan ke tabel Antrean Wilayah di STATE.md dengan status [OPEN].
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate 0 <audit-dir>`):
  - Jumlah berkas di Tabel Rekonsiliasi path-map.md == 100% berkas kode sumber dalam *scope*.
  - Setiap berkas Tier 3 memiliki bukti 1-pass berjangkar :Lxx dan tag [LOCKED-TIER3].
  - STATE.md memiliki minimal 1 wilayah berstatus [OPEN].
<!-- @SLICE:STAGE-0:END -->

---

<!-- @SLICE:STAGE-A:START -->
### TAHAP A — Region Value & Verbatim Facts (STAGE-A pada Wilayah Aktif R_i)

- Tujuan: Mengunci peta nilai (L-VALUE) dan fakta aturan teknis verbatim (FACTS.md) khusus untuk kontrak/modul di Wilayah Aktif R_i.
- Input Wajib: Daftar berkas Wilayah R_i dari STATE.md / path-map.md.
- Prosedur Eksekusi:
  1. Pada bagian Wilayah R_i di path-map.md, isi tabel L-VALUE untuk setiap berkas di R_i yang mencakup:
     - Aset, saldo akun/vault/PDA/object, atau hak klaim yang dikelola,
     - Current Balance (saldo awal/saat ini),
     - Intended Capacity / Latent Power (kapasitas nilai maksimal saat beroperasi normal/darurat, otoritas mint/burn/transfer/signer/likuidasi—wajib diisi agar kontrak/modul bersaldo 0 tetap terukur nilainya),
     - Invariant nilai utama yang tidak boleh dilanggar.
  2. Baca kode sumber Wilayah R_i dan ekstrak fakta teknis ke `FACTS.md` dengan format wajib:
     [ID-FAKTA] | [Region R_i] | [Path/File.ext:Lxx-Lyy] | [Fungsi/Instruksi/Variabel Eksak] | [Kondisi/Rumus Kode Asli] | [Prerequisite Inversion Hint: Bagaimana kondisi ini bisa dipatahkan?].
  3. Dilarang menulis rangkuman kabur atau memakai token kompresi (..., dll., dst., etc., rest of logic).
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate A <audit-dir>`):
  - Seluruh berkas di Wilayah R_i memiliki entri L-VALUE lengkap dengan kolom Intended Capacity di path-map.md.
  - Setiap berkas di Wilayah R_i memiliki fakta verbatim berjangkar :Lxx beserta kolom Prerequisite Inversion Hint di FACTS.md.
<!-- @SLICE:STAGE-A:END -->

---

<!-- @SLICE:STAGE-B:START -->
### TAHAP B — Region Path & 3-Edge Mapping (STAGE-B pada Wilayah Aktif R_i)
- Tujuan: Memetakan seluruh jalur masuk, perpindahan, dan titik potong fungsi/instruksi di Wilayah R_i (L-PATH) sebelum berburu celah.
- Input Wajib: Kode sumber Wilayah R_i dan entri L-VALUE / FACTS.md Wilayah R_i.
- Prosedur Eksekusi:
  1. Pada bagian Wilayah R_i di path-map.md, petakan jalur antar-fungsi/instruksi dan antar-modul menggunakan tiga kategori Edge wajib:
     - `[EDGE-ASSET]`: Setiap fungsi/instruksi/handler yang menerima, memindahkan, mencetak, membakar, atau mengunci token/koin/aset/object (Path/File.ext:Lxx-Lyy).
     - `[EDGE-VALUATION]`: Setiap fungsi/ekspresi yang menghitung harga, kurs tukar, totalAssets, totalSupply, indeks bunga/reward, bobot suara, atau pembulatan aritmatika/desimal (Path/File.ext:Lxx-Lyy).
     - `[EDGE-CONTROL/LATENT]`: Setiap fungsi otorisasi, validasi *signer/authority/account/capability*, perubahan parameter, likuidasi, penyelesaian sengketa (*dispute*), *pause/unpause*, CPI/callback/hook eksternal, serta titik masuk data off-chain (relayer, tanda tangan kriptografis, merkle/ZK proof, keeper, oracle pusher) (Path/File.ext:Lxx-Lyy).
  2. Tandai setiap jalur yang menyeberang dari Wilayah R_i ke wilayah lain (R_j).
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate B <audit-dir>`):
  - Blok Wilayah R_i di path-map.md memuat pemetaan ketiga tag ([EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT]) lengkap dengan jangkar :Lxx.
<!-- @SLICE:STAGE-B:END -->

---

<!-- @SLICE:STAGE-C1:START -->
### TAHAP C1 — Gelombang 1: Blind Adversarial Hunt & Pengisian Radar (STAGE-C1 pada Wilayah Aktif R_i)

- Tujuan: Menemukan anomali murni berdasarkan insting adversarial pada L-VALUE dan L-PATH Wilayah R_i tanpa bias katalog metode, sekaligus memanen sinyal lintas-kontrak/lintas-modul ke RADAR.md.
- Aturan Besi `STAGE-C1`: DILARANG KERAS membuka _ROUTER.md atau membaca file plugin M-xxx, AF-xx, DOM-xx, POV-xx, maupun CHAIN-xx pada tahap ini.
- Prosedur Eksekusi:
  1. Telusuri setiap jalur [EDGE-ASSET], [EDGE-VALUATION], dan [EDGE-CONTROL/LATENT] di Wilayah R_i.
  2. Jika suatu jalur dicurigai berbahaya tetapi setelah diperiksa ternyata sudah dijaga secara ketat oleh kode (require, assert!, ensure!, *account constraint*, modifier, urutan mutasi state, atau fakta di FACTS.md), catat ke `04-code-guarded.md` lengkap dengan jangkar baris kode penjaganya (Path/File.ext:Lxx-Lyy).
     **Status `TERSANGKAL` hanya sah setelah 5 Jalur Permissionless diuji** (`references/methods/M-005-guard-inversion.md` §3): J1 mutasi variabel guard, J2 pemicuan via entitas hulu, J3 peracunan state input, J4 eskalasi lintas-kontrak/`whenNotPaused` asimetris, J5 cross-whitelist confusion & callback `initiator`. Tulis tepat 5 baris di §3 `04-code-guarded.md`, masing-masing `TERTUTUP`/`TEMBUS` + alasan + jangkar. Guard yang TEMBUS satu jalur **dilarang** di `04` — pindahkan ke `05-raw-leads.md` dengan tag `[TEMBUS-Jn]`. Guard dinamis/matematis (rasio, pembulatan, saldo, waktu, harga, panjang array) juga **dilarang** di `04`.
  3. Jika ditemukan celah potensial yang belum terpatahkan, catat sebagai observasi awal [WAVE-1-BLIND] di `05-raw-leads.md` pada bagian Wilayah R_i.
  4. Setiap kali melihat fungsi/instruksi/variabel di Wilayah R_i menulis, membaca, atau memengaruhi state yang juga disentuh oleh fungsi/kontrak/modul lain, wajib catat ke `RADAR.md` dengan tag `[TOUCHES: KontrakAtauModul.variabelAtauFungsi]` beserta Path/File.ext:Lxx-Lyy.
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate C1 <audit-dir>`):
  - Wilayah R_i memiliki catatan di 04-code-guarded.md dan/atau observasi [WAVE-1-BLIND] di 05-raw-leads.md dengan jangkar :Lxx.
  - RADAR.md memiliki entri sinyal dari Wilayah R_i yang memuat tag [TOUCHES: ...].
<!-- @SLICE:STAGE-C1:END -->

---

<!-- @SLICE:STAGE-C2:START -->
### TAHAP C2 — Gelombang 2: Cross-Pollination, Lazy-Load _ROUTER.md, & Antrean [QUEUED] (STAGE-C2 pada Wilayah Aktif R_i)
- Tujuan: Mempertajam perburuan di Wilayah R_i dengan mengadu observasi Gelombang 1 terhadap Inversi FACTS.md, Rantai RADAR.md, dan Bank Ilmu (_ROUTER.md), lalu menyusun antrean kandidat berkualitas ([QUEUED]) berdasarkan urutan EV (SOUL.md §3).
- Input Konteks Otomatis (`--context-packet`): Fakta Wilayah R_i dari FACTS.md, sinyal [TOUCHES: ...] yang beririsan dari RADAR.md, dan tabel indeks _ROUTER.md.
- Prosedur Eksekusi:
  1. Operasi 1 — Inversi Prasyarat `FACTS.md`:
     Baca kolom Prerequisite Inversion Hint pada fakta Wilayah R_i. Uji apakah asumsi tersebut dapat diruntuhkan melalui pinjaman kilat (*flash loan*), donasi/injeksi saldo langsung, nilai batas (0, 1, MAX), perbedaan presisi/desimal, pemalsuan akun/objek, atau urutan panggil.
  2. Operasi 2 — Perakitan Rantai `RADAR.md` (*Chained Exploit*):
     Periksa apakah ada dua atau lebih entri di RADAR.md yang memiliki tag `[TOUCHES: KontrakAtauModul.variabelAtauFungsi]` yang sama. Jika Fungsi/Instruksi X mengubah state yang diasumsikan konstan oleh Fungsi/Instruksi Y, rakit menjadi kandidat serangan berantai.
  3. Operasi 3 — *Lazy-Loading* Bank Ilmu via `_ROUTER.md`:
     Baca tabel indeks di references/methods/_ROUTER.md, methodology/attack-forms/_ROUTER.md, methodology/domains/_ROUTER.md, references/pov/_ROUTER.md, dan references/chains/_ROUTER.md. Panggil read_file hanya pada file plugin yang Trigger Symptom-nya cocok dengan gejala kode di Wilayah R_i.
  4. Penyaringan Kualitas Segitiga & Pengisian Tabel `[QUEUED]` di `05-raw-leads.md`:
     - Setiap ide/observasi yang ternyata patah oleh fakta di FACTS.md atau penjaga kode wajib dipindahkan ke `04-code-guarded.md`.
     - Seluruh kandidat yang lolos 3 syarat kualitas Segitiga (memiliki dampak L-VALUE, jalur L-PATH yang dapat dijangkau, dan tidak patah oleh FACTS.md) dimasukkan ke Tabel Antrean `[QUEUED]` di 05-raw-leads.md (tanpa batas plafon total**—tidak boleh ada kandidat valid yang dibuang).
     - Wajib urutkan kandidat `[QUEUED]` berdasarkan **Prioritas EV (`SOUL.md §3`: P1 s/d P5) dan pasangkan masing-masing dengan minimal satu Assigned M-xxx dan satu Assigned AF-xx.
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate C2 <audit-dir>`):
  - Dokumentasi penyilangan [WAVE-2-CROSS] Wilayah R_i tercatat.
  - Seluruh kandidat berstatus [QUEUED] di 05-raw-leads.md memiliki jangkar :Lxx, peringkat EV (P1`–`P5), serta ID plugin valid M-xxx dan AF-xx.
<!-- @SLICE:STAGE-C2:END -->

---

<!-- @SLICE:STAGE-D:START -->
### TAHAP D — Prove: Pembuktian Segitiga per Rolling Batch Maksimal 3 Kandidat (STAGE-D pada Wilayah Aktif R_i)
- Tujuan: Membuktikan kandidat secara mendalam tanpa membuat memori agen penuh/terkompres.
- Aturan Kapasitas Batch (`Rolling Batch <= 3`, terikat wilayah):
  - Tarik maksimal 3 kandidat `[QUEUED]` **wilayah R_i** dengan EV tertinggi dari tabel antrean ke dalam blok `[ACTIVE-BATCH]` di 05-raw-leads.md, dan ubah statusnya menjadi `[ACTIVE]`.
  - Dilarang keras memiliki lebih dari 3 kandidat berstatus [ACTIVE] pada saat bersamaan.
  - Setiap kartu wajib menulis `Batch ID: <R_i>-B<nn>` (contoh `R1-B01`, `R1-B02`, `R2-B01`). Semua kartu dalam satu batch wajib memakai `Batch ID` yang **sama**, berprefiks wilayah aktif.
  - `[ACTIVE]` dari wilayah lain **dilarang** ikut dalam batch R_i.
  - Batch terakhir boleh berisi 1–2 kartu bila sisa `[QUEUED]` wilayah itu < 3 (contoh 7 lead → `B01`:3, `B02`:3, `B03`:1).
  - **Dilarang pindah wilayah** selama `[QUEUED]` wilayah R_i masih > 0. Nomor batch di-reset ke `B01` saat wilayah berganti.
- Prosedur Eksekusi untuk Setiap Kandidat `[ACTIVE]`:
  1. Baca file plugin spesifik references/methods/M-xxx-*.md dan methodology/attack-forms/AF-xx-*.md yang ditugaskan pada kandidat tersebut.
  2. Eksekusi dan tuliskan Tiga Titik Bukti Segitiga secara lengkap di 05-raw-leads.md:
     - Titik 1 — Jejak Kode Eksak (*Exact Code Trace*): Rangkaian pemanggilan dari entry point publik hingga baris mutasi state/aset (Path/File.ext:Lxx-Lyy) beserta kondisi penjaga yang dilewati.
     - Titik 2 — Bukti Eksekusi / Jejak Matematika Konkret (*Concrete Execution / Math Proof*): Uji PoC menggunakan *test runner* ekosistem terkait (forge test, cargo test, sui move test, aptos move test, snforge test, pytest, go test, dll.) atau perhitungan langkah demi langkah menggunakan angka konkret (saldo awal, input transaksi, hasil pembagian/pembulatan, saldo akhir). Dilarang menggunakan klaim naratif tanpa angka/eksekusi.
     - Titik 3 — Delta Nilai & Kerusakan Invariant (*Value Delta & Broken Invariant*): Selisih nilai sebelum vs sesudah serangan dan invariant spesifik dari FACTS.md / path-map.md yang terbukti pecah.
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate D <audit-dir>`):
  - Jumlah kandidat [ACTIVE] di 05-raw-leads.md berada pada rentang 1..5 (atau 0 jika wilayah bersih sejak C2).
  - Setiap kandidat [ACTIVE] memiliki ketiga komponen Bukti Segitiga terisi lengkap dan bebas dari token kompresi (..., dll., dst., etc., rest of logic).
<!-- @SLICE:STAGE-D:END -->

---

<!-- @SLICE:STAGE-E:START -->
### TAHAP E — Verdict: Pengadilan Bukti Batch Aktif (STAGE-E pada Wilayah Aktif R_i)

- Tujuan: Mengadili seluruh kandidat [ACTIVE] pada batch saat ini menggunakan standar templates/VERDICT.md dan mengosongkan kembali meja operasi 05-raw-leads.md.
- Prosedur Eksekusi:
  1. Evaluasi bukti Tahap D untuk setiap kandidat [ACTIVE] dan pindahkan kandidat tersebut dari 05-raw-leads.md ke salah satu dari 4 wadah keputusan akhir:
     - `06-refuted-invalid.md`: Jika PoC gagal, perhitungan membuktikan tidak ada keuntungan/kerugian, atau tertahan oleh penjaga kode yang baru terlihat saat eksekusi. Wajib catat alasan teknis dan baris kode (Path/File.ext:Lxx-Lyy) yang menggagalkannya.
     - `07-needs-next-step.md`: Jika logika serangan solid tetapi membutuhkan verifikasi tambahan di luar kode lokal (misal state on-chain live atau konfigurasi relayer eksternal).
     - `08-valid-not-eligible.md`: Jika perilaku/risiko benar terjadi tetapi tidak memenuhi syarat kelayakan program (*out-of-scope*, *known issue*, asumsi admin terpercaya).
     - `09-confirmed-findings.md`: Jika dan hanya jika ketiga titik Bukti Segitiga terbukti utuh tanpa asumsi palsu.
  2. Setelah seluruh kandidat batch ini dipindahkan ([ACTIVE] == 0), periksa tabel `[QUEUED]` Wilayah R_i di 05-raw-leads.md:
     - Jika masih ada `[QUEUED] > 0`: Kembali ke Tahap D (`STAGE-D`), tarik batch berikutnya `R_i-B(n+1)` (maksimal 3 kandidat `[QUEUED]` wilayah yang sama dengan EV tertinggi menjadi `[ACTIVE]`), dan ulangi siklus D -> E. **Jangan pindah wilayah lebih dulu.**
     - Jika `[ACTIVE] == 0` DAN `[QUEUED] == 0`: Lanjutkan ke Tahap F (`STAGE-F`).
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --gate E <audit-dir>`):
  - Jumlah kandidat berstatus [ACTIVE] di 05-raw-leads.md == `0`.
  - Setiap kandidat yang keluar dari 05-raw-leads.md telah tercatat secara verbatim di 06-refuted-invalid.md, 07-needs-next-step.md, 08-valid-not-eligible.md, atau 09-confirmed-findings.md.
<!-- @SLICE:STAGE-E:END -->

---

<!-- @SLICE:STAGE-F:START -->
### TAHAP F — Incremental Disclosure & Penutupan Wilayah (STAGE-F pada Wilayah Aktif R_i)
- Tujuan: Menulis naskah laporan siap-kirim (*Submission-Ready Report*) untuk setiap temuan Wilayah R_i di 09-confirmed-findings.md selagi konteks kode dan PoC Wilayah R_i masih 100% segar di memori, lalu menutup Wilayah R_i.
- Prosedur Eksekusi:
  1. Pastikan untuk Wilayah R_i di 05-raw-leads.md: `[ACTIVE] == 0` dan `[QUEUED] == 0`.
  2. Untuk setiap temuan milik Wilayah R_i yang masuk ke `09-confirmed-findings.md`, lengkapi blok Submission-Ready Disclosure yang mencakup:
     - Judul Temuan Presisi (Akar Masalah + Dampak Nilai),
     - Tingkat Keparahan (*Severity*) & Peringkat EV (SOUL.md §3),
     - Ringkasan Eksekutif & Berkas/Baris Kode Terdampak (Path/File.ext:Lxx-Lyy),
     - Alur Eksploitasi Langkah demi Langkah & Bukti PoC / Perhitungan Konkret,
     - Rekomendasi Perbaikan Kode (*Diff/Patch* Spesifik).
  3. Jalankan perintah pengunci wilayah:

         python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>

  4. Ubah status Wilayah R_i di STATE.md menjadi `[CLOSED]`.
  5. Lakukan Hard Context Flush: lepaskan beban ingatan internal Wilayah R_i, ambil Wilayah [OPEN] berikutnya (R_{i+1}) di STATE.md, ubah menjadi [ACTIVE], dan mulai kembali dari Tahap A (`STAGE-A`).
- Syarat Lulus Gate (`python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>`):
  - Wilayah R_i tidak menyisakan kandidat [QUEUED] maupun [ACTIVE] di 05-raw-leads.md.
  - Seluruh entri Wilayah R_i di 09-confirmed-findings.md telah memiliki blok *Submission-Ready Disclosure* lengkap tanpa token kompresi.
<!-- @SLICE:STAGE-F:END -->

---

<!-- @SLICE:FINAL-SWEEP:START -->
### PENUTUPAN GLOBAL — Cross-Region Final Sweep (FINAL-SWEEP)

- Tujuan: Memastikan tidak ada serangan rantai lintas-wilayah (*cross-region chain*) yang terlewat setelah seluruh Wilayah R_1 .. R_N berstatus [CLOSED].
- Prosedur Eksekusi:
  1. Baca seluruh isi RADAR.md dari R_1 sampai R_N.
  2. Periksa apakah ada sinyal [TOUCHES: ...] yang baru ditemukan pada wilayah-wilayah akhir (R_N) yang memengaruhi state atau mematahkan invariant di wilayah-wilayah awal (R_1).
  3. Jika ditemukan kombinasi lintas-wilayah baru yang belum pernah diuji:
     - Masukkan ke 05-raw-leads.md dengan label wilayah CROSS-REGION,
     - Jalankan siklus Tahap D -> Tahap E -> Tahap F (maksimal 3 kandidat per batch) hingga kembali bersih (0).
  4. Jalankan verifikasi final seluruh repositori audit:

         python3 tools/verify_segitiga.py --final <audit-dir>
<!-- @SLICE:FINAL-SWEEP:END -->

---

## 3. Arsitektur Modular *Drop-in Plugin* (1 File = 1 Item)

Agar penambahan metode baru (misal M-011) atau bentuk serangan baru (misal AF-11) hanya membutuhkan pembuatan 1 file mandiri tanpa mengedit silang berkas lain:

1. Lima Direktori Plugin & Router Otomatis:
   - references/methods/M-xxx-<slug>.md -> diindeks oleh references/methods/_ROUTER.md
   - methodology/attack-forms/AF-xx-<slug>.md -> diindeks oleh methodology/attack-forms/_ROUTER.md
   - methodology/domains/DOM-<slug>.md -> diindeks oleh methodology/domains/_ROUTER.md
   - references/pov/POV-<slug>.md -> diindeks oleh references/pov/_ROUTER.md
   - references/chains/CHAIN-<slug>.md -> diindeks oleh references/chains/_ROUTER.md

2. Standar Header 4-Baris Wajib:
   Baris 1 sampai 4 pada setiap file plugin wajib berformat:

       # [ID-PLUGIN] Nama Metode / Bentuk Serangan / Domain / POV / Chain
       - Classes: [Daftar kelas masalah atau domain]
       - Trigger Symptom: [Gejala kode spesifik kapan file ini wajib di-load pada Tahap C2/D]
       - Paired Items: [ID pasangan plugin yang direkomendasikan]

3. Alur Kerja Sinkronisasi (`--sync`):
   - Tambahkan atau revisi 1 file plugin di foldernya.
   - Jalankan python3 tools/verify_segitiga.py --sync.
   - Skrip otomatis memperbarui tabel _ROUTER.md terkait dan langsung terbaca oleh --context-packet pada Tahap C2 dan Tahap D.
