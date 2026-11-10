# [POV-relayer-mev] Sudut Pandang: Eksekutor Urutan Transaksi (MEV), Relayer, Keeper, & Solver
- Classes: MEV-SEARCHER, RELAYER, KEEPER, ORDERING, INTENT-SOLVER
- Trigger Symptom: Hasil eksekusi bergantung pada urutan transaksi dalam blok, parameter *slippage/deadline*, tanda tangan pengguna, atau kiriman data relayer/keeper.
- Paired Items: M-008, AF-05, AF-08, AF-10, DOM-bridge-offchain

---

## 1. Kemampuan & Sumber Daya Aktor
- Dapat melihat transaksi/pesan/tanda tangan yang tertunda dan menyisipkan transaksi tepat sebelum (*front-run*) serta tepat sesudah (*back-run*) transaksi target.
- Jika bertindak sebagai relayer/keeper/solver: dapat memilih waktu eksekusi, memecah batch, atau mengubah parameter fungsi yang tidak dikunci oleh tanda tangan pengguna.

## 2. Pertanyaan Bedah di STAGE-C2 & STAGE-D
1. Sandwich & Front-Run: Jika saya masuk tepat sebelum transaksi harvest/distributeReward/rebalance di Path/File.ext:Lxx-Lyy dan keluar tepat sesudahnya, berapa bagian nilai pengguna lama yang berpindah ke saya?
2. Manipulasi Parameter Relayer: Saat pengguna menyerahkan tanda tangan izin (*permit/intent*), parameter apa di fungsi tujuan yang dapat saya ubah (misal alamat penerima, besaran fee relayer, jalur swap) tanpa membatalkan validitas tanda tangan tersebut?
