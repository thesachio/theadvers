# [M-003] Irrational Multi-Identity Sybil & Zero-Time Loop
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Protokol memberi reward/bonus/penalti berbasis identitas, atau memungkinkan satu pihak memegang beberapa posisi/akun/objek yang dapat berinteraksi dalam satu transaksi atau satu jendela eksekusi.
- Paired Items: AF-03, AF-05, M-005, M-009, POV-unprivileged

---

## 1. Inti Metode

Jangan pernah menyempitkan metode ini menjadi "dua EOA / dua wallet". Prinsip mekanisnya:

> **Dua atau lebih identitas, akun, objek, capability, atau kontrak yang dikendalikan satu penyerang dan dapat berinteraksi secara atomik atau dalam jendela eksekusi yang sama (Δt = 0), di mana kerugian pada satu identitas dikompensasi oleh keuntungan yang lebih besar pada identitas lainnya.**

### Manifestasi lintas-paradigma

| Runtime | Bentuk konkret |
| :--- | :--- |
| EVM / Tron | Dua EOA atau kontrak pembantu (`Attacker_A`, `Attacker_B`) dalam satu transaksi/batch |
| Solana | Dua signer, atau satu signer mengendalikan beberapa account/alias dalam satu instruksi |
| Move (Sui/Aptos) | Dua capability/posisi/objek milik satu owner dalam satu PTB |
| TON | Dua actor atau dua jalur pesan dikendalikan satu penyerang terhadap target yang sama |

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Self-Transfer & Ping-Pong Loop.** Apa yang terjadi bila identitas pertama memindahkan/mendelegasikan hak ke dirinya sendiri (`from == to`), atau memantulkannya `A → B → A` berulang dalam jendela yang sama (Δt = 0)? Cari akrual/bonus yang dihitung per-hop tetapi tidak pernah tergerus.
2. **Self-Liquidation / Self-Penalty Arbitrage.** Apa yang terjadi bila identitas pertama sengaja membuat posisinya terkena likuidasi/slashing/lelang/bad-debt, sementara identitas kedua bertindak sebagai likuidator/penawar yang memanen bonus atau mengalihkan kerugian (*bad debt socialization*) ke kolam publik?
3. **Zero / Boundary & Dust Amplification.** Masukkan `0`, `1` unit terkecil, atau `batas_minimum − 1` antar-identitas untuk menguji apakah biaya/penalti terpotong menjadi `0` karena pembulatan dan dapat di-loop.
4. **Sybil pada gerbang berbasis identitas.** Hitung ulang reward/kuota/whitelist bila jumlah identitas dilipatgandakan dalam satu blok.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** fungsi yang membedakan atau tidak membedakan identitas + jalur masuknya.
- **Titik 2:** PoC **WAJIB** menghadirkan minimal dua identitas/akun/objek/capability yang dikendalikan penyerang (`Attacker_A` dan `Attacker_B`) dalam satu jendela eksekusi. **PoC satu identitas yang gagal TIDAK membuktikan gugurnya hipotesis multi-identitas.**
- **Titik 3:** `Profit(Attacker_A + Attacker_B) > 0`, atau `bad debt` terukur pada kolam publik.

## 4. Routing Simulasi

- Untuk sub-kasus *Self-Liquidation / Bad-Debt* atau *Ping-Pong Loop*, **DILARANG menggugurkan lead dengan hitungan pertidaksamaan di atas kertas**. Wajib simulasi test + **Strike 3 Fuzz** yang mengacak ukuran posisi, kemiringan harga flashloan, dan urutan likuidasi parsial.
- Untuk sub-kasus loop, fuzz wajib mengacak **jumlah iterasi** karena laba sering baru positif di iterasi ke-n.

## 5. Kapan Metode Ini TIDAK Dipakai

- Protokol membatasi satu identitas per entitas secara kriptografis dan tidak ada interaksi antar-akun (mis. satu posisi per address tanpa transfer).
- Keuntungan satu identitas terbukti selalu lebih kecil dari biayanya, tanpa jalur amplifikasi (→ `REJECTED_NEGATIVE_EV` di `06`, wajib log fuzz).
