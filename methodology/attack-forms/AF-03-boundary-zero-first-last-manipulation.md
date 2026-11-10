# [AF-03] Eksploitasi State Kosong (0->1 / 1->0), Nilai Batas, & Refleksif (self)
- Classes: ZERO-STATE, BOUNDARY-VALUE, FIRST-DEPOSITOR, SELF-TRANSFER
- Trigger Symptom: Terdapat percabangan saat totalSupply == 0, penarikan terakhir, input 0 / 1 / MAX, atau parameter sumber dan tujuan dapat diisi entitas yang sama.
- Paired Items: M-002, M-004, M-007, DOM-vault, DOM-staking

---

## 1. Mekanisme Serangan Universal
Penyerang memicu cabang logika khusus yang hanya aktif saat modul kosong (0), saat seluruh pengguna keluar lalu masuk kembali (*empty-then-reenter*), saat diberikan input bernilai 0 / MAX, atau saat fungsi dipanggil secara refleksif (from == to, liquidator == borrower, tokenIn == tokenOut).

## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Uji Skenario Siklus Kosong-Ulang (`Empty Pool Reset`):
   - Buat state di mana seluruh pengguna menarik dananya hingga totalSupply == 0, namun rewardIndex, accumulatedFees, atau sisa saldo debu tidak di-reset ke kondisi awal.
   - Masukkan setoran baru dan buktikan apakah penyetor baru langsung mewarisi seluruh akumulasi masa lalu atau mengalami kegagalan perhitungan.
2. Uji Input `0` & Input Refleksif pada `Path/File.ext:Lxx-Lyy`:
   - Panggil fungsi dengan amount = 0 untuk melihat apakah ia melewati pemeriksaan saldo tetapi tetap memperbarui timestamp/hak klaim.
   - Panggil fungsi dua-pihak dengan akun/objek yang sama (A == B) dan lacak bagaimana variabel memori sementara menulis ulang state penyimpanan.
3. Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika terdapat penjaga eksplisit (require(amount > 0), require(from != to), atau penguncian *dead shares* permanen saat inisialisasi) di jalur tersebut.
