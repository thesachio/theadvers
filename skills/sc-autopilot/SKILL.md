---
name: sc-autopilot
description: Master Skill Otonom untuk menjalankan atau melanjutkan siklus penuh audit Segitiga secara otomatis dari STAGE-0 (Global Partitioning 100% Berkas) -> Siklus Vertikal Wilayah R_1..R_N (STAGE-A -> B -> C1 -> C2 -> Rolling Batch D->E -> F) -> Cross-Region FINAL-SWEEP hingga COMPLETED dengan proteksi penuh terhadap kompresi konteks.
---

# Skill sc-autopilot — Mesin Orkestrator Otonom Siklus Vertikal A–F Lintas-Wilayah (theadvers v2.0)

Anda adalah Mesin Otonom `sc-autopilot`. Tugas Anda adalah mengorkestrasi dan mengeksekusi seluruh rangkaian audit pada repositori/proyek target secara mandiri dari awal hingga seluruh Wilayah Uang (R_1 .. R_N) berstatus `[CLOSED]` dan verifikasi akhir (--final) dinyatakan `PASS`.

Anda dapat dipanggil pada audit baru (mulai dari STAGE-0) maupun pada audit yang sedang berjalan (melanjutkan otomatis dari posisi kursor di STATE.md setelah kompresi konteks atau pergantian sesi).

---

## 1. Hukum Pengendali Loop Otonom (*Autopilot Iron Laws*)

Selama sc-autopilot berjalan, Anda terikat pada 6 hukum mekanis yang tidak boleh dilanggar:

1. Jangan Pernah Mengandalkan Ingatan Chat (*Zero-Trust on Chat Memory*):
   Di awal setiap transisi tahap (STAGE-0, STAGE-A, STAGE-B, STAGE-C1, STAGE-C2, STAGE-D, STAGE-E, STAGE-F, FINAL-SWEEP), Anda wajib mengeksekusi:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

   Output perintah tersebut adalah satu-satunya acuan aturan tahap (@SLICE:STAGE-*), status wilayah, fakta FACTS.md, dan sinyal RADAR.md Anda.
2. Jangan Pernah Melompati Gate (`Verify-Before-Transition`):
   Anda dilarang mengubah Current Stage di STATE.md ke tahap berikutnya sebelum perintah python3 tools/verify_segitiga.py --gate <tahap> <audit-dir> (atau --close-region / --final) mengembalikan status `PASS` (exit code 0). Jika FAIL, perbaiki kekurangan di berkas kerja saat itu juga dan jalankan ulang Gate.
3. Selesaikan Satu Wilayah dari `A` sampai `F` Sebelum Pindah Wilayah:
   Dilarang keras menyentuh berkas Wilayah R_{i+1} selama Wilayah Aktif R_i belum melewati STAGE-F (Submission-Ready Disclosure di 09-confirmed-findings.md) dan belum lulus --close-region <R_i>.
4. Kuras Habis Antrean `[QUEUED]` dengan *Rolling Batch* Maksimal 3 `[ACTIVE]`:
   - Di STAGE-C2, masukkan seluruh kandidat yang lolos saringan Segitiga ke Tabel [QUEUED] di 05-raw-leads.md (tanpa plafon total, diurutkan menurut Prioritas EV SOUL.md §3: P1 s/d P5).
   - Di STAGE-D, tarik maksimal 3 kandidat `[QUEUED]` menjadi [ACTIVE]. Buktikan di STAGE-D, lalu adili di STAGE-E ke wadah kanonik (06-refuted-invalid.md, 07-needs-next-step.md, 08-valid-not-eligible.md, atau 09-confirmed-findings.md) hingga [ACTIVE] == 0.
   - Ulangi putaran STAGE-D -> STAGE-E sampai `[QUEUED] == 0` DAN `[ACTIVE] == 0` untuk Wilayah R_i.
5. Larangan Mutlak Token Kompresi Malas:
   Jangan pernah menulis ..., dll., dst., etc., and so on, rest of logic, atau rest of code di berkas audit mana pun. Setiap klaim wajib memiliki jangkar verbatim `Path/File.ext:Lxx-Lyy`.
6. Write-Ahead Checkpoint di `STATE.md`:
   Perbarui kursor di STATE.md sebelum memulai suatu tahap dan segera setelah Gate tahap tersebut lulus.

---

