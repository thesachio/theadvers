# [CHAIN-flash-oracle-liquidation] Rantai: Modal Kilat -> Distorsi Harga/Indeks -> Pinjaman/Likuidasi Paksa
- Classes: FLASH-LOAN, ORACLE-MANIPULATION, LIQUIDATION-CASCADE
- Trigger Symptom: Sumber harga/indeks di [EDGE-VALUATION] bergantung pada state on-chain yang dapat digerakkan sesaat untuk memicu [EDGE-CONTROL/LATENT].
- Paired Items: M-004, M-006, AF-01, AF-06, DOM-oracle, DOM-lending

---

## 1. Anatomi Rantai Serangan (Langkah 1 -> Langkah 2 -> Langkah 3)
1. Langkah 1 (Persiapan Posisi & Modal Kilat):
   Penyerang menyiapkan posisi di modul target (atau mengincar posisi pengguna besar), lalu mengambil pinjaman kilat dalam jumlah besar.
2. Langkah 2 (Distorsi Sumber Valuasi di `Path/FileA.ext:Lxx-Lyy`):
   Penyerang menggerakkan cadangan pool, rasio vault, atau state penentu harga yang dibaca oleh adapter valuasi protokol.
3. Langkah 3 (Eksekusi Likuidasi / Pinjaman di `Path/FileB.ext:Lxx-Lyy` & Pemulihan Harga):
   Pada harga yang terdistorsi tersebut, penyerang mengeksekusi likuidasi paksa untuk menyita agunan dengan diskon besar (atau meminjam aset melebihi nilai kolateral), lalu mengembalikan state pool ke posisi semula dan melunasi pinjaman kilat.

## 2. Syarat Pembuktian di STAGE-D
- Hitung biaya penggerakan harga (*swap fee / slippage*) dibanding keuntungan bersih dari likuidasi/pinjaman berlebih, dan pastikan hasilnya menguntungkan secara positif dalam satu transaksi.
