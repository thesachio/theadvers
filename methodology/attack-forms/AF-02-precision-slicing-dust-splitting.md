# [AF-02] Pemecahan Transaksi Mikro, Eksploitasi Pembulatan, & Akumulasi Dust
- Classes: ROUNDING-EXPLOIT, PRECISION-LOSS, MICRO-SPLITTING, DECIMAL
- Trigger Symptom: Terdapat pembagian integer untuk fee/share/utang/likuidasi atau konversi antar-desimal yang membulatkan ke arah yang menguntungkan pemanggil.
- Paired Items: M-001, M-002, M-007, DOM-vault, DOM-amm

---

## 1. Mekanisme Serangan Universal
Penyerang memilih ukuran input spesifik tepat di bawah atau di atas ambang pembagian bilangan bulat (*integer truncation threshold*), atau memecah satu operasi besar menjadi $N$ operasi mikro dalam satu transaksi/batch untuk menghilangkan biaya (*fee = 0*), membayar utang lebih kecil dari seharusnya, atau mengekstrak aset ekstra dari setiap pembulatan.
## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Isolasi Rumus Aritmatika di `Path/File.ext:Lxx-Lyy`:
   Tulis persamaan integer eksaknya, misal fee = (amount * feeBps) / 10000 atau sharesBurned = (assets * totalSupply) / totalAssets.
2. Hitung Titik Eksploitasi Konkret:
   - Cari nilai amount maksimum di mana amount * numerator < denominator sehingga hasil bagi bernilai 0 (atau berkurang 1 unit penuh).
   - Hitung dampak kumulatif jika operasi tersebut diulang $K$ kali (atau dilakukan dengan token berdesimal rendah seperti 6 atau 8 desimal di mana 1 unit bernilai signifikan).
3. Kondisi Gugur ke `06-refuted-invalid.md` atau `08-valid-not-eligible.md`:
   - Gugurkan ke 06-refuted-invalid.md jika kode sudah menggunakan pembulatan ke atas (mulDivUp / ceil) untuk kewajiban pengguna dan pembulatan ke bawah (mulDivDown / floor) untuk hak pengguna.
   - Pindahkan ke 08-valid-not-eligible.md jika kebocoran maksimal hanya 1 wei token berdesimal 18 per transaksi dan biaya gas/eksekusi untuk mengulanginya jauh melampaui nilai yang didapat tanpa adanya mekanisme amplifikasi.

## 3. Bentuk Serangan (Cara Menyerang) — dari Registry v1

- **[BENTUK-01] Serangan Langsung** — input ekstrem (`0`, `1`, `MAX`) dari EOA polos.
- **[BENTUK-03] Bundler Transaksi** — pecah menjadi N panggilan kecil dalam satu bundel lalu gabungkan hasilnya; uji salami-slicing vs bulk.
- **[BENTUK-05] Hentikan Siklus di Tengah** — biarkan posisi di status pending lalu picu konversi, agar pembulatan terjadi pada state setengah jadi.

Rujuk `M-007`, `M-009`.
