# [POV-DEFI-02] Sudut Pandang: Valuation Source vs Execution Sink Mismatch
- Classes: CLASS-C (Protokol + Sumber Valuasi A [Oracle] + Venue Eksekusi B [DEX/AMM Spot]), CLASS-B
- Trigger Symptom: Kontrak membaca harga acuan dari Sumber A (Oracle/TWAP), tetapi mengeksekusi swap/rebalance/likuidasi ke Sumber B (pool spot) dengan `amountOutMin == 0`, parameter pemanggil, atau dihitung dari spot reserve Sumber B.
- Paired Items: M-001, M-004, M-005, M-008, AF-06, POV-liquidator, DOM-oracle

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin dengan modal pinjaman kilat pada pasangan aset di kolam likuiditas Sumber B (DEX/AMM spot). Tidak butuh peran protokol — hanya kemampuan memindahkan rasio likuiditas dalam satu transaksi atomik.

## 2. Gejala di Kode

Kontrak memakai Sumber A (Oracle eksternal atau TWAP) untuk memvalidasi kesehatan posisi atau nilai aset, **tetapi mengeksekusi** penukaran aset, pelepasan jaminan, atau penyeimbangan portofolio secara langsung di Sumber B (kolam spot atau pasar internal).

Fungsi yang memicu eksekusi ke Sumber B dapat dipanggil publik (atau dipicu tidak langsung oleh pengguna), sedangkan batas penerimaan minimum (`minimum output` / slippage guard) bernilai `0`, diambil dari parameter pemanggil, atau dihitung dari cadangan spot Sumber B saat transaksi berlangsung — bukan diturunkan ketat dari harga acuan Sumber A.

## 3. Rangkaian Serangan

1. **Siapkan:** siapkan modal atau flashloan pada pasangan aset di kolam Sumber B.
2. **Picu:** dalam satu transaksi atomik, pindahkan rasio likuiditas di Sumber B secara ekstrem (sementara harga di Sumber A tetap statis), lalu panggil fungsi protokol yang mengeksekusi transaksi ke Sumber B.
3. **Ekstraksi:** protokol mengeksekusi penukaran/pelepasan aset pada harga Sumber B yang terdistorsi, lalu penyerang memulihkan posisi Sumber B untuk mengekstrak selisih nilai dari protokol.

## 4. Auditor Blindspot

Auditor berhenti memeriksa risiko manipulasi harga begitu melihat kontrak membaca harga acuan dari Oracle yang tahan manipulasi satu blok (Sumber A), **tanpa memeriksa ke mana eksekusi riil dikirim (Sumber B)** dan bagaimana batas slippage pada eksekusi tersebut dihitung.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** (`REJECTED_POC_FAILS` / `REJECTED_NEGATIVE_EV`) **hanya setelah simulasi PoC** membuktikan bahwa: (a) `amountOutMin` pada eksekusi Sumber B diturunkan ketat dari harga Sumber A (dengan toleransi terukur), atau (b) distorsi Sumber B tidak dapat menggeser hasil eksekusi melewati toleransi tersebut, atau (c) laba penyerang selalu negatif setelah biaya.
- **Wajib PoC** dengan urutan: distorsi Sumber B → panggil fungsi protokol → pulihkan Sumber B. Ukur selisih nilai protokol sebelum/sesudah.
- Fuzz wajib mengacak: kedalaman likuiditas Sumber B, ukuran flashloan, dan selisih waktu/rasio antara Sumber A dan B.