## 2. Tahap Persiapan Ruang Kerja (*Workspace Bootstrap / Resume Check*)

Saat sc-autopilot dipanggil, periksa direktori kerja <audit-dir>:

1. Jika `<audit-dir>` belum memiliki berkas kerja kanonik:
   Buat direktori <audit-dir> dan <audit-dir>/notes/, lalu salin seluruh berkas dari templates/ ke <audit-dir>/:
   - INTEL.md            <- PRASYARAT STAGE-0 (diisi sekali di awal, lihat skill `sc-pre-intel`)
   - STATE.md
   - FACTS.md
   - RADAR.md
   - path-map.md
   - 04-code-guarded.md
   - 05-raw-leads.md
   - 06-refuted-invalid.md
   - 07-needs-next-step.md
   - 08-valid-not-eligible.md
   - 09-confirmed-findings.md
2. **PRE-STAGE-0 — Project Intelligence Brief (WAJIB sebelum STAGE-0):**
   Jika `<audit-dir>/INTEL.md` belum sah, jalankan skill `sc-pre-intel` untuk mengisinya, lalu periksa:

       python3 tools/verify_segitiga.py --intel <audit-dir>

   INTEL **bukan tahap baru** — ia prasyarat `--gate 0`. `Deployment Stage`
   (`MAINNET` | `TESTNET` | `DEVNET`) yang diisi di sini menentukan `Mode Uji` seluruh audit:
   `MAINNET` -> `FORK_LIVE` wajib di `09`; `TESTNET`/`DEVNET` -> `FORK_TESTNET` wajib.
   Jangan lanjut ke STAGE-0 selama `--intel` masih FAIL.

3. Pastikan Indeks `_ROUTER.md` Sinkron:
   Jalankan sinkronisasi router plugin satu kali:

       python3 tools/verify_segitiga.py --sync

4. Baca Posisi Kursor Saat Ini:
   Jalankan:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

   Lompat langsung ke langkah mesin status di Bagian 3 yang sesuai dengan nilai Current Stage pada STATE.md.

---

## 3. Mesin Status Otonom (sc-autopilot Execution Loop)

Jalankan loop mesin status berikut secara terus-menerus hingga Current Stage == COMPLETED:

### STEP 0 — Jika Current Stage == STAGE-0 (Global Partitioning & Rekonsiliasi 100% Berkas)
1. Checkpoint Mulai: Pastikan STATE.md mencatat Active Region: NONE, Current Stage: STAGE-0.
2. Inventarisasi Universal 100% Berkas Scope:
   - Pindai seluruh berkas kode sumber dalam *scope* proyek target pada bahasa/runtime apa pun (.sol, .vy, .rs, .move, .cairo, .go, .ts, .py, .circom, .nr, .fc, dll.).
   - Daftarkan 100% berkas ke Bagian 1 (Tabel Rekonsiliasi 100% Berkas Sumber) di path-map.md.
   - Klasifikasikan ke dalam Tier 1 (`CORE-ASSET`), Tier 2 (`VALUATION-CONTROL-LATENT` — termasuk modul saldo awal `0` dengan `Intended Capacity > 0` dan jembatan off-chain), atau Tier 3 (`ISOLATED-PERIPHERAL`).
   - Untuk setiap berkas Tier 3, lakukan pemeriksaan 1-pass, tulis bukti jangkar Path/File.ext:Lxx-Lyy bahwa berkas tersebut tidak memegang/memutasi nilai atau kontrol, dan beri tag `[LOCKED-TIER3]`.
3. Partisi Wilayah Uang (`R_1 .. R_N`) Berdasarkan Prioritas EV (`SOUL.md §3`):
   - Kelompokkan seluruh berkas Tier 1 dan Tier 2 ke dalam Wilayah Uang R_1, R_2, ..., R_N (2–5 berkas yang berikatan erat per wilayah).
   - Urutkan wilayah dari EV tertinggi (P1) ke terendah (P5) dan tuliskan ke Tabel Antrean Wilayah di STATE.md dengan status [OPEN].
4. Verifikasi Gate 0:

       python3 tools/verify_segitiga.py --gate 0 <audit-dir>

5. Transisi ke Wilayah Pertama:
   Ubah wilayah [OPEN] pertama (R_1) menjadi [ACTIVE] di STATE.md, set Active Region: R_1, Current Stage: STAGE-A, Current Batch ID: NONE, dan lanjutkan ke STAGE-A.

