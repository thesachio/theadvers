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

## 3. Kacamata Attacker (Gejala di Kode)

Fungsi publik tanpa penjaga otoritas adalah pintu masuk, tetapi **kerusakan biasanya tidak terjadi di pintu itu** — ia terjadi di tempat lain yang mengasumsikan state sudah final. Tiga bentuk yang wajib diperiksa:

1. **Pintu internal yang terbuka.** Fungsi yang seharusnya `internal`/`private`, atau seharusnya hanya dipanggil sekali saat inisialisasi (`initialize`, `setup`, `init`), dideklarasikan `public`/`external` tanpa pengunci.
2. **Amplifikasi modal sesaat.** Pinjam modal besar, setor, picu perhitungan kurs/reward/pinjaman, tarik kembali — dalam satu transaksi. Yang dicari: selisih nilai yang tertinggal.
3. **Peracunan state untuk aktor berizin.** Penyerang tak berizin **tidak perlu** memegang peran Keeper/Relayer/Solver. Ia cukup meracuni state/antrean/saldo lewat fungsi publik, lalu menunggu aktor sah menjalankan rutinitasnya. Ini **Jalur 3** dari 5 Jalur Permissionless (`M-005` §3) dan tidak memerlukan reentrancy sama sekali.

## 4. Auditor Blindspot

Auditor memeriksa fungsi publik satu per satu dan menyimpulkan "tidak ada yang bisa dilakukan penyerang" karena setiap fungsi tampak aman secara lokal. Yang tidak diperiksa: **komposisi antar-fungsi** dan **efeknya terhadap fungsi berizin yang dieksekusi belakangan**.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila seluruh entrypoint publik terbukti tidak dapat mengubah state yang dibaca fungsi bernilai, dibuktikan dengan pelacakan pembaca (bukan asumsi).
- **Wajib PoC** untuk Jalur 3: (a) racuni state lewat jalur permissionless, lalu (b) picu fungsi rutin sebagai Keeper/Relayer — `vm.prank` untuk aktor sah diizinkan menurut `templates/VERDICT.md`, **tetapi state racun wajib berasal dari panggilan nyata penyerang**, bukan `vm.store`.
- Fuzz wajib mengacak: ukuran modal flashloan, urutan panggilan, dan selang waktu antara peracunan dan eksekusi rutin.
