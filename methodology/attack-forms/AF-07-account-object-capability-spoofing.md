# [AF-07] Substitusi Akun/PDA/Objek Palsu, Bypass Otoritas, & Arbitrary Call
- Classes: ACCOUNT-SPOOFING, ACCESS-BYPASS, ARBITRARY-CALL, CAPABILITY-LEAK
- Trigger Symptom: Fungsi menerima referensi akun/kontrak/objek dari luar tanpa validasi pemilik/seed/relasi lengkap, atau mengeksekusi panggilan dinamis.
- Paired Items: M-005, POV-unprivileged, POV-malicious-integrator

---

## 1. Mekanisme Serangan Universal
Penyerang memanggil fungsi publik/eksternal dengan menyuplai alamat kontrak, akun (Solana/Rust), atau objek (Move) tiruan yang dikendalikannya sendiri untuk melewati pemeriksaan otoritas, memalsukan state konfigurasi, atau memaksa modul mengeksekusi panggilan berbahaya atas nama modul tersebut.

## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Periksa Rantai Validasi Input di `Path/File.ext:Lxx-Lyy`:
   - Daftar seluruh parameter akun/alamat/objek yang diterima fungsi.
   - Cari parameter yang tidak diverifikasi ikatannya terhadap penyimpanan utama (misal: akun token vault diperiksa memiliki mint == X, tetapi tidak diperiksa apakah authority == poolPDA, sehingga penyerang bisa memasukkan akun token miliknya sendiri).
2. Konstruksi Payload Substitusi / Arbitrary Call:
   - Buat kontrak/akun palsu yang mengembalikan nilai true atau saldo semu saat dipanggil oleh modul target, ATAU
   - Arahkan parameter target dan calldata pada fungsi router untuk memanggil token.transferFrom(korban, penyerang, jumlah) memanfaatkan *allowance* korban.
3. Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika target/akun sudah dikunci melalui daftar putih (*whitelist*), derivasi alamat deterministik (PDA/CREATE2) yang terverifikasi, atau pemeriksaan pemilik/otoritas yang lengkap.
