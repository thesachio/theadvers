# theadvers — Template Workflow Audit Web3 (SEGITIGA + OFFCHAIN)

**Repo ini adalah TEMPLATE, bukan proyek audit.** Tidak memuat kode kontrak tertentu dan tidak
memuat temuan. Tujuannya: dijalankan/di-fork untuk audit baru, lalu diisi — termasuk sebagai
basis **sc-autopilot (segitiga + offchain)**.

Metode inti: **Segitiga** — `L-VALUE → L-PATH → L-FLOW` — diperluas dengan **Tahap E (off-chain)**
dan ditutup **Tahap F (verdict)**. Enam tahap, enam gate.

## Berkas konstitusi (mengikat)

| Berkas | Isi | Kapan dibaca |
|---|---|---|
| **`SOUL.md`** | identitas persona, sikap adversarial, hukum kognitif | setiap sesi, sebelum apa pun |
| **`AGENTS.md`** | konstitusi operasional: Langkah −1, anti-truncate, staging, tangga bukti | setiap sesi + tiap `delegate_task` |
| **`AUTOPILOT-MAPPING.md`** | peta Fase 1-4 lama → Tahap A-F (untuk sc-autopilot) | saat menjalankan mode autopilot |
| **`CLASSIFICATION.md`** | tiga sumbu klasifikasi: LAPIS (baru) × CLASS (lama) × AF (baru) | saat menulis lead `05` |

Ketiganya adalah berkas **kerja**, bukan arsip. Bila mengubah metode, ubah di sini — bukan di
salinan lain.

## Cara pakai untuk audit baru

**Template dan hasil audit DIPISAH.** Repo ini hanya berisi metode + alat; hasil audit tinggal di
repo inbox/privat terpisah agar `ingest.py` dapat membacanya dari root dan agar temuan tidak
terpublikasi sebelum dilaporkan.

```bash
# 1. Salin template ini ke folder kerja audit (tanpa .git)
rsync -a --exclude .git <path-template>/ ~/audits/<nama-proyek>/
cd ~/audits/<nama-proyek>

# 2. Tandai pin target (commit yang diaudit) — WAJIB
$EDITOR target/PIN.md

# 3. Siapkan wadah hasil (dibuat lokal, TIDAK masuk repo template)
mkdir -p audit/notes/backups audit/lab
cp templates/STATE.md templates/INTEL.md audit/
cp templates/04-code-guarded.md templates/05-raw-leads.md templates/06-refuted-invalid.md \
   templates/07-needs-next-step.md templates/08-valid-not-eligible.md \
   templates/09-confirmed-findings.md templates/FACTS.md templates/RADAR.md audit/

# 4. Mulai dari Tahap A0 sesuai audit/STATE.md
```

**Jangan** menyalin isi `references/` ke folder audit — folder itu adalah rujukan metode, dipakai
lintas proyek.

## Struktur

```
SOUL.md               identitas persona (mengikat)
AGENTS.md             konstitusi operasional (mengikat)
AUTOPILOT-MAPPING.md  peta Fase 1-4 -> Tahap A-F
CLASSIFICATION.md     LAPIS x CLASS x AF — tiga sumbu, jangan dicampur
methodology/          metode: 1 dokumen induk + 6 modul plug-in + flow-diagram
references/           18 berkas rujukan metode & POV & tooling (dilampirkan, bukan di-link)
templates/            wadah hasil + 3 template submission
verify/               SCHEMA.md (aturan MANIFEST.json) + ingest.py + VERDICT + RUBRIK
tools/                gate checker + verifikasi integritas
```

Hasil audit **dibuat** oleh operator di folder kerja, tidak disimpan di repo ini:

```
audit/                wadah per proyek (TIDAK di repo template)
  STATE.md            kursor: TAHAP (A-F) + pot/jahitan aktif + Gate Meter
  INTEL.md            Tahap A0
  notes/money-ledger.md, notes/path-map.md, notes/backups/
  lab/                harness PoC
  04..09              wadah hasil
  FACTS.md, RADAR.md
target/PIN.md         commit, cara reproduce, repo pendukung
```

