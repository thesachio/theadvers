# [CHAIN-evm-tron] Rantai: EVM (Ethereum/L2) & Tron (TVM) — Tooling, Jebakan, Batas RPC
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Target berbahasa Solidity/Vyper pada jaringan EVM (Ethereum, L2) atau Tron TVM; `Path/File.ext:Lxx-Lyy` berkedip `.sol`; ada proxy/upgradeable, signature/permit, atau `msg.value` di loop/multicall.
- Paired Items: POV-EVM-01, M-005, M-010, AF-07, CHAIN-flash-oracle-liquidation

---

## 1. Tooling & Census (STAGE-A/B)

- **Census:** `cast balance` / `cast call` / `cast storage` / `cast code`; `getAccountInfo` tidak ada → pakai slot proxy.
- **WAJIB probe via PROXY, bukan impl** — storage impl kosong. Pelajaran empiris: membaca impl langsung menghasilkan state nol yang menyesatkan.
- **Parity:** `cast code` + disassembly dispatch (3 bentuk selector: `EQ`, `GT`, `SUB`-inverted; selector `0x00xx` muncul sebagai `PUSH3`(0x62)/`PUSH2`(0x61)); gunakan `tools/deploy_parity.py`.
- **Batas RPC (Alchemy):** 300 CU/s; `eth_getLogs` ~75 CU, maks 10 blok gratis; `trace_*` tidak tersedia. Untuk log lintas-blok lebar pakai publicnode; bila gagal, chunking + korelasi event manual.

## 2. Jebakan Kode (STAGE-C)

1. **`msg.value` di dalam loop / Multicall / delegatecall.** Nilai `msg.value` **tetap** sepanjang konteks panggilan dan **tidak berkurang** setelah dibaca. Di dalam `for`, atau pada kontrak yang mewarisi `Multicall` (`delegatecall`), pemanggil dapat mengirim `1 unit` satu kali dan memakainya berulang di setiap iterasi. Rujuk `POV-EVM-01`.
2. **Proxy, upgradeability, & implementasi tak terinisialisasi.** Apakah impl memanggil `_disableInitializers()` di `constructor()`? Tanpa itu siapa pun dapat memanggil `initialize()` langsung pada impl. Apakah `initialize()` bisa dipanggil lebih dari sekali? Ada tabrakan slot proxy↔impl?
3. **Kriptografi, EIP-712, Permit, Merkle.** Signature replay: apakah hash mengikat `nonce` (dinaikkan di storage), `block.chainid`, dan `address(this)`? Zero-address `ecrecover`: apakah diverifikasi `signer != address(0)`? Permit front-running DoS: `token.permit(...)` tanpa `try/catch` dapat diambil dari mempool sehingga transaksi utama `revert`. **Jangan** `abi.encodePacked` pada >1 tipe dinamis (`string`, `bytes`, `array`).
4. **Bridge / relayer message spoofing.** Jika Messenger/Relayer mengeksekusi `_to.call(_data)`, periksa apakah **seluruh** kontrak internal berhak istimewa yang mempercayai `msg.sender == Messenger` sudah masuk blacklist `_to`.
5. **EIP-1153 Transient Storage & Return Bomb.** `TSTORE`/`TLOAD` wajib dibersihkan (`TSTORE(slot, 0)`) di akhir panggilan agar tidak bocor ke sub-panggilan berikutnya dalam transaksi yang sama. `.call()` ke alamat tak dipercaya → waspadai returndata raksasa yang menghabiskan gas pemanggil.

## 3. Khusus Tron (TVM)

- `1 TRX = 10^6 SUN` (**6 desimal**), **bukan** 18 desimal seperti `1 ether = 10^18 wei`. Periksa semua kode warisan EVM yang masih mengalikan/membagi dengan `1e18`.
- Waspadai pemisahan pembayaran native TRX (`msg.value`) dan token bawaan TRC-10 (`msg.tokenvalue` & `msg.tokenid`), serta keunikan penanganan *Energy* pada panggilan eksternal TVM.

## 4. Fork & Eksekusi (STAGE-D)

- `--fork-url` endpoint publik (`rpc-env.sh` / `.env.rpc`, cek `RPC-STATUS.md`).
- `FOUNDRY_JOBS=1` wajib (worker tunggal).
- Mode uji mengikuti `SIKLUS` di kartu lead (`templates/05-raw-leads.md` §5); proyek mainnet → `FORK_LIVE`.
