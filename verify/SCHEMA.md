# SCHEMA — MANIFEST.json (v1)

**Template ini adalah satu-satunya berkas yang dibaca mesin dari repo inbox submission.**
Semua klaim harus *machine-checkable*; yang tidak bisa diperiksa skrip akan menggugurkan
klaim itu sendiri sebelum sampai ke penilai manusia.

Divalidasi oleh `tools/ingest.py` (lihat `--selftest` untuk uji internal).

---

## Struktur top-level

```json
{
  "version": 1,
  "project": "<slug-proyek>",
  "upstream": { "agent": "<nama>", "date": "YYYY-MM-DD", "submitted_to_program": false },
  "sources": [
    { "name": "<label-sumber>", "url": "https://github.com/<org>/<repo>", "commit": "<SHA-40>" }
  ],
  "findings": [ { ...lihat bawah... } ]
}
```

> **`version` adalah integer `1`, BUKAN string.** Menulis `"6.2.4"` (versi skema internal)
> menyebabkan `[FATAL] version tidak didukung`.

---

## Field per finding

| Field | Tipe | Wajib | Aturan |
|---|---|---|---|
| `id` | string | **ya** | unik dalam manifest; konvensi `<PREFIX>-<NN>` |
| `title` | string | **ya** | satu baris |
| `file` | string | **ya** | path relatif terhadap **root inbox**, berkas harus ada |
| `lines` | `[int,int]` | **ya** | `1 <= start <= end <= jumlah baris file` |
| `snippet` | string | disarankan | harus benar-benar muncul di rentang itu (whitespace dinormalkan) |
| `claim` | string | **ya** | satu kalimat mekanis |
| `impact` | enum | **ya** | `theft` · `grief` · `dos` · `design` · `none` |
| `victim` | enum | **ya** | `sponsor` · `user` · `protocol` · `third-party` · `none` |
| `actor` | enum | **ya** | `unprivileged` · `solver` · `oracle` · `admin` |
| `live` | bool | **ya** | `true` hanya bila kode ter-deploy di produksi |
| `poc` | string | **ya** | path berkas test, harus ada |
| `cmd` | string | **ya** | perintah persis untuk menjalankan PoC |
| `severity_claimed` | enum | **ya** | `S1` · `S2` · `S3` · `S4` |
| `not_verified` | `[string]` | disarankan | hal yang **TIDAK** dicek penulis |

### Field tambahan yang divalidasi silang

| Field | Nilai sah | Kapan wajib |
|---|---|---|
| `cycle` | `P1_PRE_DEPLOY` · `P2_TESTNET_ONLY` · `P3_LIVE_PARTIAL` · `P4_LIVE_FULL` · `P0_UNKNOWN` | bila `live: true` |
| `eligibility` | `LIVE_MATCH` · `HEAD_ONLY_PROVEN` · `TESTNET_ONLY` · `ENTRYPOINT_RELOCATED` · `REGRESSION_FIXED` · `ENV_ERROR` · `UNVERIFIABLE` · `IDENTITY_ONLY` | bila menyertakan `cycle` |
| `tangga_bukti` | `A` · `A-HEAD` · `B` · `C` · `D` | selalu disarankan |
| `wadah` | `08-…` · `09-…` | bila ingin lolos cek penempatan |
| `live_identity` | string terukur (`accountId()`, `sha256(ProgramData)`, hash impl EIP-1967) | **WAJIB bila `eligibility: LIVE_MATCH`** |

---

## Aturan penyaringan (dijalankan `ingest.py`, nol biaya model)

Klaim **gugur otomatis** bila:

1. field wajib hilang, atau enum tidak dikenal
2. `lines` tidak valid / melebihi jumlah baris file
3. `snippet` tidak ditemukan di rentang yang diklaim
4. berkas target tidak ada (path relatif terhadap root inbox)
5. berkas PoC tidak ada
6. `cmd` kosong
7. `id` duplikat dalam satu manifest
8. `commit` sumber tidak cocok dengan HEAD repo yang di-clone (**peringatan**, bukan fatal)

Klaim yang gugur **tidak pernah sampai ke penilai**. Itu inti penghematannya.

---

## Validasi silang Siklus × Eligibility × Severity × Tangga Bukti

Prinsip: **SEVERITY berasal dari IMPACT**, **ELIGIBILITY berasal dari SIKLUS**. Keduanya
ortogonal — tidak boleh saling menurunkan.

| Kombinasi | Vonis |
|---|---|
| `tangga_bukti: A-HEAD` + `eligibility: LIVE_MATCH` | **KONTRADIKSI** — A-HEAD berarti HEAD-only |
| `tangga_bukti: A` + `eligibility: HEAD_ONLY_PROVEN`/`TESTNET_ONLY` | **KONTRADIKSI** — `A` menuntut objek live |
| `eligibility: HEAD_ONLY_PROVEN` + `tangga_bukti` bukan `A-HEAD`/`B`/`C` | **DITOLAK** |
| `severity_claimed: S3`/`S4` + `wadah: 09` + `eligibility != LIVE_MATCH` | **OVER-SELL** — wajib ke `08` dengan severity utuh |
| `wadah: 08` + `severity_claimed: S4` + `severity_label` mengandung "LOW" | **SEVERITY DITURUNKAN KARENA SIKLUS** — dilarang |
| `eligibility: LIVE_MATCH` tanpa `live_identity` terukur | **DITOLAK** — wajib diisi dari artefak `deploy_parity` |
| `eligibility: ENV_ERROR`/`IDENTITY_ONLY`/`UNVERIFIABLE` di `08`/`09` | **DITOLAK** — status "valid" belum terbukti |

> **Jangan pernah menulis `severity_label` yang bertentangan dengan `severity_claimed`.**
> `S4` **adalah** Low — cukup tulis `S4`. Menambahkan label "Low" di samping `S4` justru
> memicu vonis *severity diturunkan karena siklus*.

---

## Layout repo inbox

`ingest.py` membaca `MANIFEST.json` **dari root direktori** yang diberikan sebagai argumen:

```bash
python3 tools/ingest.py <url-atau-path-repo-inbox> [--dest DIR]
```

Struktur yang benar:

```
<repo-inbox>/
├── MANIFEST.json          <- dibaca mesin
├── findings/              <- laporan naratif per temuan
│   ├── L-01.md
│   └── L-02.md
└── poc/                   <- berkas test yang dirujuk field `poc`
    └── L01_Exploit.t.sol
```

`file` dan `poc` di dalam `findings[]` adalah path **relatif terhadap `<repo-inbox>`**,
bukan terhadap repo target. Untuk merujuk kode target, salin potongan yang relevan ke
`findings/snippets/` atau gunakan `snippet` sebagai gantinya.

---

## Alur submission

1. **Verifikasi mekanis** — `python3 tools/ingest.py <repo-inbox>`; target: `N/N MECH-OK`
2. **Laporan naratif** — `findings/<ID>.md`, format `templates/TECHNICAL-REPORT.md`
3. **Paket PoC** — `poc/<ID>.*`, aturan `templates/POC-PACKAGE.md`
4. **Email pengantar** — `templates/SUBMISSION-EMAIL.md`
5. **Arsip** — setelah terkirim, set `upstream.submitted_to_program: true` dan catat tanggal

> **Gerbang wajib:** klaim yang belum `MECH-OK` **DILARANG** dikirim ke program bounty,
> sekalipun laporan naratifnya terlihat meyakinkan.
