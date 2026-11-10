# [M-004] Bedah Valuasi, Kurs Share/Indeks, & Sumber Harga Universal
- Classes: VALUATION, ORACLE, EXCHANGE-RATE, INDEX
- Trigger Symptom: Nilai klaim/kolateral/share dihitung dari rasio saldo instan, harga spot AMM, feed oracle, atau indeks global yang dapat dipengaruhi transaksi eksternal.
- Paired Items: AF-01, AF-03, AF-06, DOM-oracle, POV-liquidator

---

## 1. Inti Metode Bedah
M-004 membedah setiap rumus pada [EDGE-VALUATION] untuk menguji apakah penyerang dapat menggelembungkan atau menekan nilai tukar/harga sesaat demi mencetak klaim berlebih, meminjam melampaui kolateral, atau memicu likuidasi palsu.

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Bedah Denominator & Numerator Kurs Internal (`Share / Exchange Rate`):
   - Tulis rumus kurs dari Path/File.ext:Lxx-Lyy (misal price = totalAssets / totalSupply).
   - Uji apakah numerator (totalAssets) dapat dinaikkan secara instan tanpa mencetak totalSupply (melalui donasi langsung, flash loan, atau pemanggilan fungsi *harvest/distribute reward* tepat sebelum aksi).
   - Uji apakah perubahan kurs dapat di-*sandwich* di sekitar pendistribusian hasil (*reward/yield distribution*) tanpa periode penguncian waktu (*vesting/locking*).
2. Bedah Keandalan & Kesegaran Oracle Eksternal:
   - Apakah harga diambil dari cadangan spot pool AMM dalam blok yang sama?
   - Apakah pemeriksaan kesegaran waktu (*staleness heartbeat*), batas harga minimum/maksimum, status sequencer L2, atau validasi *confidence interval* (misal Pyth/Chainlink/TWAP) lengkap di Path/File.ext:Lxx-Lyy?
   - Apa yang terjadi jika oracle mengembalikan harga ekstrem atau revert saat pasar bergejolak—apakah jalur likuidasi/penarikan ikut membeku?
3. Bedah Akumulasi Indeks Global (*Global Index Accrual*):
   - Periksa apakah indeks bunga/reward global selalu diperbarui (*accrue/updateIndex*) sebelum saldo/utang pengguna diubah. Jika pengguna masuk sebelum indeks diperbarui (atau memperbarui indeks pengguna dengan indeks lama), hitung selisih nilai yang bocor.
## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Buktikan secara matematis bahwa keuntungan dari manipulasi valuasi melampaui biaya modal/fee serangan (Net Profit > Attack Cost).
