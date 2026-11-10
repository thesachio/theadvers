# [M-007] Metamorphic Split-vs-Bulk Asymmetry
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Terdapat pembagian, pembulatan, atau pembobotan yang bergantung pada jumlah potongan input — fee, share, reward tier, bunga, atau penalti yang dihitung per-panggilan.
- Paired Items: AF-02, AF-09, M-002, M-001, POV-unprivileged

---

## 1. Inti Metode

Auditor menguji rumus dengan **satu angka tunggal**. Metode ini mewajibkan pengujian apakah rumus bersifat **non-linear** ketika input dipecah menjadi potongan kecil atau digabung menjadi satu gelombang besar dalam satu jendela eksekusi:

> `f(a + b) ≠ f(a) + f(b)`

Bila asimetri itu menguntungkan penyerang, ia dapat di-loop dengan biaya murah.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Salami Slicing (pecah jadi N potongan kecil).** Bandingkan satu panggilan `aksi(1000)` dengan 100 panggilan `aksi(10)`. Jika biaya/utang/share yang dibakar memakai pembulatan ke bawah (*floor*), memecah transaksi dapat membuat kewajiban terpotong menjadi `0` atau berkurang satu unit di setiap iterasi.
2. **Bulk Consolidation (gabung via flashloan lalu pecah).** Bandingkan eksekusi terpisah dengan menggabungkan likuiditas/posisi sesaat pada titik perhitungan bagi-hasil/reward/tier, lalu memecahnya kembali di blok yang sama.
3. **Cari titik rasio.** Untuk rumus berbentuk `a·b / c` atau akumulator indeks, cari kombinasi `(a, b, c)` yang membuat sisa pembagian berpihak ke penyerang.
4. **Uji batas populasi.** Perilaku pengguna pertama/terakhir, `totalSupply == 0`, dan transisi antar-tier sering memperbesar asimetri.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** baris ekspresi pembulatan/pembobotan, `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** loop nyata di simulator — N panggilan kecil vs 1 panggilan besar — dengan angka hasil keduanya.
- **Titik 3:** selisih kumulatif (`N × hasil_kecil − hasil_besar`) dan dampaknya dalam satuan aset.

## 4. Routing Simulasi

- **DILARANG menghitung pembulatan/salami-slicing di atas kertas lalu membuangnya sebagai `REJECTED_DUST`.**
- Setiap lead `M-007` **WAJIB** diuji di simulator dengan loop nyata (N iterasi vs 1 panggilan) + **3-Way EV Amplification** (flashloan modal besar + multicall/batch looping + chaining) + **Strike 3 Fuzz** untuk mencari rasio penyebut/pembilang yang menghasilkan kebocoran maksimum.
- Hanya boleh masuk `06` (`REJECTED_DUST` / `REJECTED_NEGATIVE_EV`) bila **log eksekusi test dan fuzz** membuktikan hasilnya tetap merugi.

## 5. Kapan Metode Ini TIDAK Dipakai

- Rumus terbukti linear terhadap jumlah potongan (tidak ada sisa pembagian yang hilang).
- Asimetri ada tetapi tidak dapat dilipatgandakan dan tidak mengunci dana — dan itu **dibuktikan lewat fuzz**, bukan hitungan kertas.
