# theadvers — Template Workflow Audit Web3 (SEGITIGA + OFFCHAIN)

**Repo ini adalah TEMPLATE, bukan proyek audit.** Tidak memuat kode kontrak tertentu dan tidak
memuat temuan. Tujuannya: dijalankan/di-fork untuk audit baru, lalu diisi.

Metode inti: **Segitiga** — `L-VALUE → L-PATH → L-FLOW` — diperluas dengan **Tahap E (off-chain)**
dan ditutup **Tahap F (verdict)**. Enam tahap, enam gate.

## Cara pakai untuk audit baru

```bash
# 1. Fork/clone template ini ke folder proyek baru
git clone <repo-ini> ~/audits/<nama-proyek>
cd ~/audits/<nama-proyek>

# 2. Isi pin target (commit yang diaudit) — WAJIB, tanpa ini temuan tak bisa direproduksi
$EDITOR target/PIN.md

# 3. Kosongkan artefak hidup (template ini sengaja berisi schema, bukan data)
#    STATE.md, INTEL.md, notes/money-ledger.md, notes/path-map.md

# 4. Mulai dari Tahap A0 (bootstrap) sesuai audit/STATE.md
```

**Jangan** menyalin isi `references/` ke folder audit — folder itu adalah rujukan metode, dipakai
lintas proyek.

## Struktur

```
methodology/          metode: 1 dokumen induk + 6 modul plug-in + flow-diagram
references/           16 berkas rujukan metode & POV & tooling (dilampirkan, bukan di-link)
templates/            wadah hasil: STATE, 04-09, FACTS, RADAR, VERDICT, SEVERITY-RUBRIC
audit/                INSTANCE yang diisi per proyek (kosong di template ini)
  STATE.md            kursor: TAHAP (A-F) + pot/jahitan aktif + Gate Meter
  INTEL.md            Fase 0: nama, overview, link, bounty, deployment
  notes/
    money-ledger.md   Tahap A — EV ledger (artefak hidup)
    path-map.md       Tahap B — peta jahitan (artefak hidup)
    backups/          backup write-ahead
  lab/                harness PoC
  04..09              wadah hasil
  FACTS.md            falsifier, dibangun setelah hipotesis
  RADAR.md            sinyal lintas-domain (append-only)
target/PIN.md         commit, cara reproduce, repo pendukung
tools/                gate checker + verifikasi integritas
```

## Alur kerja (6 tahap, 6 gate)

```
A. L-VALUE   census nilai live → EV ledger          GATE-A
B. L-PATH    peta aliran → jahitan + EV             GATE-B
C. L-FLOW    bedah sink → lead 05 (LAPIS + AF)      GATE-C
D. SIMULASI  10 bentuk serangan → 06/07/08/09       GATE-D
E. OFFCHAIN  dipicu anomali → akar kode             GATE-E
F. VERDICT   11 Pernyataan + rubrik severity        GATE-F
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
