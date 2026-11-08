# path-map — Tahap B (L-PATH)

**Pertanyaan:** ke mana uang MENGALIR, bukan hanya mengendap.

Node = kontrak. Edge = aliran dana (transfer / bridge / mint-burn / reward).
Tiap jahitan diberi `EV = max(balance_now, throughput_path)`.

## Skema jahitan

| # | Jahitan | Dari → Ke | Chain | Kelas | balance_now | throughput_path | EV | Aktor hop | Status |
|---|---|---|---|---|---|---|---|---|---|

Kolom `Kelas`: `SYNC` (satu transaksi) atau `ASYNC` (bridge hop / pesan in-flight — zona
observasi khusus, lihat `[AF-09]`).

Kolom `Aktor hop`: `on-chain` atau `off-chain` (dataworker, disputer, relayer, keeper).
Hop `off-chain` adalah pemicu Tahap E.

## Kelas kontrak transient-holder (GATE-B: zero-balance tapi WAJIB diburu)

| Kontrak | balance_now | Di jalur apa | Kenapa tetap diburu |
|---|---|---|---|
| *belum ada — Tahap B belum dijalankan* | | | |

## Cartridge domain yang aktif untuk target ini

| Domain cartridge | Dipakai? | Alasan |
|---|---|---|
| BRIDGE | ya | inti Across (hub-and-spoke, merkle bundle) |
| LP/AMM | belum diputuskan | perlu dicek apakah ada AMM di scope |
| LENDING | belum diputuskan | perlu dicek (bad debt / liquidation) |
| STAKING/REWARDS | belum diputuskan | perlu dicek (LP rewards di HubPool) |
| NFT | tidak | tidak relevan |
| DERIVATIF | belum diputuskan | perps di HyperCore handler? perlu dicek |

Kolom "belum diputuskan" wajib diputuskan sebelum GATE-B ditutup.
