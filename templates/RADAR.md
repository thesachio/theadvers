# RADAR — Sinyal Lintas-Modul & Pemicu Serangan Berantai (theadvers v2.0)

> ATURAN WAJIB TAG `[TOUCHES: ...]`:
> 1. Setiap kali membedah Wilayah R_i (terutama pada Gelombang 1 STAGE-C1), catat setiap fungsi, variabel state, akun, objek, atau penyimpanan bersama yang dapat memengaruhi atau dipengaruhi oleh modul/wilayah lain.
> 2. Setiap entri wajib memuat minimal satu tag dengan sintaks eksak: `[TOUCHES: NamaModul.namaVariabelAtauFungsi]`.
> 3. Pada Gelombang 2 (STAGE-C2) dan FINAL-SWEEP, dua atau lebih baris radar yang memiliki tag [TOUCHES: ...] yang sama wajib diadu untuk merakit Serangan Berantai (*Chained Exploit*).

---

## 1. LOG SINYAL RADAR LINTAS-MODUL / LINTAS-WILAYAH

| Radar ID | Asal Wilayah (R_i) | Jangkar Kode Asal (Path/File.ext:Lxx-Lyy) | Tag Sentuhan Wajib ([TOUCHES: NamaModul.simbol]) | Perilaku / Efek Samping yang Diamati (Verbatim) | Hipotesis Serangan Berantai (*Cross-Pollination di STAGE-C2 / FINAL-SWEEP*) | Status Uji ([OPEN-SIGNAL] / [PROMOTED-TO-05] / [GUARDED-IN-04]) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| RAD-001 | R_1 | [Path/File.ext:L55-L72] | [TOUCHES: NamaModul.namaState] | [Jelaskan secara eksak bagaimana baris kode ini mengubah/membaca state tanpa sinkronisasi atau membuka callback] | [Jelaskan modul/fungsi lain mana yang mengasumsikan state tersebut tidak berubah, dan apa dampak nilainya jika digabungkan] | [OPEN-SIGNAL] |

---

## 2. MATRIKS PASANGAN RANTAI ([TOUCHES] COLLISION MATRIX)

*Diisi pada STAGE-C2 dan FINAL-SWEEP ketika ditemukan >= 2 sinyal RADAR yang menyentuh simbol [TOUCHES: ...] yang sama.*
| Chain Pair ID | Tag [TOUCHES: ...] yang Beririsan | Radar ID Pengubah (*Writer / Mutator*) | Radar ID Pembaca / Korban (*Reader / Consumer*) | Mekanisme Serangan Gabungan & Dampak Nilai (L-VALUE) | ID Kandidat di 05-raw-leads.md (atau 04-code-guarded.md) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CPAIR-01 | [TOUCHES: NamaModul.namaState] | RAD-001 (Path/FileA.ext:L55) | RAD-002 (Path/FileB.ext:L110) | [Uraikan urutan panggil langkah demi langkah untuk memanipulasi state di A lalu mengeksploitasinya di B] | [LEAD-R1-01 / GUARD-R1-01] |
