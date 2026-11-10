# [M-010] Bedah Sinyal [TOUCHES] & Serangan Rantai Lintas-Modul Universal
- Classes: CROSS-MODULE, SHARED-STATE, COMPOSABILITY, CHAINED-EXPLOIT
- Trigger Symptom: Terdapat >= 2 entri di RADAR.md dengan tag [TOUCHES: NamaModul.simbol] yang sama, atau satu modul membaca state modul lain tanpa mengunci sinkronisasi.
- Paired Items: AF-04, AF-05, AF-06, CHAIN-shared-state-desync

---

## 1. Inti Metode Bedah
M-010 adalah metode khusus untuk Gelombang 2 (`STAGE-C2`) dan `FINAL-SWEEP` yang mengubah sinyal-sinyal terpisah di RADAR.md menjadi Serangan Berantai (*Chained Exploit*): kondisi di mana Modul A dan Modul B terlihat aman jika diaudit sendirian, namun runtuh ketika dipanggil secara berurutan dalam satu transaksi atau lintas-blok.

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Kumpulkan Pasangan Tabrakan `[TOUCHES]` dari `RADAR.md`:
   - Ambil setiap simbol NamaModul.simbol yang muncul pada >= 2 baris RADAR.md (satu sebagai *Writer/Mutator* di Path/FileA.ext:Lxx-Lyy, dan satu lagi sebagai *Reader/Consumer* di Path/FileB.ext:Lxx-Lyy).
2. Uji Asumsi Invariant yang Patah Lintas-Modul:
   - Apa asumsi implisit yang dipegang oleh *Reader* (FileB) terhadap nilai NamaModul.simbol? (Misal: FileB mengasumsikan simbol hanya berubah lewat alur X, atau sudah diperbarui pada blok ini).
   - Dapatkah *Writer* (FileA) dipanggil terlebih dahulu untuk menempatkan NamaModul.simbol ke dalam state ekstrem/tidak sinkron, lalu langsung memanggil FileB sebelum state dinormalisasi?
3. Rakit Urutan Transaksi Multi-Langkah (*Multi-Step Exploit Chain*):
   - Susun rantai aksi: Langkah 1 (Siapkan State di Modul A) -> Langkah 2 (Eksploitasi Pembacaan di Modul B) -> Langkah 3 (Kembalikan State / Tarik Keuntungan Bersih).

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan matriks interaksi antara kedua modul (Path/FileA.ext:Lxx-Lyy dan Path/FileB.ext:Lxx-Lyy) beserta bukti eksekusi/hitungan berantai yang menghasilkan delta nilai positif.