---

### STEP A — Jika Current Stage == STAGE-A (L-VALUE & Fakta Verbatim Wilayah Aktif R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Eksekusi `STAGE-A` pada Berkas Wilayah `R_i`:
   - Isi tabel L-VALUE Wilayah R_i di path-map.md (wajib mencakup Current Balance, `Intended Capacity & Latent Power`, serta Core Value Invariant berjangkar :Lxx).
   - Ekstrak seluruh aturan teknis, rumus pembulatan/skala desimal, dan syarat penjaga kode Wilayah R_i secara verbatim (Path/File.ext:Lxx-Lyy) ke FACTS.md lengkap dengan kolom `Prerequisite Inversion Hint`.
3. Verifikasi Gate A:

       python3 tools/verify_segitiga.py --gate A <audit-dir>

4. Transisi: Perbarui STATE.md (Current Stage: STAGE-B, Last Passed Gate: GATE-A) dan lanjutkan ke STAGE-B.

---

### STEP B — Jika Current Stage == STAGE-B (L-PATH & Pemetaan 3-Edge Wilayah Aktif R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Eksekusi `STAGE-B` pada Berkas Wilayah `R_i`:
   - Petakan seluruh jalur fungsi/instruksi Wilayah R_i di path-map.md ke dalam tiga kategori wajib: `[EDGE-ASSET]`, `[EDGE-VALUATION]`, dan `[EDGE-CONTROL/LATENT]`, lengkap dengan jangkar Path/File.ext:Lxx-Lyy dan titik singgung lintas-wilayah.
3. Verifikasi Gate B:

       python3 tools/verify_segitiga.py --gate B <audit-dir>

4. Transisi: Perbarui STATE.md (Current Stage: STAGE-C1, Last Passed Gate: GATE-B) dan lanjutkan ke STAGE-C1.

---
### STEP C1 — Jika Current Stage == STAGE-C1 (Gelombang 1: Blind Adversarial Hunt di Wilayah R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Eksekusi `STAGE-C1` (TANPA Membuka `_ROUTER.md` / Plugin):
   - Bedah alur kode Wilayah R_i murni dengan insting adversarial berdasarkan L-VALUE dan L-PATH.
   - Catat jalur yang sudah terbukti aman oleh penjaga kode eksak ke `04-code-guarded.md` (Path/File.ext:Lxx-Lyy).
   - Catat anomali awal ke bagian [WAVE-1-BLIND] di `05-raw-leads.md`.
   - Catat seluruh sentuhan state lintas-modul/lintas-wilayah ke `RADAR.md` dengan tag wajib `[TOUCHES: NamaModul.namaVariabelAtauFungsi]`.
3. Verifikasi Gate C1:

       python3 tools/verify_segitiga.py --gate C1 <audit-dir>

4. Transisi: Perbarui STATE.md (Current Stage: STAGE-C2, Last Passed Gate: GATE-C1) dan lanjutkan ke STAGE-C2.

---

### STEP C2 — Jika Current Stage == STAGE-C2 (Gelombang 2: Cross-Pollination & Antrean [QUEUED] di Wilayah R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir> (otomatis memuat FACTS.md, RADAR.md, dan indeks _ROUTER.md).
2. Eksekusi Tiga Penyilangan `STAGE-C2`:
   - Uji Inversi Prasyarat `FACTS.md` pada Wilayah R_i.
   - Rakit Rantai `RADAR.md` untuk setiap simbol [TOUCHES: ...] yang beririsan.
   - Lakukan Lazy-Loading `_ROUTER.md`: panggil read_file hanya pada berkas plugin (M-xxx, AF-xx, DOM-xx, POV-xx, CHAIN-xx) yang Trigger Symptom-nya cocok dengan Wilayah R_i.
3. Saringan Kualitas Segitiga & Pengisian Tabel `[QUEUED]` Tanpa Plafon Total:
   - Pindahkan hipotesis yang patah oleh FACTS.md atau penjaga kode ke `04-code-guarded.md`.
   - Masukkan seluruh kandidat yang lolos 3 syarat kualitas Segitiga ke Tabel Antrean `[QUEUED]` di 05-raw-leads.md (tanpa batas plafon total), urutkan menurut Prioritas EV (`P1` -> `P5`), Kolom Method/AF memuat hasil konsultasi katalog (ID cocok) ATAU `[NO-CATALOG]`; kandidat DILARANG gugur hanya karena tidak cocok katalog. Label M-xxx + AF-xx untuk uji dipilih di STAGE-D.
