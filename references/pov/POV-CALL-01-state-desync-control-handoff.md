# [POV-CALL-01] Sudut Pandang: State Desynchronization pada Penyerahan Kontrol
- Classes: CLASS-B (Dual-Entity: Kontrak Utama ↔ Penerima Kontrol), CLASS-C (Cross-Module Read-Only Reentrancy)
- Trigger Symptom: Panggilan keluar / transfer native coin / hook NFT / CPI terjadi saat variabel pertama (mis. `totalAssets`) sudah berubah tetapi variabel pasangannya (mis. `totalSupply`) belum diperbarui.
- Paired Items: M-002, M-006, M-008, AF-04, POV-relayer-mev

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang dapat mengendalikan kontrak penerima panggilan keluar (kontrak penyerang sebagai `receiver`/`to`/hook target). Tidak butuh peran; hanya perlu menjadi pihak yang dipanggil.

## 2. Gejala di Kode

Di tengah fungsi — sebelum baris terakhir selesai — terjadi penyerahan kontrol eksternal (pengiriman native coin/ETH, `safeTransferFrom` ERC-721/1155, hook token whitelist, atau panggilan ke kontrak eksternal) ketika **variabel pertama sudah diperbarui tetapi variabel pasangannya belum**.

Prinsip umum berlaku untuk **setiap penyerahan kontrol di tengah pembaruan dua variabel berpasangan** — bukan hanya callback EVM: termasuk CPI di tengah instruksi Solana, atau pengiriman pesan sebelum kunci state diperbarui di TON.

## 3. Rangkaian Serangan

1. **Siapkan:** penyerang membuka posisi di Kontrak A dan menyiapkan posisi terungkit di Kontrak B (atau fungsi lain yang **tidak berbagi kunci `nonReentrant`** yang sama).
2. **Picu:** penyerang memicu penarikan/likuidasi/aksi yang mengeksekusi panggilan keluar tepat di tengah pembaruan dua variabel.
3. **Ekstraksi:** di dalam callback, penyerang memanggil fungsi di Kontrak B (atau fungsi lain) yang membaca rasio timpang sementara (*inflated/deflated mid-tx state*) untuk meminjam berlebih atau melikuidasi secara tidak sah.

## 4. Auditor Blindspot

Auditor melihat kata kunci `nonReentrant` pada fungsi tersebut lalu langsung menandainya aman dari reentrancy, **tanpa memeriksa apakah ada kontrak/fungsi lain di ekosistem yang membaca state yang baru setengah selesai diperbarui**.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** jika seluruh mutasi state internal dan akuntansi bersama diselesaikan 100% sebelum interaksi eksternal (CEI murni), atau jika ada *global reentrancy lock* yang juga diperiksa seluruh fungsi pembaca/pasangan.
- **Wajib PoC** bila ada jendela mid-tx: tulis kontrak/hook penyerang di simulator yang masuk kembali ke fungsi pembaca/pasangan pada jendela tersebut, lengkap dengan *Victim Seeding* pada pool.
- **Jalur 3 — Unprivileged State Poisoning pada Eksekusi Rutin (`M-005`/`M-009`):** `nonReentrant` lokal **BUKAN** bukti aman bila fungsi pembaca/pasangan hanya bisa dipanggil aktor berizin (Keeper/Relayer/Solver/Operator). Penyerang tak berizin dapat meracuni state/antrean/saldo di fungsi publik **sebelum** aktor rutin memanggil fungsi tersebut secara normal, sehingga pembacaan state timpang terjadi **tanpa reentrancy sama sekali**. Wajib PoC: (a) racuni state lewat jalur permissionless, lalu (b) picu fungsi rutin sebagai Keeper/Relayer.
