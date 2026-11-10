# [M-007] Bedah Kondisi Batas: Saldo Nol, Pengguna Pertama/Terakhir, & Nilai Ekstrem Universal
- Classes: BOUNDARY, ZERO-STATE, EMPTY-POOL, EXTREME-INPUT
- Trigger Symptom: Modul dapat berada pada state awal totalSupply == 0, totalAssets == 0, penarikan elemen terakhir, input bernilai 0 / 1 / MAX, atau transaksi ke diri sendiri (self-transfer).
- Paired Items: AF-02, AF-03, DOM-vault, DOM-staking

---

## 1. Inti Metode Bedah
M-007 menguji perilaku modul pada titik-titik diskontinuitas matematika dan siklus hidup state: saat modul baru diinisialisasi (0), saat dikosongkan lalu diisi ulang (*re-initialization of empty pool*), serta saat menerima input ekstrem.

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Transisi `0 -> 1` (Pengguna Pertama & Pool yang Dikosongkan Ulang):
   - Periksa cabang if (totalSupply == 0) atau if (totalShares == 0) pada Path/File.ext:Lxx-Lyy.
   - Apakah kondisi tersebut juga bisa tercapai kembali setelah semua pengguna keluar (*empty pool reset*), namun menyisakan variabel indeks/reward/saldo donasi lama yang merusak pengguna baru berikutnya?
2. Transisi `1 -> 0` (Pengguna Terakhir Keluar):
   - Saat pengguna terakhir menarik seluruh share/klaimnya, apakah pembagian 0 / 0, pembulatan sisa debu (*dust*), atau penguncian *minimum liquidity* menyebabkan transaksi terakhir *revert* atau menyisakan dana terjebak?
3. Uji Input Ekstrem & Kasus Refleksif (`0`, `1`, `MAX`, `from == to`):
   - Input `0` atau `1` wei/unit: Apakah memanggil deposit(0), withdraw(0), atau stake(0) tetap memicu klaim reward, mereset pengatur waktu (*lock timer*), atau melewati pemeriksaan biaya?
   - Kasus Refleksif (`sender == receiver` / `tokenA == tokenB`): Jika fungsi transfer(from, to, amount), liquidate(borrower == liquidator), atau swap(tokenIn == tokenOut) dipanggil dengan dua entitas yang sama, apakah saldo dibaca ke variabel sementara di memori sehingga menggandakan saldo (balance[a] = balance[a] + amount)?

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan nilai input batas eksak (0, 1, MAX, atau from == to) beserta jejak baris per baris di Path/File.ext:Lxx-Lyy yang memicu anomali state.