4. Verifikasi Gate C2:

       python3 tools/verify_segitiga.py --gate C2 <audit-dir>

5. Transisi:
   - Jika terdapat kandidat [QUEUED] > 0 untuk Wilayah R_i: set Current Stage: STAGE-D, Current Batch ID: <R_i>-B01, perbarui Queued Leads Count di STATE.md, lalu lanjutkan ke STAGE-D.
   - Jika Queued Leads Count == 0 dan Active Leads Count == 0 (seluruh jalur di Wilayah R_i terbukti aman dan tercatat di 04-code-guarded.md): set Current Stage: STAGE-F di STATE.md dan lanjutkan ke STAGE-F.

---

### STEP D — Jika Current Stage == STAGE-D (Pembuktian Segitiga Rolling Batch <= 3 [ACTIVE] di Wilayah R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Penarikan Batch ke Meja Operasi (`<= 3 [ACTIVE]`):
   - Jika saat ini Active Leads Count == 0 dan Queued Leads Count > 0 untuk Wilayah R_i: tarik maksimal 3 kandidat `[QUEUED]` dengan EV tertinggi ke Blok `[ACTIVE-BATCH]` di 05-raw-leads.md, ubah statusnya menjadi `[ACTIVE]`, dan perbarui STATE.md.
3. Eksekusi Tiga Titik Bukti Segitiga:
   - Untuk setiap kandidat [ACTIVE] (maksimal 3), baca berkas plugin M-xxx dan AF-xx yang ditugaskan.
   - Lengkapi di 05-raw-leads.md:
     1. Titik 1 — Jejak Kode Eksak (`Path/File.ext:Lxx-Lyy`),
     2. Titik 2 — Bukti Eksekusi Test Runner (`forge test` / `cargo test` / `move test` / `snforge` / `pytest` / `go test`) atau Jejak Matematika Angka Konkret,
     3. Titik 3 — Delta Nilai Terukur & ID Invariant yang Pecah.
4. Verifikasi Gate D:

       python3 tools/verify_segitiga.py --gate D <audit-dir>

5. Transisi: Perbarui STATE.md (Current Stage: STAGE-E, Last Passed Gate: GATE-D) dan lanjutkan ke STAGE-E.

---
### STEP E — Jika Current Stage == STAGE-E (Pengadilan Bukti Batch Aktif & Kontrol Loop Batch di Wilayah R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Adili Seluruh Kandidat `[ACTIVE]` Sesuai `templates/VERDICT.md`:
   - Pindahkan setiap kandidat [ACTIVE] dari meja operasi 05-raw-leads.md ke wadah kanonik yang tepat:
     - `06-refuted-invalid.md` (terbantahkan/PoC gagal saat uji),
     - `07-needs-next-step.md` (butuh verifikasi state on-chain live / komponen eksternal),
     - `08-valid-not-eligible.md` (valid teknis tetapi *out-of-scope / known / trusted role / dust*), atau
     - `09-confirmed-findings.md` (lulus Tiga Titik Bukti Segitiga utuh).
   - Pastikan jumlah kandidat [ACTIVE] di 05-raw-leads.md kembali menjadi `0`.
3. Verifikasi Gate E:

       python3 tools/verify_segitiga.py --gate E <audit-dir>

4. Keputusan Cabang Rolling Batch:
   - Jika masih ada kandidat `[QUEUED] > 0` untuk Wilayah `R_i` di `05-raw-leads.md`:
     Naikkan Current Batch ID `R_i-B(n+1)` (jangan pindah wilayah selama [QUEUED] R_i > 0), set Current Stage: STAGE-D, Active Leads Count: 0 di STATE.md, dan kembali ke STEP D untuk memproses batch berikutnya (maksimal 3 kandidat).
   - Jika `[ACTIVE] == 0` DAN `[QUEUED] == 0` untuk Wilayah `R_i`:
     Set Current Stage: STAGE-F, Queued Leads Count: 0, Active Leads Count: 0, Last Passed Gate: GATE-E di STATE.md, dan lanjutkan ke STEP F.

---

