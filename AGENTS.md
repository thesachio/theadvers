# AGENTS — Konstitusi Operasional, Bootloader Konteks, & Protokol Eksekusi (theadvers v2.0)

Berkas ini adalah Konstitusi Operasional Tertinggi untuk seluruh agen (baik Orchestrator Utama, Subagent, maupun mesin otonom sc-autopilot). Setiap instruksi di berkas ini bersifat mengikat dan ditegakkan secara mekanis oleh tools/verify_segitiga.py.

---

## 1. HARD BOOTLOADER — Kewajiban Pertama Sebelum Menyentuh Kode Kontrak

Memori percakapan (*chat history*) Anda dapat terkompres sewaktu-waktu, dan berkas metodologi di dalam subfolder tidak otomatis ter-load oleh sistem. Oleh karena itu, dilarang keras menganalisis berkas kode sumber dalam *scope* (`.sol`, `.vy`, `.rs`, `.move`, `.cairo`, `.go`, `.ts`, `.py`, `.circom`, dll.) atau mengubah berkas kerja audit (`04` s/d `09`, `FACTS.md`, `RADAR.md`, `path-map.md`) sebelum menjalankan langkah pemulihan konteks berikut:

1. Baca Identitas Kognitif & Prioritas EV: Pastikan prinsip di SOUL.md (termasuk Hukum 1–7 dan §3 Urutan Prioritas EV) aktif.
2. Jalankan Injeksi Paket Konteks Segar (*JIT Context Re-Hydration*):
   Di awal sesi, di awal setiap tahap (0, A, B, C1, C2, D, E, F), dan setiap kali berganti Batch atau Wilayah, jalankan perintah CLI berikut:

       python3 tools/verify_segitiga.py --context-packet <path-ke-folder-audit>

   Perintah ini membaca STATE.md dari disk dan mencetak langsung ke layar Anda:
   - Posisi kursor aktif (Active Region R_i, Current Stage, Batch Number, Queued/Active Leads Count).
   - Potongan aturan spesifik tahap aktif (@SLICE:STAGE-*) langsung dari methodology/METHODOLOGY-SEGITIGA.md.
   - Daftar kontrak/modul Wilayah R_i yang wajib dibaca ulang.
   - Entri FACTS.md, sinyal RADAR.md ([TOUCHES: ...]), dan indeks _ROUTER.md yang relevan untuk tahap tersebut.
3. Lakukan *Write-Ahead Checkpoint* di `STATE.md`:
   Sebelum memulai pekerjaan tahap baru dan segera sesudah menyelesaikan tahap tersebut, perbarui baris status di STATE.md terlebih dahulu.

---

## 2. Struktur Ruang Kerja Audit (*Canonical Workspace Containers*)

