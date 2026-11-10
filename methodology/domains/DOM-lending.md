# [DOM-lending] Heuristik Domain: Pinjam-Meminjam, Kolateral, Utang, & Likuidasi Universal
- Classes: LENDING, BORROWING, COLLATERAL, LIQUIDATION, INTEREST
- Trigger Symptom: Modul mengelola kolateral, posisi pinjaman, akumulasi indeks bunga, batas *health factor* / LTV, atau penyitaan likuidasi.
- Paired Items: M-001, M-004, M-006, AF-06, AF-09, POV-liquidator

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Urutan Akumulasi Bunga (*Accrue First Invariant*): Indeks bunga pinjaman dan simpanan wajib diperbarui ke timestamp saat ini sebelum membaca kesehatan posisi, mencetak/membakar utang, atau mengubah kolateral.
2. Solvensi Pasca-Aksi: Tidak ada aksi pengguna (borrow, withdrawCollateral, transferPosition) yang boleh meninggalkan posisi dengan nilai agunan terboboti di bawah nilai utang (collateralValue * LTV < debtValue).
3. Kesehatan Likuidasi: Likuidasi tidak boleh menyita lebih dari 100% kolateral posisi sekaligus menyisakan utang aktif tanpa mekanisme penghapusan *bad debt*, dan tidak boleh mengizinkan *self-liquidation* yang menguntungkan peminjam.
## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]`:
  - Ketika pengguna melunasi utang (repay) atau dilikuidasi, apakah pengurangan pokok utang (*principal*) dan indeks utang pengguna menggunakan pembulatan ke atas untuk utang yang tersisa?
  - Apakah kolateral yang sedang menjadi jaminan utang masih bisa dipindahkan, di-*stake* ulang, atau digunakan di modul lain (cek tag [TOUCHES] di RADAR.md)?
- `[EDGE-VALUATION]`:
  - Periksa konversi desimal pada rumus collateralAmount * collateralPrice / debtPrice: jika kolateral berdesimal 6 dan aset pinjaman berdesimal 18, apakah faktor skala sudah tepat di Path/File.ext:Lxx-Lyy?
- `[EDGE-CONTROL/LATENT]`:
  - Uji kondisi di mana harga kolateral jatuh tajam: apakah pemeriksaan di dalam liquidate() justru *revert* ketika posisi mengalami insolvensi (*underwater*), sehingga utang macet terkunci selamanya (M-006 + AF-06 + AF-09)?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `LENDING`
- **Siklus aliran (L-PATH):** suplai → pinjam → update harga → likuidasi → lelang/bad-debt → bayar → tarik
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «kolateral tak pernah < utang tanpa jalur likuidasi tersedia»; «oracle tak bisa di-flashloan»; «share/debt tak bocor oleh pembulatan»; «bad debt tak tersosialisasi murah»
- **Aktor off-chain:**

  keeper likuidasi (diam = kelas ketiadaan-aksi), relayer oracle

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
