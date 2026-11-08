# MOD-TECHNICAL-RULES — Warisan Teknis Code-First (bukan mekanisme)

Plug-in METHODOLOGY-SEGITIGA: aturan PENULISAN, WADAH, VERDICT, BUKTI — diwarisi BY-REFERENCE
dari sistem lama; file ini hanya memuat **pointer + tambahan segitiga**. Jangan salin isi lama ke sini.

## 1. Penulisan & integritas file (warisan penuh — AGENTS.md §1.3-1.4, §4)

- Anti-truncate: `open("w")` dan `>` DILARANG untuk `audit/*.md`; pola `.tmp → fsync → os.replace`.
- Backup write-ahead SEBELUM mutasi; verifikasi ukuran + heading pasca-tulis.
- Metode write per karakteristik file (tulis-sekali / generate-massal / append-murni /
  append-lalu-patch / patch-baris) — tabel di AGENTS.md §1.3.3.
- Satu penulis per file: subagent menulis staging, Parent merge + `MERGE-LOG.tsv` + `merge_audit.py`.
- Integritas bukti: blok `BUKTI_SIMULASI`/`PERCOBAAN` WAJIB dari log nyata; nama test WAJIB ada
  di lab/arsip (verifikasi `forge test --list` sebelum menutup Fase F).

## 2. Wadah & verdict akhir (warisan penuh — VERDICT.md)

- `04` guard statis tersangkal | `05` antrean lead | `06` gugur permanen (wajib bukti untuk
  POC_FAILS/NEGATIVE_EV/DUST) | `07` belum tuntas (target 0) | `08` valid-tak-eligible (hak Fase F) |
  `09` VALID_ELIGIBLE live.
- 11 Pernyataan Wajib + TANGGA_BUKTI A/A-HEAD/B/C/D; D tidak sah menggugurkan.
- **Tambahan segitiga**: provenance lead wajib `[LAPIS: VALUE|PATH|FLOW]` + `[AF-xx]`;
  framing laporan TANPA sebutan escape-hatch governance (kondisi sekarang saja).

## 3. Gerbang anti-menyerah (warisan — AGENTS.md §3b)

- 3-Stage Escalation: 2 manual + 1 fuzz wajib sebelum gugur ke `06`.
- Self-Healing tooling: flag → harness minimal → fallback RPC; log ketiganya wajib di `07`.
- No-Code-No-Reject: gugur tanpa eksekusi = PAPER_REFUTATION → laporan ditolak.

## 4. Checkpoint & resume (warisan — AGENTS.md §0, §2b)

- `STATE.md` kursor + write-ahead sebelum pindah item; maks 50 baris; scratchpad ≤10 baris.
- Do-Not-Reopen: item di 06/08/09 terkunci permanen kecuali bukti baru material tercatat.
- **Tambahan segitiga**: `STATE.md` menunjuk TAHAP segitiga (A-F) + pot/jahitan aktif;
  `notes/money-ledger.md` dan `notes/path-map.md` adalah artefak hidup tahap A/B.

## 5. Konsultasi pendukung (POSISI BARU — bukan prosedur lama)

- FACTS/RADAR = **falsifier**: dibuka SETELAH hipotesis buta lahir (L-FLOW gate-C), bukan sebelum.
- POV catalog = **generator**: ditanya per pot ("POV mana yang muat di uang ini?").
- Konsultasi sibling lead tetap wajib sebelum PoC (anti-duplikat), tapi bukan sumber ide utama.

## 6. Guardrail Low (baru — mengikat semua tahap)

- Tiap gate A-F mencatat Low yang terlihat; Low permissionless/kerugian terukur DILARANG dibuang
  diam-diam; spesies per lapis: VALUE→stuck-funds, PATH→config-brick, FLOW→griefing/drain-laten.
- Bounty dengan tier Low berbayar (cek INTEL.md) → Low layak diajukan dengan framing jujur.
