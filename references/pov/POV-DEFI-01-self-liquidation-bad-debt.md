# [POV-DEFI-01] Sudut Pandang: Multi-Identity Self-Liquidation & Bad-Debt Socialization
- Classes: CLASS-C (Identitas 1 Borrower + Identitas 2 Liquidator + Pool + Oracle/Insurance), CLASS-B
- Trigger Symptom: Protokol memiliki fungsi likuidasi/slashing/penalti yang memberi bonus likuidator ATAU menghapus sisa utang tak beragunan (*bad debt socialization*) ketika `debt > collateral`.
- Paired Items: M-002, M-003, M-005, AF-03, POV-liquidator

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang mengendalikan **dua identitas/akun/objek/capability** sekaligus, dengan modal secukupnya untuk membuka posisi pada batas risiko ekstrem. Tidak butuh peran admin.

## 2. Gejala di Kode

Saat akun jatuh ke kondisi insolven (`debt > collateral`), fungsi likuidasi tetap memberikan bonus likuidator penuh dari kolam umum, **atau** menghapus sisa utang (*bad debt*) tanpa menyita seluruh jaminan yang tersisa di sub-akun lain, **atau** mengizinkan peminjam meminjam/menarik agunan tepat di batas harga yang dimanipulasi sesaat.

## 3. Rangkaian Serangan

1. **Siapkan:** penyerang menyiapkan **dua identitas** — pertama sebagai Kambing Hitam (posisi yang akan gagal bayar), kedua sebagai Pemburu Bonus. Tidak harus dua EOA: bisa dua akun pada pool yang sama, dua posisi, dua objek, atau dua capability.
2. **Picu:** identitas pertama membuka posisi maksimum pada batas risiko ekstrem hingga menyisakan utang macet atau memicu syarat likuidasi.
3. **Ekstraksi:** identitas kedua mengeksekusi likuidasi/klaim terhadap identitas pertama — secara atomik atau dalam jendela eksekusi yang sama — untuk mengantongi bonus likuidasi atau menyedot cadangan asuransi yang nilainya lebih besar daripada modal yang sengaja dikorbankan.

## 4. Auditor Blindspot

Auditor selalu mengasumsikan Borrower dan Liquidator adalah dua pihak yang **saling bermusuhan**, sehingga tidak pernah menghitung bahwa jika keduanya dikendalikan satu penyerang, kerugian di satu identitas bisa menghasilkan keuntungan lebih besar di identitas lain **atas beban kolam protokol**.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** (`REJECTED_NEGATIVE_EV`) **hanya setelah** simulasi PoC 2-identitas dan **Strike 3 Fuzzing** membuktikan bahwa pada seluruh ukuran posisi, kemiringan harga, dan skenario likuidasi parsial, `Total_Jaminan_Tersita` selalu lebih besar daripada `Bonus_Liquidator + Utang_Dihapus` tanpa menyisakan *bad debt* ke kolam publik.
- **DILARANG KERAS menggugurkan hanya dengan menghitung pertidaksamaan di atas kertas.** Wajib tulis tes 2-identitas (`Attacker_A` sebagai Borrower + `Attacker_B` sebagai Liquidator) + **Strike 3 Fuzz** yang mengacak jumlah pinjaman, urutan likuidasi pecahan kecil, dan distorsi harga spot/agunan. Jika gagal, lampirkan log test & fuzz di `06` (`BUKTI_SIMULASI:`).