Setiap sesi audit proyek target wajib memiliki direktori kerja terstruktur dengan berkas-berkas kanonik berikut (dibuat dari templates/):
| Berkas / Direktori | Peran Operasional & Aturan Akses |
| :--- | :--- |
| `STATE.md` | Jangkar Memori & Kursor Autopilot. Menyimpan tabel Antrean Wilayah (R_1 .. R_N yang diurutkan menurut EV SOUL.md §3), posisi Wilayah/Tahap/Batch aktif, dan *Write-Ahead Checkpoint*. |
| `FACTS.md` | Bank Fakta Verbatim & Peta Inversi Prasyarat. Berisi aturan kode eksak (Path/File.ext:Lxx-Lyy), skala presisi/desimal, invariant, dan kolom Prerequisite Inversion Hint (cara mematahkan prasyarat di Gelombang 2). |
| `RADAR.md` | Radar Sinyal Lintas-Kontrak/Lintas-Modul. Menyimpan anomali dan efek samping dengan tag wajib [TOUCHES: KontrakAtauModul.variabelAtauFungsi] untuk merakit serangan berantai. |
| `path-map.md` | Tabel Rekonsiliasi 100% Berkas Kode Sumber (Tier 1/2/3) & Peta 3-Edge per Wilayah. Menyimpan pembagian wilayah R_1 .. R_N, kapasitas nilai (Current Balance + Intended Capacity), serta jalur [EDGE-ASSET], [EDGE-VALUATION], dan [EDGE-CONTROL/LATENT]. |
| `04-code-guarded.md` | Wadah Jalur Terjaga Kode (Tahap C). Menyimpan jalur/hipotesis awal di Tahap C (C1/C2) yang setelah diperiksa terbukti sudah dijaga rapat oleh kode (require, assert!, ensure!, modifier, *account constraint*, batas state, atau fakta di FACTS.md), lengkap dengan jangkar baris kode penjaganya. |
| `05-raw-leads.md` | Antrean `[QUEUED]` & Meja Operasi Batch Aktif `[ACTIVE]` (Tahap C -> D -> E). Memiliki dua bagian per Wilayah R_i: (1) Tabel `[QUEUED]` untuk menyimpan semua kandidat kuat yang lolos saringan Tahap C tanpa batas plafon total, diurutkan menurut EV (SOUL.md §3), dan (2) Blok `[ACTIVE-BATCH]` yang menampung maksimal 5 kandidat `[ACTIVE]` dalam satu siklus pembuktian D -> E. Wajib kembali menjadi 0 ([QUEUED] == 0 dan [ACTIVE] == 0) sebelum Wilayah R_i ditutup. |
| `06-refuted-invalid.md` | Wadah Kandidat Gugur pasca-Pembuktian (Tahap E). Untuk kandidat dari 05-raw-leads.md yang patah saat uji pembuktian Tahap D (beserta bukti eksak mengapa PoC/hitungan gagal). |
| `07-needs-next-step.md` | Wadah Kandidat Butuh Langkah Lanjut (Tahap E). Untuk kandidat yang logikanya belum terbantahkan tetapi membutuhkan verifikasi lanjutan (misal pengecekan state on-chain spesifik, parameter deployment, atau komponen off-chain). |
| `08-valid-not-eligible.md` | Wadah Valid tapi Tidak Memenuhi Syarat Klaim (Tahap E). Untuk isu/risiko desain yang secara teknis valid tetapi tidak masuk kualifikasi klaim program (*out-of-scope*, *known issue*, asumsi kepercayaan admin resmi, atau di bawah ambang severity). |
| `09-confirmed-findings.md` | Wadah Temuan Terbukti & Naskah Laporan Akhir (Tahap E & Tahap F). Di Tahap E menerima kandidat yang lulus Bukti Segitiga penuh; di Tahap F (Incremental Disclosure per Wilayah) langsung dilengkapi blok Submission-Ready Report untuk Wilayah R_i selagi konteks kode masih 100% segar. |
| `notes/staging-*.md` | Area Isolasi Tulis Subagent. Subagent hanya boleh menulis ke sini; hanya Parent Orchestrator yang berhak menggabungkan (*merge*) isinya ke berkas utama. |

---

## 3. Arsitektur Siklus Eksekusi: Tahap 0 + Vertical Region Loop (A–F) + Final Sweep

Dilarang menjalankan audit secara *horizontal batch* se-repositori. Eksekusi wajib mengikuti siklus berikut:
### Fase I — Tahap 0: Global Partitioning & Rekonsiliasi 100% Berkas Sumber (1x di Awal Audit)
1. Inventarisasi 100% Berkas Scope: Daftarkan seluruh berkas kode sumber yang berada dalam *scope* (`.sol`, `.vy`, `.rs`, `.move`, `.cairo`, `.go`, `.ts`, `.py`, `.circom`, `.nr`, `.fc`, dll.) ke Tabel Rekonsiliasi 100% File di path-map.md. Tidak boleh ada satu berkas pun yang hilang.
2. Klasifikasi 3-Tier:
   - Tier 1 (`CORE-ASSET`): Kontrak/modul/program yang menyimpan, mencetak, membakar, mengunci, mengkliring, atau mentransfer token/koin/ETH/aset/object/state saldo.
   - Tier 2 (`VALUATION-CONTROL-LATENT`): Kontrak/modul penentu harga/kurs/share/oracle, modul likuidasi/lelang/dispute, pengatur akses/governance/timelock/pause/account-constraint, kontrak/akun dengan Current Balance = 0 tetapi memiliki Intended Capacity > 0, sirkuit verifikasi, serta jembatan input off-chain/relayer/keeper/signature.
   - Tier 3 (`ISOLATED-PERIPHERAL`): Interface/trait/header tipe data murni (misal `I*.sol`, definisi `trait`/`struct` tanpa logika mutasi), library matematika murni tanpa pemanggilan eksternal berbahaya (misal DELEGATECALL/CPI), atau konstanta. Wajib diperiksa 1-pass untuk memastikan tidak ada mutasi state/nilai tersembunyi, lalu diberi penanda [LOCKED-TIER3] beserta bukti baris kodenya.
