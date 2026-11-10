# VERDICT — Hukum Acara Pengadilan Bukti (theadvers v2.0 + Preferensi Rule 06/07/08/09)

Dokumen ini adalah hukum acara pada **STAGE-E** (pengadilan bukti) dan **STAGE-F** (disclosure). Tidak ada satu pun kandidat dari `05-raw-leads.md` yang boleh naik ke `09-confirmed-findings.md` tanpa melewati seluruh pernyataan di bawah ini.

> **Prinsip pemisah tunggal:** setiap wadah menuntut **jenis bukti yang berbeda**. `06` menuntut bukti *kegagalan*, `07` menuntut bukti *usaha*, `08` menuntut bukti *mekanisme*, `09` menuntut *ketiganya sekaligus*. Wadah yang diisi tanpa bukti jenisnya = laporan DITOLAK.

---

## 1. Syarat Mutlak Tiga Titik Bukti Segitiga (`L-PROVE`)

Sebuah kandidat hanya sah disebut Temuan Terkonfirmasi (`09-confirmed-findings.md`) apabila ketiga titik berikut terbukti secara simultan dan tertulis tanpa pemotongan logika:

1. Titik 1 — Jejak Kode Eksak & Keterjangkauan Jalur (`L-PATH` Verified):
   - Menyebutkan titik masuk publik/eksternal/instruksi/handler yang nyata (Path/File.ext:Lxx-Lyy).
   - Menunjukkan urutan pemanggilan hingga titik mutasi state/aset/valuasi (Path/File.ext:Lxx-Lyy).
   - Membuktikan bahwa seluruh penjaga kode (require, assert, ensure, *signer/account/capability check*, modifier) di sepanjang jalur tersebut benar-benar dapat dilewati oleh pelaku sesuai model ancaman.

2. Titik 2 — Bukti Eksekusi Konkret atau Jejak Matematika Eksak (`L-PROVE` Verified):
   - Standar Utama (Eksekusi Nyata): Hasil uji yang dapat direproduksi pada *test runner* ekosistem terkait (forge test, cargo test, move test, snforge, pytest, go test, atau harness simulasi), ATAU
   - Standar Setara (Jejak Matematika/State Konkret): Perhitungan angka konkret langkah demi langkah pada setiap baris ekspresi kode (dengan nilai awal, nilai input, hasil pembulatan/pembagian integer, dan nilai akhir yang terukur eksak).
   - Larangan: Narasi spekulatif seperti *"bisa menyebabkan overflow/kerugian"* tanpa angka konkret atau tanpa eksekusi dinyatakan BATAL DEMI HUKUM.

3. Titik 3 — Delta Nilai Terukur & Kerusakan Invariant (`L-VALUE` Verified):
   - Menunjukkan perubahan terukur pada saldo, hak klaim, kolateral, kapasitas nilai (*intended capacity*), atau pembekuan state (State Sebelum vs State Sesudah).
   - Menunjuk minimal satu invariant dari FACTS.md atau path-map.md yang terbukti pecah.

---

## 2. TANGGA BUKTI (wajib dicantumkan pada setiap verdict)

**Proyek ini LIVE DI MAINNET.** Karena itu `FORK_LIVE` adalah **default dan wajib**, bukan pilihan
yang setara dengan yang lain. Proyek yang sejak awal dinyatakan masih testnet/devnet memakai
`FORK_TESTNET` — dan status itu **wajib dicatat di `STATE.md`**, bukan disimpulkan per entri.

| Tingkat | Jenis bukti | Boleh menopang |
| :--- | :--- | :--- |
| **A** | `Mode Uji: FORK_LIVE` — fork state **produksi pada blok terakhir**, `[PASS]`, tanpa cheatcode | hingga `09` **(satu-satunya jalur sah untuk `09` pada proyek mainnet)** |
| **T-ONLY** | `Mode Uji: FORK_TESTNET` — hanya bila proyek memang testnet/devnet (tercatat di `STATE.md`) | `09` sebagai *live-of-record* testnet, dengan label eksplisit |
| **A-HEAD** | `Mode Uji: FORK_DEPLOYED_HEAD` di atas fork mainnet nyata, `[PASS]`, tanpa cheatcode | `08` [`PRE_LIVE_SCOPE`] — **hanya** bila kode HEAD **lebih baru** dari live dan belum aktif; tidak sah untuk `09` pada proyek mainnet |
| **B** | `Mode Uji: LOKAL` dengan kontrak asli (non-EVM, atau rantai tanpa RPC) | `09` (non-EVM kode cocok live) atau `08` (EVM tanpa RPC) |
| **C** | Bukti **struktural** (baca kode + `eth_call`) atau **mock pihak ketiga** | maksimal `07` (dengan `PERCOBAAN:`) atau `06` (salah baca statis) |
| **D** | Asumsi/hitungan kertas **tanpa eksekusi test** | **TIDAK SAH** untuk `09`/`08`/`07`, dan TIDAK SAH untuk `06` pada kelas `POC_FAILS`/`NEGATIVE_EV`/`DUST` |

