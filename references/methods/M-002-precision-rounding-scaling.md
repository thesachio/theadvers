# [M-002] Bedah Presisi, Pembulatan, & Skala Desimal Universal
- Classes: MATH, PRECISION, ROUNDING, DECIMAL-SCALING
- Trigger Symptom: Terdapat pembagian integer, konversi antar-token berbeda desimal (6 vs 18 vs 8), perkalian sesudah pembagian, atau perhitungan fee/share/reward bertahap.
- Paired Items: AF-02, AF-03, DOM-vault, DOM-amm

---

## 1. Inti Metode Bedah
M-002 membedah seluruh ekspresi pada [EDGE-VALUATION] yang melibatkan pembagian bilangan bulat (*integer division*), pergeseran bit, atau konversi skala desimal. Dalam sistem keuangan terdesentralisasi, pembulatan wajib selalu menguntungkan protokol/pool dan merugikan pemanggil transaksi.

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Audit Arah Pembulatan (*Rounding Direction Audit*):
   - Saat pengguna menyetor aset untuk mencetak share/klaim: jumlah share yang diterima wajib dibulatkan ke bawah (*floor*).
   - Saat pengguna menarik aset dengan nilai share tertentu: jumlah share yang dibakar wajib dibulatkan ke atas (*ceil*), dan aset yang keluar wajib dibulatkan ke bawah (*floor*).
   - Saat menghitung kewajiban utang atau biaya (*debt/fee*): kewajiban pengguna wajib dibulatkan ke atas (*ceil*).
2. Audit Hilangnya Presisi Dini (*Divide-Before-Multiply & Truncation*):
   - Cari ekspresi di mana pembagian dilakukan sebelum perkalian: (a / b) * c pada Path/File.ext:Lxx-Lyy.
   - Uji kondisi ketika a < b: apakah hasil (a / b) terpotong menjadi 0, sehingga pengguna mendapat biaya 0, penalti 0, atau bunga 0?
3. Audit Ketidaksesuaian Skala Desimal (*Cross-Decimal Mismatch*):
   - Periksa apakah rumus mengasumsikan semua aset berdesimal 18 (1e18), padahal aset dalam *scope* mendukung desimal 6 (USDC/USDT), 8 (WBTC/Move/Solana), atau desimal dinamis.
   - Uji apakah perkalian dua angka berdesimal tinggi melampaui batas tipe data (uint64, uint128, u64, i128) hingga memicu *revert* permanen atau *wrapping overflow*.

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Sajikan substitusi angka eksak pada rumus di Path/File.ext:Lxx-Lyy (misal input sebesar b - 1 atau pemecahan transaksi menjadi $N$ bagian kecil) dan tunjukkan selisih nilai bersih yang bocor.
