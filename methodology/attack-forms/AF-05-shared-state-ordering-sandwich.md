# [AF-05] Manipulasi Urutan Transaksi, Sandwich Indeks/Reward, & Desinkronisasi State
- Classes: MEV-SANDWICH, INDEX-FRONT-RUN, STATE-DESYNC, ORDERING
- Trigger Symptom: Distribusi reward/yield/bunga atau perubahan kurs dihitung tanpa periode penguncian waktu, atau >= 2 modul menyentuh [TOUCHES] state yang sama.
- Paired Items: M-003, M-009, M-010, POV-relayer-mev, CHAIN-shared-state-desync

---

## 1. Mekanisme Serangan Universal
Penyerang memanfaatkan urutan eksekusi transaksi dalam satu blok (atau urutan pemanggilan dua fungsi yang menyentuh variabel [TOUCHES: ...] yang sama) untuk masuk tepat sebelum lonjakan nilai/reward didistribusikan dan keluar tepat sesudahnya, atau memanggil Fungsi X untuk merusak asumsi state Fungsi Y.

## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Konstruksi Urutan `Tx1 -> Tx2 -> Tx3` pada `Path/File.ext:Lxx-Lyy`:
   - Tx1 (Penyerang): Masuk dengan modal besar (deposit/stake) atau mengubah state bersama melalui Modul A.
   - Tx2 (Pemicu / Korban): Distribusi yield/reward instan, *rebase*, atau eksekusi pengguna tanpa proteksi *slippage* (minOut == 0).
   - Tx3 (Penyerang): Keluar (withdraw/unstake/claim) pada blok yang sama dan membawa pergi porsi nilai milik pengguna lama.
2. Hitung Keuntungan Bersih:
   Buktikan dengan angka konkret bahwa hasil yang ditarik pada Tx3 dikurangi modal Tx1 dan biaya protokol bernilai positif (Net Profit > 0).
3. Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika reward didistribusikan secara linear berbasis waktu (*streaming vesting*), terdapat *cooldown/lockup period* yang mengikat modal, atau biaya masuk/keluar (*entry/exit fee*) lebih besar dari porsi reward yang bisa dicuri.
