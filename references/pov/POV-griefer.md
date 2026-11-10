# [POV-griefer] Sudut Pandang: Penyabotase Asimetris Bermodal Debu (*Low-Cost Griefer*)
- Classes: GRIEFING, ASYMMETRIC-DOS, QUEUE-BLOCKER, BRICKING
- Trigger Symptom: Terdapat antrean bersama, pemrosesan batch, batas kuota global, *cooldown timer*, atau syarat kesetaraan saldo yang dapat diganggu pihak ketiga.
- Paired Items: M-009, AF-09, DOM-staking, DOM-governance-control

---

## 1. Kemampuan & Sumber Daya Aktor
- Tidak harus mencuri dana ke kantong sendiri; tujuannya adalah membekukan dana bernilai besar milik pengguna/protokol (`Prioritas EV P3`) atau mematikan fungsi likuidasi/penarikan hanya dengan modal 1 wei / biaya transaksi sangat kecil.

## 2. Pertanyaan Bedah di STAGE-C2 & STAGE-D
1. Sabotase Antrean & Batch: Di Path/File.ext:Lxx-Lyy, jika saya mendaftarkan 1 item antrean yang mengarah ke kontrak penolak transfer (atau akun token *blacklisted*), apakah seluruh fungsi processBatch() / settle() milik ratusan pengguna lain ikut *revert*?
2. Sabotase Timer & Prasyarat Korban: Dapatkah saya memanggil depositFor(korban, 1) atau delegate(korban, 1) untuk mereset waktu tunggu penarikan (*unlock timestamp*) korban selamanya?
