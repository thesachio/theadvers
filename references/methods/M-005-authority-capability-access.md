# [M-005] Bedah Otoritas, Akun/Objek/Capability, & Bypass Penjaga Universal
- Classes: ACCESS-CONTROL, AUTHORITY, ACCOUNT-VALIDATION, CAPABILITY
- Trigger Symptom: Terdapat fungsi berhak istimewa, validasi akun/PDA/objek input pengguna, delegasi panggilan, perubahan parameter, atau jalur inisialisasi/upgrade.
- Paired Items: AF-07, AF-08, POV-unprivileged, POV-malicious-integrator

---

## 1. Inti Metode Bedah
M-005 membedah seluruh penjaga otorisasi pada [EDGE-CONTROL/LATENT] untuk menemukan titik masuk yang lupa divalidasi kepemilikannya, salah memvalidasi akun/objek yang disuplai pengguna, atau mengizinkan panggilan sembarang (*arbitrary call*).

## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Audit Kelengkapan Penjaga Fungsi Eksternal/Publik:
   - Periksa setiap fungsi publik pada modul Tier 1 dan Tier 2: apakah fungsi inisialisasi (initialize, init, reinitialize), fungsi migrasi/upgrade, atau fungsi *callback/hook* dapat dipanggil langsung oleh siapa saja karena tidak memverifikasi msg.sender / signer / caller?
2. Audit Validasi Akun, PDA, & Objek Input (*Account/Object Substitution*):
   - Jika fungsi menerima alamat kontrak, akun (Solana/Rust), atau objek (Move) dari parameter input pengguna:
     - Apakah kode memverifikasi pemilik (*owner*), seed/bump PDA, dan ikatan relasi (*has_one / constraint*) antara akun vault, akun mint, dan akun state konfigurasi pada Path/File.ext:Lxx-Lyy?
     - Apakah penyerang dapat menyuplai akun/kontrak palsu buatannya sendiri untuk menipu pemeriksaan saldo atau otoritas?
3. Audit Panggilan Sembarang & Delegasi (*Arbitrary External Call / Delegatecall*):
   - Jika modul memiliki router/executor yang mengeksekusi target.call(data) atau menerima target kontrak dari pengguna, uji apakah penyerang dapat mengarahkannya ke kontrak token untuk memanggil transferFrom atas *allowance* yang diberikan pengguna lain kepada kontrak router tersebut.

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan parameter input konkret yang disuplai oleh akun tanpa hak istimewa untuk melewati baris penjaga di Path/File.ext:Lxx-Lyy dan mengubah state/aset terlindungi.
