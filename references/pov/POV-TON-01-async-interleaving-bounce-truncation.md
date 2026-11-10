# [POV-TON-01] Sudut Pandang: Async Message Interleaving & Bounce Payload Truncation
- Classes: CLASS-C (Multi-Entity Async Actor Chain: Sender → Actor A → Actor B → Bounce)
- Trigger Symptom: Kontrak TON mengubah state lokal lalu mengirim pesan (`send_raw_message`) dengan mengandalkan handler `bounced` (>224 bit / `ref`) atau tanpa mengunci state pengguna selama pesan masih *in-flight*.
- Paired Items: M-002, M-007, M-009, AF-09, CHAIN-ton-async, POV-griefer

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang dapat mengirim dua pesan berurutan (atau mengatur `msg_value` gas) ke kontrak aktor target. Tidak butuh peran admin.

## 2. Gejala di Kode

1. Pesan keluar menaruh data penting untuk pemulihan (jumlah nilai, ID posisi, atau alamat pemilik) **setelah bit ke-224** dari body pesan utama atau di dalam referensi *child cell* (`ref`), padahal jaringan memotong pesan bounced hanya menyisakan 224 bit data pertama **tanpa `ref`**.
2. Selama pesan pertama masih *in-flight* menunggu balasan, status akun/posisi pengirim **tidak dikunci** (*pending lock*), sehingga pengguna dapat mengirim pesan kedua yang memodifikasi state yang sama.

Prinsip umumnya: (1) adalah **padanan asinkron dari pemangkasan data di langkah antara** (`POV-MOVE-01` / `M-007`) — payload hilang sebelum rollback sempat berjalan; (2) adalah **padanan asinkron dari status menggantung** (`M-009`) — state tidak terkunci selama siklus belum selesai.

## 3. Rangkaian Serangan

1. **Siapkan:** siapkan state awal pada kontrak asal dan atur kondisi (atau takaran `msg_value` gas) agar pesan gagal di kontrak tujuan; atau siapkan pesan kedua saat pesan pertama masih *in-flight*.
2. **Picu:** kontrak tujuan menolak pesan dan memantulkan pesan bounced yang telah terpotong; atau dua pesan *in-flight* diproses berurutan terhadap state yang sama.
3. **Ekstraksi:** handler bounce memulihkan state dengan data yang sudah hilang/terpotong, sehingga saldo tidak kembali atau kembali ke pihak yang salah; atau pesan kedua memakai state yang seharusnya sudah terkunci.

## 4. Auditor Blindspot

Auditor menganggap handler `bounced` sudah menangani kegagalan — **tanpa menghitung batas 224 bit dan hilangnya `ref`**, dan tanpa memeriksa apakah state dikunci selama pesan *in-flight*.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila seluruh data pemulihan berada di ≤224 bit pertama tanpa `ref`, **dan** state pengguna dikunci selama pesan *in-flight* (kutipan kedua kondisi).
- **Wajib PoC** di Blueprint/Tact (`blueprint test` / `@ton/sandbox`): kirim pesan → paksa gagal di tujuan → amati hasil handler bounce; untuk interleaving, kirim dua pesan sebelum bounce pertama tiba.
- Fuzz wajib mengacak: ukuran payload (di sekitar 224-bit), `msg_value` gas, dan jeda antar-pesan.
