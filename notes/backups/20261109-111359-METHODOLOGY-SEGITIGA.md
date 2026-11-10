# METHODOLOGY-SEGITIGA — Universal Web3 Audit Workflow (v1.0, 2026-11-07)

**Status**: DRAF MENGIKAT untuk run berikutnya. `AGENTS.md` (konstitusi) tetap hukum tertinggi;
dokumen ini mengoperasionalkan **ALUR perburuan**. Mekanisme lama (M-001..M-010, POV, 5-Jalur,
3-Stage, TANGGA_BUKTI, VERDICT 11, atomic-write) **TIDAK disalin — hanya direferensikan** (Peta Warisan §4).

## 0. Tujuan & Prinsip

- **Goal**: temukan kerentanan berdampak ekonomi — ke **penyedia** (protokol/LP/operator) **dan**
  **pengguna** — dan WAJIB menangkap **Low** (griefing, DoS, kerusakan ekonomi minor). Low dengan
  pemicu permissionless atau kerugian terukur **DILARANG dibuang diam-diam** (guardrail §5).
- **Urutan**: UANG dulu (L-VALUE) → JALUR kedua (L-PATH) → KODE ketiga (L-FLOW) → SIMULASI
  (10 bentuk serangan) → OFFCHAIN (opsional, dipicu anomali) → VERDICT.
- **Modular**: menambah bentuk serangan / domain / cartridge = **append satu blok** di modul
  terkait; core TIDAK perlu diubah. Kontrak ekstensi tiap modul tertulis di §3.

## 1. Alur Utama (6 Tahap + Gate)

```
A. L-VALUE   sensus nilai live (saldo, konfigurasi, role)  → EV ledger
   GATE-A    tiap kontrak bernilai > ambang WAJIB masuk B/C; keluarga "no-deploy/no-config"
             dibunuh di sini dengan 1 query — bukan dengan lab
B. L-PATH    peta siklus aliran dana (per domain cartridge) → seam list + EV per jahitan
   GATE-B    tiap jahitan punya EV = max(balance_now, throughput_path); kontrak zero-balance
             TAPI di jalur aliran tetap diburu (kelas MulticallHandler)
C. L-FLOW    bedah sink mutasi pada jahitan terpilih (M-001..M-010 + POV router) → lead `05`
   GATE-C    lead WAJIB punya provenance (lapis asal: VALUE/PATH/FLOW) + tag bentuk serangan AF-xx
D. SIMULASI  10 bentuk serangan (mod-attack-forms.md) + 3-Stage + dual-mode fork +
             Victim Seeding + kontrol positif → wadah 06/07/08/09 (warisan)
   GATE-D    verdict negatif tanpa eksekusi dilarang (No-Code-No-Reject); target akhir 07 = 0
E. OFFCHAIN  (opsional) DIPICU anomali on-chain → bedah repo bot publik → blackbox bila privat
   GATE-E    hanya bila: scope bounty memasukkan off-chain ATAU gejalanya "ketiadaan aksi"
F. VERDICT   11 Pernyataan + rubrik severity + rekonsiliasi deployment
   GATE-F    PAPER_REFUTATION + LAZY_BAILOUT + coverage pot/jahitan (Gerbang Tahap F) — semua PASS
```

**Urutan eksekusi EV-first**: bila anggaran terputus di tahap mana pun, nilai tertinggi sudah
dikerjakan lebih dulu (jam pertama = census seluruh TVL + pot terbesar).

## 2. Tabel Routing — situasi → modul

| Situasi | Modul / blok |
|---|---|
| Proyek baru dimulai | `mod-layers.md` (A→C), `mod-domain-cartridges.md` (pilih domain) |
| Ada saldo menetap / treasury | L-VALUE → EV ledger |
| Alur multi-hop / cross-chain | L-PATH → seam list |
| Gejala di fungsi transfer/index akrual | L-FLOW + `ref-pov-math.md` (POV-MATH-01) |
| Ada likuidasi/slashing/bad-debt | L-FLOW + `ref-pov-defi.md` (POV-DEFI-01/02) |
| Memilih bentuk serangan | `mod-attack-forms.md` — cocokkan gejala → AF-xx |
| Chain non-EVM | `mod-chain-cartridges.md` + `ref-chain-*.md` |
| Anomali teramati on-chain tapi kode bot privat | `mod-offchain.md` (blackbox) |
| Menulis lead/verdict/staging | `mod-technical-rules.md` (warisan teknis) |

