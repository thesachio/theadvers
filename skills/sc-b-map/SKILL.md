---
name: sc-b-map
description: Eksekusi STAGE-B (Pemetaan Jalur L-PATH dengan Tiga Kategori Edge Wajib: EDGE-ASSET, EDGE-VALUATION, dan EDGE-CONTROL/LATENT) khusus pada Wilayah Aktif R_i.
---

# Skill sc-b-map — Pemetaan Jalur 3-Edge Wilayah Aktif (STAGE-B / L-PATH)

Anda menjalankan STAGE-B (`L-PATH`) khusus untuk berkas-berkas di dalam Wilayah Aktif R_i.

---

## 1. Langkah Pertama Mutlak (Hard Bootloader Konteks)

Jalankan perintah pemulihan konteks dan lakukan *Write-Ahead Checkpoint* di STATE.md:

    python3 tools/verify_segitiga.py --context-packet <audit-dir>

Pastikan STATE.md menunjukkan Current Stage: STAGE-B untuk Wilayah Aktif R_i dan GATE-A telah lulus.

---

## 2. Prosedur Pemetaan Tiga Saraf Jalur (3-Edge Mapping) di path-map.md

Baca berkas sumber Wilayah Aktif R_i dan lengkapi bagian L-PATH untuk Wilayah R_i di path-map.md menggunakan tiga label wajib berikut:

1. `[EDGE-ASSET]` (Pipa Pergerakan Aset & Hak Klaim):
   - Petakan seluruh titik masuk, perpindahan internal, pencetakan (*mint*), pembakaran (*burn*), penguncian (*lock*), dan penarikan keluar aset/klaim/objek.
   - Format wajib: [EDGE-ASSET] [Path/File.ext:Lxx-Lyy] | [NamaModul.fungsiMasuk -> Operasi Mutasi] | [Alur perpindahan nilai & state yang berubah].

2. `[EDGE-VALUATION]` (Saraf Perhitungan Harga, Kurs, Indeks, & Pembulatan):
   - Petakan seluruh fungsi dan ekspresi yang menentukan nilai tukar share, pembacaan oracle, perhitungan totalAssets, totalSupply, indeks bunga/reward, dan konversi desimal/pembulatan integer.
   - Format wajib: [EDGE-VALUATION] [Path/File.ext:Lxx-Lyy] | [NamaModul.fungsiValuasi] | [Rumus eksak, variabel sumber yang dibaca, & arah pembulatan].

3. `[EDGE-CONTROL/LATENT]` (Jalur Otorisasi, Likuidasi, Sengketa, Callback, & Input Off-Chain):
   - Petakan seluruh jalur kontrol dan jalur laten: validasi otoritas/akun/objek/capability, fungsi likuidasi/lelang/slashing/dispute, fungsi darurat (*pause/unpause/upgrade*), panggilan keluar (*external call*, hook, callback, CPI), serta titik masuk data off-chain (relayer, keeper, tanda tangan kriptografis, bukti Merkle/ZK).
   - Format wajib: [EDGE-CONTROL/LATENT] [Path/File.ext:Lxx-Lyy] | [NamaModul.fungsiKontrolAtauLaten] | [Penjaga kode yang aktif, panggilan eksternal, & titik potong lintas-wilayah].

---

## 3. Verifikasi Gate B & Transisi ke STAGE-C1

1. Pastikan seluruh entri di path-map.md memiliki jangkar baris kode (Path/File.ext:Lxx-Lyy) dan bebas dari token kompresi (..., dll., dst., etc., rest of logic).
2. Jalankan gerbang verifikasi:

       python3 tools/verify_segitiga.py --gate B <audit-dir>
3. Setelah PASS, perbarui STATE.md (Current Stage: STAGE-C1, Last Passed Gate: GATE-B) untuk melanjutkan ke sc-c-hunt.
