# 08-VALID-NOT-ELIGIBLE — Wadah Isu Valid Teknis di Luar Kelayakan Klaim (STAGE-E)

> ATURAN PENGISIAN (`ZERO-COMPRESSION LAW`):
> 1. Wadah ini menampung kandidat dari 05-raw-leads.md yang perilakunya terbukti valid secara teknis, namun tidak memenuhi kriteria sebagai temuan utama yang *eligible* karena salah satu alasan berikut:
>    - Menyentuh modul/berkas di luar *scope* resmi (*Out-of-Scope*),
>    - Sudah dideklarasikan secara eksplisit di dokumentasi/audit sebelumnya (*Known Issue*),
>    - Bergantung penuh pada tindakan jahat dari peran yang dideklarasikan terpercaya (*Trusted Admin / Governance Centralization Risk*) tanpa adanya bypass otorisasi, atau
>    - Dampak ekonominya berada di bawah ambang batas minimal kebijakan program (misal kehilangan presisi 1 wei tanpa akumulasi).
> 2. Wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy` dan bebas dari token kompresi (..., dll., dst., etc., rest of logic).

---

## 1. TABEL ISU VALID NON-ELIGIBLE (08-VALID-NOT-ELIGIBLE)

| Non-Eligible ID | Asal Lead ID | Region (R_i) | Kategori (OUT-OF-SCOPE / KNOWN-ISSUE / TRUSTED-ROLE / DUST-IMPACT) | Jangkar Kode (Path/File.ext:Lxx-Lyy) | Ringkasan Mekanisme Teknis & Alasan Ketidaklayakan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| VNE-R1-01 | LEAD-R1-xx | R_1 | TRUSTED-ROLE | [Path/File.ext:L30-L58] | [Fungsi setParameter oleh admin tidak memiliki batas atas, namun peran admin dinyatakan sepenuhnya trusted dalam aturan scope] |

---

## 2. RINCIAN TEKNIS & CATATAN ARSITEKTURAL

### VNE-R1-01 (Eks LEAD-R1-xx) — [Judul Isu]
- Region & Modul: R_1 | [NamaModul.namaFungsi]
- Jangkar Kode Eksak (`Path/File.ext:Lxx-Lyy`): [Kutipan lokasi dan perilaku teknis]
- Bukti Perilaku Teknis: [Penjelasan konkret mengapa perilaku ini nyata]
- Alasan Klasifikasi ke `08-valid-not-eligible.md`: [Rujukan aturan scope/dokumen yang mengecualikan isu ini dari `09-confirmed-findings.md]`
