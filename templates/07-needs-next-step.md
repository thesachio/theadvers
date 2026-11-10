# 07-NEEDS-NEXT-STEP — Wadah Kandidat Butuh Verifikasi Lanjutan (STAGE-E)
> ATURAN PENGISIAN (`ZERO-COMPRESSION LAW`):
> 1. Wadah ini hanya untuk kandidat dari 05-raw-leads.md yang logika kodenya di repositori lokal valid dan belum terbantahkan, tetapi pembuktian akhirnya memerlukan informasi di luar kode lokal (misal: pembacaan state *live* on-chain, parameter konfigurasi deployment produksi, perilaku penyedia oracle/relayer eksternal, atau konfirmasi spesifikasi).
> 2. Jangan gunakan wadah ini sebagai tempat membuang kandidat yang malas diuji di kode lokal. Jika bisa dibuktikan dengan *test runner* lokal atau matematika konkret, wajib selesaikan hingga masuk ke 06-refuted-invalid.md atau 09-confirmed-findings.md.
> 3. Wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy` dan bebas dari token kompresi (..., dll., dst., etc., rest of logic).

---

## 1. TABEL ANTREAN TINDAK LANJUT (07-NEEDS-NEXT-STEP)

| Next-Step ID | Asal Lead ID | Region (R_i) | EV Rank (P1`–`P5) | Jangkar Kode (Path/File.ext:Lxx-Lyy) | Faktor Eksternal / On-Chain yang Belum Diketahui | Tindakan Verifikasi Spesifik yang Diperlukan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NEXT-R1-01 | LEAD-R1-xx | R_1 | [P1..P5] | [Path/File.ext:L70-L105] | [Contoh: Nilai parameter fee/delay pada proxy mainnet atau perilaku validasi di service relayer off-chain] | [Contoh: Query storage slot X di mainnet / uji dengan mock parameter Y] |

---

## 2. RINCIAN BUKTI SEMENTARA & PROTOKOL UJI LANJUTAN

### NEXT-R1-01 (Eks LEAD-R1-xx) — [Judul Kandidat]
- Region & Modul Terdampak: R_1 | [NamaModul.namaFungsi]
- Jejak Kode Lokal yang Sudah Terbukti (`Path/File.ext:Lxx-Lyy`): [Uraikan alur kode lokal yang membuka celah apabila kondisi eksternal terpenuhi]
- Kondisi Penentu (*Trigger Condition*): [Jika parameter/state eksternal X bernilai Y, maka invariant INV-R1-xx pecah; jika bernilai Z, maka aman]
- Rencana Eksekusi Lanjutan: [Langkah konkret untuk mengonfirmasi kondisi X]
