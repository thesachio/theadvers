---
name: sc-f-report
description: Eksekusi STAGE-F (Penulisan Submission-Ready Disclosure Inkremental di 09-confirmed-findings.md untuk Wilayah Aktif R_i, Penutupan Wilayah --close-region R_i, & Hard Context Flush) serta FINAL-SWEEP (--final) setelah seluruh wilayah selesai.
---

# Skill sc-f-report — Incremental Disclosure Wilayah (STAGE-F) & Cross-Region Final Sweep (FINAL-SWEEP)

Anda menjalankan Tahap F (`L-DISCLOSURE`) di ujung setiap Wilayah Aktif R_i selagi konteks kode dan bukti Wilayah R_i masih 100% segar di memori, serta menjalankan Penutupan Global (`FINAL-SWEEP`) setelah seluruh wilayah berstatus [CLOSED].

---

## 1. Langkah Pertama Mutlak (Hard Bootloader Konteks)

Jalankan pemulihan konteks:
python3 tools/verify_segitiga.py --context-packet <audit-dir>

---

## 2. Prosedur STAGE-F: Incremental Disclosure & Penutupan Wilayah Aktif R_i

1. Pastikan Antrean Wilayah `R_i` Bersih Mutlak:
   Verifikasi bahwa di 05-raw-leads.md tidak ada lagi kandidat milik Wilayah R_i yang berstatus [ACTIVE] maupun [QUEUED] ([ACTIVE] == 0 dan [QUEUED] == 0).
2. Lengkapi Naskah *Submission-Ready Disclosure* di `09-confirmed-findings.md`:
   Untuk setiap temuan milik Wilayah R_i di 09-confirmed-findings.md, tulis dan lengkapi Blok B (`Submission-Ready Disclosure`) secara utuh tanpa pemotongan logika:
   - Judul Presisi (Akar Masalah + Modul/Fungsi + Dampak Nilai),
   - Severity & Peringkat EV (SOUL.md §3),
   - Ringkasan Eksekutif,
   - Analisis Akar Masalah berjangkar Path/File.ext:Lxx-Lyy,
   - Langkah Eksploitasi & Kode Uji PoC / Perhitungan Konkret Lengkap,
   - Kuantifikasi Dampak Ekonomi terhadap Current Balance & Intended Capacity,
   - Rekomendasi Perbaikan Kode (*Patch/Diff* Spesifik),
   - Ubah status temuan pada tabel indeks 09-confirmed-findings.md menjadi `[SUBMISSION-READY]`.
3. Jalankan Gerbang Penutup Wilayah (`--close-region`):

       python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>

4. Transisi Wilayah & *Hard Context Flush***:
   - Setelah `--close-region <R_i>` dinyatakan `PASS`, ubah status Wilayah `R_i` pada Tabel Antrean Wilayah di `STATE.md` menjadi [CLOSED].
   - Periksa Tabel Antrean Wilayah di `STATE.md`:
     - **Jika masih ada wilayah berstatus `[OPEN]`: Ambil wilayah [OPEN] berikutnya dengan EV tertinggi (R_{i+1}), ubah statusnya menjadi [ACTIVE], set Active Region: R_{i+1}, Current Stage: STAGE-A, Current Batch ID: NONE *(reset — batch pertama wilayah baru dimulai `R{i+1}-B01`)*, lakukan Hard Context Flush (lupakan detail internal R_i yang tidak tertulis di FACTS.md/RADAR.md), dan mulai siklus baru untuk R_{i+1} menggunakan sc-a-scope.
     - Jika seluruh wilayah `R_1 .. R_N` sudah berstatus `[CLOSED]`: Set Active Region: CROSS-REGION dan Current Stage: FINAL-SWEEP di STATE.md, lalu jalankan Bagian 3 di bawah ini.

---

## 3. Prosedur FINAL-SWEEP: Cross-Region Chain Verification & Kunci Akhir (--final)

1. Segarkan Konteks `FINAL-SWEEP`:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. Audit Silang Sinyal `RADAR.md` Lintas-Wilayah (`R_1 .. R_N`):
   - Periksa seluruh baris di RADAR.md: apakah ada sinyal [TOUCHES: NamaModul.simbol] yang baru ditemukan pada wilayah-wilayah akhir (R_N) yang mematahkan asumsi fakta atau menyentuh variabel yang sama di wilayah-wilayah awal (R_1)?
   - Jika ditemukan rantai lintas-wilayah baru yang belum pernah diuji:
     - Masukkan ke Tabel [QUEUED] di 05-raw-leads.md dengan Region CROSS-REGION,
     - Jalankan siklus `sc-d-prove` -> `sc-e-verdict` -> `sc-f-report` (maksimal 3 kandidat per batch, satu `Batch ID` `<R_i>-B<nn>` berprefiks wilayah yang sama) hingga kembali bersih ([QUEUED] == 0 dan [ACTIVE] == 0). **Jangan pindah wilayah** selama `[QUEUED]` wilayah aktif masih > 0.
3. Jalankan Gerbang Pengunci Akhir (`--final`):

       python3 tools/verify_segitiga.py --final <audit-dir>

4. Setelah --final dinyatakan PASS, perbarui STATE.md (Current Stage: COMPLETED, Last Passed Gate: FINAL) dan laporkan ringkasan eksekutif hasil audit kepada pengguna.
