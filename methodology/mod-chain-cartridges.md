# MOD-CHAIN-CARTRIDGES — Tooling per Chain & Batas RPC

Plug-in METHODOLOGY-SEGITIGA tahap A/B/D. **Kontrak ekstensi**: chain baru = append satu blok.
Deteksi rantai tetap 3-level (ekstensi → manifes → sinyal kode) dari `ref-attacker-pov.md` §3;
hasil tidak pasti WAJIB ditandai `CHAIN: AMBIGUOUS`.

## EVM (Solidity/Vyper)

- **Census**: `cast balance/call/storage/code`; `getAccountInfo` tidak ada → pakai proxy slot
  EIP-1967. **WAJIB probe via PROXY**, bukan impl (storage impl kosong — pelajaran empiris dari run sebelumnya).
- **Parity**: `cast code` + disassembly dispatch (3 bentuk: `EQ`, `GT`, `SUB`-inverted; selector
  `0x00xx` jadi `PUSH3`(0x62)/`PUSH2`(0x61)); `deploy_parity.py` (SUDAH dipatch).
- **Jebakan**: `eth_call` tidak diskriminatif bila ada `fallback()` — pakai selector + probe.
- **Batas RPC (Alchemy)**: 300 CU/s; `eth_getLogs` ~75 CU, maks 10 blok free; `trace_*` tidak ada.
  → log lintas-blok lebar pakai publicnode; bila gagal, chunking + korelasi event manual.

## Solana (SVM/Rust-Anchor)

- **Census**: `solana account <pubkey>` / RPC `getAccountInfo` (lamport + rent); token via
  `getTokenAccountsByOwner`.
- **Parity**: `anchor build` + `cargo-build-sbf` (platform-tools `aarch64` v1.44 tersedia di VPS);
  `solana program dump <pid> <file.so>` untuk bytecode ter-deploy.
- **Batas Helius**: RPC 10 req/s; DAS 2 req/s; `getProgramAccounts` 5 req/s (10 kredit);
  `sendTransaction` 1 req/s; 1 jt kredit/bulan.
- **Jebakan**: keypair ≠ `declare_id!` → program closed; uji CPI vs top-level instruction (M-008);
  account post-CPI wajib `.reload()` (M-006 Prinsip A).

## Move (Sui/Aptos)

- **Census**: RPC `sui client object <id>` / `getObject`, `getDynamicFields`; Aptos REST account.
- **Parity**: `sui client publish --dry-run` / `aptos move compile`; compare `Package` on-chain.
- **POV**: POV-MOVE-01 (PTB capability & object splitting).

## TON

- **Census**: Toncenter `getAccountState`, `runGetMethod` (saldo jetton via `get_wallet_data`).
- **Async**: pesan bounce >224 bit / `ref`; handler `recv_internal` tanpa verifikasi `sender_address`
  (M-008); POV-TON-01.

## Aturan umum lintas-chain

1. Probe state WAJIB pada alamat yang MEMEGANG state (proxy/account/object), bukan turunan kosong.
2. Klaim nilai runtime WAJIB diukur (chainid, saldo, slot) — bukan diasumsikan.
3. Kegagalan query BUKAN bukti ketiadaan: ulangi via sumber lain sebelum verdict negatif.
4. Fork: `--fork-url` endpoint publik; `FOUNDRY_JOBS=1`, `CARGO_BUILD_JOBS=1`, `RAYON_NUM_THREADS=1`.
