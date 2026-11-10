# [M-003] Bedah Urutan Transisi State & Interaksi Eksternal Universal
- Classes: STATE-MACHINE, REENTRANCY, CALLBACK, CPI
- Trigger Symptom: Terdapat panggilan eksternal, transfer token/aset, hook, callback, atau CPI sebelum seluruh pembaruan state/akuntansi lokal dikunci.
- Paired Items: AF-04, AF-05, CHAIN-reentrancy-valuation

---

## 1. Inti Metode Bedah
M-003 menguji apakah suatu eksekusi meninggalkan jendela state setengah matang (*intermediate dirty state*) ketika kontrol diserahkan ke modul eksternal, penerima aset, hook, atau instruksi lintas-program (CPI).
## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Identifikasi Seluruh Titik Serah-Kontrol (*Control Handover Points*):
   - Tandai setiap baris kode pada Path/File.ext:Lxx-Lyy yang melakukan: transfer aset native, transfer token dengan hook/callback (ERC-777, ERC-721/1155 onReceived, Token-2022 transfer hook), panggilan ke alamat/kontrak dinamis, callback flash loan/swap, atau Cross-Program Invocation (CPI) / pesan asinkron.
2. Periksa State yang Belum Diperbarui (*Uncommitted State Snapshot*):
   - Pada baris tepat saat panggilan keluar terjadi, daftar seluruh variabel state di modul tersebut DAN di modul lain (lihat tag [TOUCHES: ...] di RADAR.md) yang nilainya belum mencerminkan transaksi yang sedang berjalan.
3. Uji Tiga Variasi Masuk-Ulang (*Reentrancy & Read-Only Variants*):
   - Same-Function Reentrancy: Masuk kembali ke fungsi yang sama sebelum saldo/klaim dikurangi.
   - Cross-Function Reentrancy: Masuk ke fungsi saudara di modul yang sama (misal sedang withdraw, masuk ke transfer atau borrow) yang tidak memakai pengunci (*mutex*) yang sama.
   - Cross-Module / Read-Only Reentrancy: Memiliki nonReentrant pada modul A, tetapi saat panggilan keluar terjadi, penyerang memanggil modul B yang membaca fungsi *view*/kurs dari modul A ketika totalAssets dan totalSupply modul A sedang tidak sinkron.
   - Post-CPI Account Reload (Solana/Rust): Memeriksa apakah akun yang dimutasi lewat CPI dibaca ulang (*reload*) setelah CPI selesai, atau masih memakai salinan memori lama yang basi.

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan urutan jejak eksekusi bersarang (Frame 1 -> Hook/Callback -> Frame 2 -> Frame 1 Selesai) lengkap dengan Path/File.ext:Lxx-Lyy dan bukti bahwa pengunci yang ada tidak memblokir jalur tersebut.
