---
name: sc-pre-intel
description: Eksekusi PRE-STAGE-0 (Project Intelligence Brief `INTEL.md`) — identitas proyek, link langsung, commit terpin, serta Deployment Stage (MAINNET/TESTNET/DEVNET) yang menentukan Mode Uji seluruh audit. Prasyarat --gate 0, bukan tahap baru.
---

# Skill sc-pre-intel — Project Intelligence Brief (`INTEL.md`)

Anda menjalankan **PRE-STAGE-0**: mengisi `INTEL.md` **sekali** di awal audit, sebelum STAGE-0
menyentuh satu berkas kode pun.

`INTEL.md` **bukan tahap baru**. Ia **prasyarat `--gate 0`**: selama INTEL belum sah, gate 0 FAIL dan
STAGE-A tidak boleh dimulai. Ia diperbarui hanya bila jaringan/deployment berubah.

---

## 1. Langkah Pertama Mutlak

1. Siapkan berkas:

       cp templates/INTEL.md <audit-dir>/INTEL.md

2. Jalankan pemeriksa INTEL setiap kali selesai mengisi satu bagian:

       python3 tools/verify_segitiga.py --intel <audit-dir>

   Exit 0 = INTEL sah. Exit 1 = ada bagian yang belum memenuhi syarat (pesan menunjuk bagiannya).

---

## 2. Prosedur Pengisian (urut, jangan dilompati)

### §0 — Deployment Stage (WAJIB, menentukan seluruh audit)

**Isi ini lebih dulu.** Ia menentukan `Mode Uji` di STAGE-D dan syarat `09`.

| Nilai | Kapan dipakai | Akibat |
| :--- | :--- | :--- |
| `MAINNET` | protokol berjalan di jaringan produksi publik | `09` wajib `Mode Uji: FORK_LIVE` + blok fork |
| `TESTNET` | hanya berjalan di testnet publik, belum produksi | `09` wajib `Mode Uji: FORK_TESTNET` |
| `DEVNET` | jaringan pengembangan privat/terbatas | `09` wajib fork devnet, dicatat eksplisit di laporan |

**DILARANG mengosongkan.** Tidak ada default — stage yang tidak dinyatakan membuat `--gate 0` FAIL.
`MAINNET` **DILARANG** bila §5 `Bukti Live` belum berisi artefak konkret (hex bytecode / ukuran /
lamport). Ini yang membedakan "sudah live" dari "seharusnya live".

### §1 — Identitas
Nama proyek + overview 1–3 kalimat. Bila tidak ada README/docs yang menjelaskan mekanisme, tulis
`TIDAK_DITEMUKAN — <sumber yang diperiksa>`. **Dilarang mengarang deskripsi.**

### §2 — Link referensi langsung
UI/dApp, Docs resmi, Repo GitHub spesifik, dan **Commit terpin**.
- Commit wajib hash hasil `git rev-parse` — **bukan** `latest`/`main`.
- Setiap URL wajib dibuktikan hidup di sesi yang sama (`curl -sI` → 200/30x, atau pembacaan halaman).
  Catat perintahnya di baris `Diverifikasi Oleh`.
- URL mati → `TIDAK_DITEMUKAN`.

### §3 — Aturan Bug Bounty
Platform + **URL langsung ke halaman proyek** (bukan beranda platform). Bila tidak ada aturan scope
tertulis, tulis `TIDAK_DITEMUKAN — tidak ada aturan scope tertulis`. **Dilarang menyimpulkan scope
dari praktik umum.**

### §4 — Laporan audit lampau
Hanya laporan yang punya tautan. "Disebut di README tanpa link" **bukan** laporan —
tulis `TIDAK_DITEMUKAN — README menyebut "audit by X" tanpa tautan (klaim tak terverifikasi)`.

### §5 — Deployment & Live Surface (terukur)
- `Chain / Network Aktif` — nama + chainId yang benar-benar dipakai
- `Kontrak Utama (alamat)` — entrypoint/proxy
- `Implementation Aktif` — alamat impl di balik proxy (slot EIP-1967 `0x360894a1...382bbc`), atau `bukan proxy`
- `Blok Referensi` — nomor blok terakhir (titik fork awal di STAGE-D) — **wajib untuk MAINNET**
- `VERSION_RELATION` — `LIVE_IS_DEPLOYED_COMMIT` | `LIVE_NEWER_THAN_HEAD` | `HEAD_NEWER_THAN_LIVE` | `LIVE_UNVERIFIED`
- `Bukti Live` — **perintah + keluaran nyata**:

      $ cast code 0xAbC...123 --rpc-url $RPC
      0x6080604052... (12481 bytes)

  Tanpa artefak konkret (hex / ukuran bytecode / lamport / "non-kosong"), bagian ini **belum sah**.

### §6 — Catatan Ketiadaan
Wajib diisi bila `Intel Status = PARTIAL`. Setiap `TIDAK_DITEMUKAN` **wajib** punya alasan + sumber
yang sudah dicoba. `TIDAK_DITEMUKAN` tanpa alasan = INTEL **tidak jujur**.

---

## 3. Empat Hukum Pengisian

1. **Satu alasan per ketiadaan.** `TIDAK_DITEMUKAN` saja tidak cukup — sertakan alasan + sumber dicoba.
2. **"Gagal diakses" ≠ "tidak ada".** 403/429/login/timeout → `TIDAK_DITEMUKAN (batas akses: <penyebab>)`.
3. **Dilarang mengisi slot dengan asumsi.** Ragu → turunkan ke `TIDAK_DITEMUKAN`.
4. **Konsistensi status.** `Intel Status = COMPLETE` hanya sah bila **keenam** butir §6 `DITEMUKAN`.
   Satu `TIDAK_DITEMUKAN` ⇒ status **wajib** `PARTIAL`.

---

## 4. Gate & Transisi

1. Jalankan:

       python3 tools/verify_segitiga.py --intel <audit-dir>

2. Setelah PASS, lanjutkan ke STAGE-0:

       python3 tools/verify_segitiga.py --context-packet <audit-dir>

   `--gate 0` kini menagih INTEL **dan** Tabel Rekonsiliasi 100% berkas sekaligus. INTEL yang belum
   sah akan menggagalkan gate 0.

3. Perbarui `STATE.md` (Current Stage: STAGE-0, Active Region: NONE) **sebelum** mulai inventarisasi.

---

## 5. Kapan INTEL Diperbarui

Hanya bila **jaringan/deployment berubah**:

- `TESTNET → MAINNET` (protokol naik produksi)
- alamat kontrak / implementation berganti
- `Blok Referensi` perlu dinaikkan ke blok yang lebih baru untuk fork

Saat itu terjadi: isi baris `Perubahan Stage` (tanggal + alasan), lalu **ulangi**
`--intel` dan `--gate 0` untuk wilayah yang belum `[CLOSED]`. Wilayah yang sudah `[CLOSED]`
**tidak** dibuka kembali hanya karena stage berubah — cukup dicatat di laporan.

**DILARANG** memperbarui `Blok Referensi` per lead atau per batch. Satu INTEL = satu titik acuan
awal; blok fork per batch dicatat di `STATE.md`, bukan di sini.

---

## 6. Yang DILARANG di `INTEL.md`

- Hipotesis kerentanan (itu milik `05-raw-leads.md`)
- Status wilayah / stage / gate (itu milik `STATE.md`)
- Rekonsiliasi berkas & Tier (itu milik `path-map.md`)
- URL hasil mesin pencari, hash karangan, nama auditor dari ingatan
- Nilai placeholder template yang dibiarkan (`<...>`, `[Tulis ...]`)
