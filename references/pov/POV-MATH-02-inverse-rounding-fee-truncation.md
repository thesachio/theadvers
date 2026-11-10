# [POV-MATH-02] Sudut Pandang: Inverse-Function Rounding & Multi-Hop Fee Truncation
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Pasangan konversi 2 arah (*Exact-Input* vs *Exact-Output*: `deposit` vs `mint`, `withdraw` vs `redeem`) atau pembagian proporsi/fee ≥2 tahap berurutan.
- Paired Items: M-001, M-004, M-007, AF-02, POV-unprivileged

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin dengan modal awal kecil. Tidak butuh peran apa pun — hanya kemampuan memanggil fungsi konversi berulang.

## 2. Gejala di Kode

Dua fungsi yang seharusnya **saling invers** (`deposit(aset)` ↔ `mint(share)`, `withdraw(aset)` ↔ `redeem(share)`) memakai arah pembulatan yang keduanya menguntungkan pengguna, atau fee dipotong di ≥2 titik (setiap hop) sehingga sisa pembagian hilang ke arah yang bisa dimanfaatkan.

Kombinasi klasik: `deposit` membulatkan ke bawah (share diterima lebih sedikit — baik), `withdraw` juga membulatkan ke bawah (aset keluar lebih sedikit — baik). **Aman.** Bahaya ada saat satu sisi membulatkan ke arah yang salah, atau saat fee dipotong dua kali dengan truncation di antaranya.

## 3. Rangkaian Serangan

1. **Siapkan:** hitung kombinasi input yang membuat `f⁻¹(f(x)) > x` atau `f⁻¹(f(x)) < x` secara menguntungkan.
2. **Picu:** lakukan konversi bolak-balik dalam satu transaksi, atau pecah menjadi banyak hop kecil.
3. **Ekstraksi:** selisih kumulatif tertinggal di tangan penyerang.

## 4. Auditor Blindspot

Auditor menguji satu arah konversi saja. Yang tidak diuji: **perilaku komposisi** — apa yang terjadi bila `deposit` lalu `withdraw` dipanggil berulang dengan nilai yang membuat sisa pembagian berpihak ke penyerang.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **DILARANG** menggugurkan dengan hitungan pembulatan di atas kertas. Wajib loop nyata di simulator: N konversi kecil vs 1 konversi besar.
- **Wajib** *3-Way Amplification* (modal besar + batch/multicall + chaining) dan **Strike 3 Fuzz** yang mengacak rasio input/output, desimal token, dan jumlah hop.
- **Gugur** (`REJECTED_DUST` / `REJECTED_NEGATIVE_EV`) hanya bila log test dan fuzz membuktikan hasilnya tetap merugi.
