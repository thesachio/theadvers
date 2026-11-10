# FACTS — Bank Fakta Verbatim & Peta Inversi Prasyarat (theadvers v2.0)

> HUKUM JANGKAR VERBATIM (`ZERO-COMPRESSION LAW`):
> 1. Dilarang menulis rangkuman naratif kabur atau memakai token pemotongan malas (..., dll., dst., etc., and so on, rest of logic).
> 2. Setiap baris fakta wajib memuat lokasi baris eksak (Path/File.ext:Lxx-Lyy), simbol/fungsi eksak, dan kondisi/rumus kode aslinya.
> 3. Kolom Prerequisite Inversion Hint wajib diisi pada STAGE-A karena menjadi peta serangan utama saat memasuki Gelombang 2 (STAGE-C2).

---

## 1. TABEL FAKTA VERBATIM & INVERSI PRASYARAT PER WILAYAH

| Fact ID | Region (R_i) | Verbatim Anchor (Path/File.ext:Lxx-Lyy) | Modul & Simbol/Fungsi Eksak | Kategori (VALUE / SCALE / GUARD / STATE / LATENT) | Ekspresi / Kondisi / Rumus Kode Asli (Verbatim) | Prerequisite Inversion Hint *(Bagaimana asumsi fakta ini dapat dipatahkan di Gelombang 2?)* |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-R1-01 | R_1 | [Path/File.ext:L10-L25] | [NamaModul.namaFungsi] | GUARD | [Tulis syarat require/assert/constraint/rumus eksak dari kode] | [Tulis kondisi pematah: misal donasi langsung mengubah denominator, nilai batas 0, urutan panggil lintas-modul, atau bypass otoritas] |

---

## 2. DAFTAR INVARIANT NILAI & AKUNTANSI PER WILAYAH

*Setiap Wilayah R_i wajib mendefinisikan minimal satu invariant nilai terukur yang akan diuji kehancurannya pada Tahap C dan Tahap D.*

| Invariant ID | Region (R_i) | Jangkar Kode Terkait (Path/File.ext:Lxx-Lyy) | Rumus / Pernyataan Invariant Eksak | Skenario Pemicu Kerusakan (*Break Condition*) |
| :--- | :--- | :--- | :--- | :--- |
| INV-R1-01 | R_1 | [Path/File.ext:L40-L85] | [Contoh: sum(userShares) * exchangeRate <= totalVaultAssets] | [Contoh: Pembulatan ke bawah pada beban utang atau inflasi indeks saat totalSupply == 0] |
