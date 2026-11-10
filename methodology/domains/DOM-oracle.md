# [DOM-oracle] Heuristik Domain: Adapter Harga, TWAP, Feed Eksternal, & Penilaian Aset Universal
- Classes: ORACLE, PRICE-FEED, TWAP, DECIMAL-NORMALIZATION
- Trigger Symptom: Modul membaca harga dari sumber eksternal/internal, menggabungkan beberapa feed, atau menormalisasi desimal harga lintas-aset.
- Paired Items: M-002, M-004, AF-06, CHAIN-flash-oracle-liquidation

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Kebenaran Skala & Unit Harga: Harga yang dikembalikan oleh adapter oracle wajib dinormalisasi secara konsisten terhadap desimal feed DAN desimal aset dasar (base/quote).
2. Ketahanan Manipulasi Satu Blok: Harga yang digunakan untuk keputusan solvensi/likuidasi tidak boleh berasal dari rasio saldo instan atau cadangan spot yang dapat diubah dengan pinjaman kilat dalam blok yang sama.
3. Keamanan Fallback & Staleness: Kegagalan satu sumber harga tidak boleh menghasilkan harga 0 yang dianggap valid, dan tidak boleh pula mematikan permanen fungsi penyelamatan dana pengguna.
## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-VALUATION]`:
  - Periksa rumus normalisasi di Path/File.ext:Lxx-Lyy: apakah kode mengalikan alih-alih membagi ketika menggabungkan dua feed terbalik (misal ETH/USD dan USD/USDC)?
  - Untuk oracle berbasis eksponen dinamis (seperti Pyth): apakah kode menangani nilai eksponen negatif dan positif serta memeriksa lebar *confidence interval*?
- `[EDGE-CONTROL/LATENT]`:
  - Apakah pemeriksaan batas usia data (*staleness threshold*) terlalu sempit untuk feed yang detak jantungnya (*heartbeat*) 24 jam, sehingga membuat fungsi liquidate dan withdraw selalu *revert* di kondisi normal (AF-09)?
  - Apakah harga LP token dihitung langsung dari reserve * price / totalSupply tanpa rumus *fair LP pricing*, sehingga rentan terhadap *Read-Only Reentrancy* (AF-04) atau manipulasi cadangan (AF-06)?
