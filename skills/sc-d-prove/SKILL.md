---
name: sc-d-prove
description: Eksekusi STAGE-D (Pembuktian Tiga Titik Segitiga dengan Sistem Rolling Batch Maksimal 5 Kandidat [ACTIVE] per Putaran) pada Wilayah Aktif R_i.
---

# Skill sc-d-prove — Pembuktian Segitiga Rolling Batch (STAGE-D / L-PROVE)

Anda menjalankan Tahap D (`L-PROVE`) untuk Wilayah Aktif R_i menggunakan mekanisme Rolling Batch (Maksimal 5 Kandidat `[ACTIVE]` sekaligus di `05-raw-leads.md`) agar kedalaman pembuktian mencapai 100% tanpa kompresi konteks.

---

## 1. Langkah Pertama Mutlak (Hard Bootloader & Penarikan Batch)

1. Jalankan Pemulihan Konteks:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. Tarik Rolling Batch ke Meja Operasi (`<= 5 [ACTIVE]`):
   - Periksa Bagian 2 (Tabel [QUEUED]) di 05-raw-leads.md untuk Wilayah Aktif R_i.
   - Ambil maksimal 5 kandidat `[QUEUED]` dengan peringkat EV tertinggi (`P1` -> `P5`), ubah statusnya menjadi `[ACTIVE]`, dan buat kartu pembuktiannya di Bagian 3 (Blok Meja Operasi `[ACTIVE-BATCH]`) pada 05-raw-leads.md.
   - Aturan Besi: Dilarang keras memiliki lebih dari 5 kandidat berstatus [ACTIVE] pada saat bersamaan. Biarkan kandidat ke-6 dan seterusnya tetap berstatus [QUEUED] untuk diproses pada batch berikutnya setelah batch ini selesai diadili di STAGE-E.
   - Perbarui STATE.md (Current Stage: STAGE-D, Current Batch, Queued Leads Count, Active Leads Count).

---

## 2. Prosedur Pembuktian Tiga Titik Segitiga untuk Setiap Kandidat [ACTIVE]

Untuk masing-masing kandidat [ACTIVE] di meja operasi (maksimal 5 kandidat):

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
