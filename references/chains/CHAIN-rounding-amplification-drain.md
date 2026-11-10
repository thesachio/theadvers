# [CHAIN-rounding-amplification-drain] Rantai: State Kosong/Desimal -> Amplifikasi Kurs -> Kuras Pool via Pembulatan
- Classes: PRECISION-AMPLIFICATION, FIRST-DEPOSITOR, ROUNDING-DRAIN
- Trigger Symptom: Kombinasi state awal/kosong (M-007) atau donasi langsung (AF-01) memperbesar nilai 1 unit share, lalu diikuti pemotongan pembulatan berulang (AF-02).
- Paired Items: M-002, M-007, AF-01, AF-02, AF-03, DOM-vault

---
## 1. Anatomi Rantai Serangan (Langkah 1 -> Langkah 2 -> Langkah 3)
1. Langkah 1 (Penciptaan Unit Share Berharga Tinggi di `Path/File.ext:Lxx-Lyy`):
   Pada pool yang baru dibuat atau yang baru dikosongkan (totalSupply == 0), penyerang menyetor jumlah minimal untuk memegang sedikit share, lalu menginjeksi aset sehingga 1 share bernilai sangat besar (misal 1 share = 10.000 token).
2. Langkah 2 (Eksploitasi Pembulatan Berulang):
   Karena 1 share kini bernilai sangat besar, kesalahan pembulatan 1 wei share pada fungsi withdraw atau mint tidak lagi bernilai debu, melainkan bernilai ribuan token.
3. Langkah 3 (Kuras Berulang dalam Satu Transaksi):
   Penyerang melakukan siklus mint/withdraw tepat pada batas pembulatan (0.99 share dibulatkan ke bawah/atas) berulang kali untuk menguras aset pool sekaligus menarik kembali modal injeksinya.

## 2. Syarat Pembuktian di STAGE-D
- Tunjukkan bahwa modal injeksi pada Langkah 1 tidak hilang ke tangan pihak lain dan berhasil ditarik kembali bersama dana kurasan pada Langkah 3.
