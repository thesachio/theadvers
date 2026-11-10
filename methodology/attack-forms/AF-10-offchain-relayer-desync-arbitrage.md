# [AF-10] Eksploitasi Kesenjangan Off-Chain vs On-Chain, Relayer Abuse, & Delay Arbitrage
- Classes: OFFCHAIN-ONCHAIN-DESYNC, RELAYER-MANIPULATION, STALE-PROOF, BRIDGE
- Trigger Symptom: Sistem menggabungkan komponen *off-chain* (indexer, relayer, keeper, sequencer, prover) dengan kontrak/modul *on-chain*.
- Paired Items: M-008, DOM-bridge-offchain, POV-relayer-mev

---

## 1. Mekanisme Serangan Universal
Penyerang mengeksploitasi jeda waktu (*latency*), perbedaan aturan validasi, atau asumsi kepercayaan antara layanan *off-chain* dan modul *on-chain*—misalnya dengan mengubah state *on-chain* tepat setelah bukti/tanda tangan *off-chain* diterbitkan namun sebelum transaksi relayer dieksekusi.
## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Petakan Jendela Waktu Antara Pembuatan Bukti Off-Chain & Eksekusi On-Chain (`Path/File.ext:Lxx-Lyy`):
   - Identifikasi state *on-chain* apa yang diasumsikan tetap sama oleh komponen *off-chain* saat menandatangani pesan atau membuat root Merkle/ZK.
2. Uji Skenario *State Mutation Between Sign and Execute***:
   - Minta izin/tanda tangan/kuotasi dari sistem *off-chain* pada kondisi state $S_1$.
   - Sebelum mengeksekusi bukti tersebut di *on-chain*, lakukan transaksi langsung di *on-chain* (misal menarik kolateral, memindahkan posisi, atau mengubah parameter akun) menjadi state $S_2$.
   - Eksekusi bukti *off-chain* tadi pada state $S_2$ dan buktikan bahwa modul *on-chain* tidak memverifikasi ulang prasyarat $S_1$.
3. **Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika modul *on-chain* melakukan validasi ulang terhadap seluruh invariant state kritis pada saat transaksi dieksekusi dan mengikat snapshot versi state di dalam bukti.

## 3. Bentuk Serangan (Cara Menyerang) — dari Registry v1

- **[BENTUK-02] Transaktor Pemicu** — relayer/keeper sah menjalankan rutinitasnya; yang dirancang penyerang adalah **state yang dibacanya**.
- **[BENTUK-04] Racun State Dulu, Korban Eksekusi Terakhir** — kronologis: attacker meracuni state (tx 1) → korban/relayer menjalankan rutin (tx 2) → hasil tx korban dibajak. Kerugian di tx **korban** wajib terukur.
- **[BENTUK-09] Penyisipan Lintas-Transaksi (Async)** — dua pesan asinkron saling menyusup tanpa `pending-lock`.

Rujuk `M-008`, `POV-TON-01`, `POV-relayer-mev`.
