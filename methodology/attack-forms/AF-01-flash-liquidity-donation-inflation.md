# [AF-01] Injeksi Likuiditas Kilat, Donasi Langsung, & Inflasi Share/Rasio
- Classes: FLASH-LOAN, DONATION, SHARE-INFLATION, SOLVENCY
- Trigger Symptom: Perhitungan share/klaim/reward bergantung pada saldo aset riil atau cadangan pool yang dapat diubah secara instan dalam satu transaksi/blok.
- Paired Items: M-001, M-004, DOM-vault, DOM-amm

---

## 1. Mekanisme Serangan Universal
Penyerang menggunakan modal besar sesaat (pinjaman kilat / *flash loan*) atau mengirimkan aset langsung ke alamat/akun penyimpanan modul tanpa melewati fungsi pencatatan resmi (*direct transfer / donation*) untuk mengubah rasio antara totalAssets dan totalSupply sebelum transaksi pengguna lain atau perhitungan valuasi dieksekusi.

## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Tentukan Variabel Target pada `Path/File.ext:Lxx-Lyy`:
   Identifikasi ekspresi yang membaca saldo riil atau cadangan pool secara langsung (misal token.balanceOf(vault) atau saldo akun vault) sebagai pembagi/pengali.
2. Susun Urutan Eksekusi Uji:
   - Langkah 1: Siapkan state awal (misal penyerang mencetak unit share minimal 1 atau mengambil posisi awal).
   - Langkah 2: Injeksi aset langsung atau gunakan likuiditas kilat untuk menggelembungkan denominator/numerator kurs.
   - Langkah 3: Eksekusi transaksi korban (atau fungsi pencetak klaim/pinjaman) yang mengalami pembulatan ke 0 atau penilaian agunan berlebih.
   - Langkah 4: Tarik kembali share/likuiditas penyerang dan hitung selisih saldo akhir.
3. Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan kandidat jika modul menggunakan pelacakan saldo internal murni (*internal accounting*) yang mengabaikan donasi langsung, atau menerapkan *virtual shares/assets offset* yang membuat biaya donasi penyerang selalu lebih besar daripada nilai yang berhasil diekstrak (Attack Cost > Extracted Value).