## Submission ke program bounty

Setelah Tahap F, temuan yang layak dikirim ke program memakai **repo inbox terpisah**:

```
<repo-inbox>/
├── MANIFEST.json          <- diverifikasi tools/ingest.py (WAJIB MECH-OK)
├── findings/<ID>.md       <- templates/TECHNICAL-REPORT.md
├── poc/<ID>.<ext>         <- templates/POC-PACKAGE.md
└── snippets/              <- kutipan kode yang dirujuk field `file`
```

```bash
python3 verify/ingest.py <repo-inbox>    # target: N/N MECH-OK
```

**Gerbang:** temuan yang belum `MECH-OK` DILARANG dikirim, sekalipun laporannya meyakinkan.
Email pengantar: `templates/SUBMISSION-EMAIL.md`.

## Alur kerja (6 tahap, 6 gate)

```
A. L-VALUE   census nilai live -> EV ledger          GATE-A
B. L-PATH    peta aliran -> jahitan + EV             GATE-B
C. L-FLOW    bedah sink -> lead 05 (LAPIS + AF)      GATE-C
D. SIMULASI  10 metode x POV -> 06/07/08/09          GATE-D
E. OFFCHAIN  dipicu anomali -> akar kode             GATE-E
F. VERDICT   11 Pernyataan + rubrik severity         GATE-F
```

## Rujukan (dilampirkan penuh di `references/`)

Tidak ada yang "di-link saja". Semua berkas ada di dalam repo agar tetap terbaca saat offline
dan tidak bergantung pada versi skill yang berubah.

| Berkas | Isi |
|---|---|
| `ref-method-registry.md` | M-001..M-010 (registry metode bedah) |
| `ref-attacker-pov.md` | Router POV 8-field + aturan deteksi rantai |
| `ref-pov-call.md` | POV surface panggilan (callback, reentrancy, delegatecall) |
| `ref-pov-defi.md` | POV DeFi (self-liquidation, bad debt, valuation vs execution) |
| `ref-pov-math.md` | POV matematika (indeks akrual, inverse rounding) |
| `ref-pov-chain.md` | POV lintas-rantai & asinkron |
| `ref-calls-tokens-reentrancy.md` | Token non-standar, hook, reentrancy |
| `ref-math-and-vaults.md` | Vault/share accounting, pembulatan |
| `ref-defi-oracles-liquidation.md` | Oracle, staleness, likuidasi |
| `ref-chain-evm-tron.md` / `ref-chain-solana.md` / `ref-chain-sui-move.md` / `ref-chain-ton-async.md` | Tooling & batas per rantai |
| `ref-test-evm-advanced.md` / `ref-test-multichain-advanced.md` | Teknik harness & fuzz |
| `ref-atomic-write.md` | Aturan tulis atomik (anti-truncate) |

## Aturan yang mengikat

1. **Anti-truncate** — `open("w")` dan `>` DILARANG untuk `audit/*.md`. Pakai `.tmp → fsync → os.replace`.
2. **Baca UTUH** — kode wajib dibaca dari `function` sampai `}` penyeimbang. `grep` hanya untuk
   *menemukan*, bukan menyimpulkan.
3. **No-Code-No-Reject** — gugur tanpa eksekusi test = `PAPER_REFUTATION_DETECTED`.
4. **3-Stage** sebelum mengunci di `06` — 2 manual + 1 fuzz wajib.
5. **Write-ahead checkpoint** — geser `STATE.md` SEBELUM mulai item berikutnya.
6. **Bukti dari log nyata** — blok `BUKTI_SIMULASI`/`PERCOBAAN` tidak boleh disusun dari ingatan.
7. **Provenance** — tiap lead wajib `[LAPIS: VALUE|PATH|FLOW]` + `[AF-xx]`.

## Validasi

```bash
python3 tools/verify_segitiga.py --audit-dir audit
```

Memeriksa G1–G8 (provenance, rentang baris, bukti nyata, batas STATE, file kosong, registry AF).