## 3. Peta Modul & Kontrak Ekstensi

| Modul | Isi | Cara menambah (tanpa sentuh file lain) |
|---|---|---|
| `methodology/mod-layers.md` | Detail L-VALUE/L-PATH/L-FLOW + gate + alat | lapis baru = 1 blok |
| `methodology/mod-attack-forms.md` | Registry AF-01..AF-10 (bentuk serangan) | AF-11 = 1 blok di bawah |
| `methodology/mod-domain-cartridges.md` | Bridge/Lending/LP/Staking/NFT/Derivatif: siklus + invarian senyap + POV | domain baru = 1 blok |
| `methodology/mod-chain-cartridges.md` | Tooling per chain (EVM/Solana/Move/TON) + batas RPC | chain baru = 1 blok |
| `methodology/mod-offchain.md` | Doktrin trigger-on-anomaly + blackbox + scope | kebijakan baru = 1 blok |
| `methodology/mod-technical-rules.md` | Warisan teknis: penulisan, wadah, verdict, bukti | aturan baru = 1 blok |

## 4. Peta Warisan (by-reference — single source of truth)

| Sistem lama | Sumber | Dipakai di tahap |
|---|---|---|
| M-001..M-010 | `references/ref-method-registry.md` | C (bedah), D (routing sim) |
| POV router + 8-field | `references/ref-attacker-pov.md` + `references/ref-pov-*.md` | C (generator per pot) |
| 5 Jalur Permissionless | registry M-005 | C (klasifikasi reachability) |
| 3-Stage Escalation + Victim Seeding + dual-mode fork | `templates/VERDICT.md` §Tangga Bukti + `references/ref-test-evm-advanced.md` | D |
| TANGGA_BUKTI A/B/C/D + No-Code-No-Reject | konstitusi AGENTS.md + VERDICT.md | D, F |
| Wadah 04-09 + 11 Pernyataan | VERDICT.md | D, F |
| Atomic-write, staging, 1-penulis, anti-truncate | AGENTS.md §1.3-1.4, §4 | semua tahap (penulisan) |
| CLASS-A/B/C topologi (sumbu lama, tetap mengikat) | `references/ref-method-registry.md` §1 | B (panjang rantai), C — lihat `CLASSIFICATION.md` |
| deploy_parity (sudah dipatch PUSH3/SUB) + probe-via-proxy | `tools/deploy_parity.py` + catatan ledger | A, F |

## 5. Guardrail Low & Checkpoint

- **Guardrail Low**: tiap gate A-F wajib mencatat Low yang terlihat (griefing/DoS/damage minor) —
  bila digugurkan, alasan tertulis; bila hidup, masuk `05`/`08` sesuai aturan verdict.
  Spesies Low per lapis: VALUE→stuck-funds, PATH→config-brick, FLOW→griefing/drain-laten.
- **Checkpoint**: `STATE.md` menunjuk tahap + item aktif; pindah tahap = write-ahead checkpoint.
- **Framing laporan**: TIDAK menyebut escape-hatch governance; argumen dipusatkan pada kondisi
  sekarang (rule-money-first §3b).

## 6. Perubahan dari workflow lama (ringkas)

1. Urutan eksekusi: EV-ledger menggantikan nomor unit `03` (queue tetap jadi INDEKS).
2. FACTS/RADAR: turun jadi falsifier pasca-hipotesis (bukan generator).
3. Filter hipotesis palsu dipindah ke HULU (census 1 query) — bukan di lab (30-60 menit).
4. Lapis L-PATH baru: kontrak zero-balance di jalur dana tetap diburu.
5. Off-chain: dipicu anomali, bukan dibaca menyeluruh.
6. Segitiga menurun mulus: domain tanpa nilai menetap → otomatis merosot jadi code-first murni.
