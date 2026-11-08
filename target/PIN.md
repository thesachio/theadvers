# TARGET PIN — <org>/<repo>

Berkas ini mengunci **apa yang diaudit**. Tanpa pin, temuan tidak bisa direproduksi
dan tidak bisa dibandingkan lintas run.

## Commit teraudit

| Field | Nilai |
|---|---|
| Repo | `https://github.com/<org>/<repo>` |
| Branch | `<branch>` |
| Commit | `<40-char hash>` |
| Commit subject | `<subject>` |
| Diverifikasi | `<perintah>` → `<keluaran>` (`YYYY-MM-DD`) |

## Riwayat run (isi bila ini audit ulang)

| Run | Commit | Selisih |
|---|---|---|
| run 1 | `<hash>` | baseline |
| run 2 | `<hash>` | `<n> commit — <sifat perubahan>` |
| run 3 | `<hash>` | `<n>` |

Bila commit identik dengan run sebelumnya, baca `audit/METHODOLOGY-DELTA.md`:
run ulang pada kode identik **bukan** audit kode baru, dan klaim temuan baru wajib
dibuktikan sebagai false negative run lama.

## Cara menurunkan ulang (reproducible checkout)

```bash
# 1. Clone source asli (JANGAN modifikasi — kode target read-only)
git clone https://github.com/<org>/<repo>.git /path/to/target
cd /path/to/target
git checkout <commit>
git submodule update --init --recursive   # bila ada .gitmodules

# 2. Verifikasi pin
git rev-parse HEAD                        # wajib sama dengan tabel di atas

# 3. Build (selalu single-job di mesin terbatas; build penuh bisa OOM)
export FOUNDRY_JOBS=1
forge build contracts/                    # atau path spesifik, bukan seluruh repo
```

Aturan build per rantai ada di `methodology/mod-chain-cartridges.md`
(`CARGO_BUILD_JOBS=1` untuk Rust, `RAYON_NUM_THREADS=1`).

## Kawasan di luar kontrak utama yang wajib dicatat

Folder repo yang bukan kontrak utama namun sering masuk scope bounty:

- `script/` — deploy + operational tasks
- `deployments/`, `broadcast/` — peta alamat live
- `generated/`, `idls/` — artefak ABI/IDL
- `<isi sendiri: programs/, packages/, dst.>`

## Repo / kanal pendukung (Tahap E — offchain)

| Repo / kanal | URL | Commit | Status bedah |
|---|---|---|---|
| `-` | `-` | `-` | belum |

Cek dulu apakah scope bounty target memang mencakup off-chain
(`methodology/mod-offchain.md` §Pemicu). Bila tidak, kolom ini boleh kosong.
