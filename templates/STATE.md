# AUDIT EXECUTION STATE (CHECKPOINT — SEGITIGA + OFFCHAIN)

- Target Repo: `<org/repo>` @ `<commit>` (lihat `target/PIN.md`)
- Last Updated: `<timestamp atau step>`
- Active Phase: `A_LVALUE` | `B_LPATH` | `C_LFLOW` | `D_SIMULASI` | `E_OFFCHAIN` | `F_VERDICT`
- Active Sub-Stage: `A0_BOOTSTRAP` | `A1_CENSUS` | `B1_PATHMAP` | `C1_AUDIT` | `D1_POC` | `E1_BLACKBOX` | `F1_JUDGE`

## 1. Cursor Position (Titik Lanjut Eksak)
- Last Completed Item: `<item> -> hasil 1 baris`
- CURRENT_ACTIVE_ITEM: `<item aktif — hanya satu>`
- Active Files in Scope: `<BerkasA.sol>, <BerkasB.sol>` (path nyata, bukan nama generik)
- Active Strike Count: `0/3` (2 Manual + 1 Mandatory Fuzz; kosongkan sebelum Tahap D)
- Cognitive Load: NORMAL | FATIGUE (≥2 kegagalan mekanis berturut → WAJIB checkpoint & sesi baru)
- Lead Sequence Basis: EV_DESC (lead EV tertinggi WAJIB dikerjakan paling awal)

## 2. Gate Meter (GATE-A s/d GATE-F — wajib PASS sebelum naik tahap)
| Gate | Syarat | Status |
|---|---|---|
| GATE-A | census nilai live tiap kontrak bernilai + konfigurasi live | PENDING |
| GATE-B | tiap jahitan punya EV = max(balance_now, throughput_path); zero-balance di jalur tetap diburu | PENDING |
| GATE-C | tiap lead `05` bawa `[LAPIS]` + `[AF-xx]` + kutip rentang baris utuh | PENDING |
| GATE-D | tidak ada verdict negatif tanpa eksekusi; 3-Stage; target `07` = 0 | PENDING |
| GATE-E | offchain hanya bila terpicu anomali / scope bounty; bukti on-chain ada | N/A |
| GATE-F | 11 Pernyataan + PAPER_REFUTATION + LAZY_BAILOUT + coverage PASS | PENDING |

## 3. Guardrail Low (wajib diisi tiap gate — kosong hanya boleh dengan alasan tertulis)
- GATE-A: `-` | GATE-B: `-` | GATE-C: `-` | GATE-D: `-` | GATE-E: `-` | GATE-F: `-`

## 4. Working Memory Scratchpad (Maks 10 Baris — Konteks Sementara Item Aktif)
- `<Berkas>.sol:L142 — <observasi konkret yang membuat item ini perlu perhatian khusus>.`

## 5. Do-Not-Reopen List (Sudah Final, Dilarang Dibaca Ulang)
- Completed Items: `-`
- Dead-End Leads (06): `-`
- Verified Leads (08): `-`
- Confirmed (09): `-`

---

## 6. Aturan Pengisian (hapus bagian ini saat disalin ke proyek)

- **Cursor Position** — hanya SATU item aktif. `Active Files in Scope` wajib path nyata.
- **Gate Meter** — status hanya `PENDING`/`PASS`/`FAIL`/`N/A`. `PASS` menuntut bukti, bukan
  pernyataan; bukti tersimpan di `notes/money-ledger.md` (A), `notes/path-map.md` (B),
  `05-raw-leads.md` (C), `06`/`07`/`08`/`09` (D), `notes/offchain-*.md` (E), `templates/VERDICT.md` (F).
- **Guardrail Low** — tiap gate WAJIB mencatat Low yang terlihat (griefing/DoS/kerusakan
  minor). Low permissionless dengan kerugian terukur DILARANG dibuang diam-diam.
  Spesies per tahap: A→stuck-funds, B→config-brick, C→griefing/drain-laten.
- **Working Memory Scratchpad** — maks 10 baris, hanya untuk item aktif. Temuan final pindah
  ke `05-raw-leads.md`, bukan ditinggal di sini.
- **Do-Not-Reopen List** — tulis ID saja beserta kelas vonisnya. Alasannya ada di `06`/`08`/`09`.
- **Write-Ahead Rule** — perbarui file ini SEBELUM memulai item berikutnya.
- **Strike Count** — wajib terisi (`0/3`,`1/3`,`2/3`,`3/3`) selama Tahap D. Lead DILARANG
  dipindah ke `06` sebagai `REJECTED_POC_FAILS`/`NEGATIVE_EV`/`DUST` sebelum `3/3`
  (Strike 1 manual+Victim Seeding, Strike 2 perbaikan urutan+amplifikasi, Strike 3 fuzz)
  beserta log di `BUKTI_SIMULASI:`.
- **Cognitive Load** — isi `FATIGUE` setelah ≥2 kegagalan mekanis berturut-turut. Saat
  `FATIGUE`: DILARANG memulai lead baru; tulis checkpoint lalu lanjut sesi baru.
- **Lead Sequence Basis** — `EV_DESC` wajib. Aktivitas non-penemuan (setup build, remapping,
  debug tooling, RPC) **tidak** boleh menggeser lead ber-EV tinggi ke ekor.
