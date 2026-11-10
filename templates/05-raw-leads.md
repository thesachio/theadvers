# 05-RAW-LEADS — Antrean Kandidat [QUEUED] & Meja Operasi Batch Aktif [ACTIVE] (theadvers v2.0)
> ATURAN BESI KAPASITAS & ROLLING BATCH:
> 1. Bagian 2 (Tabel Antrean `[QUEUED]`): Menampung seluruh kandidat yang lolos saringan kualitas Segitiga pada `STAGE-C2` tanpa batas plafon total. Jangan pernah membuang kandidat valid hanya karena jumlahnya banyak. Urutkan berdasarkan Prioritas EV (`SOUL.md §3`: `P1` s/d `P5`) dan pasangkan dengan M-xxx serta AF-xx.
> 2. Bagian 3 (Blok Meja Operasi `[ACTIVE-BATCH]`): Hanya boleh berisi maksimal 5 kandidat berstatus `[ACTIVE]` dalam satu siklus pembuktian STAGE-D -> STAGE-E.
> 3. Setelah STAGE-E selesai mengadili batch aktif ke wadah 06 / 07 / 08 / 09, jumlah [ACTIVE] wajib kembali menjadi `0`. Jika masih ada [QUEUED] > 0 untuk Wilayah R_i, tarik batch berikutnya (maksimal 5 kandidat) hingga [QUEUED] == 0 dan [ACTIVE] == 0.
> 4. Dilarang menulis token kompresi (..., dll., dst., etc., rest of logic). Wajib cantumkan Path/File.ext:Lxx-Lyy.
> 5. **TARGET OBJEK & DEPLOY_PARITY WAJIB PER LEAD.** Sebelum menulis PoC, setiap kartu `[ACTIVE]` wajib menyatakan objek on-chain yang diserang (`TARGET_OBJEK`) dan membawa artefak `deploy_parity.py`. `MODE_UJI_POC` diturunkan dari `SIKLUS`, bukan dipilih bebas — PoC dibangun pada kondisi yang **relevan** dengan jaringan proyek (`INTEL.md §0`).
>    | `SIKLUS` | `MODE_UJI_POC` sah | Syarat `INTEL.md §0` |
>    | :--- | :--- | :--- |
>    | `P4_LIVE_FULL` | `FORK_LIVE` | `MAINNET` |
>    | `P2_TESTNET_ONLY` | `FORK_TESTNET` | `TESTNET` / `DEVNET` |
>    | `P3_LIVE_PARTIAL` | `FORK_LIVE` | `MAINNET` (sebagian entrypoint belum terbukti) |
>    | `P1_PRE_DEPLOY` | `FORK_DEPLOYED_HEAD` atau `LOKAL` | bebas — tidak ada objek live untuk di-fork |
>    `--gate D` menolak kombinasi yang tidak konsisten dan menolak kartu tanpa artefak yang benar-benar ada di disk.

---

## 1. CATATAN PERBURUAN DUA GELOMBANG PER WILAYAH (STAGE-C1 & STAGE-C2)

### 1.1 Wilayah Aktif R_1 — Observasi Gelombang 1 ([WAVE-1-BLIND])
*Diisi pada STAGE-C1 murni dari pembacaan L-VALUE dan L-PATH tanpa membuka _ROUTER.md atau file plugin.*

- `[WAVE-1-BLIND] [OBS-R1-01]` | Path/File.ext:Lxx-Lyy | NamaModul.namaFungsi | Gejala & Asumsi yang Ditemukan: [Jelaskan ketimpangan state/nilai/kontrol secara eksak] | Sinyal Radar Terkait: [RAD-001 / NONE]

### 1.2 Wilayah Aktif R_1 — Penyilangan Gelombang 2 ([WAVE-2-CROSS])
*Diisi pada STAGE-C2 dengan mengadu observasi C1 terhadap Inversi FACTS.md, Rantai [TOUCHES] di RADAR.md, dan pencocokan gejala di _ROUTER.md.*

- `[WAVE-2-CROSS] [CROSS-R1-01]` | Sumber Pemicu: [Fact ID F-R1-xx / Radar Pair CPAIR-xx / Observasi OBS-R1-xx] | Plugin Cocok dari `_ROUTER.md`: [M-xxx, AF-xx, DOM-xx, POV-xx, CHAIN-xx] | Keputusan Saringan: [LOLOS KE QUEUED sebagai LEAD-R1-01 / GUGUR KE 04-code-guarded.md sebagai GUARD-R1-xx]

---

## 2. TABEL ANTREAN KANDIDAT BERKUALITAS ([QUEUED]) — TANPA PLAFON TOTAL

*Seluruh kandidat yang lolos saringan Segitiga di Wilayah Aktif wajib masuk ke tabel ini dan diurutkan dari EV tertinggi (P1) ke terendah (P5). Saat wilayah ditutup (--close-region), tidak boleh ada lagi baris yang berstatus [QUEUED].*