### STEP F — Jika Current Stage == STAGE-F (Incremental Disclosure di 09 & Penutupan Wilayah R_i)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Tulis Naskah *Submission-Ready Disclosure* Selagi Konteks `R_i` 100% Segar:
   - Untuk setiap temuan milik Wilayah R_i di `09-confirmed-findings.md`, lengkapi Blok B (`Submission-Ready Disclosure`) secara utuh (Ringkasan Eksekutif, Analisis Akar Masalah :Lxx, Langkah Eksploitasi & PoC Lengkap, Kuantifikasi Dampak Nilai, dan Rekomendasi Patch) serta ubah statusnya menjadi `[SUBMISSION-READY]`.
3. Jalankan Gerbang Penutup Wilayah (`--close-region`):

       python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>

4. Tutup Wilayah `R_i`, Lakukan *Hard Context Flush*, & Pilih Wilayah Berikutnya:
   - Di STATE.md, ubah status Wilayah R_i menjadi `[CLOSED]`.
   - Periksa Tabel Antrean Wilayah di STATE.md:
     - Jika masih ada Wilayah `R_{i+1}` yang berstatus `[OPEN]`:
       Ubah status R_{i+1} menjadi `[ACTIVE]`, set Active Region: R_{i+1}, Current Stage: STAGE-A, Current Batch ID: NONE (reset — batch berikutnya mulai B01), Queued Leads Count: 0, Active Leads Count: 0. Lakukan Hard Context Flush (lepaskan ingatan kode internal R_i) dan kembali ke STEP A untuk Wilayah `R_{i+1}`.
     - Jika seluruh Wilayah `R_1 .. R_N` telah berstatus `[CLOSED]`:
       Set Active Region: CROSS-REGION, Current Stage: FINAL-SWEEP di STATE.md, dan lanjutkan ke STEP FINAL-SWEEP.

---

### STEP FINAL-SWEEP — Jika Current Stage == FINAL-SWEEP (Penyapuan Rantai Lintas-Wilayah & Penguncian Akhir)
1. Re-Hydrate Konteks: Jalankan python3 tools/verify_segitiga.py --context-packet <audit-dir>.
2. Evaluasi Tabrakan `[TOUCHES: ...]` Lintas-Wilayah di `RADAR.md`:
   - Periksa seluruh entri RADAR.md dari R_1 hingga R_N. Apakah ada sinyal [TOUCHES: NamaModul.simbol] dari wilayah akhir yang mematahkan invariant atau berpasangan dengan sinyal di wilayah awal dan belum pernah diuji sebagai rantai?
   - Jika ada kandidat lintas-wilayah baru: masukkan ke 05-raw-leads.md dengan Region CROSS-REGION, jalankan siklus `STAGE-D -> STAGE-E -> STAGE-F` (maksimal 3 per batch) hingga kembali bersih ([QUEUED] == 0 dan [ACTIVE] == 0).
3. Jalankan Gerbang Pengunci Akhir (`--final`):

       python3 tools/verify_segitiga.py --final <audit-dir>

4. Selesai (`COMPLETED`):
   Setelah --final dinyatakan PASS, perbarui STATE.md (Current Stage: COMPLETED, Last Passed Gate: FINAL) dan sajikan ringkasan hasil akhir audit kepada pengguna.

---

## 4. Protokol Jika sc-autopilot Mendelegasikan Tahap ke Subagent
Apabila lingkungan eksekusi Anda mendukung pemanggilan Subagent dengan *context window* terpisah:
1. Parent sc-autopilot tetap memegang kendali eksklusif atas STATE.md dan seluruh pemanggilan verify_segitiga.py --gate.
2. Sebelum memanggil Subagent untuk mengerjakan suatu tahap/batch pada Wilayah R_i, Parent wajib menjalankan python3 tools/verify_segitiga.py --context-packet <audit-dir> dan menyalin outputnya secara utuh ke dalam prompt Subagent.
3. Subagent wajib menulis hasilnya ke berkas terisolasi notes/staging-<region>-<stage>-<item>.md yang diawali dengan blok `## STAGING MANIFEST` maksimal 16 baris.
4. Parent memeriksa berkas staging tersebut (memastikan bebas token kompresi dan memiliki jangkar Path/File.ext:Lxx-Lyy), menggabungkannya ke berkas kanonik utama, lalu mengeksekusi Gate tahap terkait.
