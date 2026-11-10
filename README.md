# theadvers v2.0 — Mesin Audit Adversarial Berbasis Bukti (Metode Segitiga)

**Repo ini adalah MESIN/FRAMEWORK, bukan proyek audit.** Tidak memuat kode kontrak target dan tidak
memuat temuan. Dipakai dengan cara disalin ke folder kerja audit baru, lalu dijalankan tahap demi
tahap atau otonom lewat `sc-autopilot`.

Metode inti: **Segitiga** — `L-VALUE` (di mana nilai) → `L-PATH` (jalur sentuh) → `L-PROVE`
(bukti eksekusi). Tiga titik wajib terhubung; anomali tanpa dampak nilai bukan temuan.

---

## 1. Siklus Eksekusi

```
STAGE-0   Global Partitioning & Rekonsiliasi 100% Berkas → 3 Tier → Wilayah Uang R_1..R_N
   │
   ├── Untuk SETIAP Wilayah R_i (vertikal, tidak menyeberang sebelum bersih):
   │     STAGE-A   L-VALUE  : kapasitas nilai + fakta verbatim (path-map.md, FACTS.md)
   │     STAGE-B   L-PATH   : peta 3-edge ([EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT])
   │     STAGE-C1  Gelombang 1 — Blind Adversarial Hunt (dilarang buka plugin)
   │     STAGE-C2  Gelombang 2 — Inversi FACTS + rantai RADAR + lazy-load _ROUTER → [QUEUED]
   │     STAGE-D   Prove — Rolling Batch maksimal 5 [ACTIVE]
   │     STAGE-E   Verdict — 06 / 07 / 08 / 09
   │     STAGE-F   Disclosure — blok 09 + wadah cases/<FIND-ID>/ → --close-region R_i
   │
   └── FINAL-SWEEP  Cross-region chain sweep → --final
```

Setiap transisi wajib lulus gate mekanis. **Dilarang** mengubah `Current Stage` sebelum gate PASS.

---

## 2. Berkas Konstitusi (mengikat)

| Berkas | Isi | Kapan dibaca |
| :--- | :--- | :--- |
| **`SOUL.md`** | identitas, 7 Hukum Kognitif Besi, prioritas EV P1–P5, pantangan mutlak | setiap sesi, sebelum apa pun |
| **`AGENTS.md`** | konstitusi operasional: hard bootloader, wadah kanonik, siklus A–F, drop-in plugin, zero-compression, tabel gate | setiap sesi + tiap `delegate_task` |
| **`methodology/METHODOLOGY-SEGITIGA.md`** | 9 blok `@SLICE` yang disuntik ulang per tahap oleh `--context-packet` | diekstrak otomatis, bukan dibaca penuh |

---

## 3. Struktur

```
SOUL.md                     identitas + hukum kognitif + prioritas EV
AGENTS.md                   konstitusi operasional
methodology/
  METHODOLOGY-SEGITIGA.md   mesin alur (@SLICE: STAGE-0, A, B, C1, C2, D, E, F, FINAL-SWEEP)
  attack-forms/             AF-01..AF-10 — bentuk serangan uji (1 berkas = 1 bentuk)
  domains/                  DOM-* — heuristik domain (vault, lending, amm, oracle, staking, bridge, governance)
references/
  methods/                  M-001..M-010 — metode bedah universal
  pov/                      POV-* — sudut pandang aktor (unprivileged, liquidator, relayer-mev, griefer, integrator)
  chains/                   CHAIN-* — pola serangan berantai (reentrancy, desync, oracle, rounding, offchain)
templates/                  wadah kerja audit + standar laporan
  STATE.md FACTS.md RADAR.md path-map.md
  04-code-guarded.md 05-raw-leads.md 06-refuted-invalid.md
  07-needs-next-step.md 08-valid-not-eligible.md 09-confirmed-findings.md
  VERDICT.md                hukum acara pengadilan bukti (STAGE-E/F)
  TECHNICAL-REPORT.md POC-PACKAGE.md SUBMISSION-EMAIL.md SEVERITY-RUBRIC.md
  case/                     chat.md, laporan-teknis.md, poc.md (standar wadah cases/<ID>/)
skills/                     sc-a-scope, sc-b-map, sc-c-hunt, sc-d-prove, sc-e-verdict, sc-f-report, sc-autopilot
tools/
  verify_segitiga.py        mesin gate + context re-hydrator + router sync
  deploy_parity.py          rekonsiliasi deployment (LIVE_MATCH / LIVE_IDENTITY)
verify/
  SCHEMA.md                 aturan field laporan
  VERDICT.md                hukum acara lengkap (11 Pernyataan, #11e PAPER_REFUTATION)
  SEVERITY-RUBRIC.md        matriks severity lintas platform
  ingest.py                 gerbang submission (MECH-OK)
```

---

## 4. Cara Pakai untuk Audit Baru