### 2b. Fork wajib menyebut blok, dan blok itu harus blok live

`Mode Uji: FORK_LIVE` **wajib** menyertakan `chain`, `block`, dan `RPC`. Entri tanpa `block:` tidak
sah — "fork live" tanpa nomor blok tidak dapat direproduksi dan tidak membuktikan state apa pun.

```
Mode Uji: FORK_LIVE (chain: ethereum, block: 21345678, RPC: https://...)
```

Fork pada blok lama **bukan** `FORK_LIVE` — itu snapshot historis dan wajib ditandai `LOKAL` +
`DEPLOYMENT_MATCH: UNVERIFIED (<alasan>)`.

### 2c. `VERSION_RELATION` — relasi versi diukur, bukan diasumsikan

Hindari asumsi "repo HEAD selalu lebih baru" atau "live selalu lebih baru". Ukur sekali per
kontrak sebelum menggulirkan batch pertama di STAGE-D:

| Nilai | Cara membuktikan | Kode pembanding yang dipakai |
| :--- | :--- | :--- |
| `LIVE_IS_DEPLOYED_COMMIT` | `cast code <impl aktif>` cocok dengan build commit tertentu | repo (commit itu) |
| `LIVE_NEWER_THAN_HEAD` | impl aktif memuat kode yang **tidak ada** di HEAD (upgrade sudah jalan, repo tertinggal) | **bytecode live**, bukan repo |
| `HEAD_NEWER_THAN_LIVE` | HEAD memuat perubahan yang belum aktif di proxy live | keduanya: live untuk `09`, HEAD untuk `08` |
| `LIVE_UNVERIFIED` | bytecode live tidak bisa dipastikan berasal dari commit mana | tidak boleh `09` |

**`LIVE_IDENTITY` wajib terukur:** alamat **impl aktif** dibaca dari slot EIP-1967 proxy
(`0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`), bukan dari nama berkas repo.
Implementation yang **terpasang tapi belum di-`upgradeTo`** bukan live — ia milik `08`, bukan `09`.

`DEPLOYMENT_MATCH` dan `TANGGA_BUKTI` wajib dicantumkan **bahkan pada verdict yang gugur** — tanpa keduanya, vonis dianggap belum sah dan entri wajib dikembalikan ke penulisnya.

---

### 2d. Rekonsiliasi Deployment — `deploy_parity.py` (WAJIB, satu perintah per kontrak)

`VERSION_RELATION` di §2c **tidak boleh ditebak**. Ia dihasilkan oleh alat, bukan penilaian manual:

```bash
python3 tools/deploy_parity.py --paradigm <evm|solana|sui|aptos|ton|generic> \
  --chain <mainnet|testnet|local> --addr <ALAMAT> --rpc <RPC> \
  --entrypoints "<signature yang diserang PoC>" --repo <path repo> \
  --out <audit-dir>/notes/deploy-parity-<ID>.json
```

**Aturan keras:** `bytecode identik` **DILARANG** dijadikan syarat. Build Foundry jarang
reproducible (metadata hash, optimizer, versi solc) dan setiap repo punya siklus rilis berbeda.
Yang diuji adalah **keberadaan & perilaku entrypoint yang diserang PoC**, bukan hash berkas.

#### Empat Siklus Deployment (gerbang awal)

| Siklus | Kondisi terukur | Konsekuensi |
| :--- | :--- | :--- |
| `P1_PRE_DEPLOY` | `cast code` = `0x` / akun tidak ada | PoC tetap wajib (`FORK_DEPLOYED_HEAD`/`LOKAL`) → `08` |
| `P2_TESTNET_ONLY` | kode ada, chainId = testnet/devnet | `08` `TESTNET_ONLY` — **kecuali** INTEL §0 menyatakan proyek memang testnet/devnet |
| `P3_LIVE_PARTIAL` | kode ada di mainnet, sebagian entrypoint tidak terbukti | lanjut ke verdict entrypoint |
| `P4_LIVE_FULL` | semua entrypoint PoC terbukti ada & berperilaku | kandidat `09` |

#### Empat Pra-Syarat sebelum menyimpulkan apa pun

1. **Proxy** — baca slot EIP-1967 impl (`0x360894a1…2bbc`), beacon (`0xa3f0ad74…3d50`), admin (`0xb5312768…6103`). Bila proxy, yang dianalisis **implementation**, bukan proxy.
2. **Fallback-router** — bila probe mengembalikan `MissingFallbackHandler` (selector `0x08c63e27`), entrypoint hidup di **handler**, bukan di kontrak titik serang → `ENTRYPOINT_RELOCATED`.
3. **Library / delegatecall** — bila entrypoint hidup di callee, uji pada **callee** dan catat di artefak.
4. **Multi-kontrak (router → hub → allocator)** — untuk attack-chain, **setiap** kontrak yang menjadi entrypoint diperiksa terpisah; satu artefak JSON per kontrak.

