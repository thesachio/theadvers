# AGENTS.md — KONSTITUSI WORKFLOW (Segitiga + Offchain)

**Konstitusi Operasional Keras.** Mengikat Parent Orchestrator maupun seluruh Subagent
(`delegate_task`). Bila bertentangan dengan berkas lain, berkas ini menang.

- **Workspace root (CWD):** root repo audit ini
- **Proyek target:** `<path/ke/target>` (di-pin di `target/PIN.md`)
- **Hakim akhir:** `templates/VERDICT.md`
- **Identitas & sikap:** `SOUL.md`

---

## 0. LANGKAH −1 — PRE-FLIGHT RESUME CHECK (WAJIB PALING PERTAMA)

Mengalahkan seluruh aturan lain. Jangan menyentuh Tahap A sebelum ini selesai.

### 1. Cek `audit/STATE.md`
- **BELUM ADA** → mulai Tahap A0, dan **segera buat `audit/STATE.md`**. Audit tanpa
  STATE.md dilarang melewati Tahap A.
- **SUDAH ADA** → **MODE RESUME**. **DILARANG mengulang dari Tahap A.** Baca STATE.md dan
  lanjutkan dari `CURRENT_ACTIVE_ITEM`.

### 2. Booting hemat-konteks (mode resume)
- **A** — Baca **HANYA** `audit/STATE.md` lebih dulu.
- **B** — Lihat `CURRENT_ACTIVE_ITEM` dan `Working Memory Scratchpad`.
- **C** — Buka **file audit** relevan (`audit/05-raw-leads.md` bila di Tahap C,
  `audit/notes/money-ledger.md` bila di Tahap A) **hanya pada baris item aktif**.
  **DILARANG memuat satu file audit penuh.**
- **D** — **DILARANG membaca ulang kode** dari item di `Do-Not-Reopen List`, dan
  **DILARANG menguji ulang** lead di `06`/`08`/`09` yang terkunci.

> ⚠️ **BATAS OBJEK — JANGAN DITAFSIRKAN SENDIRI.**
> Hemat-konteks **HANYA untuk `audit/*.md`**. **KODE SUMBER TARGET TIDAK TERMASUK.**
> - Kode **WAJIB dibaca UTUH** dari `function` sampai `}` penyeimbang sebelum menulis lead
>   atau PoC. Gunakan `read_file` ber-`offset`/`limit` bila fungsi > 60 baris.
> - **`grep`/`sed`/`head`/`tail` HANYA untuk menemukan lokasi.** DILARANG dipakai
>   menyimpulkan isi fungsi atau membuktikan klaim negatif.
> - **Pengecualian:** larangan baca-ulang gugur bila item di `Do-Not-Reopen List` tidak
>   mencatat rentang baca (`File:awal-akhir` + jumlah baris). Tanpa rentang, item dianggap
>   **belum selesai** dan pembacaan utuh **WAJIB**.
>
> Alasan aturan ini berlawanan arah: hemat-token melindungi **file audit** yang tumbuh
> besar; anti-hemat melindungi **pemahaman kode** yang hancur oleh potongan.

### 3. Write-Ahead Checkpoint
**DILARANG** berpindah item sebelum memperbarui `audit/STATE.md`:
1. `CURRENT_ACTIVE_ITEM` → item berikutnya,
2. `Gate Meter` → status gate yang terlewati,
3. `Do-Not-Reopen List` → item yang baru gugur/terkunci.

Checkpoint ditulis **sebelum** pekerjaan berikutnya dimulai, bukan sesudahnya.

---

## 1. Eksekusi, Proteksi Target, Disiplin Memori

1. **Mode eksekusi**
   - **Mode A (sekuensial):** jalankan A→F di agen utama untuk repo kecil–menengah.
   - **Mode B (orchestrated):** `delegate_task` dengan `max_concurrent_children: 1`,
     sekuensial, agar konteks tetap ringan.
2. **Worker tunggal wajib:** `FOUNDRY_JOBS=1`, `CARGO_BUILD_JOBS=1`, `RAYON_NUM_THREADS=1`.
   Build penuh di mesin terbatas OOM — selalu bangun path spesifik.
3. **Local fork:** boleh dijalankan otomatis dengan endpoint publik dari `rpc-env.sh`
   (memuat `.env.rpc`; cek `RPC-STATUS.md` bila ada). Kegagalan RPC **bukan** bukti ketiadaan.
4. **Larangan mutlak:** DILARANG menyiarkan transaksi keluar (`--broadcast`, `cast send`),
   DILARANG mengedit kontrak target (read-only 100%), DILARANG membuat `AGENTS.md` di dalam
   folder proyek target, DILARANG memanggil `skill_manage` atau `memory` saat audit berjalan.
