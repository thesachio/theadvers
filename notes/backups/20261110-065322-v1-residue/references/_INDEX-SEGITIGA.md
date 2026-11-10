# INDEKS PENERAPAN SEGITIGA (ditempel di setiap `ref-*.md`)

Blok ini menjelaskan **bagaimana berkas referensi ini dipakai** di workflow segitiga
(Tahap A–F). Tanpa blok ini, agen membacanya sebagai metode lama dan memakai istilah yang
sudah tidak berlaku.

## Istilah: lama → baru

| Istilah lama | Padanan segitiga |
|---|---|
| Fase 2 (hunt) | **Tahap C** (`L-FLOW`) |
| Fase 3 (lab/PoC) | **Tahap D** (`SIMULASI`) |
| Fase 4 (verdict) | **Tahap F** (`VERDICT`) |
| Fase 1 (recon) | **Tahap A** (`L-VALUE`) + **Tahap B** (`L-PATH`) |
| Fase 0 (intel) | **Tahap A0** (`BOOTSTRAP`) |
| Putaran 1 / Putaran 2 | **Tahap C** (bedah) / **Tahap C** (sintesis lintas-jahitan) |
| unit `S-n` dari `03-attack-surface-queue.md` | **pot** (`money-ledger.md`) atau **jahitan** (`path-map.md`) |
| `00b-file-inventory.md` | *tidak dipakai* — populasi diganti census `money-ledger` |
| `01-threat-and-env.md` | *tidak dipakai* — aset/otoritas hidup di `money-ledger` + `FACTS` `LINGKUNGAN` |
| `02-state-and-var-matrix.md` | *tidak dipakai* — delta state ditulis per lead di `05` |
| `00-project-map.md` | `target/PIN.md` (pin) + `path-map.md` (aliran) |

## Posisi berkas referensi ini terhadap tiga sumbu

Setiap lead di `05` membawa tiga tag ortogonal (lihat `CLASSIFICATION.md`):

- `[LAPIS: VALUE|PATH|FLOW]` — **asal lead**
- `[CLASS-A|B|C]` — **topologi entitas** (menentukan paket metode wajib)
- `[AF-xx]` — **bentuk serangan** (`methodology/mod-attack-forms.md`)

Berkas `ref-*.md` memberi konten untuk **sumbu apa** — lihat baris di bawah.

## Aturan pakai

1. **Referensi adalah generator hipotesis, bukan penentu prioritas.** Prioritas tetap EV
   menurun dari `money-ledger.md`.
2. **Gejala kode adalah pemicu tunggal.** Kolom `Kelas Entitas Tipikal` menunjukkan topologi
   **tipikal**, bukan pembatas — gejala di `CLASS-A` boleh membuka katalog `CLASS-C`.
3. **`[LAPIS]` wajib diisi saat lead ditulis.** Bila sebuah metode menemukan anomali
   *tanpa* lewat census nilai atau peta aliran (murni bedah kode), lapisnya `FLOW`.
4. **`[CLASS-x]` wajib diisi** — tanpanya paket metode wajib tidak diketahui.
5. **`[AF-xx]` wajib diisi** — tanpanya lead ditolak G1.

## Matriks: berkas referensi × tahap

Dibaca sebagai: `●` = dipakai aktif di tahap itu · `○` = dirujuk sesekali · `—` = tidak dipakai.

Tahap: **A** = L-VALUE (census) · **B** = L-PATH (peta aliran) · **C** = L-FLOW (bedah) ·
**D** = SIMULASI (PoC/fuzz) · **E** = OFFCHAIN · **F** = VERDICT.

| Berkas | A | B | C | D | E | F | Peran utama |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `ref-method-registry.md` | — | ○ | ● | ● | — | ○ | M-001..M-010 + 5 Jalur + CLASS-A/B/C |
| `ref-attacker-pov.md` | — | ○ | ● | — | ○ | — | router gejala → POV |
| `ref-pov-call.md` | — | — | ● | ○ | — | — | katalog POV penyerahan kontrol |
| `ref-pov-defi.md` | — | — | ● | ○ | — | — | katalog POV DeFi/likuidasi |
| `ref-pov-math.md` | — | ○ | ● | ○ | — | — | katalog POV akrual/pembulatan |
| `ref-pov-chain.md` | — | ● | ● | ○ | — | — | katalog POV per rantai (zona ASYNC) |
| `ref-calls-tokens-reentrancy.md` | — | ○ | ● | ○ | — | — | checklist token/hook/reentrancy |
| `ref-math-and-vaults.md` | ○ | — | ● | ○ | — | — | checklist pembulatan/share |
| `ref-defi-oracles-liquidation.md` | — | ○ | ● | ○ | — | — | checklist oracle/likuidasi |
| `ref-chain-evm-tron.md` | ● | ○ | ○ | ○ | — | ○ | tooling EVM/Tron |
| `ref-chain-solana.md` | ● | ○ | ○ | ○ | — | ○ | tooling Solana |
| `ref-chain-sui-move.md` | ● | ○ | ○ | ○ | — | ○ | tooling Sui/Aptos |
| `ref-chain-ton-async.md` | ● | ○ | ○ | ○ | — | ○ | tooling TON |
| `ref-test-evm-advanced.md` | — | — | — | ● | — | ○ | harness uji EVM (Tier 1-5) |
| `ref-test-multichain-advanced.md` | — | — | — | ● | — | ○ | harness uji non-EVM (Tier 6) |
| `ref-atomic-write.md` | ● | ● | ● | ● | ● | ● | protokol tulis (semua tahap) |

### Bacaan kunci

- **Tahap C adalah pusat gravitasi** — 9 dari 16 berkas aktif di sini. Wajar: C adalah
  tempat hipotesis lahir.
- **Tahap A hanya butuh 5 berkas** (4 `ref-chain-*` + `ref-atomic-write`). Census nilai
  tidak butuh POV atau harness — hanya tooling rantai.
- **Tahap D hanya butuh 4** (`ref-test-*`, `ref-method-registry`, `ref-atomic-write`).
  Jangan membawa katalog POV ke lab; itu generator, bukan bahan harness.
- **Tahap E tidak butuh berkas khusus** — offchain dipandu `methodology/mod-offchain.md`;
  referensi hanya dirujuk bila anomali menyentuh kode.
- **`ref-atomic-write.md` satu-satunya yang ● di semua tahap** karena ia mengatur cara
  menulis artefak, bukan isi analisis.

### Aturan beban baca (hemat token)

| Tahap | Wajib dibuka | Dilarang dibuka |
|---|---|---|
| A | `ref-chain-<rantai>.md`, `ref-atomic-write` | seluruh `ref-pov-*`, `ref-test-*` |
| B | `ref-pov-chain.md` (jahitan ASYNC), `ref-chain-<rantai>` | `ref-test-*` |
| C | `ref-method-registry` + `ref-attacker-pov`, lalu **hanya 1-2** `ref-pov-*` yang gejalanya cocok | 4 katalog POV sekaligus |
| D | `ref-test-*`, `ref-method-registry` (routing) | `ref-attacker-pov` (sudah selesai tugasnya) |
| E | `methodology/mod-offchain` + `ref-calls-tokens-reentrancy` bila perlu | `ref-test-*` |
| F | `templates/VERDICT` + `ref-method-registry` (ambang gugur) | seluruh `ref-pov-*` |
