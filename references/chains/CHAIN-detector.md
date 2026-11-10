# [CHAIN-detector] Rantai: Deteksi Rantai 3-Level & Aturan Umum Lintas-Chain
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Proyek belum dinyatakan rantainya di `INTEL.md`, atau `path-map.md` memuat berkas dari beberapa ekosistem sekaligus (mis. `.sol` + `.rs` + `.move`).
- Paired Items: CHAIN-evm-tron, CHAIN-solana, CHAIN-sui-move, CHAIN-ton-async

---

## 1. Urutan Deteksi (wajib berurutan, bukan sebaliknya)

1. **Ekstensi berkas** — `.sol`/`.vy` → EVM/TVM · `.rs` + `Anchor.toml`/`declare_id!` → Solana · `.move` + `Move.toml` → Sui/Aptos · `.fc`/`.tact` + `blueprint.config.ts` → TON.
2. **Manifes build** — `foundry.toml`/`hardhat.config` · `Anchor.toml`/`Cargo.toml` · `Move.toml` · `package.json` + `blueprint`.
3. **Sinyal kode** — `msg.sender`/`msg.value` → EVM/TVM · `ctx.accounts`/`invoke` → Solana · `&mut`+`object::id`+`has key` → Move · `send_raw_message`+`recv_internal` → TON.

**Hasil tidak pasti WAJIB ditandai `CHAIN: AMBIGUOUS`** dan dicatat di `FACTS.md` domain `LINGKUNGAN` — dilarang menebak. Untuk Tron vs EVM: periksa `msg.tokenvalue`/`msg.tokenid` dan satuan `SUN` (6 desimal).

## 2. Aturan Umum Lintas-Chain (mengikat semua plugin `CHAIN-*`)

1. **Probe state WAJIB pada alamat yang MEMEGANG state** — proxy/account/object, **bukan** turunan kosong. Membaca impl proxy langsung akan menghasilkan state nol yang menyesatkan.
2. **Klaim nilai runtime WAJIB diukur** (chainid, saldo, slot, lamport, object version) — bukan diasumsikan.
3. **Kegagalan query BUKAN bukti ketiadaan.** `status: 0`, `revert 0x`, timeout, atau `eth_getLogs` terbatas rentang wajib diulang lewat sumber lain / `cast code` / `getAccountInfo` sebelum verdict negatif.
4. **Worker tunggal wajib.** `FOUNDRY_JOBS=1`, `CARGO_BUILD_JOBS=1`, `RAYON_NUM_THREADS=1`.
5. **Fork:** `--fork-url` endpoint publik dari `rpc-env.sh` (memuat `.env.rpc`; cek `RPC-STATUS.md`).
6. **Mode uji mengikuti `SIKLUS`** di kartu lead (`templates/05-raw-leads.md` §5). Proyek mainnet → `FORK_LIVE`; testnet/devnet → `FORK_TESTNET`; pre-deploy → `FORK_DEPLOYED_HEAD`/`LOKAL`.

## 3. Peta Rantai → Plugin

| Rantai | Plugin tooling/jebakan | POV khas |
| :--- | :--- | :--- |
| EVM (Ethereum/L2), Tron (TVM) | `CHAIN-evm-tron` | `POV-EVM-01` |
| Solana (SVM) | `CHAIN-solana` | `POV-SOL-01` |
| Move (Sui/Aptos) | `CHAIN-sui-move` | `POV-MOVE-01` |
| TON | `CHAIN-ton-async` | `POV-TON-01` |
