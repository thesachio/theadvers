# [M-008] Caller-Callee Assumption Seam & Direct Downstream Bypass
- Classes: CLASS-A (self-call `msg.sender == address(this)` / internal batch routing), CLASS-B, CLASS-C
- Trigger Symptom: Ada pasangan kontrak hulu→hilir (Router→Pool, Gateway→Vault, Manager→Strategy, Hub→Adapter), atau handler yang menerima pesan/instruksi dengan `sender`/`initiator` dari luar.
- Paired Items: AF-07, AF-08, AF-10, M-005, POV-relayer-mev

---

## 1. Inti Metode

Jangan mengunci metode ini pada nama modifier seperti `onlyRouter` atau `onlyManager`. Aturan umumnya:

> Periksa apakah jalur **hilir** benar-benar membatasi caller yang sah **DAN** mengulang seluruh validasi kritis — atau hanya mempercayai secara buta bahwa pemanggil **hulu** sudah melakukannya.

Metode ini juga menampung **jembatan off-chain / signature / relayer** (konsep v2): tanda tangan, Merkle/ZK proof, dan payload relayer adalah bentuk "hulu" yang klaimnya harus diverifikasi ulang di hilir.

### Manifestasi lintas-paradigma

| Runtime | Bentuk seam |
| :--- | :--- |
| EVM / Tron | Hulu `Router/Gateway/Manager` → Hilir `Pool/Vault/Strategy/Adapter`. Cek: apakah hilir membatasi `msg.sender`? Apakah `from`/`onBehalfOf`/`receiver` divalidasi ulang? |
| Solana | Instruksi program hilir yang seharusnya hanya sah via CPI dari program hulu terverifikasi, tetapi bisa dipanggil sebagai top-level instruction, atau tidak memeriksa signer/authority pemilik akun |
| Move (Sui/Aptos) | Fungsi modul hilir `public`/`public entry` bebas tanpa menuntut `Capability` dari modul hulu |
| TON | `recv_internal` di actor hilir memproses opcode internal tanpa memverifikasi `sender_address` adalah actor hulu resmi |

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Unvalidated Seam (celah lempar tanggung jawab).** Pada titik `Hulu → Hilir`: apakah Hulu meneruskan parameter (`receiver`, `from`, `onBehalfOf`, `token`, `data`, atau akun/objek) **tanpa** validasi karena mengira Hilir akan memvalidasinya — sementara Hilir percaya buta karena panggilan datang dari Hulu?
2. **Direct Downstream Bypass.** Jika validasi keamanan (slippage, whitelist, fee, access check) hanya ada di Hulu, periksa apakah penyerang dapat memanggil fungsi publik di Hilir **secara langsung**, melewati Hulu.
3. **Off-chain input.** Untuk signature/relayer/ZK: periksa nonce, domain separator, replay lintas-chain, `initiator`/`srcSender` pada callback, dan apakah `msg.sender` saja diperiksa tanpa `initiator`.
4. **Cross-Whitelist Confusion.** Apakah `isWhitelisted[x]` memverifikasi kecocokan pasangan aset (`pool.token() == asset`), atau hanya keberadaan alamat di daftar?

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** baris seam hulu→hilir dan/atau entrypoint hilir yang bisa dipanggil langsung, `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** PoC dengan *Victim Seeding* (korban yang sudah `approve`/menyetor) menembak hilir langsung atau menyuntikkan payload lewat seam hulu.
- **Titik 3:** delta nilai terukur (aset tertarik, validasi terlewati) + invariant yang pecah.

## 4. Routing Simulasi

- Periksa di kode hilir: apakah pemanggil dikunci ke alamat hulu tunggal **DAN** seluruh parameter kritis divalidasi penuh?
- Jika fungsi hilir bisa dipanggil langsung, atau menerima parameter bebas yang tidak divalidasi ulang → **wajib tulis PoC**.
- Bila hulu **dan** hilir sama-sama memvalidasi penuh (dibuktikan dengan kutipan keduanya) → `06` `REJECTED_MISMATCH`.

## 5. Kapan Metode Ini TIDAK Dipakai

- Tidak ada relasi hulu→hilir (kontrak tunggal tanpa pemanggil eksternal terpisah).
- Hilir mengunci `msg.sender` ke hulu tunggal **dan** memvalidasi ulang seluruh parameter kritis — dibuktikan per parameter.
