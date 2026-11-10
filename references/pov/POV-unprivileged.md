# [POV-unprivileged] Sudut Pandang: Penyerang Eksternal Tanpa Izin & Modal Pinjaman Kilat
- Classes: EXTERNAL-ATTACKER, FLASH-CAPITAL, PERMISSIONLESS
- Trigger Symptom: Terdapat fungsi publik/eksternal tanpa penjaga otoritas pada [EDGE-ASSET], [EDGE-VALUATION], atau [EDGE-CONTROL/LATENT].
- Paired Items: M-001, M-005, AF-01, AF-07

---

## 1. Kemampuan & Sumber Daya Aktor
- Tidak memiliki peran khusus (*admin/owner/governance/operator*), tetapi dapat membuat banyak akun/kontrak pembantu dalam satu transaksi.
- Memiliki akses modal likuiditas tak terbatas secara instan dalam satu transaksi melalui pinjaman kilat (*flash loan / flash mint / flash swap*).
- Dapat memanggil fungsi publik mana pun dengan kombinasi parameter ekstrem (0, 1, MAX, alamat sendiri, akun duplikat).

## 2. Pertanyaan Bedah di STAGE-C2 & STAGE-D
1. Cari Pintu Terbuka di `[EDGE-CONTROL/LATENT]`: Apakah ada fungsi yang seharusnya hanya dipanggil secara internal/antar-modul atau sekali saat inisialisasi, namun dideklarasikan publik pada Path/File.ext:Lxx-Lyy?
2. Uji Amplifikasi Modal Sesaat di `[EDGE-VALUATION]`: Jika saya meminjam 1.000.000 unit aset di awal transaksi, menyetorkannya ke modul ini, memicu fungsi perhitungan kurs/reward/pinjaman, lalu menariknya kembali di akhir transaksi—apakah ada selisih nilai yang tertinggal di tangan saya?