5. **Lokasi artefak:** semua hasil di `audit/` (bukan `.audit/`).

---

## 1.3 PROTOKOL ANTI-TRUNCATE & METODE WRITE

Berlaku **global untuk seluruh tahap** dan **setiap Subagent**. Aturan ini diangkat ke
konstitusi karena Subagent hanya memuat skill fasenya sendiri dan tidak akan melihatnya
dari sana.

### 1.3.1 Hukum Atomisitas — `open("w")` DILARANG

- **DILARANG KERAS** `open(path,"w")` (Python), `>` (shell), dan `sed -i` untuk **seluruh**
  `audit/*.md`, termasuk `STATE.md`, `04`–`09`, dan `notes/`.
- **Alasan:** `open(path,"w")` memotong file ke **0 byte saat dibuka**, sebelum satu byte
  ditulis. Bila penulisan gagal di tengah (disk penuh, proses mati), isi asli **hilang permanen**.
- **Mutasi sah:** native `write_file`, `patch`, `append` (via tool), atau skrip dengan pola
  **`.tmp` → `flush` → `fsync` → `os.replace()`**.
- **`>>` shell juga dilarang** pada file audit: tidak atomik dan tidak terlindungi lock.

### 1.3.2 Backup write-ahead
Backup **SEBELUM** mutasi. Backup yang dibuat setelah kegagalan menyimpan kekosongan.
Verifikasi pasca-tulis: ukuran ≠ 0 **dan** heading wajib masih ada.

### 1.3.3 Tabel metode write per karakteristik file

**DILARANG memakai "append selalu" sebagai resep tunggal.** File yang diubah berulang
akan punya status basi bila hanya di-append.

| Karakteristik | File | Metode wajib | DILARANG |
|---|---|---|---|
| Tulis sekali | `INTEL.md`, `target/PIN.md` | `write_file` awal; tambahan → `append` | tulis ulang penuh |
| Generate massal | `notes/money-ledger.md`, `notes/path-map.md` | script + verifikasi `grep -n` | baca penuh |
| Append-murni | `06`, `08`, `09`, `RADAR` | `append` | edit entri setelah ditulis |
| Append lalu ubah status | `04`, `05`, `07` | entri baru → `append`; status → `patch` | append saja |
| Edit tabel/baris | `STATE`, `04` tabel gate | `patch` baris | tulis ulang penuh |
| Staging Subagent | `notes/staging-<tahap>-<item>.md` | `write_file` / `atomic_write` | menulis ke `04`–`09` |

**Aturan pemilihan:** metode dengan token terendah **yang tetap benar**.

### 1.3.4 Satu penulis per file
Subagent **DILARANG** menulis ke `audit/04`–`09`. Mereka menulis entri lengkap ke
`audit/notes/staging-<tahap>-<item>.md`; **Parent** yang menggabungkan (lihat §4).
Ringkasan ≤16 baris tidak dapat membawa muatan 120–160 baris, dan
`max_concurrent_children` adalah konfigurasi yang bisa berubah, bukan jaminan.

---

## 1.4 INTEGRITAS BUKTI — DILARANG MENULIS BUKTI DARI INGATAN

**Hukum:** blok `BUKTI_SIMULASI:` dan `PERCOBAAN:` di `06`/`07`/`08`/`09` **WAJIB** ditempel
dari keluaran yang benar-benar dijalankan. Menyusunnya dari narasi atau ingatan =
**`FABRICATED_EVIDENCE`** = laporan **DITOLAK**.

**Mengapa terpisah dari gerbang lain:** gerbang otomatis hanya memeriksa *ada-tidaknya*
baris `$ ...` atau kata `BUKTI_SIMULASI`. Semuanya **PASS** meski isinya palsu.

**Verifikasi wajib sebelum menutup Tahap F:**

```bash
# 1. Nama test di 06/07/08/09 harus ADA di lab atau arsip
forge test --list | grep -oE 'test[A-Za-z0-9_]+' | sort -u > /tmp/real.txt
cat audit-lab-archive/*.sol 2>/dev/null \
  | grep -hoE 'function (test[A-Za-z0-9_]+)' | sed 's/function //' >> /tmp/real.txt
sort -u /tmp/real.txt -o /tmp/real.txt
# ekstrak test_* dari 06/07/08/09; sisa yang tidak cocok = FABRICATED_EVIDENCE
```

```bash
# 2. Nomor File:Baris wajib dicek ulang, bukan dari ingatan
# 3. Setiap "Perintah yang dijalankan:" harus punya keluarannya, bukan hanya perintahnya
```

