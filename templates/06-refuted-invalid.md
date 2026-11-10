# 06-REFUTED-INVALID — Wadah Kandidat Gugur Pasca-Pembuktian (STAGE-E)

> ATURAN PENGISIAN (`ZERO-COMPRESSION LAW`):
> 1. Wadah ini menampung kandidat dari meja operasi 05-raw-leads.md yang gugur saat uji pembuktian di `STAGE-D` / `STAGE-E` (misal: eksekusi test gagal/revert, perhitungan angka konkret membuktikan tidak ada pencurian/kerusakan nilai, atau tertahan penjaga kode di modul lain yang baru terlihat saat penelusuran penuh).
> 2. Setiap kandidat yang digugurkan wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy` dan alasan teknis eksak mengapa ia patah. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).

---

## 1. TABEL RINGKASAN KANDIDAT GUGUR (06-REFUTED-INVALID)

| Refuted ID | Asal Lead ID | Region (R_i) | Titik Masuk (NamaModul.namaFungsi) | Jangkar Kode Penahan / Pembantah (Path/File.ext:Lxx-Lyy) | Ringkasan Mengapa Eksploitasi Gagal Saat Pembuktian |
| :--- | :--- | :--- | :--- | :--- | :--- |
| REF-R1-01 | LEAD-R1-xx | R_1 | [NamaModul.namaFungsi] | [Path/File.ext:L112-L128] | [Jelaskan secara eksak mengapa PoC revert atau mengapa hitungan matematis tidak menghasilkan delta nilai positif/kerusakan] |

---

## 2. ARSIP DETAIL PEMBUKTIAN YANG TERBANTAHKAN

### REF-R1-01 (Eks LEAD-R1-xx) — [Judul Kandidat yang Gugur]
- Region & EV Awal: R_1 | [P1..P5]
- Plugin yang Diuji: [M-xxx, AF-xx]
- Hipotesis Awal: [Ringkasan dugaan serangan sebelum diuji]
- Jejak Kode & Titik Patah (`Path/File.ext:Lxx-Lyy`): [Kutipan kondisi kode atau urutan state yang mematahkan hipotesis]
- Bukti Kegagalan PoC / Perhitungan Konkret: [Log revert dari test runner atau hitungan angka konkret yang membuktikan invariant tetap terjaga]
