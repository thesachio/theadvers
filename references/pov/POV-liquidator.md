# [POV-liquidator] Sudut Pandang: Likuidator, Arbitrase Lelang, & Pemburu Insentif Penyitaan
- Classes: LIQUIDATOR, AUCTION-BIDDER, SELF-LIQUIDATION, BAD-DEBT
- Trigger Symptom: Terdapat jalur likuidasi, lelang agunan, klaim bonus penalti, atau penutupan paksa posisi tidak sehat.
- Paired Items: M-004, M-006, AF-06, DOM-lending

---

## 1. Kemampuan & Sumber Daya Aktor
- Dapat bertindak ganda: sebagai likuidator eksternal sekaligus sebagai peminjam (pemilik posisi yang sengaja dibuat kritis) melalui dua akun berbeda (*self-liquidation*).
- Mengincar selisih antara utang yang dibayar dan nilai agunan + bonus likuidasi yang diterima.

## 2. Pertanyaan Bedah di STAGE-C2 & STAGE-D
1. Eksploitasi *Self-Liquidation***: Jika posisi saya berada sedikit di bawah batas sehat, dapatkah akun kedua saya melikuidasi posisi saya sendiri pada `Path/File.ext:Lxx-Lyy` untuk menyita seluruh agunan bernilai tinggi sambil membiarkan sisa utang buruk ditanggung oleh protokol?
2. **Penyitaan Berlebih (*Over-Seizure*): Apakah rumus penyitaan membatasi jumlah maksimal utang yang boleh dilikuidasi (*close factor*), atau saya bisa melikuidasi 100% posisi besar hanya karena kesehatannya turun 1 wei di bawah ambang batas?
3. Kegagalan Likuidasi Saat Rugi: Jika nilai agunan jatuh di bawah nilai utang, apakah saya masih memiliki insentif ekonomi dan jalur kode yang tidak *revert* untuk membersihkan posisi tersebut?
