# [CHAIN-reentrancy-valuation] Rantai: Panggilan Keluar -> Pembacaan Valuasi Basi Lintas-Modul
- Classes: READ-ONLY-REENTRANCY, VALUATION-DESYNC, CROSS-MODULE
- Trigger Symptom: Modul A melakukan panggilan keluar/transfer/CPI sebelum memperbarui saldo/share, dan Modul B di RADAR.md membaca kurs/saldo Modul A.
- Paired Items: M-003, M-004, M-010, AF-04, POV-malicious-integrator

---

## 1. Anatomi Rantai Serangan (Langkah 1 -> Langkah 2 -> Langkah 3)
1. Langkah 1 (Pemicu di Modul A — `Path/FileA.ext:Lxx-Lyy`):
   Penyerang memanggil fungsi penarikan/likuiditas di Modul A yang mengirimkan aset keluar (atau memicu hook/callback/CPI) ketika totalAssets sudah berkurang tetapi totalSupply belum dibakar (atau sebaliknya).
2. Langkah 2 (Eksploitasi di Modul B di Dalam Callback — `Path/FileB.ext:Lxx-Lyy`):
   Saat eksekusi berada di tangan callback penyerang, penyerang memanggil Modul B (yang memiliki tag [TOUCHES] membaca kurs/harga dari Modul A). Karena kunci *reentrancy* Modul A tidak diperiksa oleh fungsi *view* atau oleh Modul B, Modul B menghitung nilai agunan/share menggunakan rasio yang sedang terdistorsi tajam.
3. Langkah 3 (Penyelesaian & Ekstraksi Nilai):
   Penyerang meminjam/mencetak aset berlebih di Modul B, lalu membiarkan panggilan awal di Modul A selesai secara normal.

## 2. Syarat Pembuktian di STAGE-D
- Tunjukkan kedua jangkar (FileA:Lxx dan FileB:Lyy), buktikan tidak adanya *cross-contract reentrancy lock* pada jalur pembacaan, dan hitung selisih kurs saat jendela callback terbuka.