| Lead ID | Region (R_i) | EV Rank (P1`–`P5) | Verbatim Anchor (Path/File.ext:Lxx-Lyy) | Titik Masuk & Target (NamaModul.namaFungsi) | Ringkasan Mekanisme & Dampak L-VALUE | Assigned Method (M-xxx) | Assigned Attack Form (AF-xx) | Plugin Tambahan (DOM/POV/CHAIN) | Status Antrean ([QUEUED] / [ACTIVE] / [MOVED-TO-06..09]) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LEAD-R1-01 | R_1 | P1 | [Path/File.ext:L60-L95] | [NamaModul.namaFungsi] | [Jelaskan mekanisme eksploitasi dan invariant nilai yang diincar] | M-001 | AF-01 | [DOM-xx / NONE] | [QUEUED] |

---

## 3. BLOK MEJA OPERASI PEMBUKTIAN ([ACTIVE-BATCH]) — MAKSIMAL 5 KANDIDAT [ACTIVE]

- Active Region: R_1
- Current Batch Number: 1
- Current `[ACTIVE]` Leads Count: 0 *(Wajib <= 5 saat STAGE-D, dan wajib 0 setelah dipindahkan ke 06/07/08/09 pada STAGE-E)*

*Salin struktur kartu pembuktian di bawah ini hanya untuk kandidat yang sedang berstatus [ACTIVE] pada batch saat ini (maksimal 5 kartu). Setelah kandidat selesai diadili di STAGE-E, pindahkan seluruh isi kartunya ke wadah tujuan (06 / 07 / 08 / 09) dan kosongkan dari bagian ini.*
### [CONTOH FORMAT KARTU SAAT STAGE-D — KOSONGKAN SETELAH STAGE-E]
- Lead ID & Judul: [LEAD-R1-01 — Judul Kandidat]
- Status Saat Ini: [TEMPLATE-CONTOH — Ganti menjadi [ACTIVE] saat menarik kandidat dari tabel [QUEUED]]
- Region & EV Rank: R_1 | P1
- Assigned Plugins Loaded: M-xxx (references/methods/M-xxx-*.md) + AF-xx (methodology/attack-forms/AF-xx-*.md)
- TARGET_OBJEK: [chain:alamat kontrak/program/module yang diserang lead ini — mis. ethereum:0xAbC…123 / solana:<pubkey>]
- DEPLOY_REPORT: notes/deploy-parity-[LEAD-R1-01].json *(artefak `deploy_parity.py`; wajib ada di disk sebelum --gate D)*
- SIKLUS: [P1_PRE_DEPLOY | P2_TESTNET_ONLY | P3_LIVE_PARTIAL | P4_LIVE_FULL]
- VERDICT_ENTRYPOINT: [LIVE_MATCH | HEAD_ONLY_PROVEN | TESTNET_ONLY | ENTRYPOINT_RELOCATED | ENV_ERROR | IDENTITY_ONLY]
- MODE_UJI_POC: [FORK_LIVE | FORK_TESTNET | FORK_DEPLOYED_HEAD | LOKAL] *(diturunkan dari SIKLUS + INTEL §0, lihat Aturan 5)*
- Fork PoC: [chain, block: <n>, RPC] *(wajib bila MODE_UJI_POC = FORK_LIVE / FORK_TESTNET)*
- Titik 1 — Jejak Kode Eksak (`Exact Code Trace`):
  - Entry Point: [Path/File.ext:Lxx-Lyy — NamaModul.fungsiMasuk]
  - Alur Panggilan & Mutasi: [Path/File.ext:Lxx-Lyy — Urutan perubahan state/saldo dan alasan mengapa penjaga kode berhasil dilewati]
- Titik 2 — Bukti Eksekusi / Jejak Matematika Konkret (`Concrete Execution / Math Proof`):
  - Perintah Uji / Test Runner: [forge test --match-test ... / cargo test ... / move test ... / Jejak Perhitungan Eksak]
  - Jejak Angka / Log Eksekusi: [Tulis angka konkret langkah demi langkah: state awal, nilai input, hasil operasi baris demi baris, state akhir]
- Titik 3 — Delta Nilai & Invariant yang Pecah (`Value Delta & Broken Invariant`):
  - Delta Nilai: [State/Saldo Sebelum -> State/Saldo Sesudah; keuntungan penyerang atau kerugian protokol]
  - Invariant yang Dilanggar: [Rujuk ID Invariant dari FACTS.md / path-map.md, misal INV-R1-01]
- Keputusan Akhir `STAGE-E` (`Verdict`): [Dipindahkan ke 06-refuted-invalid.md / 07-needs-next-step.md / 08-valid-not-eligible.md / 09-confirmed-findings.md]
