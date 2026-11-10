# [POV-MOVE-01] Sudut Pandang: Programmable Transaction Block (PTB) Capability & Object Splitting
- Classes: CLASS-B (2 Objek Mandiri), CLASS-C (Rantai Panggilan PTB Multi-Objek)
- Trigger Symptom: Fungsi Move menerima ≥2 objek (`&mut Pool` + `&mut Position`/`Receipt`) tanpa `assert!(receipt.pool_id == object::id(pool))`, ATAU memakai geser bit kiri `<<` pada matematika kustom (`u128`/`u256`).
- Paired Items: M-006, M-007, M-008, AF-03, CHAIN-sui-move, POV-unprivileged

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang menyusun **Programmable Transaction Block (PTB)** — satu transaksi berisi rantai panggilan. Tidak butuh capability admin; cukup mampu membuat objek sendiri dan merangkai panggilan.

## 2. Gejala di Kode

1. Fungsi memverifikasi kesamaan tipe generik `<T>`, tetapi **lupa memeriksa ikatan ID objek induk** (`assert!(receipt.container_id == object::id(container))`), atau menyediakan fungsi publik alternatif yang dapat menghancurkan *Hot Potato* dengan syarat lebih ringan.
2. Fungsi matematika kustom melakukan `value << shift` di mana pemeriksaan batas mask overflow **meleset 1 bit** — tidak menangkap bit tinggi yang terbuang, karena operasi `<<` di Move tidak otomatis *abort* saat bit signifikan tergeser keluar.

Prinsip umumnya: (1) adalah **padanan Move dari aliasing referensi** (`POV-SOL-01` / `M-006`) — tipe sama tidak menjamin objek sama; (2) adalah **padanan Move dari pemangkasan di langkah antara** (`POV-MATH-02` / `M-007`) — bit tinggi hilang sebelum validasi akhir.

## 3. Rangkaian Serangan

1. **Siapkan:** dalam satu PTB, buat atau akses `Container_Palsu` dengan rasio ekstrem (atau siapkan angka input tepat di batas bit-mask).
2. **Picu:** cetak `Position`/`Receipt` bernominal besar dari `Container_Palsu` (atau picu pemotongan bit atas pada `<<` sehingga kewajiban setor terhitung sangat kecil).
3. **Ekstraksi:** masih di PTB yang sama, gunakan `Position`/`Receipt` tersebut pada `Container_Asli` untuk menarik/mengklaim nilai lebih besar daripada yang disetor.

## 4. Auditor Blindspot

Auditor melihat constraint tipe generik `<T>` dan menganggap objek sudah terikat pada kontainer yang benar — **tanpa menyadari bahwa tipe sama tidak menjamin ID objek sama**, dan tanpa menguji PTB sebagai satu unit eksekusi berantai.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila setiap fungsi yang menerima ≥2 objek memeriksa `object::id` induk secara eksplisit (kutipan `assert!`), dan `<<` dibungkus pemeriksaan bit-mask penuh (fuzz batas bit wajib).
- **Wajib PoC** yang mengeksekusi satu PTB utuh: buat objek palsu → cetak receipt → pakai pada kontainer asli. Pisahkan langkah di transaksi berbeda tidak membuktikan apa pun.
- Untuk kasus `<<`: fuzz wajib mengacak `shift` di sekitar batas (`127`, `128`, `255`, `256`).
