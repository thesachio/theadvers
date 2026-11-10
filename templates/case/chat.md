# CHAT, PENGANTAR SUBMISSION, & JEJAK PENALARAN — `[FIND-xxx]`

> **ATURAN PENGISIAN (`cases/<ID>/chat.md` — Berbasis `templates/SUBMISSION-EMAIL.md` & `sc-phase3` Langkah 2e)**:
> 1. Berkas ini adalah **pintu masuk komunikasi** untuk tim triase/klien sekaligus ringkasan jejak penemuan per kasus. Tujuannya membuat triager langsung memahami skala dampak dan membuka `laporan-teknis.md` serta `poc.md`.
> 2. **Gerbang Wajib**: Hanya boleh dikirim setelah seluruh klaim terverifikasi mekanis (`MECH-OK` / lolos Gate `verify_segitiga.py`).
> 3. **Tabel Aturan Wajib**:
>    - **Subjek $\le 70$ karakter, severity di depan**: Triager memilah berdasarkan severity; subjek panjang terpotong.
>    - **Jumlah & lokasi temuan di paragraf pertama**: Menetapkan skala sebelum detail.
>    - **Satu kalimat dampak terukur**: Angka menarik perhatian; kata "kritis" tanpa angka tidak.
>    - **Sebut commit yang diuji (`SHA-12`)**: Memungkinkan triager langsung membandingkan.
>    - **Nyatakan belum dipublikasikan**: Menunjukkan itikad *responsible disclosure*.
>    - **Tanpa permintaan pembayaran di kontak pertama**.
> 4. **Yang DILARANG di Bagian Pesan Pengantar**:
>    - Dilarang menuliskan langkah eksploitasi mentah yang panjang di badan pesan pembuka (itu isi `laporan-teknis.md`).
>    - Dilarang mengklaim severity lebih tinggi dari yang dibuktikan impact di `poc.md`.
>    - Dilarang memakai token pemotongan malas (`...`, `dll.`, `dst.`, `etc.`).

---

## 1. PESAN PENGANTAR SIAP KIRIM (*SUBMISSION EMAIL / INITIAL TRIAGE CHAT*)

```text
Subject: [<Proyek>] <Severity> — <Judul satu baris tanpa sensasi, <= 70 karakter>

Halo tim <Proyek>,

Saya menemukan isu dengan tingkat keparahan <Severity> pada komponen <NamaModul/Kontrak> di commit <SHA-12> yang memenuhi kriteria cakupan audit / program bug bounty Anda.

Ringkasan Eksekutif Kasus:
- ID & Severity : <FIND-xxx> (<Severity> — Rujukan: <Platform / Matriks Universal>)
- Dampak Terukur: <Satu kalimat dampak terukur: berapa dana/aset yang terdampak dalam angka eksak>
- Lokasi Kode   : <Path/File.ext:Lxx-Lyy>
- Status Bukti  : Terbukti [PASS] melalui simulasi <FORK_LIVE / FORK_DEPLOYED_HEAD / LOKAL>

Folder kasus ini melampirkan:
1. `laporan-teknis.md` — Laporan teknis 9-bagian lengkap (ringkasan, kutipan kode, akar masalah, tabel prasyarat, langkah reproduksi, keluaran nyata, dampak kuantitatif, patch diff, dan batas verifikasi).
2. `poc.md` — Paket Proof-of-Concept yang dapat langsung dijalankan (lengkap dengan spesifikasi lingkungan, perintah eksak, kontrol positif, kode uji utuh, dan log eksekusi).

Saya belum mempublikasikan isi laporan ini dan tidak akan melakukannya sampai ada konfirmasi dari tim Anda. Saya bersedia membantu proses reproduksi atau memberikan penjelasan tambahan bila diperlukan.

Salam,
<Nama / Tim Auditor>
<Kontak>
```

---

## 2. PANDUAN TEMPEL CEPAT UNTUK PLATFORM (*IMMUNEFI / CANTINA / SHERLOCK*)

*Bila pelaporan menggunakan formulir platform:*
1. **Kolom Title**: `<Judul satu baris dari Bagian 1, <= 70 karakter>`
2. **Kolom Severity & Rujukan**: `<Severity> | Impact: <High/Medium/Low> | Likelihood: <High/Medium/Low> | Rujukan: <URL/Bagian Rubrik>`
3. **Kolom Description**: Tempel **Bagian 1 s.d. Bagian 8** dari `cases/<ID>/laporan-teknis.md`.
4. **Kolom Proof of Concept**: Tempel seluruh isi `cases/<ID>/poc.md`.

---

## 3. JEJAK PENALARAN & RINGKASAN RIWAYAT UJI (`lead-<ID>.md`)

- **Asal Lead & Klasifikasi**: `<LEAD-ID> | [LAPIS: VALUE|PATH|FLOW] | [CLASS-A|B|C] | [AF-xx] | Metode: <M-xxx>`
- **Hipotesis Satu Baris**: `<Hipotesis awal saat ditemukan di Tahap C>`
- **Jejak Pengujian & Eskalasi di Tahap D**:
  - **Berkas & Fungsi Test**: `<Path/TestFile.ext — namaFungsiTest>`
  - **Kontrol Positif**: `<Nama fungsi kontrol positif yang membuktikan jalur normal berhasil [PASS]>`
  - **Ringkasan Perintah & Hasil**: `$ <perintah eksak>` $\rightarrow$ `[PASS]` (`Delta Nilai: <angka eksak>`)
- **Putusan Hakim Tahap E/F (`VERDICT.md`)**:
  - `VERDICT: VALID_ELIGIBLE | TANGGA_BUKTI: <A|B> | DEPLOYMENT_MATCH: LIVE_MATCH | LIVE_IDENTITY: <identitas terukur>`
