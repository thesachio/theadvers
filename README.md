# theadvers — Audit Run 3 (METHODOLOGY-SEGITIGA + OFFCHAIN)

Repo kerja audit **Across Protocol** dengan metode **Segitiga (L-VALUE → L-PATH → L-FLOW)**
diperluas dengan **Tahap E (off-chain)**.

- **Target kode:** `across-protocol/contracts` @ `d0725ea001ca119a529065c22134298ec353941c`
  (lihat `target/PIN.md`)
- **Metode:** `methodology/METHODOLOGY-SEGITIGA.md` + 6 modul plug-in
- **Alasan run ketiga:** `audit/METHODOLOGY-DELTA.md` — **wajib dibaca sebelum Tahap A**

## Status

**SKELETON ONLY.** Belum ada pekerjaan audit. `STATE.md` menunjuk `A0_BOOTSTRAP`.

## Struktur

```
methodology/          metode (6 modul + flow-diagram) — sumber kebenaran alur
templates/            STATE, 04-09, FACTS, RADAR, VERDICT, SEVERITY-RUBRIC, MERGE-LOG
audit/
  STATE.md            kursor: TAHAP (A-F) + pot/jahitan aktif + Gate Meter
  METHODOLOGY-DELTA.md apa yang berubah dari run 1-2, dan yang DILARANG diklaim
  INTEL.md            Fase 0 (nama, overview, link, bounty, deployment)
  notes/
    money-ledger.md   Tahap A — EV ledger (artefak hidup)
    path-map.md       Tahap B — peta jahitan (artefak hidup)
    backups/          backup write-ahead
  lab/                harness Foundry/Rust (PoC)
  04..09              wadah hasil (kosong)
  FACTS.md            falsifier, dibangun ulang dari nol
  RADAR.md            sinyal lintas-domain (append-only)
target/PIN.md         commit, cara reproduce, repo pendukung
tools/                verifikasi integritas & merge
```

## Alur kerja (ringkas)

```
A. L-VALUE   census nilai live → EV ledger          GATE-A
B. L-PATH    peta aliran → jahitan + EV             GATE-B
C. L-FLOW    bedah sink → lead 05 (LAPIS + AF)      GATE-C
D. SIMULASI  10 bentuk serangan → 06/07/08/09       GATE-D
E. OFFCHAIN  dipicu anomali → akar kode             GATE-E
F. VERDICT   11 Pernyataan + rubrik severity        GATE-F
```

## Aturan yang mengikat

Konstitusi operasional penuh ada di `AGENTS.md` workspace induk. Yang paling sering dilanggar:

1. **Anti-truncate** — `open("w")` dan `>` DILARANG untuk `audit/*.md`. Pakai `.tmp → fsync → os.replace`.
2. **Baca UTUH** — kode kontrak wajib dibaca dari `function` sampai `}` penyeimbang. `grep` hanya untuk *menemukan*, bukan menyimpulkan.
3. **No-Code-No-Reject** — gugur tanpa eksekusi test = `PAPER_REFUTATION_DETECTED`.
4. **3-Stage** sebelum mengunci di `06` — 2 manual + 1 fuzz wajib.
5. **Write-ahead checkpoint** — geser `STATE.md` SEBELUM mulai item berikutnya.
6. **Bukti dari log nyata** — blok `BUKTI_SIMULASI`/`PERCOBAAN` tidak boleh disusun dari ingatan.

## Build target (single-job, wajib)

```bash
FOUNDRY_JOBS=1 forge build contracts/
```

Build penuh OOM di VPS ini. Selalu bangun path tertentu, bukan seluruh repo.
