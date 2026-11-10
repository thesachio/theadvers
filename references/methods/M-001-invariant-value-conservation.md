# [M-001] Bedah Konservasi Nilai & Simetri Akuntansi Universal
- Classes: ACCOUNTING, VALUE-CONSERVATION, SOLVENCY
- Trigger Symptom: Terdapat pasangan fungsi masuk/keluar nilai (deposit/withdraw, mint/burn, lock/unlock, borrow/repay, stake/unstake) atau pencatatan saldo internal terpisah dari saldo riil.
- Paired Items: AF-01, AF-02, DOM-vault, DOM-lending

---

## 1. Inti Metode Bedah
M-001 menguji hukum kekekalan nilai di dalam Wilayah Aktif R_i: tidak boleh ada nilai, share, hak klaim, atau kapasitas utang yang tercipta tanpa setoran setara, atau hilang/tertahan tanpa pengurangan kewajiban yang setara.

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Pasangkan Setiap Jalur Masuk dan Keluar (`[EDGE-ASSET]`):
   - Sandingkan fungsi penambah klaim (deposit, mint, stake, addCollateral, openPosition) dengan fungsi pengurang klaim (withdraw, redeem, unstake, removeCollateral, closePosition, liquidate).
   - Tulis rumus perubahan state untuk keduanya secara berdampingan dengan jangkar Path/File.ext:Lxx-Lyy.
2. Uji Ketidaksimetrisan Variabel (*Asymmetric Accounting*):
   - Apakah jalur masuk menambahkan variabel A menggunakan rumus X, tetapi jalur keluar mengurangi variabel A menggunakan rumus Y?
   - Apakah ada biaya (*fee*), bunga, penalti, atau potongan token (*fee-on-transfer*) yang dihitung saat masuk tetapi dilupakan saat keluar (atau sebaliknya)?
3. Bandingkan Akuntansi Internal vs Saldo Riil (*Internal vs Actual Balance Desync*):
   - Jika modul menyimpan variabel pelacak internal (misal totalDeposits atau trackedBalance) sekaligus membaca saldo riil (balanceOf / saldo akun/objek), periksa apa yang terjadi jika aset dikirim langsung tanpa melalui fungsi masuk resmi (*direct injection/donation*).
   - Sebaliknya, jika fungsi pembersih (skim, sweep, recoverToken) tersedia, periksa apakah fungsi tersebut dapat menyapu aset yang sebenarnya masih menjadi jaminan klaim pengguna.
## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan urutan siklus penuh (Masuk -> Operasi Tengah -> Keluar) beserta lokasi Path/File.ext:Lxx-Lyy.
- Hitung dengan angka konkret bahwa Nilai Keluar > Nilai Masuk (pencurian/inflasi klaim) atau Total Kewajiban > Total Aset Pendukung (insolvensi).
