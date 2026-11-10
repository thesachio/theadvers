# [AF-06] Manipulasi Harga/Valuasi, Pemicuan Likuidasi Prematur, & Self-Liquidation
- Classes: ORACLE-MANIPULATION, LIQUIDATION-ABUSE, BAD-DEBT, AUCTION
- Trigger Symptom: Nilai agunan/utang atau batas kesehatan posisi menggunakan harga spot/oracle yang dapat digerakkan, basi (*stale*), atau diskon likuidasi melebihi jaminan.
- Paired Items: M-004, M-006, M-010, DOM-lending, DOM-oracle, POV-liquidator

---

## 1. Mekanisme Serangan Universal
Penyerang memanipulasi komponen penentu valuasi ([EDGE-VALUATION]) atau memanfaatkan kelemahan rumus likuidasi ([EDGE-CONTROL/LATENT]) untuk: (a) meminjam aset melampaui nilai agunan sebenarnya, (b) memicu penyitaan paksa atas posisi pengguna yang sehat, atau (c) melikuidasi posisinya sendiri (*self-liquidation*) guna mengantongi bonus likuidasi dan meninggalkan utang macet (*bad debt*) pada protokol.
## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Bedah Rumus Kesehatan & Bonus Likuidasi di `Path/File.ext:Lxx-Lyy`:
   - Hitung berapa kolateral yang disita (collateralSeized = debtRepaid * price * (1 + bonus)) dibanding sisa agunan dan sisa utang posisi tersebut.
2. Uji Skenario *Self-Liquidation* & *Bad Debt***:
   - Ketika rasio agunan posisi berada di antara `100%` dan `100% + liquidationBonus`, uji apakah pemilik posisi (melalui akun kedua) dapat melikuidasi dirinya sendiri untuk menyita `100%` agunan hanya dengan membayar sebagian utang, lalu membiarkan sisa utangnya menjadi kerugian protokol.
3. **Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika sumber harga tidak dapat dimanipulasi secara ekonomis dan rumus likuidasi membatasi penyitaan sekaligus melakukan sosialisasi/penutupan *bad debt* dengan benar.

## 3. Bentuk Serangan (Cara Menyerang) — dari Registry v1

- **[BENTUK-09] Penyisipan Lintas-Transaksi** — valuasi membaca Sumber A (oracle/TWAP) tetapi eksekusi dikirim ke Sumber B (pool spot): distorsi B → panggil protokol → pulihkan B.
- **[BENTUK-02] Transaktor Pemicu** — seeding posisi korban lebih dulu (`vm.prank(victim)`), lalu likuidasi/premanen.
- **[BENTUK-03] Bundler Transaksi** — flashloan modal besar + likuidasi + pemulihan posisi dalam satu blok.
- **[BENTUK-01] Serangan Langsung** — self-liquidation dua identitas (`Attacker_A` borrower, `Attacker_B` liquidator).

Rujuk `POV-DEFI-01`, `POV-DEFI-02`, `M-003`.
