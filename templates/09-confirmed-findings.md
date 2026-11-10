# 09 — Confirmed Findings (Bounty-Ready / Live Production Only)

> **Penerapan Segitiga & Wadah Kasus (`cases/<ID>/`)**:
> 1. Wadah murni untuk temuan berstatus `VALID_ELIGIBLE` yang lolos **Sepuluh Pernyataan Keras (§8) + Integritas #11 (§9)** di `templates/VERDICT.md`, terbukti lewat eksekusi simulasi PoC tanpa curang (`POC_STATUS: PASS`), membuktikan bahaya finansial nyata (`CRITICAL` / `HIGH` / `MEDIUM`, atau `LOW` dengan pemicu *permissionless*), **DAN** terbukti eksis pada bytecode/kontrak produksi aktif (`DEPLOYMENT_MATCH: LIVE_MATCH`).
> 2. **Gerbang Pemisahan `09` (LIVE) vs `08` (HEAD-ONLY / PRE-LIVE) di STAGE-F**:
>    - **Masuk ke `09` ini**: PoC `[PASS]` pada state produksi nyata (`Mode Uji: FORK_LIVE`, atau `FORK_DEPLOYED_HEAD` yang entrypoint-nya terverifikasi eksis & berperilaku identik pada objek live melalui `deploy_parity.py` -> `LIVE_MATCH`).
>    - **Pindahkan ke `08-valid-not-eligible.md`** (`LOW_CLASS: PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)`): Apabila PoC terbukti `[PASS]` di atas kode repositori (`FORK_DEPLOYED_HEAD` / `LOKAL`), namun pada Rekonsiliasi Langkah 0 STAGE-F terbukti bahwa kontrak/fungsi tersebut belum di-deploy ke mainnet (`HEAD-only` / `P1_PRE_DEPLOY`) atau belum masuk daftar alamat bounty aktif (`[REPO_STAGED]`).
> 3. **Pemisahan Indeks `09` dan Wadah Kasus `cases/<ID>/`**:
>    - Berkas `09-confirmed-findings.md` ini menyimpan **Tabel Indeks** dan **Blok Metadata + Tiga Titik Bukti Segitiga** untuk setiap temuan `VALID_ELIGIBLE`.
>    - Seluruh detail naratif 9-bagian, paket PoC berkontrol positif, dan naskah komunikasi/pengantar disimpan di dalam satu folder per temuan pada **`cases/<ID>/`** yang wajib berisi 3 berkas:
>      1. `cases/<ID>/chat.md` (berbasis `SUBMISSION-EMAIL.md` + ringkasan diskusi/verdict `lead-<id>.md`)
>      2. `cases/<ID>/laporan-teknis.md` (berbasis 9 bagian wajib `TECHNICAL-REPORT.md`)
>      3. `cases/<ID>/poc.md` (berbasis 5 bagian wajib & aturan Kontrol Positif `POC-PACKAGE.md`)

---

## 1. TABEL INDEKS TEMUAN VALID TERKONFIRMASI (`STAGE-E` / `STAGE-F`)