3. Partisi Antrean Wilayah (`R_1 .. R_N`): Kelompokkan seluruh berkas Tier 1 dan Tier 2 yang saling terhubung ke dalam unit Wilayah Uang (`R_1, R_2, ..., R_N`) (idealnya 2–5 kontrak/modul yang berikatan erat per wilayah), urutkan berdasarkan Prioritas EV (`SOUL.md §3`), dan daftarkan ke STATE.md dengan status [OPEN].
4. Kunci Gate 0: Jalankan python3 tools/verify_segitiga.py --gate 0 <audit-dir>.

### Fase II — Siklus Vertikal per Wilayah (R_i: Tahap A -> B -> C1 -> C2 -> [Batch D -> E] -> F)
Ambil wilayah pertama yang berstatus [OPEN] di STATE.md, ubah menjadi [ACTIVE], dan jalankan tahapan berikut secara berurutan khusus pada kontrak/modul di Wilayah R_i:

- Tahap A (`Region Value & Facts` di `R_i`):
  - Jalankan --context-packet untuk memuat @SLICE:STAGE-A.
  - Petakan L-VALUE untuk semua kontrak/modul di R_i pada path-map.md, wajib mencakup kolom Current Balance dan Intended Capacity / Latent Value.
  - Ekstrak seluruh fakta teknis, rumus pembulatan, syarat require/if/assert!/ensure!, dan invariant Wilayah R_i secara verbatim (Path/File.ext:Lxx-Lyy) ke FACTS.md, lengkap dengan kolom Prerequisite Inversion Hint (cara mematahkan asumsi tersebut).
  - Kunci dengan python3 tools/verify_segitiga.py --gate A <audit-dir>.

- Tahap B (`Region Path & 3-Edge` di `R_i`):
  - Jalankan --context-packet untuk memuat @SLICE:STAGE-B.
  - Petakan jalur fungsi/instruksi di dalam Wilayah R_i (dan titik potongnya ke wilayah lain) di path-map.md menggunakan tiga label wajib:
    1. [EDGE-ASSET] (mutasi saldo/token/koin/ETH/share/object),
    2. [EDGE-VALUATION] (pembacaan harga, kurs, totalAssets, totalSupply, indeks bunga/reward, bobot, presisi/desimal),
    3. [EDGE-CONTROL/LATENT] (otorisasi, validasi signer/authority/account/capability, perubahan parameter, likuidasi, dispute, pause, CPI/callback/hook, input relayer/signature/ZK proof off-chain).
  - Kunci dengan python3 tools/verify_segitiga.py --gate B <audit-dir>.

- Tahap C1 (`Gelombang 1 — Blind Adversarial Hunt` di `R_i`):
  - Jalankan --context-packet untuk memuat @SLICE:STAGE-C1.
  - Aturan Besi C1: Dilarang membuka _ROUTER.md atau file plugin M-xxx/AF-xx. Bedah kode Wilayah R_i dengan insting murni berdasarkan L-VALUE dan L-PATH.
  - Jalur yang langsung terbukti aman oleh penjaga kode eksak dicatat ke `04-code-guarded.md` beserta Path/File.ext:Lxx-Lyy penjaganya.
  - Kandidat anomali awal dicatat sebagai observasi [WAVE-1-BLIND] di 05-raw-leads.md.
  - Setiap kali menemukan fungsi/state di R_i yang memengaruhi atau dipengaruhi kontrak/modul lain, wajib tambahkan sinyal ke RADAR.md dengan tag `[TOUCHES: KontrakAtauModul.variabelAtauFungsi]`.
  - Kunci dengan python3 tools/verify_segitiga.py --gate C1 <audit-dir>.
