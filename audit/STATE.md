# AUDIT EXECUTION STATE — <NAMA-PROYEK> (METHODOLOGY-SEGITIGA v1.1)

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Kursor checkpoint — dipakai di **Tahap A–F (semua)**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

- Target: `<org/repo>` @ `<commit>` (lihat `target/PIN.md`)
- Last Updated: `<YYYY-MM-DD>` — `<status>`
- Active Phase: **TAHAP A (L-VALUE)** — bukan Tahap A/B lama
- Active Sub-Stage: `A0_BOOTSTRAP`

## 1. Cursor Position (Titik Lanjut Eksak)
- Last Completed Item: `-` (belum ada)
- CURRENT_ACTIVE_ITEM: `A0_BOOTSTRAP` — isi `audit/INTEL.md` + `target/PIN.md` terverifikasi
- Active Files in Scope: `<isi path nyata, bukan nama generik>`
- Stage Sequence: A (L-VALUE) → B (L-PATH) → C (L-FLOW) → D (SIMULASI) → E (OFFCHAIN, opsional) → F (VERDICT)
- Active Strike Count: `0/3` (kosong sampai Tahap D)
- Cognitive Load: NORMAL | FATIGUE (≥2 kegagalan mekanis berturut → checkpoint & sesi baru)

## 2. Gate Meter (GATE-A s/d GATE-F — wajib PASS sebelum naik tahap)
| Gate | Syarat | Status |
|---|---|---|
| GATE-A | census nilai live tiap kontrak bernilai > ambang + konfigurasi live | PENDING |
| GATE-B | tiap jahitan punya EV = max(balance_now, throughput_path); zero-balance di jalur tetap diburu | PENDING |
| GATE-C | tiap lead `05` bawa `[LAPIS: VALUE\|PATH\|FLOW]` + `[AF-xx]` + kutip rentang baris utuh | PENDING |
| GATE-D | tidak ada verdict negatif tanpa eksekusi; 3-Stage; target `07` = 0 | PENDING |
| GATE-E | offchain hanya bila terpicu anomali / scope bounty; bukti on-chain ada | N/A (belum dipicu) |
| GATE-F | 11 Pernyataan + PAPER_REFUTATION + LAZY_BAILOUT + coverage PASS | PENDING |

## 3. Guardrail Low (wajib diisi tiap gate — TIDAK boleh kosong tanpa alasan tertulis)
- GATE-A: `-` | GATE-B: `-` | GATE-C: `-` | GATE-D: `-` | GATE-E: `-` | GATE-F: `-`

## 4. Working Memory Scratchpad (maks 10 baris)
- `-`

## 5. Do-Not-Reopen List
- Kosong. Bila ini audit ulang, lihat `audit/METHODOLOGY-DELTA.md` §Konsekuensi.

## 6. Aturan Pengisian
- Baca `methodology/METHODOLOGY-SEGITIGA.md` §1 untuk urutan A-F dan gate masing-masing.
- `notes/money-ledger.md` (Tahap A) dan `notes/path-map.md` (Tahap B) adalah artefak hidup — wajib dibuat sebelum GATE-A/B ditutup.
- Write-ahead: geser `CURRENT_ACTIVE_ITEM` SEBELUM mulai item berikutnya.
- Maks 50 baris. Temuan final ke `05`, bukan di sini.