#### Tujuh Verdict Entrypoint (jangan disatukan)

| Verdict | Arti | Wadah |
| :--- | :--- | :--- |
| `LIVE_MATCH` | entrypoint PoC terbukti ada & berperilaku sama di objek live | **`09`** |
| `HEAD_ONLY_PROVEN` | siklus `P1`, atau live tak tersedia | **`08`** `PRE_LIVE_SCOPE` |
| `TESTNET_ONLY` | siklus `P2` pada proyek mainnet | **`08`** `TESTNET_ONLY` |
| `ENTRYPOINT_RELOCATED` | entrypoint ada di handler/callee, bukan kontrak titik serang | **`08`** + catatan rute |
| `REGRESSION_FIXED` | live lulus **dan** PoC di HEAD gagal (**dua** log eksekusi) | **`06`** `REJECTED_BY_DESIGN` |
| `ENV_ERROR` / `UNVERIFIABLE` | RPC gagal 2×, rate-limit, revert tak terklasifikasi | **`07`** `TOOL_BLOCKED` |
| `IDENTITY_ONLY` | rantai belum dikenal / entrypoint tak terbaca otomatis | **`07`** `NEXT_EXPLORE` |

#### Anti-false-negative pada deteksi deployment

- **`ENV_ERROR` tidak pernah menjadi bukti ketiadaan.** Rate-limit, 403 RPC, timeout, `revert 0x`
  → `07` `TOOL_BLOCKED`, **bukan** `HEAD_ONLY_PROVEN` dan **bukan** `06`.
- **`ENTRYPOINT_ABSENT` hanya sah** bila seluruh metode gagal **dan** ada bukti tambahan
  (`git log -S` tidak menemukan fungsi tersebut). Untuk paradigma `generic`, `ABSENT` **dilarang
  mutlak** — gunakan `IDENTITY_ONLY`.
- **`REGRESSION_FIXED` wajib dua log**: live `[PASS]` + HEAD `[FAIL]`. Tanpa itu → `ENV_ERROR`.
- **`DEPLOYMENT_MATCH` ≠ `LIVE_MATCH` padahal alamat live tersedia** → **DILARANG** langsung
  menggeser ke `08`. Catat `RECHECK_REQUIRED` + `commit_ref` + `nearest_tag`, kembalikan ke
  STAGE-D untuk **satu putaran PoC kedua** yang menembak objek live (via Factory resmi, atau
  `vm.etch` bytecode live yang **dicatat sebagai deviasi**). Baru bila tetap tidak cocok → `08`.

#### `DEPLOYMENT_REPORT` wajib di setiap entri `06`/`08`/`09`

```
DEPLOYMENT_REPORT : <audit-dir>/notes/deploy-parity-<ID>.json
SIKLUS            : P1_PRE_DEPLOY | P2_TESTNET_ONLY | P3_LIVE_PARTIAL | P4_LIVE_FULL
VERDICT_ENTRYPOINT: LIVE_MATCH | HEAD_ONLY_PROVEN | TESTNET_ONLY | ENTRYPOINT_RELOCATED | REGRESSION_FIXED | ENV_ERROR | IDENTITY_ONLY
```

Entri tanpa `DEPLOYMENT_REPORT` yang menunjuk artefak nyata **tidak sah** — penentuan wadah
`06`/`08`/`09` tidak boleh berdiri di atas asumsi.

> **Batas wewenang:** rekonsiliasi adalah pekerjaan **STAGE-E/F**, bukan STAGE-D. STAGE-D
> **dilarang** menghentikan penulisan PoC hanya karena kontrak belum live atau versi repo berbeda.

---

## 3. Matriks Keputusan Wadah Kanonik (04 / 06 / 07 / 08 / 09)