**Label sah:** "terverifikasi" hanya bila ada kutipan kode + log eksekusi. Tanpa keduanya,
label jujur adalah **"indikasi"**.

---

## 2. Arsitektur File Murni di `audit/`

Satu berkas = satu domain murni. Hemat token dan bebas risiko tertimpa.

- **`STATE.md`** — kursor checkpoint. `Active Phase` (TAHAP A–F), `CURRENT_ACTIVE_ITEM`,
  `Gate Meter`, `Guardrail Low`, `Working Memory Scratchpad` (maks 10 baris),
  `Do-Not-Reopen List`. **Maks 50 baris.** Skema: `templates/STATE.md`.
- **`INTEL.md`** — Tahap A0: identitas proyek, overview, link UI, repo + commit,
  aturan bounty, laporan audit terdahulu, kanal off-chain. **Maks 40 baris.**
- **`notes/money-ledger.md`** — **Tahap A**, artefak hidup. Tiap baris wajib dari query
  nyata. **Probe via PROXY**, bukan impl.
- **`notes/path-map.md`** — **Tahap B**, artefak hidup. Node = kontrak, edge = aliran dana.
  `EV = max(balance_now, throughput_path)`. Jahitan `ASYNC` ditandai.
- **`04-code-guarded.md`** — murni hipotesis yang dihentikan **Guard Statis/Struktural**
  yang terbukti `TERSANGKAL` (tidak tembus 5 Jalur Permissionless). **DILARANG** memuat
  guard dinamis/matematis, atau guard statis yang `TEMBUS`.
- **`05-raw-leads.md`** — antrean aktif. Tiap entri **WAJIB** tiga tag ortogonal:
  `[LAPIS: VALUE|PATH|FLOW]` (asal lead) + `[CLASS-A|B|C]` (topologi entitas → paket metode)
  + `[AF-xx]` (bentuk serangan), ditambah `File:Baris` berupa **rentang**.
  Lihat `CLASSIFICATION.md`. Semua anomali mutasi state, patch-scar, view-vs-write, dan
  seluruh guard dinamis masuk sini.