- Tahap C2 (`Gelombang 2 — Cross-Pollination & Antrean [QUEUED]` di `R_i`):
  - Jalankan --context-packet untuk memuat @SLICE:STAGE-C2 (skrip akan menyuntikkan fakta R_i dari FACTS.md, sinyal [TOUCHES] dari RADAR.md, dan tabel indeks _ROUTER.md).
  - Lakukan 3 operasi penyilangan untuk Wilayah R_i:
    1. Inversi `FACTS.md`: Uji apakah prasyarat di FACTS.md bisa dipatahkan lewat urutan transaksi, pinjaman kilat (*flash loan*), donasi/injeksi saldo langsung, nilai batas (0, 1, MAX), perbedaan presisi/desimal, pemalsuan akun/objek, atau urutan panggil.
    2. Rantai `RADAR.md`: Pasangkan sinyal [TOUCHES] yang menyentuh variabel/fungsi yang sama untuk menemukan *Chained Exploit*.
    3. Lazy-Load Bank Ilmu via `_ROUTER.md`: Baca hanya file plugin M-xxx, AF-xx, DOM-xx, POV-xx, atau CHAIN-xx yang Trigger Symptom-nya cocok dengan Wilayah R_i.
  - Saringan Kualitas & Pembentukan Antrean `[QUEUED]`:
    - Pindahkan dugaan yang patah oleh FACTS.md atau penjaga kode ke `04-code-guarded.md`.
    - Semua kandidat yang lolos saringan kualitas Segitiga (tanpa batas plafon total—baik 2, 8, maupun 15 kandidat) wajib dimasukkan ke tabel `[QUEUED]` di 05-raw-leads.md, diurutkan menurut Prioritas EV (`SOUL.md §3`), dan dipasangi Assigned M-xxx serta Assigned AF-xx.
  - Kunci dengan python3 tools/verify_segitiga.py --gate C2 <audit-dir>.

- Siklus Rolling Batch Tahap D (`Prove`) & Tahap E (`Verdict`) di Wilayah `R_i`:
  Selama masih ada kandidat berstatus [QUEUED] untuk Wilayah R_i di 05-raw-leads.md:
  1. Penarikan Batch (Maksimal 5 Kandidat `[ACTIVE]`):
     - Tarik maksimal 5 kandidat `[QUEUED]` dengan EV tertinggi ke blok `[ACTIVE-BATCH]` di 05-raw-leads.md dan ubah statusnya menjadi [ACTIVE].
     - Dilarang keras memproses lebih dari 5 kandidat [ACTIVE] sekaligus dalam satu batch.
  2. Tahap D (`Prove Batch Aktif`):
     - Jalankan --context-packet untuk memuat @SLICE:STAGE-D beserta isi file plugin M-xxx & AF-xx yang ditugaskan pada kandidat di batch tersebut.
     - Untuk setiap kandidat [ACTIVE] di 05-raw-leads.md, bangun Bukti Segitiga:
       - Titik 1 (Jejak Kode Eksak): Kutipan Path/File.ext:Lxx-Lyy dari titik masuk hingga titik mutasi nilai.
       - Titik 2 (Bukti Eksekusi / Matematika Konkret): Hasil uji PoC dengan *test runner* ekosistem terkait (forge test, cargo test, sui move test, aptos move test, snforge test, pytest, go test, dll.) atau jejak perhitungan angka langkah demi langkah dengan nilai konkret.
       - Titik 3 (Delta Nilai / Invarian): Bukti terukur berapa nilai yang bocor/terkunci atau invariant apa yang pecah.
     - Kunci dengan python3 tools/verify_segitiga.py --gate D <audit-dir>.
  3. Tahap E (`Verdict Batch Aktif`):
     - Jalankan --context-packet untuk memuat @SLICE:STAGE-E dan standar templates/VERDICT.md.
     - Adili seluruh kandidat [ACTIVE] pada batch tersebut dan pindahkan dari 05-raw-leads.md ke wadah final yang sesuai:
       - `06-refuted-invalid.md` (jika patah saat pembuktian),
       - `07-needs-next-step.md` (jika butuh verifikasi eksternal/on-chain lanjutan),
       - `08-valid-not-eligible.md` (jika valid secara teknis tetapi tidak memenuhi syarat kelayakan/scope), atau
       - `09-confirmed-findings.md` (jika lulus Bukti Segitiga penuh).
     - Kunci dengan python3 tools/verify_segitiga.py --gate E <audit-dir> (memastikan jumlah kandidat [ACTIVE] di 05-raw-leads.md kembali menjadi `0`).
  4. Cek Sisa Antrean `[QUEUED]` Wilayah `R_i`:
     - Jika di 05-raw-leads.md masih ada kandidat Wilayah R_i yang berstatus [QUEUED] > 0, kembali ke Langkah 1 (Tarik Batch Berikutnya, maksimal 5 kandidat) dan ulangi D -> E.
     - Jika [ACTIVE] == 0 DAN [QUEUED] == 0 untuk Wilayah R_i, lanjut ke Tahap F.

