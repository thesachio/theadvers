# [CHAIN-ton-async] Rantai: TON — Asinkron, Bounce 224-Bit, Gas Chain, Jetton Spoofing
- Classes: CLASS-B, CLASS-C
- Trigger Symptom: Target berbahasa FunC/Tact pada TON; `Path/File.ext` berkedip `.fc`/`.tact`; ada `send_raw_message`, handler `bounced`, `recv_internal`, atau alur pesan multi-hop.
- Paired Items: POV-TON-01, M-008, M-009, AF-09, CHAIN-offchain-sign-onchain-mutate

---

## 1. Hukum Utama TON

> **Tidak ada transaksi atomik lintas kontrak.** Kegagalan di kontrak hilir **tidak** membatalkan perubahan state di kontrak hulu secara otomatis.

Ini sumber utama semua kelas bug TON: state hulu sudah berubah, sementara hilir gagal dan hanya mengirim pesan pantulan yang **terpotong**.

## 2. Tooling & Census (STAGE-A/B)

- **Census:** Toncenter `getAccountState`, `runGetMethod` (saldo jetton via `get_wallet_data`).
- **Parity:** Blueprint/Tact build + bandingkan kode on-chain via `getAccountState`/`get_code`.

## 3. Jebakan Kode (STAGE-C)

1. **Handler `bounced` cacat — batas 224 bit.** Setiap kali fungsi mengubah state (mengurangi saldo, menandai pesanan, mencetak klaim) lalu `send_raw_message`, lacak apa yang terjadi bila tujuan gagal:
   - (a) Apakah pesan dikirim dengan flag *bounceable* (`0x18`) dan kontrak punya cabang `bounced` di `recv_internal`?
   - (b) **Jebakan batas 256-bit:** pesan `bounced` dipotong jaringan dan hanya mengembalikan **256 bit pertama** body (dikurangi prefix 32-bit `0xffffffff` → **tersisa 224 bit**). Bila jumlah dana atau alamat pengguna ditaruh setelah bit ke-224 atau di dalam `ref`, handler **tidak bisa membacanya** dan state/dana rusak permanen. Rujuk `POV-TON-01`.
2. **Putusnya rantai pesan akibat `msg_value` habis.** Pada alur `User → A → B → C`, jika A mengubah state sebelum memastikan `msg_value` cukup membayar `compute_fee` + `fwd_fee` untuk **seluruh rantai hingga C**, pesan bisa kehabisan gas di B. Kegagalan di fase *action* sering **tidak** memicu `bounced` utuh kembali ke A → desinkronisasi permanen.
3. **Pemalsuan notifikasi Jetton.** Jetton terdistribusi: setiap pemilik punya kontrak `Jetton Wallet` sendiri. Saat menerima `transfer_notification` (op `0x7362d09c`) atau `internal_transfer`, **DILARANG** mempercayai jumlah token di pesan. Kontrak wajib memverifikasi `sender_address` adalah `Jetton Wallet` resmi miliknya (atau menghitung `state_init` dari `Jetton Master`). Tanpa ini, penyerang membuat jetton palsu dan mengirim notifikasi bohong untuk menguras brankas.
4. **Race antar-pesan asinkron.** Pesan A→B memakan waktu antar-blok. Selama A menunggu callback dari B, pengguna/penyerang dapat menyisipkan pesan baru ke A. Periksa apakah A mengunci status pengguna/posisi (`is_locked` / `pending_query_id`) selama pesan *in-flight*. Rujuk `M-009`.
5. **Verifikasi `sender_address` pada `recv_internal`.** Handler internal yang menerima opcode administratif tanpa memeriksa `sender_address` adalah actor hulu resmi → padanan TON dari `M-008` (caller-callee seam).

## 4. Eksekusi (STAGE-D)

- Harness: Blueprint (`blueprint test`) / `@ton/sandbox`.
- PoC bounce wajib: kirim pesan → paksa gagal di tujuan → amati hasil handler `bounced`.
- PoC interleaving wajib: kirim dua pesan sebelum bounce pertama tiba.
- Fuzz wajib mengacak: ukuran payload di sekitar 224-bit, `msg_value` gas, jeda antar-pesan.
