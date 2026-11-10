# STATE — Kursor Memori Kerja, Antrean Wilayah, & Write-Ahead Checkpoint (theadvers v2.0)

> ATURAN BESI (`ZERO-COMPRESSION & WRITE-AHEAD`):
> 1. Berkas ini adalah sumber kebenaran tunggal untuk posisi eksekusi agen dan sc-autopilot.
> 2. Perbarui blok CURSOR AKTIF dan LOG WRITE-AHEAD CHECKPOINT sebelum memulai tahap baru dan segera sesudah menyelesaikan tahap tersebut.
> 3. Setiap awal tahap, jalankan: python3 tools/verify_segitiga.py --context-packet <audit-dir>.

---

## 1. CURSOR AKTIF (MACHINE-READABLE)

- Target Project / Repo: [ISI_NAMA_PROYEK_ATAU_REPO]
- Primary Languages & Runtime: [ISI_BAHASA_DAN_RUNTIME, misal: Solidity/EVM, Rust/Solana, Move, Cairo, Go, Off-Chain TS/Py]
- Total Scope Files Reconciled: 0
- Active Region: NONE *(Isi NONE saat STAGE-0, R_1..R_N saat loop wilayah, atau CROSS-REGION saat FINAL-SWEEP)*
- Current Stage: STAGE-0 *(Nilai valid: STAGE-0, STAGE-A, STAGE-B, STAGE-C1, STAGE-C2, STAGE-D, STAGE-E, STAGE-F, FINAL-SWEEP, COMPLETED)*
- Current Batch ID: NONE *(Format `<R_i>-B<nn>`, mis. R1-B01. Di-reset ke B01 saat wilayah berganti)*
- Queued Leads Count (Active Region): 0 *(Jumlah kandidat berstatus [QUEUED] di 05-raw-leads.md untuk wilayah aktif)*
- Active Leads Count (Active Batch): 0 *(Wajib 1..3 saat STAGE-D; 1–2 hanya bila batch terakhir wilayah; wajib 0 setelah STAGE-E & saat menutup wilayah)*
- Batch Scope: Satu batch = satu wilayah *(kartu [ACTIVE] wilayah lain dilarang ikut)*
- Last Passed Gate: NONE
- Next Exact Action: Jalankan inventarisasi 100% berkas scope ke Tabel Rekonsiliasi di path-map.md dan kunci dengan --gate 0.

---

## 2. TABEL ANTREAN WILAYAH UANG (R_1 .. R_N) — URUTAN PRIORITAS EV (SOUL.md §3)

*Diisi pada STAGE-0 setelah 100% berkas sumber direkonsiliasi ke Tier 1/2/3 di path-map.md. Seluruh berkas Tier 1 dan Tier 2 wajib masuk ke salah satu Wilayah R_i.*

| Region ID | Nama Wilayah Uang / Klaster Modul | Peringkat EV (P1`–`P5) | Daftar Berkas Sumber (Path/File.ext) | Status Wilayah ([OPEN] / [ACTIVE] / [CLOSED]) | Ringkasan Hasil (09 Confirmed / 07 Next-Step) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R_1 | [Nama Klaster Nilai Tertinggi] | P1 | [Path/File1.ext, Path/File2.ext] | [OPEN] | 0 Confirmed / 0 Next-Step |
| R_2 | [Nama Klaster Berikutnya] | P2 | [Path/File3.ext] | [OPEN] | 0 Confirmed / 0 Next-Step |

---

## 3. RINGKASAN KALKULASI WADAH KANONIK (04 s/d 09)

| Wadah Kanonik | Jumlah Entri Total Lintas-Wilayah | Keterangan Status |
| :--- | :--- | :--- |
| `04-code-guarded.md` | 0 | Jalur/hipotesis yang terbukti sudah dijaga rapat oleh kode pada Tahap C |
| `05-raw-leads.md` (`[QUEUED]`) | 0 | Antrean kandidat lolos Segitiga di wilayah aktif (wajib 0 saat wilayah ditutup) |
| `05-raw-leads.md` (`[ACTIVE]`) | 0 | Meja operasi pembuktian batch aktif (maksimal 3 per batch, satu Batch ID, wajib 0 usai Tahap E) |
| `06-refuted-invalid.md` | 0 | Kandidat yang patah/gugur saat pembuktian Tahap D/E |
| `07-needs-next-step.md` | 0 | Kandidat yang membutuhkan verifikasi state live / komponen eksternal |
| `08-valid-not-eligible.md` | 0 | Perilaku valid teknis tetapi di luar kelayakan klaim (*out-of-scope / known / admin*) |
| `09-confirmed-findings.md` | 0 | Temuan sahih lulus Bukti Segitiga + dilengkapi *Submission-Ready Report* di Tahap F |

---

## 4. LOG WRITE-AHEAD CHECKPOINT (JEJAK PEMULIHAN ANTI-KOMPRESI)

*Catat setiap pergantian tahap/batch/wilayah secara kronologis. Jangan menghapus baris lama.*

| Checkpoint ID | Wilayah & Tahap (R_i / STAGE) | Status (START / GATE-PASS) | Berkas yang Diubah & Jangkar Utama (Path/File.ext:Lxx-Lyy) | Instruksi Pemulihan Presisi Jika Sesi Terputus |
| :--- | :--- | :--- | :--- | :--- |
| CP-001 | GLOBAL / STAGE-0 | START | path-map.md, STATE.md | Lanjutkan pendataan 100% berkas scope ke Tier 1/2/3 di path-map.md lalu jalankan --gate 0. |
