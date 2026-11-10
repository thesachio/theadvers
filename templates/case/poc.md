# <FIND-ID> — Paket Proof-of-Concept & Cara Menjalankan (`cases/<ID>/poc.md`)

> **ATURAN PENGISIAN (`cases/<ID>/poc.md` — Standar Wajib `templates/POC-PACKAGE.md` & `sc-phase3` Langkah 2c)**:
> 1. **PoC yang tidak dapat dijalankan orang lain bukanlah bukti.** Berkas ini menyatukan petunjuk eksekusi 5-bagian (`POC-PACKAGE.md`) beserta kode uji lengkap yang dapat langsung dijalankan.
> 2. **Tujuh Aturan Isi PoC (Mengikat)**:
>    - **Satu skenario per berkas/kasus**: Jangan menggabungkan skenario yang tidak relevan agar jelas mana yang lulus.
>    - **Kontrol Positif WAJIB (`test_KONTROL_...`)**: Setiap PoC wajib memuat kasus kontrol positif yang membuktikan jalur normal berjalan sukses sebelum/di samping kasus eksploitasi. Jika menguji penolakan/DoS, wajib periksa selector error spesifik (`vm.expectRevert(Contract.ErrorSpesifik.selector)`), dilarang `expectRevert()` polos.
>    - **Tanpa cheatcode produksi**: `vm.store`, `vm.etch` state protokol, `vm.prank(admin)` untuk mengarang state adalah pelanggaran (`REJECTED_CHEATCODE`).
>    - **Victim Seeding disimulasikan**: State korban wajib dibentuk melalui transaksi nyata (`vm.prank(victim)`), bukan disuntikkan ke slot storage.
>    - **Tanpa hardcode hasil**: Dilarang menggunakan `assert(true)` untuk memalsukan kelulusan.
>    - **Kode utuh 100%**: Dilarang memotong kode PoC dengan `...`, `// rest of code`, `dll.`, `dst.`, atau `etc.`.
> 3. **Yang DILARANG KERAS**:
>    - Menempelkan log yang tidak pernah dihasilkan $\rightarrow$ **`FABRICATED_EVIDENCE`**.
>    - Mengandalkan `--broadcast` / `cast send` ke jaringan nyata.
>    - Mengedit kode sumber kontrak target agar PoC berhasil.

---

## 1. Lingkungan

- **Finding ID & Target Lokasi**: `[FIND-001 | Path/File.ext:Lxx-Lyy]`
- **Toolchain & Versi**: `[Foundry (forge vX.Y.Z) / Cargo (cargo vX.Y.Z) / Sui-Aptos Move / @ton/sandbox]`
- **Mode Uji & RPC**: `[FORK_LIVE (URL RPC / .env.rpc, Block: <N>) | FORK_DEPLOYED_HEAD | LOKAL (tanpa jaringan)]`
- **Commit Target**: `[SHA-40 atau SHA-12 dari target/PIN.md]`
- **Lokasi Berkas Test di Lab**: `[Path/TestFile.t.sol:L1-Lnn]`
- **Catatan Khusus Non-EVM (Bila Relevan)**: `[Misal: Solana wajib '--features test' bila memakai helper test; Sui/Aptos sertakan versi Move.toml; TON sertakan inisialisasi state @ton/sandbox]`

---

## 2. Perintah

```bash
$ [Satu perintah persis untuk menjalankan PoC dari root proyek/lab, misal: FOUNDRY_JOBS=1 forge test --match-contract Find001ExploitTest -vvv]
```

---

## 3. Keluaran yang Diharapkan (`BUKTI_SIMULASI`)

```text
$ [Perintah persis yang dijalankan]
[Tempelkan baris-baris kunci keluaran nyata dari terminal: mencakup kelulusan [PASS] fungsi Kontrol Positif, kelulusan [PASS] fungsi Eksploitasi, serta cetakan angka saldo/state Sebelum vs Sesudah]
```

---

## 4. Bila Gagal (Troubleshooting Reproduksi)

- **Gejala 1 (RPC Rate-Limited / Timeout pada Mode Fork)**: `[Ganti endpoint RPC di .env.rpc menggunakan daftar cadangan di rpc-free-tier.md atau jalankan ulang dengan flag --fork-block-number <N>.]`
- **Gejala 2 (Build / Stack-too-Deep / Toolchain)**: `[Pastikan menjalankan dengan FOUNDRY_JOBS=1 / CARGO_BUILD_JOBS=1 dan flag kompilasi sesuai Bagian 1.]`

---

## 5. Kode Lengkap Proof-of-Concept (Wajib Memuat Kontrol Positif & Eksploitasi Utuh)

*Salin seluruh isi berkas test PoC di bawah ini secara utuh dari baris pertama (`pragma` / `import` / `use`) hingga kurung kurawal penutup terakhir tanpa elipsis (`...`):*

```solidity
// Lokasi Berkas Uji: Path/TestFile.t.sol (atau .rs / .move / .ts)
// Target Cacat     : Path/File.ext:Lxx-Lyy

/// 1. KONTROL POSITIF (WAJIB) — Membuktikan jalur eksekusi normal hidup dan berjalan sah
// function test_KONTROL_inputSah_sukses() public { ... }

/// 2. SKENARIO EKSPLOITASI — Membuktikan pelanggaran invarian / ekstraksi nilai oleh penyerang tak berizin
// function test_FIND001_exploit() public { ... }
```
