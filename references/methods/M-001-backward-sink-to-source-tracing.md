# [M-001] Backward Sink-to-Source Tracing (Kebalikan Arah Baca Auditor)
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Terdapat fungsi yang mengeluarkan/mencetak/menghapus nilai (transfer, mint, burn, withdraw, repay, seize) dan alur masuknya tampak dijaga guard yang rapi bila dibaca dari atas ke bawah.
- Paired Items: AF-01, AF-02, M-002, M-007, POV-unprivileged

---

## 1. Inti Metode

Auditor standar membaca fungsi dari baris paling atas (validasi/guard) ke bawah, sehingga mudah terhipnotis bahwa fungsi sudah terlindungi. **M-001 membalik arah baca**: mulai dari titik pengeluaran nilai paling bawah (*The Sink*) lalu mundur ke atas (*The Source*).

Pertanyaan pemandu tunggal:

> *"Bagaimana cara memperbesar angka yang keluar di Sink sambil memperkecil pengorbanan di Source, menggunakan input yang diizinkan?"*

Konservasi nilai (v2) adalah **konsekuensi** dari metode ini: bila jumlah yang keluar tidak setara dengan yang masuk di seluruh variabel berpasangan, invariant akuntansi pecah. M-001 menemukan **jalur**; M-002 mengukur **selisihnya**.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Tandai *The Sink*.** Cari baris yang benar-benar mengeluarkan nilai: `transfer`/`safeTransfer`, `mint`/`_mint`, `burn`, `withdraw`, penghapusan utang, atau penyitaan jaminan. Catat `Path/File.ext:Lxx-Lyy`.
2. **Lacak mundur setiap variabel pembentuk angka di Sink.** Untuk setiap variabel, tanyakan: *siapa yang bisa menulisnya, lewat pintu mana, dengan syarat apa?*
3. **Cari asimetri Source vs Sink.** Apakah ada jalur yang menambah angka Sink **tanpa** menambah beban di Source (atau sebaliknya)? Kandidat: pembulatan ke bawah saat menambah kewajiban, pembulatan ke atas saat mengurangi hak, donasi langsung yang mengubah denominator, atau state yang dibaca dari sumber berbeda dengan state yang ditulis.
4. **Periksa pasangan variabel berpasangan.** Untuk setiap pasangan (saldo internal vs saldo riil, `totalSupply` vs `sum(balances)`, utang vs kolateral), tanyakan apakah keduanya selalu bergerak bersama. Pasangan yang bisa bergerak sendiri-sendiri = kandidat.
5. **Catat ke `05-raw-leads.md`** dengan `[WAVE-1-BLIND]` (C1) lalu pasangkan `AF-xx` di C2.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** rangkaian pemanggilan dari entrypoint publik ke baris Sink, beserta guard yang dilewati — `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** PoC yang memaksimalkan selisih Sink−Source, atau jejak angka konkret langkah demi langkah.
- **Titik 3:** delta nilai terukur (sebelum vs sesudah) + invariant dari `FACTS.md`/`path-map.md` yang pecah.

## 4. Routing Simulasi (Simulation-First Gate)

Selama jalur Source→Sink tidak melanggar kemustahilan statis sempit (KS-1..KS-4), **WAJIB langsung tulis tes simulasi PoC** dan **Strike 3 Fuzzing** (`testFuzz_`) untuk memaksimalkan selisih antara Sink dan Source. Dilarang menggugurkan dengan hitungan kertas.

## 5. Kapan Metode Ini TIDAK Dipakai

- Modul tidak mengeluarkan nilai apa pun (murni view/registry tanpa sink).
- Jalur Sink sudah dibuktikan tertutup oleh guard statis yang tidak tembus 5 Jalur Permissionless (→ `04-code-guarded.md`, rujuk `M-005`).
