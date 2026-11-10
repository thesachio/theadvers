# [POV-malicious-integrator] Sudut Pandang: Kontrak/Token/Akun Pihak Ketiga Berbahaya & Callback Penjebak
- Classes: MALICIOUS-TOKEN, HOOK-TRAP, SPOOFED-ACCOUNT, EXTERNAL-CALLBACK
- Trigger Symptom: Modul berinteraksi dengan token/aset/kontrak/akun/objek yang disuplai pengguna atau melakukan panggilan keluar (*external call*/CPI).
- Paired Items: M-003, M-005, AF-04, AF-07

---

## 1. Kemampuan & Sumber Daya Aktor
- Dapat men-deploy kontrak/objek/token kustom atau menyuplai akun miliknya sebagai argumen ke dalam fungsi protokol.
- Saat protokol memanggil kontrak/hook milik aktor ini, aktor dapat memanggil balik (*reenter*) ke fungsi mana pun di dalam Wilayah R_i atau wilayah lain, mengembalikan nilai palsu, atau menghabiskan gas/komputasi.

## 2. Pertanyaan Bedah di STAGE-C2 & STAGE-D
1. Eksploitasi Saat Panggilan Keluar: Ketika baris kode di Path/File.ext:Lxx-Lyy memanggil transfer/callback ke alamat saya, variabel state apa yang belum diperbarui dan modul mana di RADAR.md yang bisa saya panggil untuk membaca state basi tersebut?
2. Tipuan Kontrak/Akun Pasangan: Jika saya memasukkan pasangan [TokenAsli, TokenPalsuBuatanSaya] ke dalam pool/router/lending, dapatkah saya menguras TokenAsli menggunakan valuasi semu dari TokenPalsuBuatanSaya?

## 3. Mengapa Bisa Lolos & Batas Realitas (STAGE-D)

**Blindspot:** auditor memakai token/kontrak "normal" (ERC-20 standar) di harness, sehingga jalur callback dan nilai balik palsu tidak pernah terpicu.

- **Gugur** bila protokol hanya berinteraksi dengan aset yang alamatnya di-*whitelist* dan **whitelist divalidasi per-pasangan**, serta tidak ada panggilan keluar ke alamat yang disuplai pengguna.
- **Wajib PoC** memakai mock pihak ketiga yang **meniru perilaku nyata** (callback yang benar-benar memanggil balik, nilai balik yang secara sah bisa dihasilkan). Mock yang mengarang payload mustahil hanya menopang bukti struktural (`TANGGA_BUKTI C`), tidak sah untuk `09`.
- Selisih nilai wajib diukur: aset asli keluar vs aset palsu masuk.
