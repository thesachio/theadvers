# 06-REFUTED-INVALID — Wadah Kandidat Gugur Pasca-Pembuktian (STAGE-E)

> ATURAN PENGISIAN (`PAPER_REFUTATION GUARD` + `ZERO-COMPRESSION LAW`):
> 1. Wadah ini menampung kandidat dari meja operasi 05-raw-leads.md yang gugur saat uji pembuktian di `STAGE-D` / `STAGE-E` (eksekusi test gagal/revert, hitungan angka konkret membuktikan tidak ada pencurian/kerusakan nilai, atau tertahan penjaga kode di modul lain yang baru terlihat saat penelusuran penuh).
> 2. Setiap entri wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy`, `TANGGA_BUKTI`, dan `DEPLOYMENT_MATCH` — **bahkan pada vonis gugur**. Tanpa keduanya, vonis dianggap belum sah dan entri dikembalikan ke penulisnya.
> 3. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).

---

## GERBANG ANTI-PAPER-REFUTATION (`PAPER_REFUTATION_DETECTED`)

Wadah `06` **DILARANG KERAS** dipakai untuk membuang lead hanya dengan hitungan kertas atau alasan teks.

Untuk kelas `REJECTED_POC_FAILS`, `REJECTED_NEGATIVE_EV`, dan `REJECTED_DUST`, entri **WAJIB** memuat blok `BUKTI_SIMULASI:` berisi:

1. **Perintah eksekusi test nyata** (`$ forge test --match-test ...` / `$ cargo test ...` / `$ sui move test ...`) beserta keluarannya,
2. **Ringkasan kode setup** yang membuktikan telah dilakukan *Victim Lifecycle Seeding* dan *3-Way EV Amplification*,
3. **Log hasil Strike 3 Mandatory Fuzzing** (`testFuzz_... (runs: 256, ...)` / `proptest` / `halmos`) yang membuktikan invarian tetap tidak tertembus.

Entri tanpa log eksekusi test dan fuzz di atas adalah pelanggaran **PAPER_REFUTATION_DETECTED** → laporan DITOLAK di STAGE-F dan lead dikembalikan ke `STAGE-D`.

**Empat Kemustahilan Statis Sempit** — satu-satunya kondisi yang boleh gugur **tanpa** kode test (`verify/VERDICT.md` §4):

| # | Kelas | Syarat (semua harus terpenuhi) |
| :--- | :--- | :--- |
| **KS-1** | `REJECTED_MISMATCH` | Salah baca statis literal: kutipan `File:Baris` yang diklaim terbukti **tidak** berisi kode yang diklaim, dibuktikan dengan kutipan ulang rentang utuh |
| **KS-2** | `REJECTED_BY_DESIGN` | Perilaku terdokumentasi sebagai disengaja dan dapat dikutip persis dari NatSpec / `DESIGN.md` / README resmi / proposal governance |
| **KS-3** | `REJECTED_GENESIS_MIRAGE` | Prasyarat hanya terpenuhi pada kondisi genesis (`totalSupply == 0` atau pool tunggal terkunci) **dan** tidak ada jalur mengosongkannya, dibuktikan dengan pembacaan utuh fungsi penghasil state |
| **KS-4** | `REJECTED_NON_LIVE_INIT` | Fungsi target tidak dapat dijangkau karena slot inisialisasi terkunci permanen, dibuktikan dari bytecode/storage live — bukan asumsi |

Di luar empat kondisi itu, seluruh kelas `REJECTED_*` **WAJIB** melampirkan `BUKTI_SIMULASI:`.

---

## 1. TABEL RINGKASAN KANDIDAT GUGUR (06-REFUTED-INVALID)

| Refuted ID | Asal Lead ID | Region (R_i) | Kelas Verdict | Titik Masuk (NamaModul.namaFungsi) | Jangkar Kode Penahan / Pembantah (Path/File.ext:Lxx-Lyy) | Bukti (BUKTI_SIMULASI / KS-n) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REF-R1-01 | LEAD-R1-xx | R_1 | REJECTED_POC_FAILS | [NamaModul.namaFungsi] | [Path/File.ext:L112-L128] | BUKTI_SIMULASI: lihat §2 |

---

## 2. ARSIP DETAIL PEMBUKTIAN YANG TERBANTAHKAN

### REF-R1-01 (Eks LEAD-R1-xx) — [Judul Kandidat yang Gugur]
- Region & EV Awal: R_1 | [P1..P5]
- VERDICT: [REJECTED_POC_FAILS | REJECTED_NEGATIVE_EV | REJECTED_DUST | REJECTED_NO_VICTIM | REJECTED_FANTASY_MOCK | REJECTED_CHEATCODE | REJECTED_PRIVILEGED_FANTASY | REJECTED_GENESIS_MIRAGE | REJECTED_NON_LIVE_INIT | REJECTED_BY_DESIGN | REJECTED_MISMATCH | REJECTED_UNPROVEN_DEPLOYMENT]
- TARGET_FILE: 06-refuted-invalid.md
- TANGGA_BUKTI: [A | A-HEAD | B | C] *(wajib terisi meski vonis gugur)*
- DEPLOYMENT_MATCH: [LIVE_MATCH | HEAD-only (PROVEN_ON_REPO_HEAD) | UNVERIFIED (<sumber yang gagal>)]
- Mode Uji: [FORK_LIVE (chain, block, RPC) | FORK_DEPLOYED_HEAD | LOKAL]
- Plugin yang Diuji: [M-xxx, AF-xx]
- Hipotesis Awal: [Ringkasan dugaan serangan sebelum diuji]
- Jejak Kode & Titik Patah (`Path/File.ext:Lxx-Lyy`): [Kutipan kondisi kode atau urutan state yang mematahkan hipotesis]
- Alasan Teknis Kegagalan: [Mengapa eksploitasi patah, dinyatakan sebagai mekanisme — bukan narasi]

**BUKTI_SIMULASI:**

```text
$ [perintah eksak, misal: FOUNDRY_JOBS=1 forge test --match-test test_LEADR101_exploit -vvv]
[tempelkan log terminal nyata: hasil revert / angka tanpa delta / hasil fuzz Strike 3]
```

*Atau, untuk KS-1..KS-4:*
```text
KS-n : [nama kondisi]
Kutipan ulang rentang utuh (Path/File.ext:Lxx-Lyy) yang membuktikan kemustahilan statis.
```

---

## 3. KELAS YANG WAJIB `BUKTI_SIMULASI` (tanpa pengecualian)

`REJECTED_POC_FAILS` · `REJECTED_NEGATIVE_EV` · `REJECTED_DUST` · `REJECTED_NO_VICTIM` · `REJECTED_FANTASY_MOCK` · `REJECTED_CHEATCODE` · `REJECTED_PRIVILEGED_FANTASY` · `REJECTED_UNPROVEN_DEPLOYMENT`

Semuanya bergantung pada **angka** (EV, ambang, keberadaan korban, sifat entitas) — dan angka tidak boleh dinilai di atas kertas.
