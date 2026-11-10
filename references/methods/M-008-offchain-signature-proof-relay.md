# [M-008] Bedah Jembatan Hibrida: Tanda Tangan, Bukti Merkle/ZK, & Relayer Off-Chain Universal
- Classes: CRYPTOGRAPHY, SIGNATURE, MERKLE-ZK, OFFCHAIN-RELAY, CROSS-CHAIN
- Trigger Symptom: Modul memverifikasi tanda tangan (ecrecover/Ed25519/EIP-712), bukti merkle/ZK, pesan lintas-rantai, nonce, deadline, atau input dari relayer/keeper/sequencer.
- Paired Items: AF-08, AF-10, DOM-bridge-offchain, POV-relayer-mev

---

## 1. Inti Metode Bedah
M-008 membedah batas kepercayaan antara dunia *off-chain* (penandatangan, prover, relayer, pesan jembatan lintas-rantai) dan verifikator *on-chain* pada [EDGE-CONTROL/LATENT].

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Audit Keunikan & Ikatan Konteks Pesan/Tanda Tangan (*Replay & Domain Separation*):
   - Periksa seluruh parameter yang masuk ke dalam hash pesan/tanda tangan atau *public inputs* bukti ZK/Merkle di Path/File.ext:Lxx-Lyy.
   - Apakah hash tersebut mengikat: (a) identitas kontrak/modul target, (b) chainId / domain jaringan, (c) alamat penerima/eksekutor, (d) jumlah/aksi spesifik, (e) nonce unik yang langsung dibatalkan (*invalidated*) sebelum eksekusi, dan (f) batas waktu kedaluwarsa (*deadline*)?
   - Jika satu saja komponen di atas tidak masuk ke dalam hash, uji apakah tanda tangan/bukti yang sah dapat diputar ulang (*replay*) atau dibelokkan parameternya oleh relayer/MEV.
2. Audit Kelemahan Kriptografi & Leaf Merkle/ZK:
   - Apakah hasil pemulihan tanda tangan memeriksa nilai kosong (address(0)) dan kelenturan tanda tangan (*signature malleability*)?
   - Pada pohon Merkle: apakah daun (*leaf*) di-hash dua kali atau diberi awalan berbeda dari simpul tengah (*internal node*)? Apakah satu akun dapat mengklaim berkali-kali pada epoch yang sama?
   - Pada sirkuit/verifikator ZK: apakah seluruh *public input* benar-benar dikunci (*constrained*) di dalam sirkuit dan diperiksa batas medan primanya (*field aliasing*)?
3. Audit Ketidakcocokan Logika Off-Chain vs On-Chain:
   - Jika terdapat kode layanan *off-chain* (.ts, .py, .go) dalam *scope*, bandingkan rumus validasi/serialization di kode *off-chain* dengan kode verifikator *on-chain*.

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan konstruksi payload/tanda tangan/bukti yang dimodifikasi atau di-replay beserta baris verifikasi di Path/File.ext:Lxx-Lyy yang gagal menolaknya.
