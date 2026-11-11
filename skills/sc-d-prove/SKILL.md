---
name: sc-d-prove
description: Eksekusi STAGE-D (Pembuktian Tiga Titik Segitiga dengan Rolling Batch 3 Kandidat [ACTIVE] per Putaran, terikat satu wilayah & satu Batch ID) pada Wilayah Aktif R_i.
---

# Skill sc-d-prove — Pembuktian Segitiga Rolling Batch (STAGE-D / L-PROVE)

Anda menjalankan Tahap D (`L-PROVE`) untuk Wilayah Aktif R_i menggunakan mekanisme Rolling Batch (Maksimal 3 Kandidat `[ACTIVE]` sekaligus di `05-raw-leads.md`) agar kedalaman pembuktian mencapai 100% tanpa kompresi konteks.

---

## 1. Langkah Pertama Mutlak (Hard Bootloader & Penarikan Batch)

1. Jalankan Pemulihan Konteks:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. Tarik Rolling Batch ke Meja Operasi (`1..3 [ACTIVE]`, satu wilayah, satu `Batch ID`):
   - Periksa Bagian 2 (Tabel [QUEUED]) di 05-raw-leads.md untuk Wilayah Aktif R_i.
   - Ambil maksimal 3 kandidat `[QUEUED]` **wilayah R_i** dengan peringkat EV tertinggi (`P1` -> `P5`), ubah statusnya menjadi `[ACTIVE]`, dan buat kartu pembuktiannya di Bagian 3 (Blok Meja Operasi `[ACTIVE-BATCH]`) pada 05-raw-leads.md.
   - **Sebelum menulis PoC, tetapkan kondisi live objek yang diserang.** Untuk SETIAP kartu `[ACTIVE]`
     jalankan deteksi terukur (satu perintah per lead, artefak bernama LEAD-ID):

     ```bash
     python3 tools/deploy_parity.py --paradigm <evm|solana|sui|aptos|ton|generic> \
       --chain <mainnet|testnet|local> --addr <TARGET_OBJEK> --rpc <RPC> \
       --entrypoints "<signature yang diserang>" --repo <repo> \
       --out <audit-dir>/notes/deploy-parity-<LEAD-ID>.json
     ```

     Lalu isi di kartu: `TARGET_OBJEK`, `DEPLOY_REPORT`, `SIKLUS`, `VERDICT_ENTRYPOINT`,
     `MODE_UJI_POC`, dan baris `Fork PoC` (chain + block + RPC).

     **`MODE_UJI_POC` diturunkan, bukan dipilih bebas** — PoC wajib dibangun pada kondisi yang relevan:

     | `INTEL.md §0` | `SIKLUS` | `MODE_UJI_POC` |
     | :--- | :--- | :--- |
     | `MAINNET` | `P4_LIVE_FULL` / `P3_LIVE_PARTIAL` | `FORK_LIVE` + blok |
     | `TESTNET` / `DEVNET` | `P2_TESTNET_ONLY` | `FORK_TESTNET` + blok |
     | apa pun | `P1_PRE_DEPLOY` | `FORK_DEPLOYED_HEAD` atau `LOKAL` |

     `--gate D` menolak kombinasi yang tidak konsisten (mis. proyek mainnet tetapi PoC memakai
     `FORK_TESTNET`, atau `SIKLUS: P4_LIVE_FULL` tetapi diuji `LOKAL`).

   - Aturan Besi: Dilarang keras memiliki lebih dari 3 kandidat berstatus [ACTIVE] pada saat bersamaan. Biarkan kandidat ke-4 dan seterusnya tetap berstatus [QUEUED] untuk diproses pada batch berikutnya setelah batch ini selesai diadili di STAGE-E.
   - Setiap kartu WAJIB memuat `Batch ID: <R_i>-B<nn>` (mis. `R1-B01`); semua kartu dalam satu batch memakai `Batch ID` yang sama dan berprefiks wilayah aktif. Kartu wilayah lain → `--gate D` FAIL.
   - Batch terakhir boleh berisi 1–2 kartu bila sisa `[QUEUED]` wilayah itu < 3 (contoh 7 lead → B01:3, B02:3, B03:1).
   - Perbarui STATE.md (Current Stage: STAGE-D, Current Batch ID, Queued Leads Count, Active Leads Count).

---

## 2. Prosedur Pembuktian Tiga Titik Segitiga untuk Setiap Kandidat [ACTIVE]

Untuk masing-masing kandidat [ACTIVE] di meja operasi (maksimal 3 kandidat):
   - Pilih label uji WAJIB: M-xxx (metode bedah) + AF-xx (bentuk serangan yang diuji) — `--gate D` menagih keduanya. Di sinilah katalog menjadi alat, bukan di C2.
   - Muat bekal dari hasil C2: POV-xx, CHAIN-xx (harness/mode fork), fakta FACTS.md (tipe data/desimal/sentinel), dan rantai [TOUCHES] RADAR.md — pagar terarah agar uji tidak membabi-buta.

1. Lazy-Load Plugin Spesifik Kandidat:
   Baca berkas references/methods/M-xxx-*.md dan methodology/attack-forms/AF-xx-*.md (serta DOM-*/POV-*/CHAIN-* bila ada) yang ditugaskan pada kandidat tersebut.
2. Bangun Titik 1 — Jejak Kode Eksak (`Exact Code Trace`):
   - Kutip titik masuk publik/eksternal/instruksi (Path/File.ext:Lxx-Lyy) dan lacak urutan pemanggilan hingga baris mutasi state/aset/valuasi (Path/File.ext:Lxx-Lyy).
   - Tunjukkan secara eksak mengapa setiap penjaga kode di sepanjang jalur tersebut berhasil dilewati.
3. Bangun Titik 2 — Bukti Eksekusi Nyata atau Jejak Matematika Konkret (`Concrete Execution / Math Proof`):
   - Opsi Utama (Test Runner Ekosistem): Tulis dan jalankan pengujian PoC menggunakan *test runner* proyek (forge test, cargo test, move test, snforge, pytest, go test, dll.) dan rekam hasil eksekusinya.
   - Opsi Setara (Jejak Matematika Konkret): Jika lingkungan eksekusi tidak dapat dijalankan secara lokal untuk komponen tersebut, sajikan perhitungan angka konkret langkah demi langkah pada setiap baris ekspresi kode (saldo awal, input spesifik, hasil pembagian integer/pembulatan, saldo akhir).
   - Catatan Jujur: Jika saat pengujian PoC atau perhitungan konkret kandidat tersebut gagal/revert/terbantahkan, catat bukti kegagalannya secara jujur di kartu tersebut agar siap dipindahkan ke 06-refuted-invalid.md pada STAGE-E.
4. Bangun Titik 3 — Delta Nilai Terukur & Kerusakan Invariant (`Value Delta & Broken Invariant`):
   - Hitung selisih nilai bersih (State Sebelum vs State Sesudah) dan sebutkan ID Invariant dari FACTS.md / path-map.md yang pecah.

---

## 3. Verifikasi Gate D & Transisi ke Tahap E

1. Pastikan seluruh kartu [ACTIVE] di 05-raw-leads.md bebas dari token kompresi terlarang (..., dll., dst., etc., rest of logic).
2. Jalankan gerbang verifikasi:

       python3 tools/verify_segitiga.py --gate D <audit-dir>

3. Setelah PASS, perbarui STATE.md (Current Stage: STAGE-E, Last Passed Gate: GATE-D) untuk mengadili batch ini melalui sc-e-verdict.
