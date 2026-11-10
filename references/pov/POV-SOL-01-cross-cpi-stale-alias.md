# [POV-SOL-01] Sudut Pandang: Cross-CPI Stale AccountInfo & Duplicate Writable Alias
- Classes: CLASS-B (Program Utama ↔ Target CPI atau 2 Akun Alias), CLASS-C
- Trigger Symptom: Instruksi Solana menerima ≥2 akun `mut` / `ctx.remaining_accounts` bertipe serupa tanpa constraint `key() !=`, ATAU melakukan CPI lalu membaca/menulis variabel akun lokal tanpa `.reload()?`.
- Paired Items: M-003, M-006, AF-05, CHAIN-solana, POV-unprivileged

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin dengan satu akun valid miliknya. Tidak butuh authority khusus — hanya kemampuan menyusun daftar akun dalam satu instruksi.

## 2. Gejala di Kode

1. Tidak ada constraint `constraint = account_a.key() != account_b.key()` pada pasangan akun sumber/tujuan atau daftar `remaining_accounts`.
2. Setelah mengeksekusi CPI (yang mengubah saldo/state akun di runtime), kode langsung membaca field `account.amount` atau `state.value` dari variabel Rust yang dideserialisasi **di awal fungsi** tanpa memanggil `.reload()?`, atau menulis kembali struct lama sehingga menimpa hasil CPI.

Prinsip umumnya adalah **padanan Solana dari `M-006`**: (a) referensi kembar yang diproses dua kali, dan (b) snapshot lokal basi yang dipakai atau ditulis balik setelah interaksi eksternal.

## 3. Rangkaian Serangan

1. **Siapkan:** siapkan satu akun valid milik penyerang.
2. **Picu:** panggil instruksi dengan akun yang sama untuk parameter `source` dan `destination` (atau duplikat di `remaining_accounts`), atau picu CPI yang mengubah saldo akun.
3. **Ekstraksi:** program memproses penjumlahan/klaim di atas snapshot memori yang belum diperbarui (atau menimpa pengurangan saldo), menggandakan hak penyerang dalam satu instruksi.

## 4. Auditor Blindspot

Auditor melihat deklarasi tipe `Account<'info, ...>` di Anchor sudah memeriksa pemilik dan tipe, lalu menganggapnya aman — **tanpa memeriksa kesamaan identitas antar-dua akun** dan tanpa memeriksa titik `reload` setelah CPI.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila ada constraint `key() !=` untuk setiap pasangan akun yang diproses, **dan** setiap pembacaan pasca-CPI didahului `.reload()?` (dibuktikan dengan kutipan baris).
- **Wajib PoC** dengan akun kembar nyata pada runtime (`cargo test-sbf` / `solana-program-test`), bukan pembacaan kode saja.
- Fuzz wajib mengacak: jumlah `remaining_accounts`, posisi duplikat, dan urutan CPI.