| Kondisi Hasil Pemeriksaan | Wadah Tujuan Wajib | Kapan Dipindahkan | Bukti Minimum |
| :--- | :--- | :--- | :--- |
| Jalur/ide sudah tertahan oleh penjaga kode (require/assert/constraint/fakta FACTS.md) saat penyempitan awal. | `04-code-guarded.md` | STAGE-C1 atau STAGE-C2 | Kutip Path/File.ext:Lxx-Lyy dan ekspresi penjaga yang membuat jalur tersebut aman. |
| Kandidat masuk meja operasi 05-raw-leads.md, tetapi saat diuji di STAGE-D PoC gagal, hitungan membuktikan tidak ada dampak, atau tertahan penjaga kode yang baru terlihat saat eksekusi. | `06-refuted-invalid.md` | STAGE-E | Lihat §4 (kelas + `BUKTI_SIMULASI` atau KS-1..KS-4). |
| Logika kode mendukung serangan, tetapi **pengujian belum tuntas** karena batas tooling/komputasi/data eksternal. | `07-needs-next-step.md` | STAGE-E | Lihat §5 (`Disposition:` + `PERCOBAAN:` berisi log nyata). |
| Mekanisme **sudah terbukti** (`[PASS]`), tetapi tidak eligible: pre-live, admin-only, atau Low. | `08-valid-not-eligible.md` | STAGE-E | Lihat §6 (`LOW_CLASS` + `POC_STATUS: PASS` + dampak terukur). |
| Ketiga titik Bukti Segitiga terbukti utuh, live, dan bahaya finansial nyata. | `09-confirmed-findings.md` | STAGE-E (Bukti) & STAGE-F (Laporan Siap-Kirim) | Lihat §7 + §8 + §9. |

---

## 4. Aturan Masuk `06-refuted-invalid.md` (Gerbang Anti-Paper-Refutation)

**Kelas yang sah di `06`:** `REJECTED_POC_FAILS`, `REJECTED_NEGATIVE_EV`, `REJECTED_DUST`, `REJECTED_NO_VICTIM`, `REJECTED_FANTASY_MOCK`, `REJECTED_CHEATCODE`, `REJECTED_PRIVILEGED_FANTASY`, `REJECTED_GENESIS_MIRAGE`, `REJECTED_NON_LIVE_INIT`, `REJECTED_BY_DESIGN`, `REJECTED_MISMATCH`, `REJECTED_UNPROVEN_DEPLOYMENT`.

**Kewajiban bukti:**

- Kelas `REJECTED_POC_FAILS` / `REJECTED_NEGATIVE_EV` / `REJECTED_DUST` **WAJIB** memuat blok `BUKTI_SIMULASI:` berisi perintah test yang benar-benar dijalankan beserta log terminalnya, termasuk bukti *Victim Seeding* dan minimal **1× Fuzzing** (`testFuzz_` / `proptest` / `halmos`) pada Strike 3.
- Pelanggaran → **`PAPER_REFUTATION_DETECTED`** → laporan DITOLAK, entri dikembalikan ke STAGE-D.

**Empat Kemustahilan Statis Sempit (satu-satunya yang boleh gugur tanpa kode test):**

| # | Kelas | Syarat (semua harus terpenuhi) |
| :--- | :--- | :--- |
| **KS-1** | `REJECTED_MISMATCH` | Salah baca statis literal: kutipan `File:Baris` yang diklaim terbukti **tidak** berisi kode yang diklaim, dibuktikan dengan kutipan ulang rentang utuh |
| **KS-2** | `REJECTED_BY_DESIGN` | Perilaku terdokumentasi sebagai disengaja dan dapat dikutip: NatSpec, `DESIGN.md`, README resmi, atau proposal governance yang menyebut perilaku itu persis |
| **KS-3** | `REJECTED_GENESIS_MIRAGE` | Prasyarat hanya terpenuhi pada kondisi genesis (`totalSupply == 0` atau pool tunggal terkunci) **dan** tidak ada jalur mengosongkannya, dibuktikan dengan pembacaan utuh |
| **KS-4** | `REJECTED_NON_LIVE_INIT` | Fungsi target tidak dapat dijangkau karena slot inisialisasi terkunci permanen, dibuktikan dari bytecode/storage live — bukan asumsi |

Kelas `REJECTED_NO_VICTIM`, `REJECTED_FANTASY_MOCK`, `REJECTED_CHEATCODE`, `REJECTED_PRIVILEGED_FANTASY`, dan `REJECTED_UNPROVEN_DEPLOYMENT` **BUKAN** kemustahilan statis: semuanya bergantung pada angka/keberadaan korban dan wajib melampirkan bukti eksekusi.

---

## 5. Aturan Masuk `07-needs-next-step.md` (Gerbang Anti-Lazy-Bailout)

`07` **bukan** tempat menyimpan lead yang belum dikerjakan. Ia hanya sah untuk lead yang **sudah diusahakan sampai batas tooling**, dan usaha itu harus terbaca dari berkasnya.

**Field wajib per entri** — `Disposition:` dan `PERCOBAAN:` **tidak boleh dihilangkan**:

