---
name: sc-c-hunt
description: Eksekusi Perburuan Dua Gelombang pada Wilayah Aktif R_i — STAGE-C1 (Blind Adversarial Hunt + Pengisian RADAR.md [TOUCHES]) dan STAGE-C2 (Cross-Pollination via Inversi FACTS.md, Rantai RADAR.md, & Lazy-Loading _ROUTER.md menuju Antrean [QUEUED] di 05-raw-leads.md).
---

# Skill sc-c-hunt — Perburuan Dua Gelombang (STAGE-C1 & STAGE-C2 / L-HUNT)

Anda menjalankan Tahap C (`L-HUNT`) pada Wilayah Aktif R_i yang terbagi secara ketat menjadi Gelombang 1 (`STAGE-C1`) dan Gelombang 2 (`STAGE-C2`). Dilarang mencampur kedua gelombang ini.

---

## 1. Eksekusi Gelombang 1: STAGE-C1 (*Blind Adversarial Hunt & Radar Harvesting*)

1. Muat Konteks `STAGE-C1`:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. ATURAN BESI `STAGE-C1`:
   DILARANG KERAS membuka berkas _ROUTER.md atau membaca berkas plugin M-xxx, AF-xx, DOM-xx, POV-xx, maupun CHAIN-xx selama berada di STAGE-C1. Gunakan murni insting adversarial Anda terhadap L-VALUE dan L-PATH Wilayah R_i.
3. Tiga Tugas Wajib di `STAGE-C1`:
   - Catat Jalur Terjaga ke `04-code-guarded.md`: Setiap jalur pada path-map.md yang dicurigai namun setelah diperiksa ternyata sudah dijaga rapat oleh kode (require, assert, ensure, *account/capability constraint*, atau fakta di FACTS.md) wajib dicatat ke 04-code-guarded.md beserta jangkar Path/File.ext:Lxx-Lyy dan ekspresi penjaganya.
     **Sebelum menulis entri `04`, WAJIB membaca `references/methods/M-005-guard-inversion.md` §3** (5 Jalur Permissionless). Setiap GUARD berstatus `TERSANGKAL` wajib disertai tabel **tepat 5 baris** (J1–J5) di §3 `04-code-guarded.md`: satu baris per jalur, berisi `TERTUTUP`/`TEMBUS` + alasan + jangkar `Path/File.ext:Lxx-Lyy`.
     **Guard yang TEMBUS salah satu jalur DILARANG masuk `04`** — tulis sebagai lead di `05-raw-leads.md` dengan tag `[TEMBUS-Jn]`. `--rules` menolak entri `TERSANGKAL` yang tabel jalurnya tidak lengkap (`RULES-04`).
   - Catat Observasi Awal ke `05-raw-leads.md` (`[WAVE-1-BLIND]`): Setiap ketimpangan logika, asumsi rapuh, atau celah potensial di Wilayah R_i dicatat pada bagian [WAVE-1-BLIND] di 05-raw-leads.md dengan jangkar Path/File.ext:Lxx-Lyy.
   - Panen Sinyal Lintas-Modul ke `RADAR.md` (`[TOUCHES: ...]`): Setiap fungsi/instruksi di Wilayah R_i yang menulis, mengubah, atau mengasumsikan variabel state/akun/objek yang juga disentuh oleh modul lain wajib dicatat ke RADAR.md dengan tag eksak `[TOUCHES: NamaModul.namaVariabelAtauFungsi]`.
4. Kunci Gate C1:

       python3 tools/verify_segitiga.py --gate C1 <audit-dir>

   Setelah PASS, ubah Current Stage di STATE.md menjadi STAGE-C2.

---

## 2. Eksekusi Gelombang 2: STAGE-C2 (*Cross-Pollination, Lazy-Load _ROUTER.md, & Antrean [QUEUED]*)

1. Muat Konteks `STAGE-C2` (Otomatis Menyuntikkan `FACTS`, `RADAR`, & `_ROUTER.md`):

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. Lakukan Tiga Operasi Penyilangan (`[WAVE-2-CROSS]` di `05-raw-leads.md`):
   - Operasi 1 — Inversi Prasyarat `FACTS.md`: Ambil setiap baris fakta Wilayah R_i di FACTS.md, baca kolom Prerequisite Inversion Hint, dan uji apakah syarat tersebut dapat diruntuhkan lewat pinjaman kilat, donasi langsung, nilai batas (0, 1, MAX), perbedaan desimal, atau urutan transaksi.
   - Operasi 2 — Perakitan Rantai `RADAR.md` (`[TOUCHES]` Collision): Periksa apakah ada >= 2 sinyal di RADAR.md yang menyentuh tag [TOUCHES: NamaModul.simbol] yang sama. Jika ada, isi Matriks Pasangan Rantai di RADAR.md dan rakit skenario *Chained Exploit*.
   - Operasi 3 — *Lazy-Loading* Bank Ilmu via `_ROUTER.md`: Baca tabel indeks _ROUTER.md (methods, attack-forms, domains, pov, chains). Panggil read_file hanya pada berkas plugin yang Trigger Symptom-nya cocok dengan gejala di Wilayah R_i.
3. Saringan Kualitas Segitiga & Pengisian Tabel `[QUEUED]` Tanpa Plafon Total:
   - Pindahkan hipotesis yang patah oleh FACTS.md atau penjaga kode ke `04-code-guarded.md`.
   - Seluruh kandidat yang lolos 3 syarat kualitas Segitiga (memiliki dampak L-VALUE, jalur L-PATH, dan tidak patah oleh FACTS.md) wajib dimasukkan ke Bagian 2 (Tabel Antrean `[QUEUED]`) di 05-raw-leads.md tanpa batas plafon total (jangan pernah membuang kandidat valid).
   - Urutkan seluruh kandidat [QUEUED] berdasarkan Prioritas EV (`SOUL.md §3`: `P1` s/d `P5`).
   - **Bukti baca (MATCH).** Setiap plugin yang dipakai di kolom Method/AF/Plugin wajib punya baris MATCH di §1.3 dengan kutipan **verbatim** dari berkas plugin. `--gate C2` mencocokkan kutipan ke isi berkas; kutipan palsu/ingatan = FAIL.
   - **Katalog = sinyal wawasan, BUKAN gerbang.** Isi kolom Assigned Method / Assigned Attack Form dengan HASIL konsultasi katalog (ID yang gejalanya cocok) ATAU penanda `[NO-CATALOG]`. Kandidat DILARANG gugur hanya karena tidak cocok katalog — pola tanpa kategori adalah temuan orisinal reasoning Anda sendiri. Pilihan M-xxx + AF-xx untuk pelaksanaan uji dikukuhkan di STAGE-D.
4. Kunci Gate C2:
python3 tools/verify_segitiga.py --gate C2 <audit-dir>

   Setelah PASS, perbarui STATE.md (Current Stage: STAGE-D, Queued Leads Count, Last Passed Gate: GATE-C2) untuk melanjutkan ke sc-d-prove.
