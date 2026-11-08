# FLOW DIAGRAM — METHODOLOGY-SEGITIGA (0 → akhir)

Artefak diagram alir resmi; pasangan `METHODOLOGY-SEGITIGA.md` §1.
Notasi: ◇ = gate keputusan; [ ] = artefak hidup; ⚠ = guardrail Low (wajib di tiap gate).

```
┌────────────────────────────────────────────────────────────┐
│ FASE 0 — PROJECT INTEL (warisan sc-project-intel)          │
│ INTEL.md: scope bounty, repos org GitHub, severity basis,  │
│ alamat live, komit HEAD, laporan audit lama                │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐   ⚠ catat Low
│ TAHAP A — L-VALUE : sensus nilai live                      │   terlihat (stuck-
│ • saldo × chain × token besar × native                     │   funds, config
│ • konfigurasi live: role holders, whitelist, messenger,    │   brick) — dilarang
│   pause, fee params                                        │   dibuang diam-diam
│ • WAJIB probe via PROXY (bukan impl)                       │
│ [notes/money-ledger.md — EV terurut]                       │
└───────────────────────────┬────────────────────────────────┘
                            ▼
                    ◇ GATE-A: pot > ambang?
                    │   YA ──────────────────────┐
                    │   TIDAK                    │
                    ▼                            │
        pot = 0 DAN tidak di jalur aliran        │
        → MATI DINI (1 query, bukan lab)         │
        → catat no-victim di ledger              │
                                                 ▼
┌────────────────────────────────────────────────────────────┐
│ TAHAP B — L-PATH : peta siklus aliran                      │
│ • node = kontrak, edge = aliran dana (domain cartridge)    │
│ • EV per jahitan = max(balance_now, throughput_path)       │
│ • tandai jahitan ASYNC (bridge hop, in-flight)             │
│ [notes/path-map.md — seam list + EV]                       │
└───────────────────────────┬────────────────────────────────┘
                            ▼
                    ◇ GATE-B: jahitan EV > 0?
                    │   YA ──────────────────────┐
                    │   TIDAK                    │
                    ▼                            │
        cabang tanpa throughput → PANGKAS        │
        (anti state-space blowup)                │
                                                 ▼
┌────────────────────────────────────────────────────────────┐   ⚠ catat Low
│ TAHAP C — L-FLOW : bedah sink mutasi                       │   (griefing,
│ • baca fungsi UTUH (aturan A0, rentang baris)              │   drain-laten)
│ • toolkit M-001..M-010 + POV sebagai GENERATOR             │
│   ("POV mana yang muat di uang ini?")                      │
│ • klasifikasi reachability: 5 Jalur Permissionless         │
│ • FACTS/RADAR = FALSIFIER (dibuka SETELAH hipotesis buta)  │
│ • lead → audit/05 + tag [LAPIS:x] [AF-xx] [LOAD:M-xxx]     │
└───────────────────────────┬────────────────────────────────┘
                            ▼
                    ◇ GATE-C: lead punya provenance + AF tag?
                    │   YA ──────────────────────┐
                    │   TIDAK                    │
                    ▼                            │
        kembalikan: baca utuh + tag               │
                                                 ▼
┌────────────────────────────────────────────────────────────┐
│ TAHAP D — SIMULASI (3-Stage Escalation, per lead)          │
│ • pilih bentuk serangan AF-01..AF-10 (mod-attack-forms)    │
│ • Strike1: manual + Victim Seeding + kontrol positif       │
│ • Strike2: perbaikan urutan + 3-Way Amplification          │
│ • Strike3: FUZZ wajib (testFuzz_/proptest/halmos)          │
│ • dual-mode fork: FORK_LIVE / FORK_DEPLOYED_HEAD           │
└───────────────────────────┬────────────────────────────────┘
                            ▼
        ┌───────────────────┼───────────────────────┐
        ▼                   ▼                       ▼
   [PASS]              [FAIL/gagal]            [MENTOK alat]
        │                   │                       │
        ▼                   ▼                       ▼
  kandidat 09         REJECTED_* → 06        07: NEXT_EXPLORE/
  (Fase F mengadili)  (bukti log simulasi     NEXT_MAINNET/
                      WAJIB — PAPER_         TOOL_BLOCKED
                      REFUTATION gate)       (3-step self-heal dulu)
        │
        ▼
┌────────────────────────────────────────────────────────────┐
│ TAHAP E — OFFCHAIN (opsional, DIPICU — bukan dibaca penuh)  │
│ PICU: (1) scope bounty memasukkan offchain                  │
│       (2) anomali on-chain teramati                         │
│       (3) kelas ketiadaan-aksi (keeper diam)                │
│ • repo publik → bedah JALUR anomali saja                    │
│ • repo privat → rekonstruksi blackbox dari event            │
│ • temuan diajukan atas MANIFESTASI on-chain                 │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│ TAHAP F — VERDICT (hakim akhir)                             │
│ • 11 Pernyataan Wajib + severity rubric (OWASP/Immunefi)    │
│ • rekonsiliasi deployment: LIVE_MATCH vs HEAD-only          │
│   (deploy_parity + dispatch parity)                         │
│ • pemisahan wadah:                                         │
│   09 = VALID_ELIGIBLE (live, dampak nyata)                  │
│   08 = valid-tak-eligible (HEAD-only/LOW/ADMIN)             │
│   07 = belum tuntas (target 0)                              │
│   06 = gugur permanen (wajib bukti log)                     │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│ LAPORAN AKHIR + LOOP BALIK                                 │
│ Gate penutup:                                              │
│  □ PAPER_REFUTATION (06 berisiko wajib log)                │
│  □ LAZY_BAILOUT (07 wajib PERCOBAAN)                       │
│  □ coverage 100% + 00b sinkron                             │
│  □ merge_audit.py (staging/hash/entri)                     │
│ Loop balik:                                                │
│  → Do-Not-Reopen List (STATE.md)                           │
│  → pelajaran run → PATCH MODUL terkait (1 blok,            │
│    core tidak disentuh)                                    │
└────────────────────────────────────────────────────────────┘
```

## Guardrail samping (berlaku di SEMUA gate)

- **Low tidak boleh dibuang diam-diam**: tiap gate mencatat Low yang terlihat;
  spesies: A→stuck-funds, B→config-brick, C→griefing/drain-laten, D→DoS minor.
- **Checkpoint write-ahead**: pindah tahap/item = update STATE.md DULU.
- **Framing laporan**: tanpa sebutan escape-hatch governance (kondisi sekarang saja).

## Loop umpan balik antar-tahap

```
B (path) menemukan pot baru bernilai → kembali ke A (census ulang node tersebut)
C (flow) menemukan jahitan asinkron mencurigakan → kembali ke B (perdalam peta)
D (simulasi) [PASS] tapi saldo blok kebetulan 0 → tahan di 08 + RECHECK_REQUIRED
E (offchain) anomali baru → lead baru masuk C/D dengan provenance [LAPIS:OFFCHAIN]
F menolak laporan (PAPER_REFUTATION) → kembali ke D untuk lead terkait
```
