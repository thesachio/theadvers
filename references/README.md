# references/ — Rujukan Metode (dilampirkan penuh)

Semua berkas di sini **disalin utuh**, bukan di-link. Alasan: template harus tetap terbaca
saat offline dan tidak boleh bergantung pada versi skill yang berubah di luar repo.

## Registry & router

| Berkas | Isi | Dipakai di tahap |
|---|---|---|
| `ref-method-registry.md` | M-001..M-010 — registry metode bedah + 5 Jalur Permissionless + CLASS-A/B/C | C, D |
| `ref-attacker-pov.md` | Router POV 8-field + aturan deteksi rantai (ekstensi → manifes → sinyal kode) | B, C |

## Katalog POV (generator hipotesis — ditanya per pot)

| Berkas | Isi |
|---|---|
| `ref-pov-call.md` | Surface panggilan: callback, reentrancy, delegatecall, self-call seam |
| `ref-pov-defi.md` | Self-liquidation, bad-debt socialization, valuation vs execution |
| `ref-pov-math.md` | Indeks akrual desync, inverse rounding, salami |
| `ref-pov-chain.md` | Lintas-rantai & asinkron: pesan in-flight, interleaving, replay lintas-chain |

## Domain pendukung

| Berkas | Isi |
|---|---|
| `ref-calls-tokens-reentrancy.md` | Token non-standar, hook transfer, reentrancy |
| `ref-math-and-vaults.md` | Vault/share accounting, pembulatan arah salah |
| `ref-defi-oracles-liquidation.md` | Oracle staleness, manipulasi, jalur likuidasi |

## Tooling per rantai

| Berkas | Rantai |
|---|---|
| `ref-chain-evm-tron.md` | EVM + Tron (solc-tron, flatten) |
| `ref-chain-solana.md` | SVM/Rust-Anchor (cargo-build-sbf, account reload) |
| `ref-chain-sui-move.md` | Move (PTB, object splitting) |
| `ref-chain-ton-async.md` | TON (async bounce, recv_internal) |

## Harness & integritas

| Berkas | Isi |
|---|---|
| `ref-test-evm-advanced.md` | Teknik uji EVM lanjutan (fork, cheatcode, fuzz) |
| `ref-test-multichain-advanced.md` | Teknik uji multi-rantai |
| `ref-atomic-write.md` | Aturan tulis atomik (anti-truncate, `.tmp → fsync → os.replace`) |

## Aturan pemakaian

1. **POV = generator, bukan filter.** Tanya per pot: *"POV mana yang muat di uang ini?"*
   Jangan membaca 4 katalog lalu menyaring.
2. **Registry = rujukan tag.** Setiap lead `05` membawa `[LOAD: M-xxx]` dan `[AF-xx]`
   (bentuk serangan ada di `methodology/mod-attack-forms.md`).
3. **Jangan edit berkas di sini.** Perbaikan metode lewat `methodology/` + commit terpisah,
   supaya perubahan bisa dilacak.
