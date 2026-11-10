# 04-CODE-GUARDED — Wadah Jalur & Hipotesis Terjaga Kode (STAGE-C1 & STAGE-C2)

> ATURAN PENGISIAN (`ZERO-COMPRESSION LAW`):
> 1. Wadah ini mencatat setiap jalur ([EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT]) atau hipotesis serangan di Tahap C (C1 maupun C2) yang setelah diperiksa terbukti sudah dijaga secara rapat oleh kode.
> 2. Mencatat jalur terjaga secara presisi mencegah agen atau Subagent berikutnya memeriksa ulang jalur buntu yang sama di putaran lain.
> 3. Setiap entri wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy` dan ekspresi kode penjaganya. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).

---

## 1. TABEL JALUR TERJAGA KODE PER WILAYAH (R_1 .. R_N)

| Guard ID | Region (R_i) | Gelombang (C1-BLIND / C2-CROSS) | Titik Masuk & Simbol (NamaModul.namaFungsi) | Hipotesis Serangan yang Diuji | Jangkar Penjaga Kode (Path/File.ext:Lxx-Lyy) | Ekspresi Penjaga Kode Asli & Alasan Mengapa Serangan Tertahan (Verbatim) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| GUARD-R1-01 | R_1 | C1-BLIND | [NamaModul.namaFungsi] | [Contoh: Mencoba menarik melebihi saldo share melalui pembulatan ke atas] | [Path/File.ext:L88-L94] | [Kutipan ekspresi require/assert/constraint/pembulatan ke bawah yang secara matematis mengunci celah tersebut] |
