# MOD-ATTACK-FORMS — Registry 10 Bentuk Serangan (AF-01..AF-10)

Plug-in METHODOLOGY-SEGITIGA tahap D. **Kontrak ekstensi**: AF-11 = append satu blok di bawah
(mirip registry M-0XX §4) — core dan modul lain TIDAK disentuh.
Bentuk serangan ORTOGONAL terhadap lapis: lapis memilih TARGET, bentuk memilih CARA SERANG.
Setiap lead di `05` WAJIB membawa tag `[AF-xx]` (GATE-C).

Format blok: ID | Nama | Gejala pemicu | Setup prasyarat | Metode lama diperluas | Bukti minimum | Wadah target.

---

### [AF-01] Serangan Langsung & Tidak Langsung
- **Gejala pemicu**: fungsi sink dapat dipanggil langsung; atau validasi hanya ada di hulu (router/gateway).
- **Setup**: EOA polos menembak sink; kontrol positif jalur sah WAJIB hidup.
- **Metode**: M-001 (sink-to-source), M-008 (direct downstream bypass).
- **Bukti**: PoC single-tx, tanpa cheatcode. **Wadah**: 05 → 09/08/06 sesuai verdict.

### [AF-02] Transaktor Pemicu (mock/self/victim) Lalu Serangan
- **Gejala pemicu**: jalur sah butuh partisipasi pihak lain (deposit, approve, callback, isi pesanan).
- **Setup**: seeding pihak pemicu dulu (`vm.prank(victim)` transaksi normal), LALU attacker menyerang;
  kontrol positif = pemicu berhasil menjalankan alurnya.
- **Metode**: M-003 (identitas ganda), M-010 (allowance/delegated authority).
- **Bukti**: PoC dua fase + kontrol positif. **Wadah**: 05 → sesuai verdict.

### [AF-03] Bundler Transaksi + Manipulasi, Lalu Serangan
- **Gejala pemicu**: multicall/batch/flashloan/PTB memungkinkan N langkah atomik dalam 1 blok.
- **Setup**: 1 bundel atomik berisi manipulasi + eksekusi; uji `f(a+b) ≠ f(a)+f(b)` (M-007).
- **Metode**: M-003, M-007, POV-EVM-01 (multicall context reuse).
- **Bukti**: PoC bundel + fuzz ukuran. **Wadah**: 05 → sesuai verdict.

### [AF-04] Racun State Dulu, Korban Eksekusi Terakhir (Unprivileged State Poisoning)
- **Gejala pemicu**: fungsi berizin (keeper/relayer/solver) membaca state yang BISA ditulis
  pengguna tak berizin (saldo, antrean, array, harga pool).
- **Setup**: KRONOLOGIS — attacker meracuni state (tx 1) → korban menjalankan tx rutin (tx 2)
  → hasil tx korban dibajak / korban rugi.
- **Metode**: M-005 Jalur 3, M-009.
- **Bukti**: dua tx berurutan, kerugian di tx KORBAN terukur. **Wadah**: 05 → 09/08 (severity korban).

### [AF-05] Hentikan Siklus Hidup di Tengah (Half-Baked / Suspended State)
- **Gejala pemicu**: proses multi-tahap (request→finalize, propose→execute, initiateCooldown→claim).
- **Setup**: langkah-1 gantung → panggil jalur samping (transfer/borrow/liquidate/cancel) →
  langkah-2 finalisasi. Uji double-spend/penghindaran penalti pada status menggantung.
- **Metode**: M-009, POV-CALL-02.
- **Bukti**: PoC 3 langkah berurutan. **Wadah**: 05 → sesuai verdict.

### [AF-06] Panen Pasif State Sisa & Drift Pasca-Upgrade (Live Residual State)
- **Gejala pemicu**: allowance aktif, saldo mengendap, konfigurasi basi, slot pasca-upgrade belum init.
- **Setup**: BACA STATE LIVE dulu (`cast call/storage`, `getAccountInfo`) — bukti sisa NYATA, bukan dugaan.
- **Metode**: M-010 (5 konsep general).
- **Bukti**: log state live + PoC penyedotan. **Wadah**: 05 → 08/09 (kelas stuck-funds sering Low).

### [AF-07] Penyerahan Kontrol di Tengah State Timpang & Stale Writeback
- **Gejala pemicu**: baca-ke-lokal → interaksi eksternal/CPI/callback → tulis-balik lokal basi;
  atau state pasangan berubah sebagian saat panggilan keluar.
- **Setup**: mutasi di tengah jendela (via token callback, CPI, hook) lalu tulis-balik.
- **Metode**: M-006 Prinsip A, POV-CALL-01.
- **Bukti**: PoC urutan baca→interaksi→tulis-balik. **Wadah**: 05 → sesuai verdict.

### [AF-08] Desinkron Temporal & Akrual (Waktu, Jendela Akrual, Staleness)
- **Gejala pemicu**: indeks akrual (globalIndex/userIndex), fee berbasis waktu, staleness oracle,
  batas quoteTimeBuffer — nilai dibaca pada waktu berbeda.
- **Setup**: `vm.warp`/Δt=0, dua pembacaan pada blok/jendela berbeda, bandingkan delta ekspektasi vs aktual.
- **Metode**: M-002, M-004 (view vs write), POV-MATH-01.
- **Bukti**: PoC deviasi angka + fuzz parameter waktu. **Wadah**: 05 → sesuai verdict.

### [AF-09] Penyisipan Lintas-Transaksi & Asinkron (Sandwich, Valuation-Execution Mismatch, Async Interleaving)
- **Gejala pemicu**: valuasi membaca Sumber A (oracle/TWAP), eksekusi dikirim ke Sumber B (pool spot);
  atau pesan asinkron lintas-chain tanpa pending-lock.
- **Setup**: dua tx dalam blok/jendela sama (sandwich); atau dua pesan asinkron saling menyusup.
- **Metode**: POV-DEFI-02, M-003, POV-TON-01 (async), M-009.
- **Bukti**: PoC 2-tx/jendela + fuzz urutan. **Wadah**: 05 → sesuai verdict.

### [AF-10] Kebingungan Whitelist, Partial Subcall, & Pause Asimetris
- **Gejala pemicu**: guard `isWhitelisted[x]` tanpa cek pasangan aset; `try/catch` atau `.call`
  tanpa require dengan mutasi beda antar-cabang; `whenNotPaused` memblokir penyelamatan diri
  (repay/cancel) tapi membiarkan penalti (liquidate/slash).
- **Setup**: pasangan kembar (pool.token ≠ asset), subcall gagal-sebagian, pause aktif lalu uji
  fungsi penalti vs fungsi selamat.
- **Metode**: M-008 Jalur 5, POV-CALL-02, M-005 Jalur 4.
- **Bukti**: PoC per cabang + kontras sukses/gagal. **Wadah**: 05 → sesuai verdict.

---

## Routing gejala → bentuk (cepat)

| Gejala kode | Bentuk |
|---|---|
| sink callable langsung / validasi cuma di hulu | AF-01 |
| alur butuh pihak lain dulu | AF-02 |
| multicall/batch/flashloan | AF-03 |
| fungsi berizin baca state tak-berizin | AF-04 |
| proses multi-tahap | AF-05 |
| allowance/saldo/konfigurasi basi live | AF-06 |
| baca-lokal→call→tulis-balik | AF-07 |
| indeks akrual / fee waktu / oracle staleness | AF-08 |
| valuasi vs eksekusi beda sumber / pesan asinkron | AF-09 |
| whitelist kembar / try-catch divergen / pause asimetris | AF-10 |
