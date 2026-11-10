# [M-006] Stale Local-Snapshot Write-Back & Duplicate-Reference Aliasing (`[A, A]`)
- Classes: CLASS-A (Prinsip B), CLASS-B & CLASS-C (Prinsip A & B)
- Trigger Symptom: Fungsi menyalin state ke variabel lokal lalu memanggil keluar sebelum menulisnya kembali; atau menerima ≥2 akun/objek/parameter daftar yang mungkin menunjuk identitas sama.
- Paired Items: AF-04, AF-05, M-003, M-010, POV-unprivileged

---

## 1. Inti Metode

Pisahkan tegas antara **prinsip mekanis universal** dan **istilah implementasi bahasa** (`memory`/`storage` adalah istilah Solidity/EVM, bukan prinsipnya).

**Prinsip A — Snapshot Lokal yang Stale Ditulis Kembali**
> Snapshot lokal yang stale ditulis kembali setelah interaksi eksternal/lintas-komponen, sehingga perubahan terbaru pada state persisten terhapus secara senyap.

Urutan yang dicari: **baca ke variabel lokal → mutasi state persisten via subcall/CPI/callback/fungsi lain → tulis balik variabel lokal lama ke state persisten**.

**Prinsip B — Referensi Kembar Diproses Dua Kali (`[A, A]`)**
> Dua argumen atau elemen daftar yang menunjuk ke identitas/akun/objek/resource yang sama diproses berulang sebelum state dimutasi atau tanpa deduplikasi.

### Manifestasi lintas-paradigma

| Runtime | Prinsip A | Prinsip B |
| :--- | :--- | :--- |
| EVM / Tron | `Struct memory s = map[user]` → panggilan keluar mengubah `map[user]` → `map[user] = s` | array input `[id, id]`, atau `(from, to)` dengan alamat sama |
| Solana | account data dideserialisasi sebelum CPI, ditulis balik setelah CPI tanpa `.reload()` | duplicate writable account, repeated `ctx.remaining_accounts` |
| Move (Sui/Aptos) | field dibaca ke variabel lokal sebelum memanggil modul lain, lalu menimpa field objek | duplicate object reference / duplicate recipient dalam PTB/vector |
| TON | state dibaca sebelum rantai pesan mengubahnya lalu ditimpa kembali | duplicate actor / message entry |

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. Cari fungsi yang menyalin struktur/saldo ke variabel lokal, melakukan panggilan keluar atau memanggil helper yang memutasi state sama, lalu menulis balik salinan lokal di akhir fungsi.
2. Pada setiap fungsi yang menerima ≥2 akun/objek atau parameter daftar: uji referensi kembar `[A, A]`. Periksa apakah ada pemeriksaan ketidaksetaraan / deduplikasi sebelum mutasi.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** urutan baca→mutasi→tulis-balik (Prinsip A) atau daftar argumen kembar (Prinsip B), `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** PoC yang memicu mutasi persisten di tengah, lalu membuktikan state tertimpa; untuk Prinsip B, PoC dengan `[A, A]` yang menggandakan efek.
- **Titik 3:** selisih state (seharusnya vs sesudah) + invariant yang pecah.

## 4. Routing Simulasi

- **Prinsip A:** pastikan urutan baca-lokal → mutasi-persisten → tulis-balik benar-benar **ada** di kode. Bila terbukti tidak ada penulisan balik setelah interaksi → gugur ke `06` (`REJECTED_MISMATCH`, kemustahilan statis **KS-1**). Bila ada → **langsung tulis PoC**.
- **Prinsip B:** PoC wajib memakai input kembar nyata, bukan simulasi mental. Kurangnya deduplikasi tanpa dampak terukur → `06` dengan log.

## 5. Kapan Metode Ini TIDAK Dipakai

- Tidak ada panggilan keluar di antara baca dan tulis state yang sama.
- Semua entrypoint yang menerima ≥2 identitas sudah memvalidasi ketidaksetaraan secara eksplisit (`require(a != b)`), dan fuzz tidak menemukan jalur melewatinya.
