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

1. Pindahkan ke `06-refuted-invalid.md` apabila:
   - Pengujian PoC gagal/revert, perhitungan angka konkret membuktikan tidak ada keuntungan/kerugian bersih, atau serangan tertahan oleh penjaga kode yang baru terdeteksi saat pembuktian. Wajib sertakan Path/File.ext:Lxx-Lyy penahannya.
2. Pindahkan ke `07-needs-next-step.md` apabila:
   - Alur kode lokal terbukti membuka celah, tetapi kepastian eksploitasi membutuhkan pengecekan faktor di luar repositori lokal (state *live* on-chain, parameter deployment produksi, atau layanan *off-chain* tertutup).
3. Pindahkan ke `08-valid-not-eligible.md` apabila:
   - Perilaku terbukti valid secara teknis, namun berada di luar *scope* resmi, termasuk *known issue*, membutuhkan peran terpercaya (*trusted admin/governance*) bertindak jahat, atau di bawah ambang kelayakan klaim.
4. Pindahkan ke `09-confirmed-findings.md` apabila dan hanya apabila:
   - Kandidat lulus Tiga Titik Bukti Segitiga secara utuh tanpa asumsi palsu dan lulus seluruh daftar periksa di templates/VERDICT.md.

Setelah seluruh kandidat batch ini dipindahkan:
- Hapus kartu yang sudah diadili dari Blok [ACTIVE-BATCH] di 05-raw-leads.md dan ubah status barisnya di Tabel Bagian 2 menjadi [MOVED-TO-06], [MOVED-TO-07], [MOVED-TO-08], atau [MOVED-TO-09].
- Pastikan `Current [ACTIVE] Leads Count` di `05-raw-leads.md` kembali menjadi `0`.

---

## 3. Verifikasi Gate E & Keputusan Cabang (*Rolling Batch Loop* vs STAGE-F)

1. Jalankan gerbang verifikasi:

       python3 tools/verify_segitiga.py --gate E <audit-dir>

2. Hitung sisa kandidat berstatus `[QUEUED]` untuk Wilayah Aktif R_i di Bagian 2 05-raw-leads.md:
   - CABANG 1 — Jika masih ada `[QUEUED] > 0` untuk Wilayah `R_i`:
     Jangan pindah ke Tahap F! Perbarui STATE.md (Current Stage: STAGE-D, naikkan Current Batch +1, perbarui Queued Leads Count, set Active Leads Count: 0), lalu kembali jalankan `sc-d-prove` untuk menarik batch berikutnya (maksimal 5 kandidat [QUEUED]).
   - CABANG 2 — Jika `[ACTIVE] == 0` DAN `[QUEUED] == 0` untuk Wilayah `R_i`:
     Seluruh kandidat di Wilayah R_i telah tuntas diadili. Perbarui STATE.md (Current Stage: STAGE-F, Queued Leads Count: 0, Active Leads Count: 0, Last Passed Gate: GATE-E), lalu lanjutkan ke `sc-f-report`.