- Tahap F (`Incremental Disclosure di 09-confirmed-findings.md & Penutupan Wilayah R_i`):
  - Jalankan --context-packet untuk memuat @SLICE:STAGE-F.
  - Selagi konteks kode dan PoC Wilayah R_i masih 100% segar, lengkapi setiap temuan milik Wilayah R_i di dalam `09-confirmed-findings.md` (dan tindak lanjut di 07-needs-next-step.md bila ada) menjadi format Submission-Ready Disclosure yang utuh (Ringkasan Eksekutif, Dampak & EV, Rantai Bukti Kode, Langkah Reproduksi/PoC, dan Rekomendasi Mitigasi).
  - Jalankan penutupan wilayah:

        python3 tools/verify_segitiga.py --close-region <R_i> <audit-dir>
- Setelah lulus, ubah status R_i di STATE.md menjadi `[CLOSED]`, lakukan Hard Context Flush (bersihkan beban memori internal R_i), dan ambil Wilayah [OPEN] berikutnya (R_{i+1}) mulai dari Tahap A.

### Fase III — Penutupan Global: Cross-Region Final Sweep (1x Setelah Semua Wilayah [CLOSED])
1. Jalankan --context-packet saat seluruh wilayah sudah [CLOSED] untuk memuat @SLICE:FINAL-SWEEP.
2. Periksa seluruh entri RADAR.md: apakah ada sinyal [TOUCHES: ...] yang baru ditemukan di wilayah-wilayah akhir (R_N) yang mematahkan asumsi di wilayah awal (R_1)?
3. Jika ada rantai lintas-wilayah baru yang belum diuji, masukkan ke 05-raw-leads.md (maksimal 5 per batch) -> jalankan D -> E -> F.
4. Jalankan gerbang pengunci akhir:

       python3 tools/verify_segitiga.py --final <audit-dir>

---

## 4. Arsitektur Modular *Drop-in Plugin* (1 File = 1 Item) & _ROUTER.md

Pengetahuan metode dan serangan disimpan secara modular agar mudah ditambah/direvisi tanpa mengedit banyak berkas dan tanpa membebani memori agen:

1. Lokasi Lima Folder Plugin:
   - Metode Bedah: references/methods/M-xxx-<slug>.md (Indeks: references/methods/_ROUTER.md)
   - Bentuk Serangan Uji: methodology/attack-forms/AF-xx-<slug>.md (Indeks: methodology/attack-forms/_ROUTER.md)
   - Pengetahuan Domain: methodology/domains/DOM-<slug>.md (Indeks: methodology/domains/_ROUTER.md)
   - Sudut Pandang Aktor: references/pov/POV-<slug>.md (Indeks: references/pov/_ROUTER.md)
   - Pola Serangan Berantai: references/chains/CHAIN-<slug>.md (Indeks: references/chains/_ROUTER.md)

2. Format Header 4-Baris Wajib pada Setiap File Plugin:
   Setiap file plugin wajib diawali tepat 4 baris metadata berikut di baris 1–4:

       # [ID-PLUGIN] Judul Metode / Bentuk Serangan / Domain / POV / Chain
       - Classes: [Kategori kelas masalah atau domain terkait]
       - Trigger Symptom: [Gejala kode spesifik yang memicu pembacaan file ini]
       - Paired Items: [ID plugin pasangan yang direkomendasikan, misal AF-xx, M-xxx]

3. Sinkronisasi Otomatis (`--sync`) & Aturan *Lazy-Loading***:
   - Setiap kali ada penambahan atau revisi file plugin (misal menambah `M-011` atau `AF-11`), cukup buat/ubah 1 file tersebut lalu jalankan:

         python3 tools/verify_segitiga.py --sync

   - Agen dilarang membaca seluruh file plugin di dalam folder sekaligus. Agen wajib membaca `_ROUTER.md` terlebih dahulu di Gelombang 2 (`C2`), lalu memanggil `read_file` hanya pada file plugin yang sesuai dengan gejala wilayah aktif.

---

## 5. Empat Sabuk Pengaman Anti-Kompresi Konteks (*Zero-Compression Protocol*)

