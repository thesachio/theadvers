# [CHAIN-solana] Rantai: Solana (SVM/Rust/Anchor) — Tooling, Jebakan Akun, Batas RPC
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Target berbahasa Rust/Anchor pada Solana; `Path/File.ext` berkedip `.rs`; instruksi menerima `ctx.remaining_accounts`, beberapa akun bertipe sama, atau melakukan CPI lalu membaca ulang data akun.
- Paired Items: POV-SOL-01, M-006, M-008, AF-05, CHAIN-shared-state-desync

---

## 1. Tooling & Census (STAGE-A/B)

- **Census:** `solana account <pubkey>` atau RPC `getAccountInfo` (lamport + rent); token via `getTokenAccountsByOwner`.
- **Parity:** `anchor build` + `cargo-build-sbf` (platform-tools `aarch64` v1.44 tersedia di VPS); `solana program dump <pid> <file.so>` untuk bytecode ter-deploy.
- **Batas RPC (Helius):** RPC 10 req/s; DAS 2 req/s; `getProgramAccounts` 5 req/s (10 kredit); `sendTransaction` 1 req/s; 1 juta kredit/bulan. Bila terkena limit, mundur eksponensial dan cache hasil.

## 2. Jebakan Kode (STAGE-C)

1. **Akun dinamis tak terverifikasi (`remaining_accounts` spoofing).** Akun via `ctx.remaining_accounts` **tidak** divalidasi otomatis oleh `#[derive(Accounts)]`. Setiap akun yang dibaca/ditulis wajib diperiksa manual: (a) `owner` programnya, (b) diskriminator tipe datanya, (c) ikatan `key()` ke `Pool`/`State` utama — mencegah penyisipan tick/bitmap dari pool palsu.
2. **Ketiadaan pemeriksaan signer, owner, & ikatan data.** Setiap akun otoritas wajib `Signer<'info>` / `account.is_signer`. Akun berelasi (`UserPosition` ↔ `LendingMarket`) wajib `has_one = market` atau `constraint = user_position.market == market.key()`. Tanpa ini penyerang memasangkan posisi dari pasar palsu ke pasar utama.
3. **Data akun basi setelah CPI (missing `.reload()`).** `Account<'info, T>` mendeserialisasi **hanya di awal instruksi**. Setelah CPI `transfer`/`mint`, `token_account.amount` di memori lokal **tidak berubah**. Membacanya tanpa `reload()?` = memakai saldo pra-transfer. Rujuk `POV-SOL-01`.
4. **Tabrakan benih PDA & `init_if_needed`.** Periksa `seeds = [...]`: apakah seluruh parameter kunci (`user.key()`, `mint.key()`, `pool.key()`) masuk benih? `init_if_needed` jangan sampai mengizinkan inisialisasi ulang atau penimpaan otoritas.
5. **Penutupan akun cacat (account revival) & CPI arbitrer.** Saat menutup akun, selain menguras lamport ke `0`, data wajib dihapus dan `owner` diubah ke System Program — jika tidak, akun bisa *revived* dengan menyetor lamport di instruksi berikutnya dalam transaksi yang sama. Pada setiap `invoke`/`invoke_signed`, `program_id` target wajib dikunci ke program resmi, bukan akun program sembarang dari pemanggil.
6. **Token-2022 extensions & overflow Rust.** Untuk SPL Token-2022, periksa penanganan ekstensi *Transfer Fee* (potongan saat transfer) dan *Transfer Hook*. Bila `Cargo.toml` tidak mengaktifkan `overflow-checks = true`, operasi `+`/`-`/`*` berisiko *wrapping overflow* di mode rilis.

## 3. Eksekusi (STAGE-D)

- Harness: `solana-program-test` / `cargo test-sbf`. `CARGO_BUILD_JOBS=1`.
- Akun kembar dan `remaining_accounts` wajib diuji dengan runtime nyata, bukan pembacaan kode.
- Bila RPC utama gagal, fallback ke endpoint publik dan chunking `getProgramAccounts`.