- **`06-refuted-invalid.md`** — gugur permanen. `REJECTED_POC_FAILS`/`NEGATIVE_EV`/`DUST`
  **WAJIB** `BUKTI_SIMULASI:` (gerbang #11e).
- **`07-needs-next-step.md`** — belum tuntas (`NEXT_EXPLORE`/`NEXT_MAINNET`/`TOOL_BLOCKED`).
  Wajib `Disposition:` + `PERCOBAAN:` nyata. **Target akhir = 0 entri.**
- **`08-valid-not-eligible.md`** — **eksklusif Tahap F.** `PRE_LIVE_SCOPE`,
  `ADMIN_ONLY`, `LOW_NUISANCE`. Subagent Tahap D **DILARANG** menulisnya.
- **`09-confirmed-findings.md`** — `VALID_ELIGIBLE` live, PoC `[PASS]`, tanpa cheatcode.
- **`FACTS.md`** — falsifier, dibuka **setelah** hipotesis buta lahir. Tujuh komponen per
  domain. **DILARANG** memuat hipotesis dan status deployment.
- **`RADAR.md`** — sinyal lintas-domain, append-only, dua lapis (Observasi + Kejadian).

---

## 2b. Ketahanan Konteks & Auto-Resume

1. **Cold start / compaction:** instruksi implisit yang berlaku mutlak adalah
   *"baca `audit/STATE.md` dan lanjutkan dari kursor terakhir"*. DILARANG memulai dari
   Tahap A bila STATE.md sudah ada.
2. **Larangan baca ulang:** item di `Do-Not-Reopen List` terkunci permanen. Membukanya
   hanya sah bila ada **bukti baru material** yang tercatat di `STATE.md`.
3. **Sinkronisasi atomik:** tidak boleh pindah item tanpa update STATE.md lebih dulu.
4. **Batas ukuran:** STATE.md maks 50 baris, scratchpad maks 10 baris. Temuan final pindah
   ke `05`; STATE.md menyimpan **posisi**, bukan hasil.

---

## 3. Corong Penyaringan (Simulation-First)

1. **Tahap A–B (VALUE & PATH).** Census nilai live, lalu peta aliran. Kontrak
   **zero-balance tapi dilalui aliran** wajib tetap diburu (kelas transient-holder).
2. **Tahap C (FLOW).** Bedah sink dengan `M-001..M-010` + POV sebagai **generator**
   ("POV mana yang muat di uang ini?"), bukan filter pasca-baca. Pisahkan guard statis
   vs dinamis secara tegas.
3. **Tahap D (Simulasi).** **No Code, No Reject.** Dual-mode fork + **Victim Seeding**.
   **Buta cakupan administratif:** subagent DILARANG menyentuh `08` atau menggugurkan lead
   karena HEAD-only/pre-live.
4. **Tahap E (Offchain).** Hanya bila terpicu anomali atau scope bounty mencakupnya.
5. **Tahap F (Verdict).** `templates/VERDICT.md`, 11 Pernyataan, rekonsiliasi deployment.

---

## 3b. Tiga Hukum Anti-Menyerah (mengikat Parent & Subagent)

1. **3-Stage Escalation Breaker.** DILARANG menggugurkan hipotesis
   (`REJECTED_POC_FAILS`/`NEGATIVE_EV`/`DUST`) dari 1–2 percobaan manual. Setelah
   **Strike 1** (manual + Victim Seeding) dan **Strike 2** (perbaikan urutan + amplifikasi)
   gagal, **WAJIB** **Strike 3**: satu tes fuzz (`testFuzz_`/`proptest`/`halmos`).
   **Kegagalan alat bukan strike.**
2. **Tangga Self-Healing Tooling** sebelum `TOOL_BLOCKED`: (a) flag/toolchain →
   (b) harness minimal / interface-only → (c) fallback RPC + chunking. Log ketiganya wajib
   dilampirkan di `07`.
3. **Kerjakan Sekarang.** DILARANG memarkir di `07` pekerjaan yang bisa selesai sesi ini,
   dan DILARANG membuang ke `06` tanpa log simulasi nyata.

---

## 4. Protokol Delegasi (`delegate_task`)

Setiap panggilan **WAJIB** menyertakan di `context`:

1. **Path absolut** proyek target
2. **Paradigma rantai & core invariants** (dari `INTEL.md` / `path-map.md`)
3. **Path berkas audit** yang relevan (`STATE.md`, `05`, `notes/*`)
4. **Instruksi memanggil skill fase** (bila skill tersedia) atau membaca `methodology/` +
   `references/` yang relevan
5. **Protokol Staging** (§4 di bawah)
6. **Sinyal RADAR** — hasil `grep -n -B1 -A6 "<berkas-lingkup>" audit/RADAR.md`
   (kosongkan bila tidak ada)
7. **Model mekanisme** — kutip **utuh** blok domain terkait dari `audit/FACTS.md`
   (temukan lewat `grep -n "<NamaBerkas>" audit/FACTS.md`, ≈12 baris)

Tanpa butir 7, subagent menalar tanpa model proyek dan ketajaman kembali ke nol.

- Subagent menulis entri **lengkap siap-tempel** ke `audit/notes/staging-<tahap>-<item>.md`
  (format final: kolom wajib, `File:Baris` rentang, `[LAPIS]`, `[AF-xx]`, Delta State,
  blok `PERCOBAAN:`/`BUKTI_SIMULASI:` bila relevan).
- **HUKUM SATU JALUR.** Setiap jenis usulan punya **tepat satu** file perolehan:

| Usulan | Subagent menulis | Parent menulis ke | Batas |
|---|---|---|---|
| Entri `04`/`05`/`06`/`07`/`09` | `notes/staging-<tahap>-<item>.md` | wadah masing-masing | format final siap-tempel |
| **`M-FACT`** | blok `## USULAN` di staging yang sama | `audit/FACTS.md` (`patch`) | **maks 2**/unit |
| **`R-CAND`** | `notes/radar-<item>.md` (terpisah, append) | `audit/RADAR.md` (`append`) | **maks 2**/unit |

- **DILARANG** menaruh muatan `M-FACT`/`R-CAND` di manifes balasan, dan DILARANG menulisnya
  di dua tempat. Bila muncul ganda, jalur kedua diabaikan (drift).
- Subagent mengembalikan **manifes ≤16 baris**: `STAGING: <path> | 04: <n> | 05: <n>` +
  1 baris verdict per entri + `USULAN: <n> M-FACT | <n> R-CAND | RADAR-FILE: <path>`.
  Bila kosong: `USULAN: 0 M-FACT | 0 R-CAND | RADAR-FILE: -`.
- Parent menggabungkan dengan `append`/`patch` sesuai §1.3.3, lalu **menghapus staging**
  setelah memverifikasi `grep -c '^## \[' <file>` terhadap manifes.
- **WAJIB sebelum menghapus staging:** catat baris di `audit/notes/MERGE-LOG.tsv`
  (append-only, TSV): `timestamp  phase  item  staging  sha256  n04  n05  n06  n07  n09  status`.
  `sha256` = hash staging **saat di-merge**. Menghapus staging sebelum log ditulis =
  kehilangan bukti permanen.
- **Pencocokan wajib:** `python3 tools/merge_audit.py --audit-dir audit` sebelum menutup
  tahap. Mendeteksi `STAGING YATIM`, `HASH BERUBAH`, `ENTRI HILANG`, `ENTRI EKSTRA`,
  `MERGE GANDA`. Exit 1 = wajib diperbaiki.
- **Penamaan:** staging `notes/staging-<TAHAP>-<ITEM>.md` (mis. `staging-C-L-004.md`);
  backup `notes/backups/<YYYYMMDD-HHMMSS>-<nama-asli>` (**DILARANG** menaruh backup
  langsung di `notes/`).

---

## 5. Tangga Bukti & Anti-False-Negative (rujuk `templates/VERDICT.md`)

1. **Tangga bukti** wajib dicantumkan di setiap verdict:
   - **`A`** — `Mode Uji: FORK_LIVE` terhadap bytecode produksi, `[PASS]`, tanpa cheatcode → `09`
   - **`A-HEAD`** — `FORK_DEPLOYED_HEAD` di atas fork mainnet nyata, `[PASS]`, tanpa cheatcode
     → `09` bila `LIVE_MATCH`, atau `08` [`PRE_LIVE_SCOPE`] bila belum live
   - **`B`** — `LOKAL` dengan kontrak asli (non-EVM / tanpa RPC) → `09` (live) atau `08`
   - **`C`** — bukti struktural / mock pihak ketiga → maksimal `07` atau `06`
   - **`D`** — hitungan kertas tanpa eksekusi → **TIDAK SAH**
2. **Rekonsiliasi deployment (eksklusif Tahap F):** `tools/deploy_parity.py`. Yang diuji
   adalah **keberadaan & perilaku entrypoint** yang diserang PoC, **bukan** hash bytecode
   identik. Menolak temuan karena ukuran/sha berbeda adalah `REJECTED_MISMATCH` yang salah.
3. **Kegagalan query bukan bukti ketiadaan.** `status: 0` explorer, `revert 0x`,
   timeout RPC, `eth_getLogs` terbatas → ulangi lewat sumber lain / `cast code`.
4. **Perilaku off-chain diuji black-box lebih dulu** (rekonstruksi event on-chain) sebelum
   menyatakan "butuh repo privat".
5. **Bridge/precompile:** mock pihak ketiga yang mengarang payload mustahil hanya menopang
   bukti `C`. Merelay payload yang terbukti dapat dibentuk permissionless dari Chain A via
   `vm.prank(officialEndpoint)` ke Chain B di atas local fork adalah bukti mekanis sah → `09`.

---

## 6. Pemeriksa & Alat

```bash
python3 tools/verify_segitiga.py --audit-dir audit    # G1-G10
python3 tools/verify07.py audit/07-needs-next-step.md # LAZY_BAILOUT gate
python3 tools/merge_audit.py --audit-dir audit        # integritas staging/merge
python3 tools/deploy_parity.py --paradigm <p> ...     # rekonsiliasi deployment
```

**Yang diperiksa `verify_segitiga.py`:**

| Gate | Memeriksa |
|---|---|
| G1 | tiap lead `05` punya `[LAPIS]` dan `[AF-xx]` |
| G2 | `File:Baris` berupa **rentang** (`awal-akhir`), bukan satu baris |
| G3 | entri `06` berkategori keras punya `BUKTI_SIMULASI` **dengan keluaran nyata** |
| G4 | entri `07` punya `PERCOBAAN` dengan keluaran nyata |
| G5 | entri `08`/`09` punya `BUKTI_SIMULASI` nyata |
| G6 | `STATE.md` ≤50 baris; scratchpad ≤10 baris |
| G7 | tidak ada `audit/*.md` berukuran 0 byte |
| G8 | tag `[AF-xx]` ada di `methodology/mod-attack-forms.md` |
| G9 | tiap lead punya `[CLASS-A|B|C]` (menentukan paket metode wajib) |
| G10 | tidak ada **istilah warisan** (`Fase N`, `Putaran N`, `unit S-n`, rujukan `00b`/`03`) di `audit/*.md` |

**Aturan alat:** setiap pemeriksa wajib diuji **dua arah** — PASS pada kondisi bersih,
dan **FAIL** pada pelanggaran yang disuntikkan. Pemeriksa yang tidak pernah menggigit =
pemeriksa yang tidak berguna, dan alarm palsunya membuat alarm asli diabaikan.
