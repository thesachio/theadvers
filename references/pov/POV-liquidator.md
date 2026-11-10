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

## 3. Mengapa Bisa Lolos & Batas Realitas (STAGE-D)

**Blindspot:** auditor memisahkan peran Borrower dan Liquidator secara konseptual, lalu menganggap keduanya selalu pihak berbeda yang bermusuhan.

- **Gugur** (`REJECTED_NEGATIVE_EV`) hanya bila simulasi 2-identitas + Strike 3 Fuzz membuktikan `Total_Jaminan_Tersita > Bonus_Liquidator + Utang_Dihapus` pada seluruh ukuran posisi dan skenario likuidasi parsial.
- **Wajib PoC** bila `close factor` membolehkan likuidasi >50% saat kesehatan turun 1 wei, atau bila `debt > collateral` masih menyisakan bonus penuh. PoC wajib memakai dua akun (`Attacker_A` borrower, `Attacker_B` liquidator).
- Padanan detail: `POV-DEFI-01` (self-liquidation & bad-debt socialization).