| Finding ID | Asal Lead ID | Region (`R_i`) | Severity (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`) | EV Rank (`P1`–`P5`) | Verbatim Anchor (`Path/File.ext:awal-akhir`) | Modul & Fungsi Terdampak | Plugin Pembuktian (`M-xxx` + `AF-xx`) | Wadah Case (`STAGE-F`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FIND-001` | `LEAD-R1-01` | `R_1` | `HIGH` | `P1` | `[Path/File.ext:L60-L95]` | `[NamaModul.namaFungsi]` | `M-001 + AF-01` | `cases/FIND-001` |

---

## 2. BLOK METADATA WAJIB & REKAM BUKTI PER ENTRI (`09`)

> **Aturan Keras Field Metadata (`VERDICT.md` & `SCHEMA.md`)**:
> - **`LIVE_IDENTITY` wajib TERUKUR, bukan disimpulkan.** Contoh sah: `accountId()` = `...`; `sha256(ProgramData)` = `...` untuk Solana; hash bytecode impl EIP-1967 dari artefak `deploy-parity-<ID>.json`. Tanpa `LIVE_IDENTITY` terukur, `LIVE_MATCH` ditolak.
> - **`TANGGA_BUKTI: A-HEAD` DILARANG di `09`.** `A-HEAD` berarti PoC dijalankan pada kode repo HEAD-only (milik `08`). Kombinasi `A-HEAD` + `LIVE_MATCH` adalah kontradiksi yang ditolak otomatis.
> - **`CYCLE: P1_PRE_DEPLOY` / `P2_TESTNET_ONLY` DILARANG di `09`.**

### `FIND-001` (Eks `LEAD-R1-01`) — `[Judul Satu Baris Tanpa Sensasi & Lokasi]`
- **ID**: `FIND-001`
- **Asal Lead & Provenance**: `LEAD-R1-01 | [LAPIS: VALUE|PATH|FLOW] | [CLASS-A|B|C] | [AF-xx]`
- **Region & EV Rank**: `R_1 | [P1..P5]`
- **SEVERITY**: `[CRITICAL | HIGH | MEDIUM | LOW]` *(dari IMPACT sesuai `templates/SEVERITY-RUBRIC.md`, bukan dari siklus deploy)*
- **Rujukan Severity**: `[Platform + URL atau Matriks Universal (templates/SEVERITY-RUBRIC.md Bagian 4)]`
- **VERDICT**: `VALID_ELIGIBLE`
- **TARGET_FILE**: `09-confirmed-findings.md`
- **TANGGA_BUKTI**: `[A | B]` *(`A-HEAD` dilarang di `09`)*
- **DEPLOYMENT_MATCH**: `LIVE_MATCH`
- **CYCLE**: `[P4_LIVE_FULL | P3_LIVE_PARTIAL]` *(`P1`/`P2` dilarang di `09`)*
- **ELIGIBILITY**: `LIVE_MATCH`
- **LIVE_IDENTITY**: `[Terukur: alamat impl AKTIF dari slot EIP-1967 proxy 0x360894a1...382bbc, atau accountId() / sha256 ProgramData untuk non-EVM — bukan nama berkas repo]`
- **VERSION_RELATION**: `[LIVE_IS_DEPLOYED_COMMIT | LIVE_NEWER_THAN_HEAD | HEAD_NEWER_THAN_LIVE]` *(`LIVE_UNVERIFIED` dilarang di `09`)*
- **DEPLOYMENT_REPORT**: `notes/deploy-parity-<ID>.json` *(artefak `deploy_parity.py`; wajib — `SIKLUS: P4_LIVE_FULL` + `VERDICT_ENTRYPOINT: LIVE_MATCH`)*
- **SIKLUS**: `P4_LIVE_FULL`
- **VERDICT_ENTRYPOINT**: `LIVE_MATCH`
- **POC_STATUS**: `PASS`
- **Mode Uji**: `FORK_LIVE (chain: <...>, block: <...>, RPC: <...>)` *(wajib — proyek mainnet; `FORK_DEPLOYED_HEAD`/`LOKAL` tidak sah di `09`. `FORK_TESTNET` hanya bila STATE.md menyatakan testnet/devnet)*
- **File:Baris**: `[Path/File.ext:Lxx-Lyy]` *(wajib rentang awal-akhir)*
- **Metode / POV**: `[M-xxx / AF-xx / POV-xx]`
- **Invarian Dilanggar**: `[INV-Ri-xx — rumus invarian inti dari FACTS.md / path-map.md]`
- **DAMPAK KUANTITATIF**: `[Profit bersih penyerang / kerugian protokol dalam angka eksak + satuan aset]`
- **Wadah Kasus Lengkap (`STAGE-F`)**: `cases/FIND-001/` (`chat.md`, `laporan-teknis.md`, `poc.md`)
- **Titik 1 — Jejak Kode Eksak (`Exact Code Trace`)**:
  - `[Path/File.ext:Lxx-Lyy — Urutan dari entrypoint publik hingga sink mutasi state yang melewati guard]`
- **Titik 2 — Bukti Simulasi (`BUKTI_SIMULASI`)**:
  - `$ [Perintah eksak yang dijalankan, misal: FOUNDRY_JOBS=1 forge test --match-test test_FIND001 -vvv]`
  - `[Kutipan keluaran nyata yang mencetak saldo sebelum/sesudah dan literal [PASS]]`
- **Titik 3 — Delta Nilai & Invariant yang Pecah (`Value Delta & Broken Invariant`)**:
  - `[State Sebelum vs Sesudah dalam angka eksak; detail lengkap 9-bagian ada di cases/FIND-001/laporan-teknis.md dan kode PoC utuh di cases/FIND-001/poc.md]`
