# [M-002] State-Transition Differential Analysis (Expected vs. Actual Delta)
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Fungsi memutasi beberapa variabel berpasangan (saldo↔utang, share↔aset, kolateral↔kapasitas pinjam, indeks↔akrual) dan keseimbangan antar-variabel hanya diasumsikan, tidak ditegakkan `require`.
- Paired Items: AF-02, M-001, M-007, M-004, POV-unprivileged

---

## 1. Inti Metode

Setiap mutasi state wajib menjaga keseimbangan antara **perubahan hak** dan **perubahan kewajiban** di seluruh variabel berpasangan — baik di dalam satu entitas maupun lintas-entitas. Metode ini membandingkan **delta yang diharapkan** (dari rumus desain) dengan **delta yang benar-benar terjadi** (dari eksekusi).

> Metrik inti: `ΔExpected(v) ≠ ΔActual(v)` pada salah satu variabel pasangan = invariant akuntansi pecah.

Ini juga rumah bagi **konservasi nilai** (konsep v2): nilai tidak boleh tercipta tanpa setoran setara, dan tidak boleh hilang tanpa pengurangan kewajiban setara.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Daftar variabel berpasangan** untuk berkas di `R_i`. Contoh pasangan: `totalAssets ↔ totalSupply`, `userBalance ↔ userDebt`, `collateral ↔ borrowLimit`, `rewardIndex ↔ userRewardDebt`.
2. **Tulis persamaan keseimbangan** untuk setiap pasangan: apa yang harus selalu benar setelah fungsi apa pun selesai.
3. **Hitung ΔExpected** dari rumus desain (baca ekspresi di kode, catat `Path/File.ext:Lxx-Lyy`).
4. **Cari jalur di mana ΔActual ≠ ΔExpected.** Tiga sumber umum:
   - **Pembulatan asimetris** — floor saat menambah kewajiban, ceil saat mengurangi hak.
   - **Urutan operasi** — saldo dibaca sebelum mutasi, ditulis sesudah state lain berubah.
   - **Sumber berbeda** — angka dihitung dari `balanceOf` sementara tagihan dihitung dari variabel internal (atau sebaliknya).
5. **Uji kondisi ekstrem** untuk memperbesar delta: `0`, `1` unit terkecil, `MAX`, `totalSupply == 0`, serta paruh pertama/terakhir populasi.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** fungsi yang memutasi pasangan + jalur masuknya, `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** delta terukur per variabel: nilai sebelum, input, hasil hitung baris demi baris, nilai sesudah.
- **Titik 3:** invariant persis yang pecah + angka selisihnya (bukan "berpotensi").

## 4. Routing Simulasi

Wajib PoC + **Strike 3 Fuzz** yang mengacak ukuran input dan urutan operasi. Untuk pembulatan, fuzz wajib mencakup nilai batas (`1`, `3`, `type(uint).max / rate`), karena bug pembulatan hampir selalu hanya muncul di ekstrem.

## 5. Kapan Metode Ini TIDAK Dipakai

- Tidak ada variabel berpasangan (mis. kontrak pencatat tunggal tanpa akuntansi ganda).
- Selisih terbukti hanya debu yang tidak dapat dilipatgandakan dan tidak mengunci dana (→ `REJECTED_DUST` di `06`, wajib log fuzz).
