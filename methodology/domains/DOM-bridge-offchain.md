# [DOM-bridge-offchain] Heuristik Domain: Jembatan Lintas-Rantai, Relayer, Solver, & Bukti Merkle/ZK Universal
- Classes: BRIDGE, CROSS-CHAIN, OFFCHAIN-RELAYER, MERKLE-ZK, INTENT
- Trigger Symptom: Modul mengunci/mencetak aset lintas-rantai, menerima pesan dari relayer/keeper/prover, atau memverifikasi tanda tangan/bukti Merkle/ZK.
- Paired Items: M-005, M-008, AF-07, AF-08, AF-10, POV-relayer-mev

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Eksekusi Tepat Satu Kali (*Exactly-Once Execution*): Satu pesan lintas-rantai, satu tanda tangan *intent/order*, atau satu daun klaim Merkle/ZK hanya boleh berhasil mengeksekusi pelepasan nilai maksimal satu kali di rantai tujuan yang sah.
2. Kesetaraan Nilai Lintas-Desimal & Penanganan Gagal (*Failed Message Recovery*): Jumlah yang dikunci di rantai asal (setelah normalisasi desimal antara rantai asal dan tujuan) wajib sama dengan yang dicetak di rantai tujuan, dan jika eksekusi di rantai tujuan gagal, dana pengirim di rantai asal tidak boleh terkunci selamanya.
## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]`:
  - Periksa konversi desimal lintas-rantai di Path/File.ext:Lxx-Lyy (misal token berdesimal 18 di EVM dijembatani ke desimal 8 di Solana/Move/Aptos): apakah sisa pembulatan (*dust*) hilang dari akuntansi jembatan hingga menyebabkan ketidakcocokan saldo saat dijembatani kembali?
- `[EDGE-VALUATION]`:
  - Pada sistem berbasis *intent/solver/relayer*: apakah biaya relayer atau kurs penyelesaian dapat dimanipulasi oleh eksekutor karena parameter batas minimum tidak ikut ditandatangani oleh pengguna (AF-08 + AF-10)?
- `[EDGE-CONTROL/LATENT]`:
  - Pada penerima pesan lintas-rantai (lzReceive, ccipReceive, onRecvPacket, handler relayer): apakah fungsi memeriksa keduanya, yaitu alamat *endpoint/router* lokal DAN identitas kontrak pengirim terpercaya di rantai asal (sourceChainId + trustedRemoteAddress) (AF-07)?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `BRIDGE (cross-chain intents)`
- **Siklus aliran (L-PATH):** deposit → fill → bundel worker → propose(bond) → jendela dispute → eksekusi → relay root → refund leaf → bridge-back
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «leaf tak pernah membayar melebihi pot»; «msg.value dipakai ATAU dikembalikan»; «slot root identik antar-chain adalah desain»; «handler selalu kosong di antara fill» — *(invarian generik bridge; verifikasi ulang terhadap desain protokol yang diaudit)*
- **Aktor off-chain:**

  data worker (bundel), disputer (jendela 2 jam — kelas «ketiadaan aksi»), relayer (pricing)

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
