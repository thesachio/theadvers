# money-ledger — Tahap A (L-VALUE)

**Aturan:** setiap baris WAJIB dari query nyata (`cast balance`, `cast call`, `getAccountInfo`),
bukan dari dokumentasi atau INTEL tanpa verifikasi ulang. Kolom `Bukti` memuat perintah +
keluaran, bukan narasi.

**WAJIB probe via PROXY** (slot EIP-1967), bukan impl — storage impl kosong
(`methodology/mod-chain-cartridges.md` §EVM).

## Skema

| Pot | Chain | Alamat (proxy) | Impl | Aset | Saldo | Konfigurasi live | EV | Status |
|---|---|---|---|---|---|---|---|---|

Kolom `Konfigurasi live` wajib memuat: owner/admin/crossDomainAdmin, pause flag, dan
whitelist/messenger yang relevan — bukan hanya saldo.

## EV ledger (diurutkan EV menurun — urutan kerja)

| # | Pot | EV (USD) | Sumber EV | Status |
|---|---|---|---|---|
| - | *belum ada — Tahap A belum dijalankan* | | | |

## Bukti query

```
# template
$ cast balance <addr> --rpc-url <rpc>
# <keluaran asli>
```

## Pot yang dibunuh di GATE-A (wajib dicatat + alasan)

| Pot | Alasan mati | Query pembunuh |
|---|---|---|
| - | - | - |
