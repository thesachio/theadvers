# AUTOPILOT-MAPPING — dari Fase 1-4 lama ke Tahap A-F

Template ini menggantikan alur **Fase 0-1-2-3-4** (unit-major) dengan **Tahap A-F**
(EV-major). Dokumen ini memetakan supaya `sc-autopilot` bisa dijalankan dengan metode baru
tanpa kehilangan gerbang integritas mana pun.

## Peta tahap

| Tahap baru | Menggantikan | Artefak wajib | Gate |
|---|---|---|---|
| **A0 Bootstrap** | Fase 0 (Intel) | `audit/INTEL.md`, `target/PIN.md` | PIN terverifikasi `git rev-parse` |
| **A1 Census (L-VALUE)** | Fase 1 sebagian (inventory) | `audit/notes/money-ledger.md` | **GATE-A** |
| **B1 Path map (L-PATH)** | Fase 1 sebagian (`03-attack-surface-queue`) | `audit/notes/path-map.md` | **GATE-B** |
| **C1 Audit (L-FLOW)** | Fase 2 (hunt) | `audit/05-raw-leads.md`, `audit/04-code-guarded.md` | **GATE-C** |
| **D1 PoC (Simulasi)** | Fase 3 (lab) | `06`, `07`, kandidat `09` di staging | **GATE-D** |
| **E1 Offchain** | *(baru — tidak ada di metode lama)* | `audit/notes/offchain-*.md` | **GATE-E** |
| **F1 Verdict** | Fase 4 (hakim) | `08`, `09` final | **GATE-F** |

## Perubahan besar (yang mengubah cara kerja, bukan hanya nama)

### 1. Urutan kerja: EV ledger menggantikan nomor unit
Metode lama mengiterasi `S-01..S-n` mengikuti nomor di `03-attack-surface-queue.md`.
Tahap C mengiterasi **baris `money-ledger.md` terurut EV menurun**. `03` masih berguna
sebagai **indeks**, bukan antrean.

**Konsekuensi operasional:** `delegate_task` di Tahap C menerima *satu pot/jahitan*,
bukan *satu unit S-n*.

### 2. L-PATH: kontrak zero-balance tetap diburu
Metode lama menyaring dengan saldo. Tahap B menambahkan kolom `throughput_path`:
kontrak dengan `balance_now ≈ 0` namun dilalui aliran dana (handler sementara, gateway,
adapter stateless) **wajib** masuk antrean Tahap C.

**Konsekuensi:** `delegate_task` tidak boleh menolak target hanya karena saldonya nol.

### 3. Tahap E (offchain) — kelas yang belum pernah dijalankan
Dipicu anomali on-chain atau oleh scope bounty. Bukti selalu on-chain.

**Konsekuensi:** butuh 3 jenis delegasi baru — (a) bedah repo publik, (b) rekonstruksi
blackbox dari event, (c) analisis kelas "ketiadaan aksi" (keeper seharusnya bertindak,
tidak ada transaksi).

### 4. FACTS/RADAR jadi falsifier, bukan generator
Metode lama membangun `FACTS.md` di awal, lalu hipotesis diturunkan darinya (anchoring).
Metode baru: hipotesis lahir dari kode + POV, **lalu** `FACTS`/`RADAR` dibuka untuk
menguji.

**Konsekuensi:** `FACTS.md` tidak diisi secara proaktif. Ia diisi hanya saat sebuah
hipotesis memerlukan klarifikasi mekanisme.

### 5. Provenance & tag wajib
Setiap lead `05` wajib `[LAPIS: VALUE|PATH|FLOW]` + `[AF-xx]`. Ini yang membuat
`tools/verify_segitiga.py` dapat memeriksa bahwa lead lahir dari lapis yang benar.

## Yang DIPERTAHANKAN utuh dari metode lama

Jangan "menyederhanakan" bagian ini — semuanya menutup kegagalan nyata:

- Anti-truncate (`open("w")` dilarang, pola `.tmp → fsync → os.replace`)
- Satu penulis per file + staging + `MERGE-LOG.tsv` + `merge_audit.py`
- 3-Stage Escalation (2 manual + 1 wajib fuzz) sebelum gugur
- Tangga Self-Healing Tooling sebelum `TOOL_BLOCKED`
- No Code, No Reject
- Dual-mode fork + Victim Seeding
- Tangga bukti A / A-HEAD / B / C / D
- Pemisahan murni `04`–`09`
- Buta cakupan administratif di Tahap D (subagent dilarang menyentuh `08`)

## Perintah pemeriksa per gate

```bash
# GATE-C (setiap kali selesai satu pot)
python3 tools/verify_segitiga.py --audit-dir audit

# GATE-D (sebelum menutup Tahap D)
python3 tools/verify07.py audit/07-needs-next-step.md
python3 tools/merge_audit.py --audit-dir audit

# GATE-F (sebelum menutup Tahap F)
python3 tools/verify_segitiga.py --audit-dir audit
python3 tools/deploy_parity.py --paradigm <evm|solana|sui|aptos|ton|generic> ...
```

## Aturan pemetaan untuk `delegate_task` ala autopilot

| Autopilot lama | Tahap baru | Isi context wajib |
|---|---|---|
| Unit `S-n` Fase 2 | **Pot/jahitan** Tahap C | blok `money-ledger` + blok `path-map` + `[LAPIS]` target |
| Lead Fase 3 | **Lead** Tahap D | detail lead dari `05` + `Stage Strike` |
| Hakim Fase 4 | **Tahap F** | seluruh `05`–`09` + `templates/VERDICT.md` |

Butir context (1)–(7) di `AGENTS.md` §4 tetap berlaku tanpa perubahan.
