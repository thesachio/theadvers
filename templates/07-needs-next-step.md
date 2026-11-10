# 07-NEEDS-NEXT-STEP — Wadah Kandidat Butuh Verifikasi Lanjutan (STAGE-E)

> ATURAN PENGISIAN (`ANTI-LAZY-BAILOUT` + `ZERO-COMPRESSION LAW`):
> 1. Wadah ini hanya untuk kandidat dari 05-raw-leads.md yang logika kodenya di repositori lokal valid dan belum terbantahkan, tetapi pembuktian akhirnya memerlukan informasi di luar kode lokal (pembacaan state *live* on-chain, parameter deployment produksi, perilaku oracle/relayer eksternal, atau konfirmasi spesifikasi).
> 2. **Jangan gunakan wadah ini sebagai tempat membuang kandidat yang malas diuji di kode lokal.** Jika bisa dibuktikan dengan *test runner* lokal atau matematika konkret, wajib diselesaikan hingga masuk ke 06-refuted-invalid.md atau 09-confirmed-findings.md.
> 3. `Disposition:` dan blok `PERCOBAAN:` **TIDAK BOLEH DIHILANGKAN**. `PERCOBAAN:` bukan rencana — isinya perintah yang **sudah dijalankan** beserta keluarannya.
> 4. Wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy`, `TANGGA_BUKTI`, dan `DEPLOYMENT_MATCH`.
> 5. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).

---

## GERBANG ANTI-LAZY-BAILOUT (`LAZY_BAILOUT_DETECTED`)

Entri `07` tanpa `Disposition:` **atau** tanpa blok `PERCOBAAN:` berisi log nyata → laporan **DITOLAK** dan lead dikembalikan ke `STAGE-D`.

| Label `Disposition` | Bukti yang wajib ada di entri | Tanpa bukti |
| :--- | :--- | :--- |
| `NEXT_EXPLORE` | log fuzzing (Tier 2) / differential (Tier 3) / halmos-symbolic (Tier 5) yang berjalan sampai **timeout komputasi** | `LAZY_BAILOUT_DETECTED` |
| `TOOL_BLOCKED` | log terminal **ketiga** anak tangga: (1) flag/remapping/toolchain, (2) standalone interface-only harness, (3) fallback RPC | `LAZY_BAILOUT_DETECTED` |
| `NEXT_MAINNET` | bukti rantai tanpa RPC/explorer publik; bila RPC tersedia, `07` **tidak sah** — jalankan `cast call`/`cast storage` sendiri | `LAZY_BAILOUT_DETECTED` |
| `ENV_ERROR` | minimal **dua** percobaan endpoint berbeda beserta log kegagalannya | `LAZY_BAILOUT_DETECTED` |

**Larangan pelarian wadah:** memindahkan lead dari `07` ke `08` hanya sah bila mekanismenya **sudah terbukti** (PoC `[PASS]` + dampak kuantitatif terukur). Bila ragu antara `07` dan `08`, lead itu masih `07` dan wajib `PERCOBAAN:`.

**Label basi tidak sah:** judul entri sudah dipindah ke wadah lain tetapi label lama masih tertinggal → pelanggaran.

**Target akhir `07` = 0 entri.** Setiap sisa wajib dipertahankan dengan log komputasi, bukan kalimat.

---

## 1. TABEL ANTREAN TINDAK LANJUT (07-NEEDS-NEXT-STEP)

| Next-Step ID | Asal Lead ID | Region (R_i) | EV Rank (P1`–`P5) | Disposition | TANGGA_BUKTI | PERCOBAAN (ringkas) | Tindakan Verifikasi Spesifik |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NEXT-R1-01 | LEAD-R1-xx | R_1 | [P1..P5] | [NEXT_EXPLORE / NEXT_MAINNET / TOOL_BLOCKED / ENV_ERROR] | [B / C] | lihat §2 | [Query storage slot X di mainnet / uji parameter Y] |

---

## 2. RINCIAN BUKTI SEMENTARA & PROTOKOL UJI LANJUTAN

### NEXT-R1-01 (Eks LEAD-R1-xx) — [Judul Kandidat]
- Region & Modul Terdampak: R_1 | [NamaModul.namaFungsi]
- VERDICT: NEEDS_NEXT_STEP
- Disposition: [NEXT_EXPLORE | NEXT_MAINNET | TOOL_BLOCKED | ENV_ERROR] *(tepat satu)*
- TARGET_FILE: 07-needs-next-step.md
- ALASAN: [1-2 kalimat: mengapa belum tuntas]
- BUKTI: [Ringkasan mekanisme & titik terhenti, Path/File.ext:Lxx-Lyy]
- TANGGA_BUKTI: [B | C] *(`A` / `A-HEAD` yang sudah PASS tidak sah di sini — wajib ke `09` atau `08`)*
- DEPLOYMENT_MATCH: [LIVE_MATCH | HEAD-only (PROVEN_ON_REPO_HEAD) | UNVERIFIED (<sumber yang gagal>)]
- Jejak Kode Lokal yang Sudah Terbukti (`Path/File.ext:Lxx-Lyy`): [Alur kode lokal yang membuka celah apabila kondisi eksternal terpenuhi]
- Kondisi Penentu (*Trigger Condition*): [Jika parameter/state eksternal X bernilai Y, maka invariant INV-R1-xx pecah; jika bernilai Z, maka aman]

**PERCOBAAN:**

```text
$ [perintah nyata yang dijalankan]
[tempelkan log keluaran nyata]
```

*Baris perintah tanpa keluaran = pelanggaran `LAZY_BAILOUT_DETECTED`.*

- LANGKAH BERIKUTNYA: [Aksi konkret untuk menuntaskan pengujian]
