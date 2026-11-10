# 08-VALID-NOT-ELIGIBLE — Wadah Isu Valid Teknis di Luar Kelayakan Klaim (STAGE-E)

> ATURAN PENGISIAN (`MEKANISME-TERBUKTI GUARD` + `ZERO-COMPRESSION LAW`):
> 1. Kata **"nyata dan terbukti" bersifat harfiah**: mekanisme wajib sudah lulus simulasi PoC (`POC_STATUS: PASS`) tanpa curang, dengan dampak kuantitatif terukur. Wadah ini **BUKAN** tempat menyimpan lead yang belum diuji — lead belum teruji wajib di `07-needs-next-step.md` dengan `PERCOBAAN:`.
> 2. Wadah ini menampung kandidat dari 05-raw-leads.md yang perilakunya terbukti valid secara teknis, namun tidak memenuhi kriteria sebagai temuan utama yang *eligible* karena salah satu dari tiga kelas berikut:
>    - **`PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)`** — dampak finansial nyata (Critical/High/Medium), PoC `[PASS]` pada `FORK_DEPLOYED_HEAD` / `LOKAL`, tetapi kontrak/fitur belum live di mainnet, berbeda dari bytecode produksi aktif, atau belum terdaftar di halaman alamat bounty.
>    - **`ADMIN_ONLY`** — bug mekanis nyata pada fungsi khusus admin, tanpa jalur eksploitasi eksternal.
>    - **`LOW_NUISANCE`** — DoS tanpa kehilangan dana, kerugian kecil terbatas (*capped*), atau griefing non-finansial (Severity Low / S4).
> 3. **Severity ditentukan IMPACT, bukan siklus deployment.** Menurunkan severity karena alasan "masih HEAD-only" / "hanya testnet" adalah pelanggaran; yang berubah hanya wadah (`09` vs `08`).
> 4. Wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy`, `TANGGA_BUKTI`, dan `DEPLOYMENT_MATCH`. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).

---

## GERBANG MASUK `08`

| Syarat | Konsekuensi bila gagal |
| :--- | :--- |
| `POC_STATUS: PASS` — mekanisme terbukti lewat eksekusi, bukan narasi | Kembalikan ke `07` dengan `PERCOBAAN:` (belum teruji) |
| `LOW_CLASS` terisi tepat satu dari tiga kelas di atas | Entri tidak sah; pilih kelas yang sesuai bukti |
| Dampak kuantitatif terukur (angka + satuan aset) | Kembalikan ke `STAGE-D` untuk diukur |
| `PRE_LIVE_SCOPE` menyertakan kode PoC utuh + log `[PASS]` | Entri ditolak |
| Severity konsisten dengan impact (bukan diturunkan karena siklus) | Laporan DITOLAK |

**Larangan pelarian wadah:** lead yang belum diuji lalu dilabeli `LOW_NUISANCE` / `ADMIN_ONLY` / `PRE_LIVE_SCOPE` adalah pelanggaran — `07` menuntut bukti usaha, `08` menuntut bukti mekanisme, tidak ada wadah yang boleh menampung lead yang belum dikerjakan.

---

## 1. TABEL ISU VALID NON-ELIGIBLE (08-VALID-NOT-ELIGIBLE)

| Non-Eligible ID | Asal Lead ID | Region (R_i) | LOW_CLASS | SEVERITY | POC_STATUS | Jangkar Kode (Path/File.ext:Lxx-Lyy) | Dampak Terukur |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| VNE-R1-01 | LEAD-R1-xx | R_1 | [PRE_LIVE_SCOPE / ADMIN_ONLY / LOW_NUISANCE] | [CRITICAL / HIGH / MEDIUM / LOW] | PASS | [Path/File.ext:L30-L58] | [angka + satuan] |

---

## 2. RINCIAN TEKNIS & CATATAN ARSITEKTURAL

### VNE-R1-01 (Eks LEAD-R1-xx) — [Judul Isu]
- Region & Modul: R_1 | [NamaModul.namaFungsi]
- VERDICT: VALID_NOT_ELIGIBLE
- LOW_CLASS: [PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN) | ADMIN_ONLY | LOW_NUISANCE]
- TARGET_FILE: 08-valid-not-eligible.md
- SEVERITY: [CRITICAL | HIGH | MEDIUM | LOW] *(dari IMPACT sesuai rubrik severity)*
- Rujukan Severity: [Platform + URL, atau Matriks Universal `templates/SEVERITY-RUBRIC.md`]
- POC_STATUS: PASS
- TANGGA_BUKTI: [A-HEAD | B] *(A yang sudah `LIVE_MATCH` seharusnya masuk `09`)*
- DEPLOYMENT_MATCH: [HEAD-only (PROVEN_ON_REPO_HEAD) | UNVERIFIED (<sumber yang gagal>)]
- Mode Uji: [FORK_DEPLOYED_HEAD (chain, block, RPC) | LOKAL (<alasan>)]
- Jangkar Kode Eksak (`Path/File.ext:Lxx-Lyy`): [Kutipan lokasi dan perilaku teknis]
- Dampak Kuantitatif: [Angka eksak + satuan aset; biaya serangan bila relevan]
- Alasan Ketidaklayakan: [Rujukan aturan scope / status deployment / ambang severity yang mengecualikan isu ini dari `09-confirmed-findings.md`]

**BUKTI_SIMULASI:**

```text
$ [perintah eksak yang dijalankan]
[tempelkan log nyata yang mencetak [PASS] dan angka delta nilai]
```