```text
ID                 : <id>
VERDICT            : NEEDS_NEXT_STEP
Disposition        : NEXT_EXPLORE | NEXT_MAINNET | TOOL_BLOCKED | ENV_ERROR   <- tepat satu
TARGET_FILE        : 07-needs-next-step.md
ALASAN             : <1-2 kalimat: mengapa belum tuntas>
BUKTI              : <ringkasan mekanisme & titik terhenti, Path/File.ext:Lxx-Lyy>
TANGGA_BUKTI       : B | C   (A / A-HEAD yang sudah PASS tidak sah di sini — wajib 09 atau 08)
DEPLOYMENT_MATCH   : LIVE_MATCH | HEAD-only (PROVEN_ON_REPO_HEAD) | UNVERIFIED (<sumber yang gagal>)
PERCOBAAN:
  $ <perintah nyata yang dijalankan>
  <log keluaran nyata>
LANGKAH BERIKUTNYA : <aksi konkret untuk menuntaskan pengujian>
```

**`PERCOBAAN:` bukan rencana.** Isinya perintah yang **sudah dijalankan** beserta keluarannya. Menulis `$ forge test ...` tanpa output = pelanggaran.

**Bukti wajib per `Disposition`:**

| Label | Bukti yang wajib ada di entri | Tanpa bukti |
| :--- | :--- | :--- |
| `NEXT_EXPLORE` | log fuzzing (Tier 2) / differential (Tier 3) / halmos-symbolic (Tier 5) yang berjalan sampai **timeout komputasi** | `LAZY_BAILOUT_DETECTED` |
| `TOOL_BLOCKED` | log terminal **ketiga** anak tangga: (1) flag/remapping/toolchain, (2) standalone interface-only harness, (3) fallback RPC | `LAZY_BAILOUT_DETECTED` |
| `NEXT_MAINNET` | bukti rantai tanpa RPC/explorer publik; bila RPC tersedia, `07` **tidak sah** — jalankan `cast call`/`cast storage` sendiri | `LAZY_BAILOUT_DETECTED` |
| `ENV_ERROR` | minimal **dua** percobaan endpoint berbeda beserta log kegagalannya | `LAZY_BAILOUT_DETECTED` |

**Larangan pelarian wadah.** Memindahkan lead dari `07` ke `08` hanya sah bila mekanismenya sudah terbukti secara mekanis (PoC jalan tanpa curang + dampak kuantitatif terukur). Lead yang belum teruji lalu dilabeli Low = melanggar aturan ini: `07` menuntut bukti usaha, `08` menuntut bukti mekanisme — **tidak ada wadah yang boleh menampung lead yang belum dikerjakan**.

**Label basi tidak sah.** Judul entri sudah dipindah ke wadah lain tetapi label lama masih tertinggal → dihitung sebagai pelanggaran.

**Target akhir `07` = 0 entri.** Setiap sisa wajib dipertahankan dengan log komputasi, bukan kalimat.

---

## 6. Aturan Masuk `08-valid-not-eligible.md`

Kata **"nyata dan terbukti" bersifat harfiah**: mekanisme wajib sudah `[PASS]` di simulator. `08` **bukan** tempat menyimpan lead yang belum diuji (lead belum teruji wajib di `07` dengan `PERCOBAAN:`).

**Tiga kelas sah:**

- **`PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)`** — dampak finansial nyata (Critical/High/Medium), PoC `[PASS]` pada `FORK_DEPLOYED_HEAD`/`LOKAL`, tetapi kontrak/fitur belum live, berbeda dari bytecode produksi, atau belum terdaftar di halaman alamat bounty.
- **`ADMIN_ONLY`** — bug mekanis nyata pada fungsi khusus admin, tanpa jalur eksploitasi eksternal.
- **`LOW_NUISANCE`** — DoS tanpa kehilangan dana, kerugian kecil terbatas, atau griefing non-finansial (Severity Low / S4).

**Field wajib:** `LOW_CLASS`, `POC_STATUS: PASS`, `DEPLOYMENT_MATCH`, dampak kuantitatif terukur, dan kode PoC utuh untuk kelas `PRE_LIVE_SCOPE`.

**Severity ditentukan IMPACT, bukan siklus deployment.** Menurunkan severity karena alasan "masih HEAD-only" / "hanya testnet" adalah pelanggaran; yang berubah hanya wadah (`09` vs `08`).

---

## 7. Aturan Masuk `09-confirmed-findings.md`

Wajib memenuhi **seluruh** syarat berikut:

1. **Sepuluh Pernyataan Keras** (§8) — enam mutlak + empat berbatas.
2. **Pernyataan Integritas #11** (§9) — kejujuran usaha & cakupan laporan.
3. Field metadata terukur: `TANGGA_BUKTI: A | B`, `DEPLOYMENT_MATCH: LIVE_MATCH`, `LIVE_IDENTITY` **terukur** (bukan disimpulkan), `POC_STATUS: PASS`, `VERSION_RELATION` (§2c).
4. **`Mode Uji: FORK_LIVE` wajib** — proyek ini live di mainnet, jadi `FORK_DEPLOYED_HEAD` dan `LOKAL` **tidak sah** untuk `09`. `FORK_TESTNET` hanya sah bila `STATE.md` menyatakan proyek testnet/devnet.
5. Fork wajib menyebut `chain`, `block`, `RPC` (§2b). Entri tanpa `block:` ditolak.
6. `TANGGA_BUKTI: A-HEAD` **DILARANG** di `09` — itu milik `08`.
7. `CYCLE: P1_PRE_DEPLOY` / `P2_TESTNET_ONLY` **DILARANG** di `09`.

