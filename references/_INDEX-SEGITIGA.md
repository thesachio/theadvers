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

## Tahap mana yang memakai berkas ini

| Tahap | Peran berkas ini |
|---|---|
| A (`L-VALUE`) | kolom `LINGKUNGAN`/`DATA` boleh dirujuk saat menyusun census |
| B (`L-PATH`) | kelas `ASYNC` & transient-holder menentukan jahitan mana yang diburu |
| C (`L-FLOW`) | **utama** — generator metode & POV saat membedah pot/jahitan |
| D (`SIMULASI`) | routing ke harness sesuai rantai; Strike 1/2/3 |
| E (`OFFCHAIN`) | bila anomali melibatkan aktor luar |
| F (`VERDICT`) | hanya bagian "Batas Realitas" untuk menilai kelayakan gugur |
