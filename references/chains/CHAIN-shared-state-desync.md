# [CHAIN-shared-state-desync] Rantai: Mutasi State Bersama ([TOUCHES]) -> Bypass Invariant Modul Kedua
- Classes: SHARED-STATE, ACCOUNTING-DESYNC, TOUCHES-COLLISION
- Trigger Symptom: Dua fungsi/modul di RADAR.md memiliki tag [TOUCHES: NamaModul.simbol] yang sama dengan asumsi sinkronisasi berbeda.
- Paired Items: M-001, M-010, AF-05, DOM-staking, DOM-lending

---

## 1. Anatomi Rantai Serangan (Langkah 1 -> Langkah 2 -> Langkah 3)
1. Langkah 1 (Identifikasi Tabrakan `[TOUCHES]` di `RADAR.md`):
   Temukan variabel state bersama (misal saldo token receipt, catatan utang, *checkpoint* waktu, atau *allowance* bersama) yang ditulis oleh Fungsi X (Path/FileA.ext:Lxx-Lyy) namun dibaca oleh Fungsi Y (Path/FileB.ext:Lxx-Lyy).
2. Langkah 2 (Urutan Panggilan Pemecah Asumsi):
   Panggil Fungsi X untuk mengubah state bersama tanpa memicu pembaruan akuntansi pendamping yang diharapkan oleh Fungsi Y (contoh: memindahkan token posisi staking/kolateral ke akun kedua tanpa memperbarui rewardDebt atau *health factor*).
3. Langkah 3 (Klaim Ganda / Penghindaran Kewajiban):
   Panggil Fungsi Y dari akun kedua untuk mengklaim hak/reward dua kali atas modal yang sama, atau menarik kolateral sambil meninggalkan utang.

## 2. Syarat Pembuktian di STAGE-D
- Sajikan tabel perubahan state variabel yang bersentuhan pada setiap langkah (Sebelum X -> Sesudah X -> Sesudah Y) dan tunjukkan invariant konservasi nilai (M-001) yang pecah.