Wadah kasus `cases/<FIND-ID>/` wajib lengkap: `chat.md`, `laporan-teknis.md` (9 bagian), `poc.md` (5 bagian + Kontrol Positif).

---

## 8. Sepuluh Pernyataan Keras (Eligibility & Mekanisme)

### A. Enam Pernyataan Ketat Mutlak (melanggar = `06-refuted-invalid.md`)

**1. Keaslian Entitas & Aset (No Fantasy Mock)** — seluruh token, LP token, share/receipt token, dan kontrak yang berinteraksi di dalam PoC memakai kode asli repositori, atau tiruan yang perilakunya 100% identik dengan aset produksi (tidak mengarang Fee-on-Transfer/Rebase/USDT-quirk pada token standar, dan tidak menyuntikkan kontrak jahat ke parameter yang dikunci Factory/Whitelist). → `REJECTED_FANTASY_MOCK`

**2. Kesetiaan Deployment & Pemisahan Live vs Repo-HEAD (Deployment Fidelity)** — untuk masuk ke `09-confirmed-findings.md`, kode yang diserang wajib terbukti eksis dan aktif pada deployment produksi (`LIVE_MATCH`). Apabila PoC eksploitasi berhasil (`[PASS]`) pada kode repositori (`FORK_DEPLOYED_HEAD` / `LOKAL`) namun kontrak/fitur masih `HEAD-only` (belum di-deploy atau berbeda dari bytecode produksi aktif), temuan tersebut **WAJIB disimpan secara utuh** di `08-valid-not-eligible.md` dengan kelas `PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)` — bukan dipaksakan ke `09` dan bukan diparkir di `07`. → `REJECTED_UNPROVEN_DEPLOYMENT`

**3. Keadaan Likuiditas Nyata (No Empty-Pool Mirage)** — eksploitasi terbukti berhasil pada keadaan TVL dan likuiditas nyata di produksi, bukan mengandalkan `totalSupply == 0` / First Depositor Attack pada pool yang sudah live atau sudah mencetak dead shares saat deploy — kecuali PoC membuktikan penyerang mampu membuat pool resmi baru secara permissionless atau menguras TVL ke nol lebih dulu. → `REJECTED_GENESIS_MIRAGE`

**4. Korban Rasional & Dampak Eksternal (Rational Victim)** — serangan merugikan dana protokol atau pengguna lain yang bertindak rasional (memakai parameter perlindungan normal), bukan mengharuskan korban mematikan pelindungnya sendiri (`minAmountOut = 0`, `deadline = max`, mengirim token via `ERC20.transfer` di luar jalur deposit), dan bukan hanya merusak pool terisolasi milik penyerang. **Catatan:** apabila **PENYERANG** yang sengaja mendonasikan token via `ERC20.transfer` / donasi langsung ke kontrak untuk memanipulasi akuntansi `balanceOf(address(this))`, menggagalkan guard kesamaan saldo, atau menyela alur *push-then-sync*, itu adalah **serangan valid** dan dilarang divonis `REJECTED_NO_VICTIM`. → `REJECTED_NO_VICTIM`

**5. Kelayakan Ekonomi Serangan (Positive-EV / Cost Asymmetry)** — serangan menghasilkan keuntungan finansial bersih (Profit > gas + modal hangus) **atau** sanggup membekukan dana protokol/korban bernilai besar secara permanen dengan biaya sangat murah. → `REJECTED_NEGATIVE_EV`

**6. Presisi Bukti Kode & Bukan Desain Sengaja (Code & Design Match)** — rentang `File:Baris` yang dikutip adalah akar masalah sesungguhnya, dan perilakunya tidak didokumentasikan sebagai mekanisme yang disengaja protokol. Komentar NatSpec/README yang sekadar mendeskripsikan rumus atau alur fungsi **bukan** bukti bahwa dampak eksploitasinya disengaja. → `REJECTED_MISMATCH` (baris tidak cocok) / `REJECTED_BY_DESIGN` (disengaja)

### B. Empat Pernyataan Berbatas (Bounded Threshold — memisahkan 06 / 07 / 08 / 09)

