# [DOM-amm] Heuristik Domain: AMM, Pertukaran Likuiditas, Orderbook, & Router Swap Universal
- Classes: AMM, DEX, SWAP, LIQUIDITY-POOL, SLIPPAGE
- Trigger Symptom: Modul menukar pasangan aset, menghitung kurva invarian (x*y=k, CLMM, stableswap), mengelola LP token/posisi, atau merutekan swap.
- Paired Items: M-002, M-003, M-004, AF-01, AF-02, AF-04, AF-05

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Non-Penurunan Invarian Kurva: Setelah setiap swap atau flash swap selesai, nilai fungsi kurva pool (K_after >= K_before setelah dikurangi fee resmi) tidak boleh turun.
2. Isolasi Akumulator Fee & Likuiditas Aktif: Penyedia likuiditas (LP) yang baru masuk tidak boleh mengklaim fee perdagangan yang terkumpul sebelum mereka masuk (*past accrued fees*).
3. Keamanan Eksekusi Router: Modul router tidak boleh menyisakan saldo token atau izin *allowance* pengguna yang dapat disapu oleh pemanggil berikutnya.

## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]`:
  - Apakah fungsi swap mengizinkan tokenIn == tokenOut sehingga cadangan aset yang sama dibaca dan ditulis ulang dengan nilai ganda (AF-03)?
  - Pada router/aggregator: apakah sisa token yang tidak terpakai dalam multi-hop swap dikembalikan ke pengguna asli atau tertinggal di kontrak router?
- `[EDGE-VALUATION]`:
  - Pada likuiditas terkonsentrasi (CLMM) atau kurva khusus: apakah penyeberangan batas *tick/bin* memperbarui pertumbuhan fee (feeGrowthOutside) dengan arah tanda yang benar di Path/File.ext:Lxx-Lyy?
- `[EDGE-CONTROL/LATENT]`:
  - Apakah operasi internal protokol (seperti *auto-compounding*, *buyback*, atau likuidasi otomatis) melakukan swap di AMM dengan amountOutMin == 0 atau menggunakan block.timestamp sebagai deadline sehingga dapat di-*sandwich* (AF-05)?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `LP / AMM`
- **Siklus aliran (L-PATH):** tambah likuiditas → swap → akrual fee → arbitrase balik → hapus likuiditas; loop flashloan
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «k konstan (xy=k)»; «fee monoton, non-decreasing»; «callback token tidak reenter di state timpang»; «LP token mint/burn persis proporsional»
- **Aktor off-chain:**

  bot arbitrase, quoter (harga off-chain vs pool on-chain = AF-10)

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
