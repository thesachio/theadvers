# [DOM-vault] Heuristik Domain: Vault, Pool Share, & Pengelola Yield/Strategi Universal
- Classes: VAULT, YIELD, SHARES, STRATEGY
- Trigger Symptom: Modul mencetak/membakar share atas setoran aset, mengonversi assets <-> shares, atau menyalurkan dana ke strategi eksternal.
- Paired Items: M-001, M-002, M-004, M-007, AF-01, AF-02, AF-03

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Konservasi Rasio Share: Pengguna yang menyetor lalu langsung menarik pada blok yang sama tidak boleh menerima aset lebih banyak daripada yang disetorkannya (withdraw(deposit(x)) <= x).
2. Ketahanan Penyetor Pertama & Pool Kosong: Saat totalSupply == 0 (baik saat deploy awal maupun setelah seluruh pengguna keluar), penyerang tidak boleh mampu memanipulasi rasio totalAssets / totalSupply hingga membuat penyetor berikutnya menerima 0 share.
3. Sinkronisasi Aset Strategi: totalAssets() wajib mencerminkan jumlah kas lokal ditambah nilai riil yang ditempatkan di modul strategi eksternal tanpa menghitung ganda (*double counting*) atau kehilangan jejak saat strategi merugi.

## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]`:
  - Apakah token dengan potongan biaya transfer (*fee-on-transfer*) atau *rebasing* dicatat berdasarkan parameter amount input alih-alih selisih saldo sebelum dan sesudah transfer?
  - Apakah penarikan dari strategi eksternal dapat menghasilkan jumlah lebih kecil dari yang diminta (*slippage/loss*) tanpa mengurangi share pengguna secara proporsional?
- `[EDGE-VALUATION]`:
  - Periksa arah pembulatan pada deposit/mint vs withdraw/redeem di Path/File.ext:Lxx-Lyy (M-002 + AF-02).
  - Periksa apakah keuntungan hasil panen (*harvest yield*) langsung masuk ke totalAssets secara instan sehingga dapat di-*sandwich* (AF-05).
- `[EDGE-CONTROL/LATENT]`:
  - Saat modul dalam kondisi paused atau strategi ditarik darurat (*emergency withdraw*), apakah akuntansi utang/share antara vault induk dan sub-strategi tetap sinkron?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `VAULT / POOL SHARE`
- **Siklus aliran (L-PATH):** setor aset → cetak share → alokasi ke strategi → akrual yield → konversi balik → tarik aset → (bila gagal) sosialisasi kerugian
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «withdraw(deposit(x)) ≤ x pada blok yang sama»; «penyetor pertama tidak bisa mencetak share tak terbatas saat totalSupply == 0»; «nilai strategi tidak dihitung ganda maupun hilang saat merugi»
- **Aktor off-chain:**

  manajer strategi (diam = kelas ketiadaan-aksi), keeper harvest

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