**7. Status Live Produksi & Siklus Hidup Inisialisasi (Scope & Lifecycle)** — kontrak dan cabang fitur yang diserang termasuk cakupan aktif di produksi, dan tidak menyerang `initialize()` sekali-pakai yang sudah terkunci rapat tanpa jalur re-inisialisasi.
- Menyerang `initialize()` yang sudah dieksekusi dan dikunci di produksi (implementation juga sudah `_disableInitializers()`) → **[KETAT]** `REJECTED_NON_LIVE_INIT` → `06-refuted-invalid.md`
- Mekanisme eksploitasi nyata dan PoC `[PASS]` tetapi kontrak/fitur masih pre-live (`HEAD-only`), paused, atau belum masuk daftar alamat bounty → **`VALID_NOT_ELIGIBLE [PRE_LIVE_SCOPE / HEAD_ONLY_PROVEN]`** → `08-valid-not-eligible.md` (wajib menyertakan kode PoC utuh & log `[PASS]`).

**8. Kemurnian Aktor Eksternal (Unprivileged External Path)** — seluruh langkah eksploitasi dapat dijalankan penyerang tak berizin dari awal hingga akhir, tanpa mengandalkan tindakan jahat/bodoh Admin/Owner/DAO/Keeper, dan bukan bug khusus fungsi admin tanpa jalur eksternal.
- Mengasumsikan admin memasukkan konfigurasi bunuh diri di luar batas normal, atau mengasumsikan penyedia Oracle eksternal meretas dirinya sendiri → **[KETAT]** `REJECTED_PRIVILEGED_FANTASY` → `06`. *(Bila oracle mengembalikan data jujur namun kontrak salah mengonversi desimal, salah membaca `updatedAt`, atau salah menghitung LTV, itu **bug kontrak yang valid** → `09`.)*
- Bug mekanis nyata pada fungsi **khusus admin** tanpa jalur eksploitasi eksternal → **`VALID_NOT_ELIGIBLE [ADMIN_ONLY]`** → `08` (bukan `06` — ini Low, bukan gugur).

**9. Kejujuran Sandbox & Bukti Fork Produksi (Sandbox & Fork Integrity)** — PoC dapat direproduksi dan menghasilkan `[PASS]` pada `FORK_LIVE`, `FORK_DEPLOYED_HEAD`, atau `LOKAL` (non-EVM / rantai tanpa RPC) tanpa memalsukan storage internal, dan mematuhi fisika gas/mempool rantai target.
- `vm.store`, `vm.etch` state protokol, `vm.prank(admin/pool)`, `deal` ke protokol, atau revert di state nyata → **[KETAT]** `REJECTED_CHEATCODE` / `REJECTED_POC_FAILS` → `06`
- Logika kode + PoC lokal jujur tetapi belum dapat dijalankan pada state live → bukti `C`, maksimal `07` (dengan `PERCOBAAN:`).

**10. Kalibrasi Bahaya Finansial & Severity (Financial Danger Floor)** — dampak akhir PoC membuktikan bahaya finansial nyata: pencurian dana pokok/yield signifikan, insolvensi protokol, pembekuan aset permanen/jangka panjang, atau sabotase fungsi keselamatan berbatas waktu (`repay`/`liquidate`) yang memicu penyitaan paksa/kredit macet — bukan sekadar "Annoying but not financially dangerous". Severity yang diklaim sesuai 100% dengan bukti kuantitatif pada log PoC.
- Hanya pembulatan debu (1 wei–beberapa sen) yang tak dapat dilipatgandakan dan tidak mengunci dana → **[KETAT]** `REJECTED_DUST` → `06`
- Mekanisme nyata tetapi dampak Low: DoS tanpa kehilangan dana (sekali waktu, tidak dapat diulang murah), kerugian kecil terbatas, atau griefing non-finansial → **`VALID_NOT_ELIGIBLE [LOW_NUISANCE]`** → `08`
- Klaim HIGH/MEDIUM tetapi bukti hanya kelas Low atau admin-only → **turunkan ke LOW (S4)** dan pindahkan `09` → `08`.

**Severity ditentukan Impact, BUKAN siklus deployment.** `SEVERITY` dan `ELIGIBILITY` adalah dua sumbu ortogonal dan dilarang dikalikan. Temuan yang terbukti mencuri dana tanpa syarat **tetap `CRITICAL`** meski ditempatkan di `08` dengan `PRE_LIVE_SCOPE`.

---

## 9. Pernyataan Integritas Laporan (#11)

**11. Kejujuran Usaha & Cakupan (Anti-Lazy-Bailout)** — setiap entri di `07-needs-next-step.md` memuat blok `PERCOBAAN:` berisi perintah yang benar-benar dijalankan beserta keluarannya, dan setiap `Disposition` didukung bukti sesuai tabel §5. Setiap klaim `TOOL_BLOCKED` melampirkan log ketiga usaha Tangga Self-Healing; `NEXT_EXPLORE` melampirkan log fuzzer/halmos yang mentok timeout; `NEXT_MAINNET` melampirkan bukti RPC/explorer tidak tersedia.

