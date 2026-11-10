---
name: sc-a-scope
description: Eksekusi STAGE-0 (Global Partitioning & Rekonsiliasi 100% Berkas Sumber ke Tier 1/2/3) dan STAGE-A (Pemetaan L-VALUE termasuk Intended Capacity & Ekstraksi Fakta Verbatim FACTS.md) pada Wilayah Aktif R_i.
---

# Skill sc-a-scope — Global Partitioning (STAGE-0) & Region Value/Facts (STAGE-A)

Anda menjalankan Tahap 0 (`L-PART`) (jika audit baru dimulai) dan Tahap A (`L-VALUE`) untuk Wilayah Aktif R_i. Patuhi seluruh hukum di SOUL.md, AGENTS.md, dan methodology/METHODOLOGY-SEGITIGA.md.

---

## 1. Langkah Pertama Mutlak (Hard Bootloader Konteks)

Sebelum membaca berkas sumber proyek target, jalankan perintah pemulihan konteks:

    python3 tools/verify_segitiga.py --context-packet <audit-dir>

Baca output yang tercetak di layar untuk mengetahui apakah posisi Current Stage di STATE.md berada pada STAGE-0 atau STAGE-A, serta wilayah mana yang sedang berstatus [ACTIVE].

---

## 2. Prosedur Jika Current Stage == STAGE-0 (Global Partitioning — 1x di Awal Audit)

1. Write-Ahead Checkpoint: Perbarui STATE.md (Current Stage: STAGE-0, status START).
2. Rekonsiliasi 100% Berkas Sumber dalam Scope:
   - Daftarkan seluruh berkas sumber dalam *scope* pada bahasa/runtime apa pun (.sol, .vy, .rs, .move, .cairo, .go, .ts, .py, .circom, .nr, .fc, dll.) ke Bagian 1 (Tabel Rekonsiliasi 100% Berkas) di path-map.md.
   - Klasifikasikan setiap berkas ke dalam:
     - Tier 1 (`CORE-ASSET`): Penyimpan, pencetak, pembakar, pengunci, atau pemindah aset/klaim.
     - Tier 2 (`VALUATION-CONTROL-LATENT`): Penentu harga/kurs/indeks/oracle, likuidasi/lelang/dispute, otorisasi/governance/pause, modul bersaldo awal 0 tetapi memiliki Intended Capacity > 0, serta verifikator/relayer *off-chain*.
     - Tier 3 (`ISOLATED-PERIPHERAL`): Antarmuka/trait murni, konstanta, atau helper tanpa state/nilai. Lakukan pemeriksaan 1-pass, catat bukti jangkar baris kode (Path/File.ext:Lxx-Lyy) di path-map.md, dan beri status `[LOCKED-TIER3]`.
3. Pembentukan Antrean Wilayah Uang (`R_1 .. R_N`):
   - Kelompokkan seluruh berkas Tier 1 dan Tier 2 yang saling berikatan ke dalam Wilayah Uang R_1, R_2, ..., R_N (2–5 berkas per wilayah).
   - Urutkan wilayah berdasarkan Prioritas EV (`SOUL.md §3`: `P1` s/d `P5`) dan daftarkan ke tabel Antrean Wilayah di STATE.md dengan status [OPEN].
4. Kunci Gate 0:

       python3 tools/verify_segitiga.py --gate 0 <audit-dir>

5. Transisi ke Wilayah Pertama: Ambil wilayah [OPEN] dengan EV tertinggi (misal R_1), ubah statusnya menjadi [ACTIVE], set Active Region: R_1 dan Current Stage: STAGE-A di STATE.md, lalu lanjutkan ke Bagian 3 di bawah ini.

---

## 3. Prosedur STAGE-A pada Wilayah Aktif R_i (L-VALUE & FACTS.md)

1. Segarkan Paket Konteks `STAGE-A`:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

2. Petakan Kapasitas Nilai (`L-VALUE`) di `path-map.md`:
   Untuk setiap berkas/modul di Wilayah Aktif R_i, isi tabel L-VALUE pada path-map.md yang mencakup:
   - Jenis aset, hak klaim, objek, atau state otoritas yang dikelola,
   - Current Balance / Initial State,
   - Intended Capacity & Latent Power (wajib diisi agar modul bersaldo 0 saat deploy/testnet atau modul likuidasi/router tetap terukur kapasitas ekonominya),
   - Core Value Invariant beserta jangkar Path/File.ext:Lxx-Lyy.
3. Ekstrak Fakta Verbatim & Peta Inversi Prasyarat ke `FACTS.md`:
   - Baca seluruh berkas sumber milik Wilayah R_i.
   - Catat setiap syarat penjaga (require, assert, ensure, *account/capability constraint*), rumus skala/pembulatan, dan aturan transisi state ke FACTS.md dengan format:
     [Fact ID] | [Region R_i] | [Path/File.ext:Lxx-Lyy] | [NamaModul.simbol] | [Kategori] | [Ekspresi/Rumus Kode Asli] | [Prerequisite Inversion Hint: Bagaimana mematahkan prasyarat ini di Gelombang 2?].
   - Dilarang keras memakai token kompresi (..., dll., dst., etc., rest of logic).
4. Kunci Gate A & Perbarui Checkpoint:

       python3 tools/verify_segitiga.py --gate A <audit-dir>

   Setelah PASS, perbarui STATE.md (Current Stage: STAGE-B, Last Passed Gate: GATE-A) untuk melanjutkan ke sc-b-map.
