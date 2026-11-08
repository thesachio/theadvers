# TARGET PIN — across-protocol/contracts

Berkas ini mengunci **apa yang diaudit**. Tanpa pin, temuan tidak bisa direproduksi
dan tidak bisa dibandingkan dengan run sebelumnya.

## Commit teraudit

| Field | Nilai |
|---|---|
| Repo | `https://github.com/across-protocol/contracts` |
| Branch | `master` |
| Commit | `d0725ea001ca119a529065c22134298ec353941c` |
| Commit subject | `chore(deps): bump ethers to 5.8.0 (#1597)` |
| Diverifikasi | `git rev-parse HEAD` + `git rev-parse origin/master` = identik, `rev-list --count HEAD..origin/master` = **0** (2026-11-08) |

**Catatan penting:** commit ini **identik** dengan yang dipakai run `across2`.
Konsekuensi metodologis:

- Kode target tidak berubah → run 3 **bukan** audit kode baru.
- Nilai run 3 sepenuhnya bergantung pada **perbedaan metode**, bukan perbedaan kode.
- Klaim "temuan baru" wajib dibuktikan sebagai *false negative yang terlewat metode lama*,
  bukan sekadar lead yang sama dengan nama berbeda.

## Perubahan kode sejak run 1

| Run | Commit | Selisih |
|---|---|---|
| `across` (run 1) | `b1c4e862` (`fix(ci): use Node 22.23.4`) | baseline |
| `across2` (run 2) | `d0725ea0` (`chore(deps): bump ethers`) | +4 commit (deps/CI, bukan logika kontrak) |
| `across3` (run 3) | `d0725ea0` (sama dengan run 2) | **0** |

## Cara menurunkan ulang (reproducible checkout)

```bash
# 1. Clone source asli (jangan modifikasi)
git clone https://github.com/across-protocol/contracts.git /path/to/contracts
cd /path/to/contracts
git checkout d0725ea001ca119a529065c22134298ec353941c
git submodule update --init --recursive      # lib/forge-std, lib/sp1-contracts, lib/murky

# 2. Verifikasi pin
git rev-parse HEAD                           # wajib: d0725ea001ca119a529065c22134298ec353941c

# 3. Build (WAJIB single-job; build penuh OOM di VPS ini)
source .env.audit 2>/dev/null || export FOUNDRY_JOBS=1
FOUNDRY_JOBS=1 forge build contracts/
```

## Kawasan yang TIDAK berubah tapi wajib dicatat

Folder repo yang **bukan** kontrak utama namun masuk scope bounty Across
("most of the code within the `across-protocol` repository"):

- `programs/` — Solana/Anchor (SVM spoke, sponsored CCTP program)
- `script/` — Foundry deploy + operational tasks
- `deployments/`, `broadcast/deployed-addresses.json` — peta alamat live
- `generated/`, `idls/` — artefak ABI/IDL

Folder repo penunjang (bukan `across-protocol/contracts`):

- `exclusive-relayer-configs` @ `add8b51`
- `relayer-registration-repository` @ `94a3b74`
- `v5-token-pricing` @ `5812579`

Ketiga repo ini **kanal off-chain** (Tahap E). Status di run 1-2: belum dibedah
(`grep -rc "L-OFFCHAIN" audit/notes/*.md` = 0 hasil di `across2`).