→ Pelanggaran: **`LAZY_BAILOUT_DETECTED`** → laporan DITOLAK, `07` dikembalikan ke STAGE-D. Temuan yang sudah ada tetap disimpan dan DILARANG dihapus.

**11b. Larangan Pelarian Wadah** — memindahkan lead dari `07` ke `08` (`LOW_NUISANCE`/`ADMIN_ONLY`/`PRE_LIVE_SCOPE`) hanya sah bila mekanismenya sudah terbukti secara mekanis (PoC jalan tanpa curang + dampak kuantitatif terukur). Lead yang belum teruji lalu dilabeli Low = melanggar aturan ini. Bila ragu antara `07` dan `08`, lead itu masih `07` dan wajib `PERCOBAAN:`.

**11c. Atestasi Hampa Tidak Dihitung** — klaim "sudah diperiksa, bersih" tanpa `File:Baris` konkret per fungsi yang diperiksa, atau yang bersandar hanya pada volume (`forge build`/`cargo test` PASS, jumlah berkas), **dibatalkan** dan dikembalikan ke status belum diperiksa.

**11d. Gerbang Cakupan (`AUDIT_INCOMPLETE_COVERAGE_BIAS`)** — setiap berkas Tier-1/Tier-2 wajib berjejak di `04`/`05`/`06`/`07`/`08`/`09` atau teratestasi bersitasi. Wilayah yang ditutup dengan jejak kosong → laporan DITOLAK, dikembalikan ke STAGE-A/B/C. Temuan yang sudah ada tetap disimpan, DILARANG dihapus.

**11e. Larangan Penolakan Kertas (`PAPER_REFUTATION_DETECTED`)** — entri `06` berkelas `REJECTED_POC_FAILS`/`REJECTED_NEGATIVE_EV`/`REJECTED_DUST` tanpa log eksekusi test + Strike 3 Fuzz, dan di luar KS-1..KS-4 → laporan DITOLAK, dikembalikan ke STAGE-D.

**Hubungan ketiganya:** anti-false-negative melarang menyimpulkan *"aman"* dari data kosong; #11 melarang menyimpulkan *"belum bisa diuji"* tanpa percobaan; #11e melarang menyimpulkan *"gugur"* tanpa eksekusi. Ketiganya menolak kesimpulan yang lebih murah daripada pekerjaannya.

---

## 10. Aturan Anti-False-Negative (wajib dipatuhi)

1. **Kegagalan query ≠ ketiadaan data.** `status: 0` dari explorer, timeout RPC, atau `eth_getLogs` terbatas rentang **bukan** bukti data tidak ada. Wajib diulang lewat sumber lain (RPC lain, endpoint arsip, explorer lain) sebelum menyimpulkan.
2. **Perilaku off-chain tidak otomatis "tidak dapat diuji".** Sebelum menulis "butuh repo privat", rekonstruksi perilaku dari event on-chain (`RoleGranted`, `RootBundleExecuted`, `FilledRelay`, dan event sejenis pada kontrak target).
3. **Oracle eksistensi murah lebih dulu.** Untuk ID sekuensial (`depositId`, nonce, `rootBundleId`), `numberOfDeposits()` atau hitung log memberi batas eksistensi tanpa memindai seluruh history.
4. **Decode calldata produksi** untuk menguji batas kepercayaan (parameter committed vs submitter-supplied) sebelum menyimpulkan jalur terbuka atau tertutup.

---

## 11. Checklist Penolakan Otomatis (Anti-Halusinasi & Anti-Kompresi)

Sebelum memindahkan kandidat ke 09-confirmed-findings.md, pastikan seluruh jawaban di bawah ini adalah YA:

- [ ] Apakah seluruh berkas dan fungsi yang dikutip benar-benar ada di kode sumber dalam *scope* (bukan hasil tebakan nama fungsi)?
- [ ] Apakah nomor baris (Path/File.ext:Lxx-Lyy) telah diperiksa ulang langsung terhadap berkas sumber asli?
- [ ] Apakah bukti bebas dari token kompresi terlarang (..., dll., dst., etc., and so on, rest of logic, rest of code)?
- [ ] Apakah pelaku serangan tidak membutuhkan hak istimewa (*admin/owner/governance*) yang di luar model ancaman?
- [ ] Apakah biaya/prasyarat serangan realistis dibanding dampak kerusakan atau pencurian nilai yang dihasilkan?
- [ ] Apakah `LIVE_IDENTITY` terukur dari artefak deployment, bukan disimpulkan dari nama kontrak?
- [ ] Apakah `POC_STATUS: PASS` disertai log eksekusi nyata, bukan rekonstruksi dari ingatan?
- [ ] Apakah setiap lead yang keluar dari `05-raw-leads.md` tercatat di tepat satu wadah `06`/`07`/`08`/`09`?