1. **Kewajiban Jangkar Verbatim (`Verbatim Anchor`):
   Setiap baris fakta di FACTS.md, sinyal di RADAR.md, dan entri di 04 s/d 09 wajib memuat format:
   [Path/File.ext:Lxx-Lyy] | [NamaFungsi/Variabel Eksak] | [Kondisi/Ekspresi Kode Asli].
2. Larangan Mutlak Token Pemotongan Malas:
   verify_segitiga.py akan otomatis menggagalkan Gate jika menemukan token kompresi malas berikut di dalam blok analisis teknis:
   ..., dll., dst., etc., and so on, rest of logic, rest of code, dan seterusnya, atau klaim teknis tanpa rujukan nomor baris (:L).
3. Kewajiban *Write-Ahead Checkpoint* di `STATE.md`:
   Jangan pernah berpindah tahap atau memanggil Subagent sebelum STATE.md diperbarui di disk.
4. Protokol Delegasi Subagent & Isolasi Berkas Staging:
   Jika Parent Orchestrator menggunakan Subagent untuk mengerjakan suatu tahap/batch:
   - Injeksi Konteks oleh Parent: Parent wajib menjalankan verify_segitiga.py --context-packet <audit-dir> dan menyertakan outputnya secara utuh di dalam prompt instruksi ke Subagent.
   - Larangan Tulis Langsung oleh Subagent: Subagent dilarang keras mengedit langsung STATE.md, FACTS.md, RADAR.md, path-map.md, maupun 04 s/d 09.
   - Kewajiban Tulis ke Staging dengan Manifes <= 16 Baris: Subagent wajib menulis hasilnya ke notes/staging-<region>-<stage>-<item>.md. Bagian paling atas file staging wajib diawali blok `## STAGING MANIFEST` maksimal 16 baris yang merangkum daftar item verbatim yang dihasilkan, diikuti detail lengkap di bawahnya.
- Verifikasi & Merge oleh Parent: Parent membaca manifes dan isi file staging, memastikannya bebas dari token kompresi malas, menggabungkannya ke berkas utama, lalu menjalankan verify_segitiga.py --gate <stage>.

---

## 5b. Aturan Bukti Per Wadah 06 / 07 / 08 / 09 (Mengikat, Ditegakkan `--rules` & `--gate E`)

Setiap wadah menuntut **jenis bukti yang berbeda**. Wadah yang diisi tanpa bukti jenisnya = laporan DITOLAK. Hukum acara lengkap: `templates/VERDICT.md`.

