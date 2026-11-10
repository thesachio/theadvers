---
name: sc-e-verdict
description: Eksekusi STAGE-E (Pengadilan Bukti Batch Aktif berdasarkan templates/VERDICT.md, Pengosongan Meja Operasi 05-raw-leads.md ke Wadah 06/07/08/09, dan Kontrol Putaran Rolling Batch D->E).
---

# Skill sc-e-verdict — Pengadilan Bukti Batch Aktif & Kontrol Rolling Batch (STAGE-E / L-VERDICT)

Anda menjalankan Tahap E (`L-VERDICT`) untuk mengadili seluruh kandidat [ACTIVE] pada batch saat ini di Wilayah Aktif R_i menggunakan hukum acara di templates/VERDICT.md.

---

## 1. Langkah Pertama Mutlak (Hard Bootloader Konteks)

Jalankan pemulihan konteks dan baca aturan templates/VERDICT.md:

    python3 tools/verify_segitiga.py --context-packet <audit-dir>

---

## 2. Prosedur Pengadilan Setiap Kandidat [ACTIVE] (Pengosongan Meja Operasi)

Periksa satu per satu kandidat berstatus [ACTIVE] di Bagian 3 ([ACTIVE-BATCH]) pada 05-raw-leads.md, lalu pindahkan seluruh rincian buktinya ke salah satu dari 4 wadah kanonik tujuan:

> **Setiap wadah menuntut JENIS BUKTI yang berbeda.** Memindahkan lead ke wadah yang salah = laporan DITOLAK. Aturan lengkap: `templates/VERDICT.md` §4–§9.

1. Pindahkan ke `06-refuted-invalid.md` apabila PoC gagal/revert, angka konkret membuktikan tidak ada keuntungan/kerugian bersih, atau serangan tertahan penjaga yang baru terdeteksi saat pembuktian.
   - **Wajib:** kelas `REJECTED_*` + `TANGGA_BUKTI` + `DEPLOYMENT_MATCH` + jangkar `Path/File.ext:Lxx-Lyy`.
   - Kelas `REJECTED_POC_FAILS` / `REJECTED_NEGATIVE_EV` / `REJECTED_DUST` **WAJIB** memuat `BUKTI_SIMULASI:` berisi perintah `$ ...` **beserta keluarannya**, termasuk *Victim Seeding* dan **Strike 3 Fuzz**. Tanpa itu → `PAPER_REFUTATION_DETECTED`.
   - Satu-satunya pengecualian tanpa kode test: **KS-1..KS-4** (`MISMATCH`, `BY_DESIGN`, `GENESIS_MIRAGE`, `NON_LIVE_INIT`) yang dibuktikan dengan kutipan/bytecode.
2. Pindahkan ke `07-needs-next-step.md` **hanya** apabila lead sudah diusahakan sampai batas tooling dan usaha itu terbaca dari berkasnya.
   - **Wajib:** `Disposition:` tepat satu dari `NEXT_EXPLORE` | `NEXT_MAINNET` | `TOOL_BLOCKED` | `ENV_ERROR`, **dan** blok `PERCOBAAN:` berisi perintah `$ ...` + keluaran nyata. `PERCOBAAN:` bukan rencana.
   - Bukti per label: `NEXT_EXPLORE` → log fuzz/halmos sampai timeout; `TOOL_BLOCKED` → log **ketiga** anak tangga self-healing; `NEXT_MAINNET` → bukti RPC/explorer memang tidak tersedia (bila RPC ada, `07` tidak sah); `ENV_ERROR` → dua endpoint gagal.
   - `TANGGA_BUKTI: A`/`A-HEAD` **tidak sah** di `07` (bukti yang sudah PASS wajib ke `09` atau `08`).
   - Tanpa salah satu di atas → `LAZY_BAILOUT_DETECTED`. **Target akhir `07` = 0 entri.**
3. Pindahkan ke `08-valid-not-eligible.md` **hanya** apabila mekanisme sudah **terbukti** (`POC_STATUS: PASS`).
   - **Wajib:** `LOW_CLASS` tepat satu dari `PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)` | `ADMIN_ONLY` | `LOW_NUISANCE`, dampak kuantitatif terukur, dan `BUKTI_SIMULASI:` nyata.
   - Lead yang **belum teruji** lalu dilabeli Low adalah pelarian wadah (§11b) → kembalikan ke `07`.
   - Severity ditentukan **impact**, bukan siklus deployment.
4. Pindahkan ke `09-confirmed-findings.md` apabila dan hanya apabila kandidat lulus Tiga Titik Bukti Segitiga utuh **dan** Sepuluh Pernyataan Keras (`templates/VERDICT.md` §8) **dan** Integritas #11 (§9).
   - **Wajib:** `TANGGA_BUKTI: A | B` (`A-HEAD` dilarang), `DEPLOYMENT_MATCH: LIVE_MATCH`, `LIVE_IDENTITY` terukur, `POC_STATUS: PASS`, `BUKTI_SIMULASI:` nyata.
   - `CYCLE: P1_PRE_DEPLOY` / `P2_TESTNET_ONLY` dilarang di `09`.

Setelah seluruh kandidat batch ini dipindahkan:
- Hapus kartu yang sudah diadili dari Blok [ACTIVE-BATCH] di 05-raw-leads.md dan ubah status barisnya di Tabel Bagian 2 menjadi [MOVED-TO-06], [MOVED-TO-07], [MOVED-TO-08], atau [MOVED-TO-09].
- Pastikan `Current [ACTIVE] Leads Count` di `05-raw-leads.md` kembali menjadi `0`.

---

## 3. Verifikasi Gate E & Keputusan Cabang (*Rolling Batch Loop* vs STAGE-F)

1. Audit aturan wadah lebih dulu (cepat, tanpa perlu seluruh gate):

       python3 tools/verify_segitiga.py --rules <audit-dir>

2. Jalankan gerbang verifikasi:

       python3 tools/verify_segitiga.py --gate E <audit-dir>

   `--gate E` kini juga menegakkan seluruh aturan 06/07/08/09 di atas **dan** jejak lead:
   setiap lead yang hilang dari `05-raw-leads.md` wajib muncul di **tepat satu** wadah. Lead yang
   menguap tanpa tercatat di `06`/`07`/`08`/`09` → FAIL (`#11d`).

2. Hitung sisa kandidat berstatus `[QUEUED]` untuk Wilayah Aktif R_i di Bagian 2 05-raw-leads.md:
   - CABANG 1 — Jika masih ada `[QUEUED] > 0` untuk Wilayah `R_i`:
     Jangan pindah ke Tahap F! Perbarui STATE.md (Current Stage: STAGE-D, naikkan Current Batch +1, perbarui Queued Leads Count, set Active Leads Count: 0), lalu kembali jalankan `sc-d-prove` untuk menarik batch berikutnya (maksimal 5 kandidat [QUEUED]).
   - CABANG 2 — Jika `[ACTIVE] == 0` DAN `[QUEUED] == 0` untuk Wilayah `R_i`:
     Seluruh kandidat di Wilayah R_i telah tuntas diadili. Perbarui STATE.md (Current Stage: STAGE-F, Queued Leads Count: 0, Active Leads Count: 0, Last Passed Gate: GATE-E), lalu lanjutkan ke `sc-f-report`.
