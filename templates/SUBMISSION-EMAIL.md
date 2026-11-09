# SUBMISSION-EMAIL — Template Email Pengantar ke Program Bounty

Email adalah **pintu masuk**, bukan laporannya. Tujuannya: membuat triager membuka lampiran,
bukan menjelaskan teknis secara panjang.

**Gerbang wajib:** kirim hanya setelah `tools/ingest.py` menyatakan `N/N MECH-OK`.

---

## Template

```
Subject: [<Proyek>] <Severity> — <Judul satu baris, ≤70 karakter>

Halo tim <Proyek>,

Saya menemukan <jumlah> isu pada <komponen> di commit <SHA-12> yang menurut saya
memenuhi kriteria program bug bounty Anda.

Ringkas:

1. <Severity> — <judul singkat>
   <Satu kalimat dampak terukur: berapa dana/apa yang terdampak.>
   Lokasi: <File:Baris>

2. <Severity> — <judul singkat>
   ...

Lampiran berisi laporan teknis lengkap per temuan (root cause, langkah reproduksi,
keluaran uji) beserta paket PoC yang dapat dijalankan.

Semua klaim telah diverifikasi secara mekanis dengan skrip validasi internal; berkas
MANIFEST.json menyertakan lokasi, perintah reproduksi, dan tingkat keparahan yang
diklaim untuk setiap temuan.

Saya belum mempublikasikan isi laporan ini dan tidak akan sampai ada konfirmasi dari
tim Anda.

Bersedia membantu reproduksi atau menyediakan tambahan bila diperlukan.

<Salam>
<Nama>
<Kontak>
```

---

## Aturan

| Aturan | Alasan |
|---|---|
| **Subjek ≤70 karakter, severity di depan** | Triager memilah berdasarkan severity; subjek panjang terpotong |
| **Jumlah temuan di paragraf pertama** | Menetapkan skala sebelum detail |
| **Satu kalimat dampak terukur per temuan** | Angka menarik perhatian; kata "kritis" tidak |
| **Sebut commit yang diuji** | Memungkinkan triager langsung membandingkan |
| **Nyatakan belum dipublikasikan** | Menunjukkan itikad responsible disclosure |
| **Tanpa lampiran terkunci password** | Menyulitkan triase; enkripsi hanya bila diminta program |
| **Tanpa permintaan pembayaran** | Sebutan reward negatif di kontak pertama |

---

## Yang DILARANG

- Menuliskan langkah eksploitasi lengkap di **email** (itu isi lampiran, bukan badan email)
- Menyertakan PoC yang dapat langsung disalahgunakan di badan email
- Klaim severity lebih tinggi dari yang dibuktikan impact
- Menyebut "beberapa isu" tanpa daftar — triager menganggapnya spam
- Mengirim ke alamat di luar kanal resmi program
- Follow-up sebelum waktu respons yang dijanjikan program berlalu

---

## Bila program memakai platform (Immunefi / Cantina / Sherlock)

Platform biasanya menyediakan formulir sendiri. Dalam hal itu:

1. Tempel **bagian 1–7** dari `templates/TECHNICAL-REPORT.md` ke formulir
2. Unggah `poc/` sesuai `templates/POC-PACKAGE.md`
3. Simpan `MANIFEST.json` sebagai lampiran pendukung (banyak triager memakai skrip serupa)
4. Email hanya dipakai bila diminta kontak langsung

---

## Setelah terkirim

Perbarui `MANIFEST.json`:

```json
"upstream": { "agent": "<nama>", "date": "YYYY-MM-DD", "submitted_to_program": true }
```

Catat tanggal kirim dan ID tiket platform (bila ada) di `findings/<ID>.md` bagian atas.
Tanpa pencatatan ini, temuan yang sama berisiko dikirim ulang dan dianggap duplikat.
