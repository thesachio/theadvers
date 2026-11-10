# [CHAIN-sui-move] Rantai: Move (Sui/Aptos) — Tooling, ID Objek, Hot Potato, Geser Bit
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Target berbahasa Move pada Sui/Aptos; `Path/File.ext` berkedip `.move`; fungsi menerima ≥2 objek, memakai struct Hot Potato, `Capability`, atau matematika kustom dengan `<<`.
- Paired Items: POV-MOVE-01, M-006, M-007, M-008, CHAIN-rounding-amplification-drain

---

## 1. Tooling & Census (STAGE-A/B)

- **Census:** RPC `sui client object <id>` / `getObject`, `getDynamicFields`; Aptos REST account.
- **Parity:** `sui client publish --dry-run` / `aptos move compile`; bandingkan `Package` on-chain.

## 2. Jebakan Kode (STAGE-C)

1. **Kebingungan ID lintas-objek.** Data disimpan di objek mandiri (`has key`). Ketika fungsi menerima ≥2 objek (`pool: &mut Pool<A,B>` dan `position: &mut Position` atau `receipt: &Receipt`), **kepemilikan tipe Move tidak menjamin `position` berasal dari `pool` yang sama**. Wajib ada asersi eksplisit: `assert!(position.pool_id == object::id(pool), EWrongPool)`. Tanpa ini, penyerang membuat Pool baru dengan koin tak berharga, mencetak `Position` besar di sana, lalu memakainya menguras Pool utama. Rujuk `POV-MOVE-01`.
2. **Hot Potato & PTB.** Pemanggil dapat merangkai puluhan panggilan dalam satu PTB atomik tanpa menulis kontrak baru. Untuk alur flash loan/bertahap, periksa struct **Hot Potato** (tanpa kemampuan `drop`, `store`, `key`): (a) apakah tidak sengaja diberi `drop`/`store` sehingga pinjaman tak perlu dikembalikan? (b) apakah menyimpan & memverifikasi `pool_id` serta jumlah bayar kembali? (c) apakah ada fungsi publik lain yang dapat mengonsumsi/menghancurkannya dengan syarat lebih ringan?
3. **Overflow pada geser bit & matematika kustom (kasus Cetus $223M).** VM Move memeriksa overflow pada `+`, `-`, `*`, tetapi **`<<` pada `u64`/`u128`/`u256` tidak memeriksa bit signifikan yang tergeser keluar** (akan *abort* hanya bila jumlah geseran melebihi lebar bit). Periksa `checked_shlw`, `mul_shr`, `sqrt_price`, likuiditas CLMM: kesalahan satu bit pada batas mask memungkinkan angka besar terpotong menjadi `1` saat dihitung sebagai kewajiban setor, namun mencetak likuiditas penuh.
4. **Kebocoran `Capability` & pembekuan shared object.** Periksa fungsi yang menerima/mengembalikan `AdminCap`, `TreasuryCap`, `UpgradeCap`: jangan sampai ada fungsi publik yang mengizinkan peminjaman mutlak atau *wrapping* capability oleh pihak tak berhak. Pastikan shared object (`Pool`, `GlobalState`) **tidak pernah** bisa dikirim ke alamat pribadi via `transfer::public_transfer` — itu mengubahnya jadi owned object dan membekukan protokol selamanya.
5. **Substitusi tipe generik (`Phantom Type<T>` spoofing).** Pada `public fun execute<CoinA, CoinB>(...)`, pastikan tipe generik benar-benar terikat pada objek yang diproses — bukan hanya lolos pemeriksaan tipe compile-time.

## 3. Eksekusi (STAGE-D)

- Harness: `sui move test` / `aptos move test`, atau PTB nyata di devnet lokal.
- Kasus `<<`: fuzz wajib mengacak `shift` di sekitar batas (`127`, `128`, `255`, `256`).
- Kasus ID objek: PoC wajib membuat objek palsu **dan** memakainya pada objek asli dalam satu PTB utuh.