| Wadah | Menuntut bukti | Gerbang penolak |
| :--- | :--- | :--- |
| `06-refuted-invalid.md` | Bukti **kegagalan**: kelas `REJECTED_*`, `TANGGA_BUKTI`, `DEPLOYMENT_MATCH`, jangkar `:Lxx`; kelas `POC_FAILS`/`NEGATIVE_EV`/`DUST` wajib `BUKTI_SIMULASI:` berisi `$ ...` + log + Strike 3 Fuzz | `PAPER_REFUTATION_DETECTED` (kecuali KS-1..KS-4) |
| `07-needs-next-step.md` | Bukti **usaha**: `Disposition:` (tepat satu) + `PERCOBAAN:` berisi perintah + log nyata; `TANGGA_BUKTI` A/A-HEAD dilarang | `LAZY_BAILOUT_DETECTED` |
| `08-valid-not-eligible.md` | Bukti **mekanisme**: `LOW_CLASS` (PRE_LIVE_SCOPE / ADMIN_ONLY / LOW_NUISANCE) + `POC_STATUS: PASS` + dampak kuantitatif | Pelarian wadah (#11b) |
| `09-confirmed-findings.md` | Bukti **ketiganya**: 3 Titik + Sepuluh Pernyataan + Integritas #11 + `LIVE_IDENTITY` terukur + `POC_STATUS: PASS`; `A-HEAD` dan siklus pre-deploy dilarang | ditolak ke `08`/`06` |

**Jejak lead (#11d).** Setiap lead yang keluar dari `05-raw-leads.md` wajib muncul di **tepat satu** wadah `06`/`07`/`08`/`09`. Lead yang menguap atau tercatat ganda → `--gate E` FAIL.

**Target akhir `07` = 0 entri.** Setiap sisa wajib dipertahankan dengan log komputasi, bukan kalimat.

---

## 6. Tabel Ringkasan Gerbang Penegak (tools/verify_segitiga.py)

| Perintah CLI | Kapan Wajib Dijalankan | Apa yang Diverifikasi oleh Skrip |
| :--- | :--- | :--- |
| python3 tools/verify_segitiga.py --sync | Saat menambah/mengubah file plugin M-xxx, AF-xx, DOM-xx, POV-xx, CHAIN-xx. | Memvalidasi 4 baris header plugin dan membangun ulang seluruh tabel _ROUTER.md. |
| python3 tools/verify_segitiga.py --context-packet <dir> | Wajib di awal setiap tahap, setiap batch, dan setiap pergantian wilayah. | Mencetak status STATE.md, potongan @SLICE:STAGE-* dari METHODOLOGY-SEGITIGA.md, fakta R_i, radar R_i, dan router yang relevan. |
| python3 tools/verify_segitiga.py --gate 0 <dir> | Selesai Tahap 0 (Global Partitioning). | 100% berkas kode sumber dalam scope terdaftar di Tier 1/2/3 pada path-map.md, Tier 3 terkunci 1-pass, dan antrean R_1..R_N terbentuk di STATE.md. |
| python3 tools/verify_segitiga.py --gate A <dir> | Selesai Tahap A pada Wilayah R_i. | Kontrak/modul R_i memiliki Current Balance + Intended Capacity dan fakta verbatim (:Lxx) + inversi di FACTS.md. |
| python3 tools/verify_segitiga.py --gate B <dir> | Selesai Tahap B pada Wilayah R_i. | Wilayah R_i memiliki pemetaan [EDGE-ASSET], [EDGE-VALUATION], dan [EDGE-CONTROL/LATENT] di path-map.md. |
| python3 tools/verify_segitiga.py --gate C1 <dir> | Selesai Tahap C Gelombang 1 (Blind Hunt) di R_i. | Jalur terjaga masuk ke 04-code-guarded.md, observasi awal masuk ke 05-raw-leads.md, dan sinyal lintas-kontrak tercatat dengan [TOUCHES: ...] di RADAR.md. |
| python3 tools/verify_segitiga.py --gate C2 <dir> | Selesai Tahap C Gelombang 2 (Cross-Pollination) di R_i. | Hasil penyilangan tercatat, kandidat gugur awal masuk ke 04-code-guarded.md, dan setiap kandidat [QUEUED] di 05-raw-leads.md memiliki pasangan valid M-xxx & AF-xx serta urutan EV. |
| python3 tools/verify_segitiga.py --gate D <dir> | Selesai Tahap D pada satu Batch di R_i. | Kandidat [ACTIVE] di 05-raw-leads.md berjumlah <= 5 dan semuanya memiliki 3 komponen Bukti Segitiga lengkap tanpa token kompresi. |
| python3 tools/verify_segitiga.py --gate E <dir> | Selesai Tahap E pada satu Batch di R_i. | Active Leads == 0, **plus** seluruh aturan wadah 06/07/08/09 (kelas + bukti) dan jejak lead: setiap lead yang keluar dari 05 wajib muncul di tepat satu wadah. |
| python3 tools/verify_segitiga.py --rules <dir> | Sebelum/di luar gate, khusus memeriksa wadah | Aturan 06 (`REJECTED_*` + `BUKTI_SIMULASI`/KS-n), 07 (`Disposition` + `PERCOBAAN`), 08 (`LOW_CLASS` + `POC_STATUS: PASS`), 09 (`TANGGA_BUKTI`/`LIVE_IDENTITY`/`POC_STATUS`), dan jejak lead (#11d). |
| python3 tools/verify_segitiga.py --close-region <R_i> <dir> | Selesai Tahap F pada Wilayah R_i. | Di 05-raw-leads.md baik [ACTIVE] == 0 maupun [QUEUED] == 0 untuk R_i, dan seluruh temuan R_i di 09-confirmed-findings.md telah memiliki blok *Submission-Ready Disclosure*. |
| python3 tools/verify_segitiga.py --final <dir> | Selesai seluruh wilayah & *Cross-Region Final Sweep*. | Seluruh wilayah R_1..R_N berstatus [CLOSED], 05-raw-leads.md bersih (0), bebas token kompresi, dan seluruh temuan di 09-confirmed-findings.md siap kirim. |
