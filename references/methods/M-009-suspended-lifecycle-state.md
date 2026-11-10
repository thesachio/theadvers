# [M-009] Half-Baked / Suspended Lifecycle State (Menyerang Saat Status "Menggantung")
- Classes: CLASS-A (state machine lokal), CLASS-B, CLASS-C (multi-step / async lifecycle)
- Trigger Symptom: Terdapat proses multi-tahap (`request`→`finalize`, `initiate`→`claim`, `createOrder`→`fill`, `startAuction`→`settle`, `propose`→`execute`, `initiateMigration`→`complete`) atau pesan asinkron yang punya status antara.
- Paired Items: AF-04, AF-09, M-005, M-006, POV-griefer

---

## 1. Inti Metode

Auditor menguji siklus hidup yang **selesai tuntas** dari awal hingga akhir. Metode ini mewajibkan pengujian siklus yang **sengaja dihentikan di tengah jalan** (*Pending* / *In-Flight* / *Cooldown*), lalu disusupi aksi dari jalur lain.

Metode ini juga menampung **DoS/penguncian asimetris** (konsep v2): status menggantung adalah tempat paling subur bagi pembekuan dana dan griefing, karena invariant "nilai yang sedang diproses tidak bisa dipakai dua kali" jarang ditegakkan eksplisit.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Mulai Langkah 1** dari proses multi-tahap: `requestWithdraw`, `initiateCooldown`, `createOrder`, `startAuction`, `propose`, `initiateMigration`, atau pengiriman pesan asinkron tahap pertama.
2. **JANGAN jalankan langkah penyelesaiannya.** Selama posisi berada di status *Pending / Menggantung*, panggil fungsi dari jalur lain (`transfer`, `delegate`, `borrow`, `liquidate`, `emergencyWithdraw`, `cancel` berulang) untuk memeriksa apakah saldo/jaminan yang menggantung **belum dikunci** sehingga bisa dipakai dua kali (*double-spend*) atau menghindari likuidasi.
3. **Asimetri pause/penalti.** Apakah `whenNotPaused` memblokir fungsi penyelamatan diri (`repay`, `addCollateral`, `cancel`, `withdraw`) tetapi membiarkan fungsi penalti (`liquidate`, `slash`, `seize`) tetap berjalan?
4. **Antrean yang bisa dibanjiri.** Bisakah penyerang menyumbat antrean/array pending sehingga eksekusi sah selalu revert (DoS murah, dapat diulang)?
5. **Batas waktu.** Apakah ada `deadline`/`cooldown` yang bisa di-reset murah, sehingga pengguna terkunci efektif?

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** entrypoint Langkah 1 + jalur sampingan + entrypoint penyelesaian, masing-masing `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** PoC **berurutan**: Langkah 1 (Gantung) → Panggil Jalur Sampingan → Langkah 2 (Finalize/Claim), dengan angka state di tiap tahap.
- **Titik 3:** nilai terpakai dua kali, atau dana terkunci dengan durasi/biaya yang terukur.

## 4. Routing Simulasi

- **Hanya jika** pada kode Langkah 1 (`request`/`initiate`) objek/share terbukti **langsung dibakar** (`_burn`) dan tidak bisa disentuh fungsi mana pun → `06` (`REJECTED_MISMATCH`, kemustahilan statis **KS-1**).
- Selama posisi masih tercatat di struktur state/antrean *Pending / In-Flight* → **wajib tulis PoC berurutan**. Untuk sub-kasus DoS, fuzz wajib mengacak **jumlah entri antrean** dan **frekuensi reset**, karena pembekuan biasanya hanya muncul setelah antrean melewati ambang tertentu.

## 5. Kapan Metode Ini TIDAK Dipakai

- Tidak ada proses multi-tahap (semua fungsi atomik dan selesai dalam satu transaksi).
- Objek/saldo langsung dibakar di Langkah 1 sehingga tidak ada status menggantung yang bisa disusupi.
