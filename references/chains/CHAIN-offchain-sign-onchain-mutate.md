# [CHAIN-offchain-sign-onchain-mutate] Rantai: Penerbitan Bukti Off-Chain -> Mutasi State On-Chain -> Eksekusi Bukti Basi
- Classes: OFFCHAIN-DESYNC, SIGNATURE-REPLAY, STALE-STATE-EXECUTION
- Trigger Symptom: Bukti/tanda tangan/kuotasi dibuat secara *off-chain* berdasarkan state $S_1$, sementara pengguna dapat mengubah state *on-chain* menjadi $S_2$ sebelum bukti dieksekusi.
- Paired Items: M-008, M-010, AF-08, AF-10, DOM-bridge-offchain

---

## 1. Anatomi Rantai Serangan (Langkah 1 -> Langkah 2 -> Langkah 3)
1. Langkah 1 (Perolehan Bukti/Tanda Tangan Sah pada State $S_1$):
   Penyerang memenuhi seluruh syarat saldo/kolateral pada state $S_1$ sehingga sistem *off-chain* (backend signer, prover, relayer, atau oracle) menerbitkan tanda tangan atau bukti Merkle/ZK yang sah.
2. Langkah 2 (Mutasi State On-Chain ke $S_2$ di `Path/FileA.ext:Lxx-Lyy`):
   Sebelum mengirim bukti tersebut ke fungsi verifikasi *on-chain*, penyerang memanggil fungsi *on-chain* lain untuk menarik kolateralnya, memindahkan posisinya, atau mengubah parameter akunnya sehingga prasyarat ekonomi $S_1$ sebenarnya sudah tidak terpenuhi lagi.
3. Langkah 3 (Eksekusi Bukti pada State $S_2$ di `Path/FileB.ext:Lxx-Lyy`):
   Penyerang mengeksekusi bukti dari Langkah 1 di FileB. Karena FileB hanya memeriksa keaslian tanda tangan/bukti tanpa memeriksa apakah state akun masih sama dengan $S_1$, penyerang berhasil mengekstrak nilai dua kali.

## 2. Syarat Pembuktian di STAGE-D
- Tunjukkan struktur data yang ditandatangani di FileB:Lyy dan buktikan bahwa mutasi di FileA:Lxx tidak mengubah nonce/state-hash yang diperiksa oleh FileB.