```bash
# 1. Salin mesin ke folder kerja audit (tanpa .git)
rsync -a --exclude .git --exclude notes/backups <path-repo>/ ~/audits/<nama-proyek>/
cd ~/audits/<nama-proyek>

# 2. Sinkronkan indeks plugin + pasang skill
python3 tools/verify_segitiga.py --sync

# 3. Siapkan wadah kerja dari templates/
mkdir -p audit/notes
cp templates/STATE.md templates/FACTS.md templates/RADAR.md templates/path-map.md audit/
cp templates/0*.md audit/

# 4. Isi identitas proyek pada audit/STATE.md, lalu mulai STAGE-0
python3 tools/verify_segitiga.py --context-packet audit
```

Hasil audit **tidak** disimpan di repo ini. Repo ini hanya mesin + metode.

---

## 5. Perintah Wajib

| Perintah | Kapan | Yang diperiksa |
| :--- | :--- | :--- |
| `--sync` | setiap menambah/mengubah berkas plugin | 4 baris header plugin + membangun ulang 5 `_ROUTER.md` + menyalin skill |
| `--context-packet <dir>` | awal setiap tahap, batch, dan pergantian wilayah | kursor STATE.md, `@SLICE` tahap aktif, fakta R_i, radar R_i, indeks router |
| `--gate 0` | selesai STAGE-0 | 100% berkas ke Tier 1/2/3, Tier-3 terkunci 1-pass, antrean R_1..R_N |
| `--gate A` | selesai STAGE-A | fakta R_i berjangkar `:Lxx` + tabel L-VALUE terisi |
| `--gate B` | selesai STAGE-B | ketiga tag `[EDGE-*]` terpetakan dengan jangkar |
| `--gate C1` | selesai Gelombang 1 | jalur terjaga / observasi `[WAVE-1-BLIND]` + sinyal `[TOUCHES: ...]` |
| `--gate C2` | selesai Gelombang 2 | penyilangan `[WAVE-2-CROSS]` nyata + kandidat `[QUEUED]` berpajangan M-xxx & AF-xx |
| `--gate D` | selesai STAGE-D | `[ACTIVE]` ≤ 5 dan tiga titik bukti terisi |
| `--gate E` | selesai STAGE-E | seluruh `[ACTIVE]` pindah ke 06/07/08/09 |
| `--close-region <R_i>` | selesai STAGE-F | `[QUEUED]==0`, `[ACTIVE]==0`, seluruh `cases/<FIND-ID>/` (chat.md, laporan-teknis.md 9 bagian, poc.md 5 bagian + Kontrol Positif) |
| `--final` | setelah seluruh wilayah `[CLOSED]` | semua wilayah tutup, lead bersih, bebas kompresi, wadah kasus lengkap |

Gerbang bersifat **monoton**: `GATE-C1` hanya sah bila `Last Passed Gate` di `STATE.md` sudah
mencapai C1 atau lebih tinggi. Setiap gate diuji dua arah — PASS pada kondisi bersih, **FAIL** pada
pelanggaran yang disuntikkan.

---

## 6. Aturan yang Mengikat

1. **Jangkar verbatim.** Setiap fakta dan entri wajib memuat `Path/File.ext:Lxx-Lyy` (rentang), bukan satu baris.
2. **Zero-compression.** Token `...`, `dll.`, `dst.`, `etc.`, `rest of logic` dilarang di berkas analisis; gerbang menolak otomatis.
3. **Vertical region.** Dilarang membuka STAGE-A/B/C untuk `R_{i+1}` selama `R_i` masih `[QUEUED] > 0` atau `[ACTIVE] > 0`.
4. **Rolling batch.** Maksimal 5 kandidat `[ACTIVE]`; kandidat `[QUEUED]` tidak dibuang karena kuota.
5. **Write-ahead checkpoint.** Perbarui `STATE.md` **sebelum** memulai tahap berikutnya.
6. **Bukti dari eksekusi nyata.** Blok `BUKTI_SIMULASI:` wajib berisi perintah `$ ...` beserta keluarannya; menulis dari ingatan = `FABRICATED_EVIDENCE`.
7. **Drop-in plugin.** Tambah metode/serangan/domain/POV/chain cukup dengan 1 berkas baru + `--sync`, tanpa mengedit berkas lain.
8. **Whitehat.** Dilarang menyiarkan transaksi keluar, dilarang mengedit kode target (read-only 100%).

---

## 7. Menambah Pengetahuan (Drop-in Plugin)

Format header wajib 4 baris pada setiap berkas plugin:

```markdown
# [ID-PLUGIN] Judul Metode / Bentuk Serangan / Domain / POV / Chain
- Classes: [kategori kelas masalah atau domain]
- Trigger Symptom: [gejala kode spesifik yang memicu pembacaan berkas ini]
- Paired Items: [ID plugin pasangan yang direkomendasikan]
```

Lalu jalankan `python3 tools/verify_segitiga.py --sync`. Tabel `_ROUTER.md` diperbarui otomatis dan
langsung terbaca oleh `--context-packet` pada STAGE-C2 dan STAGE-D.

Agen **dilarang** membaca seluruh berkas plugin sekaligus: baca `_ROUTER.md` lebih dulu, lalu
`read_file` hanya pada berkas yang `Trigger Symptom`-nya cocok dengan wilayah aktif.
