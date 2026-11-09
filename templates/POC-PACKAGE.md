# POC-PACKAGE — Aturan Paket Proof-of-Concept

PoC yang tidak dapat dijalankan orang lain **bukan bukti**. Berkas ini mengatur isi paket
`poc/` di repo inbox.

---

## Struktur wajib

```
poc/
├── <ID>_<Nama>.t.sol        atau  <ID>_<nama>.ts / .rs / .move
├── <ID>_<Nama>.md           <- cara menjalankan (WAJIB)
└── fixtures/                <- opsional: state awal, JSON, keypair
```

Field `poc` di `MANIFEST.json` menunjuk berkas test; field `cmd` memuat perintah persisnya.

---

## Berkas `<ID>_<Nama>.md` — 5 bagian

```markdown
# <ID> — Cara Menjalankan PoC

## Lingkungan
- Toolchain : <foundry vX / anchor vX / cargo vX>
- RPC       : <fork URL atau "lokal, tanpa jaringan">
- Commit    : <SHA target yang diuji>

## Perintah
```bash
$ <satu perintah persis>
```

## Keluaran yang Diharapkan
```
<baris kunci: [PASS] nama_test / Error Code: XXX>
```

## Bila Gagal
<Gejala umum dan penyebabnya. Mis. "jika RPC rate-limited, ganti endpoint".>
```

---

## Aturan isi PoC

| Aturan | Alasan |
|---|---|
| **Satu skenario per berkas** | Berkas gabungan menyembunyikan skenario mana yang lulus |
| **Kontrol positif wajib** | Tes "ditolak" tanpa kasus sukses tidak membuktikan guard bekerja |
| **Periksa kode error spesifik** | `expectRevert()` polos lulus pada crash apa pun, termasuk bug di tes sendiri |
| **Tanpa cheatcode produksi** | `vm.store`/`vm.deal` hanya sah untuk seeding, bukan menciptakan kondisi mustahil |
| **Victim seeding disimulasikan** | Serang state yang benar-benar dapat dibentuk pengguna (`vm.prank(victim)`) |
| **Fuzz untuk klaim batas** | Klaim "tidak pernah terjadi" butuh `testFuzz_` minimal 256 run |
| **Tanpa hardcode hasil** | Jangan `assert(true)` untuk melewati |

---

## Kontrol positif — pola wajib

Setiap PoC yang menyimpulkan "serangan gagal / guard bekerja" **harus** memuat dua kasus:

```solidity
/// LULUS — input sah harus berhasil (membuktikan jalur eksekusi hidup)
function test_KONTROL_inputSah_sukses() public { ... assertTrue(ok); }

/// DITOLAK — input serangan harus gagal dengan kode spesifik
function test_serangan_ditolak() public {
    vm.expectRevert(Contract.ErrorKodeSpesifik.selector);
    ...
}
```

Tanpa kasus pertama, "ditolak" bisa berarti tesnya sendiri rusak. Insiden nyata: tes melaporkan
3 PASS padahal error-nya `Cannot read properties of undefined` — crash di kode tes, bukan guard.

---

## Yang DILARANG

- Menempelkan log yang tidak pernah dihasilkan → **`FABRICATED_EVIDENCE`**
- Mengandalkan `--broadcast` / `cast send` ke jaringan nyata
- Mengedit kode target untuk membuat PoC berhasil
- Menyembunyikan prasyarat lingkungan (mis. "butuh `--features test`")
- PoC yang hanya berjalan di mesin penulis tanpa dokumentasi dependency

---

## Untuk rantai non-EVM

| Rantai | Harness | Catatan |
|---|---|---|
| Solana | `anchor test` / `ts-mocha` | **Wajib build `--features test`** bila memakai helper test; binary rilis menolak dengan `InvalidProductionSeed` |
| Sui/Aptos | `sui move test` | Sertakan `Move.toml` versi terpin |
| TON | `@ton/sandbox` | Sertakan inisialisasi state |

Lingkungan build **wajib** dicatat di bagian "Lingkungan" — pembaca harus dapat mereproduksi
tanpa menebak flag.
