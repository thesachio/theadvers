# TECHNICAL-REPORT — Template Laporan Temuan (bounty submission)

Satu berkas per temuan: `findings/<ID>.md`. Laporan ini **melengkapi** `MANIFEST.json`,
bukan menggantikannya — manifest yang menentukan lolos/tidaknya klaim secara mekanis.

**Gerbang masuk:** klaim harus sudah `MECH-OK` di `tools/ingest.py` sebelum laporan ini
boleh dikirim.

---

## Struktur wajib (7 bagian, urut)

```markdown
# <ID> — <Judul satu baris, tanpa sensasi>

## 1. Ringkasan
<Satu paragraf. Apa yang salah, siapa yang dirugikan, berapa nilainya.>
<Kalimat pertama harus bisa dibaca berdiri sendiri oleh engineer yang sibuk.>

Severity : S1|S2|S3|S4      (klaim; samakan dengan manifest)
Impact   : theft|grief|dos|design|none
Actor    : unprivileged|solver|oracle|admin
Victim   : sponsor|user|protocol|third-party|none

## 2. Lokasi Kode
<Satu baris per lokasi, format `path/File.ext:awal-akhir`.>

```solidity
// kutipan 5-15 baris yang benar-benar berisi cacat
```

## 3. Akar Masalah
<Mekanisme, bukan gejala. Jelaskan mengapa kode berperilaku salah.>
<Rujuk nomor baris tepat. Jangan menulis "kurang validasi" — sebut validasi apa yang hilang.>

## 4. Prasyarat
| # | Prasyarat | Terpenuhi? | Bukti |
|---|---|---|---|
| 1 | <state/kondisi yang harus ada> | ya/tidak | <File:Baris atau hasil query> |

## 5. Langkah Reproduksi
<Bernomor, dapat diikuti tanpa menebak. Sertakan perintah persis.>

```
$ <perintah setup>
$ <perintah menjalankan PoC>
```

## 6. Keluaran Nyata
<Keluaran yang BENAR-BENAR dijalankan — tempel apa adanya, jangan diringkas.>

```
<PASS/FAIL beserta log>
```

## 7. Dampak Kuantitatif
| Metrik | Nilai | Sumber |
|---|---|---|
| <dana berisiko> | <angka eksak> | <query/cast call> |
| <biaya penyerang> | <angka> | <estimasi gas/fee> |
| <korban terukur> | <jumlah> | <hasil pengukuran on-chain> |

## 8. Rekomendasi Perbaikan
<Diff atau deskripsi perubahan minimal. Sebut dampak kompatibilitas bila ada.>

```diff
- <baris lama>
+ <baris baru>
```

## 9. Yang TIDAK Diverifikasi
<Kejujuran batas. Isi ini selalu — kosong berarti Anda yakin 100%, yang jarang benar.>
- [ ] <aspek yang tidak diuji dan alasannya>
```

---

## Aturan penulisan

| Aturan | Alasan |
|---|---|
| **Judul tanpa hiperbola** — "X tidak tercakup signature", bukan "KRITIS! DANA BISA DICURI" | Judul sensasional menurunkan kredibilitas di triage pertama |
| **Setiap klaim punya `File:Baris`** | Klaim tanpa lokasi tidak dapat diverifikasi |
| **Keluaran ditempel, bukan diringkas** | Ringkasan log adalah tempat utama bukti palsu masuk |
| **Angka, bukan kata** — "500.000 USDC", bukan "banyak dana" | Severity ditentukan impact terukur |
| **Severity dari IMPACT, bukan dari siklus deploy** | Menurunkan severity karena "belum live" adalah pelanggaran |
| **Bagian 9 wajib diisi** | Menyatakan batas lebih meyakinkan daripada klaim sempurna |
| **Jangan menyalin laporan ini ke manifest** | Manifest = field terstruktur; laporan = narasi. Duplikasi memicu drift |

---

## Yang DILARANG

- Menempelkan keluaran yang tidak pernah dijalankan → **`FABRICATED_EVIDENCE`**
- Menulis severity lebih tinggi dari yang dibuktikan impact
- Menyembunyikan prasyarat yang tidak terpenuhi
- Menyebut "berpotensi" tanpa mengukur
- Mengirim sebelum `ingest.py` menyatakan `MECH-OK`
