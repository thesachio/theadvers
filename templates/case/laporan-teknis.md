# <FIND-ID> — <Judul Satu Baris, Tanpa Sensasi>

> **ATURAN PENGISIAN (`cases/<ID>/laporan-teknis.md` — Standar 9-Bagian Wajib `templates/TECHNICAL-REPORT.md`)**:
> 1. **Struktur wajib 9 bagian berurutan** di bawah ini tidak boleh diubah atau dikurangi.
> 2. **Aturan Penulisan Mengikat**:
>    - **Judul tanpa hiperbola**: Tulis mekanisme teknisnya (misal: *"Perhitungan share pada `withdraw` membulatkan ke bawah sebelum pengurangan utang"*), BUKAN *"KRITIS! DANA BISA DICURI"*.
>    - **Setiap klaim punya `Path/File.ext:Lxx-Lyy` (rentang awal-akhir)**: Klaim tanpa lokasi rentang baris tidak dapat diverifikasi.
>    - **Keluaran ditempel apa adanya, bukan diringkas**: Ringkasan log adalah tempat utama bukti palsu masuk.
>    - **Angka, bukan kata**: Tulis *"500.000 USDC"*, bukan *"banyak dana"*.
>    - **Severity dari IMPACT, bukan dari siklus deploy**: Menurunkan severity karena alasan deployment adalah pelanggaran (`VERDICT.md` §0.3).
>    - **Bagian 9 ("Yang TIDAK Diverifikasi") wajib diisi**: Menyatakan batas verifikasi secara jujur lebih meyakinkan daripada klaim sempurna.
> 3. **Yang DILARANG KERAS**:
>    - Menempelkan keluaran yang tidak pernah dijalankan $\rightarrow$ **`FABRICATED_EVIDENCE`**.
>    - Menulis severity lebih tinggi dari yang dibuktikan impact kuantitatif.
>    - Menyembunyikan prasyarat yang tidak terpenuhi atau memakai kata *"berpotensi"* tanpa mengukur.
>    - Memakai token kompresi malas (`...`, `dll.`, `dst.`, `etc.`, `rest of code`).

---

## 1. Ringkasan

[Satu paragraf padat. Kalimat pertama harus bisa dibaca berdiri sendiri oleh engineer yang sibuk: jelaskan apa yang salah pada `Path/File.ext:Lxx-Lyy`, siapa yang dirugikan, dan berapa nilai eksaknya.]

```yaml
ID               : FIND-001 (Eks LEAD-R1-01 | Region: R_1)
Severity         : CRITICAL | HIGH | MEDIUM | LOW (Samakan dengan 09-confirmed-findings.md; Setara S1|S2|S3|S4)
Impact           : theft | drain | grief | dos | freeze | fund-lock | insolvency | bad-debt | manipulation | privilege-escalation | desync
Likelihood       : High | Medium | Low — [Siapa yang bisa memicu & butuh kondisi apa]
Rujukan Severity : [Platform + URL, atau "Matriks Universal (verify/SEVERITY-RUBRIC.md Bagian 4)"]
Asumsi Severity  : [Jika platform lain dipakai, sebutkan perbedaan tier severity-nya secara jujur]
Actor            : unprivileged | external | attacker | user | borrower | liquidator | keeper | relayer | solver | router | validator | oracle
Victim           : sponsor | user | users | protocol | pool | vault | lp | lender | borrower | staker | solver | integrator | third-party
Tangga Bukti     : A | B
Mode Uji         : FORK_LIVE (chain: <...>, block: <...>, RPC: <...>) | LOKAL (<alasan>)
Deployment Match : LIVE_MATCH (Cycle: P4_LIVE_FULL | P3_LIVE_PARTIAL)
Live Identity    : [Identitas terukur dari deploy_parity: accountId() / sha256 ProgramData / impl hash EIP-1967]
Invarian Pecah   : [INV-Ri-xx — Rumus matematis invarian yang dilanggar]
```

---

## 2. Lokasi Kode

- **Lokasi Utama**: `Path/File.ext:Lxx-Lyy`
- **Lokasi Terkait / Callee**: `Path/File2.ext:Laa-Lbb`

```solidity
// Lokasi: Path/File.ext:Lxx-Lyy
// Kutipan verbatim 5-25 baris kode sumber asli yang benar-benar berisi cacat (DILARANG dipotong dengan '...')
```

---

## 3. Akar Masalah

[Jelaskan mekanisme teknis secara presisi, bukan sekadar gejala. Rujuk nomor baris tepat pada `Path/File.ext:Lxx-Lyy`. Jangan hanya menulis *"kurang validasi"* — sebutkan secara eksak validasi/invarian apa yang hilang, bagaimana state berubah dari titik masuk hingga titik mutasi, dan mengapa penjaga (*guard*) yang ada berhasil dilewati.]

---

## 4. Prasyarat & Validasi Realitas Produksi

| # | Prasyarat / Kondisi State Produksi | Terpenuhi? (`ya`/`tidak`) | Bukti Verbatim (`Path/File.ext:Lxx-Lyy` atau Hasil Query On-Chain `cast call` / `cast storage`) |
| :--- | :--- | :--- | :--- |
| 1 | `[State/kondisi kontrak atau likuiditas yang harus ada]` | `ya` | `[Path/File.ext:Lxx-Lyy atau output query RPC pada blok fork]` |
| 2 | `[Akses fungsi titik masuk oleh aktor unprivileged]` | `ya` | `[Path/File.ext:Lxx-Lyy — tidak ada guard onlyOwner/whitelist yang menghalangi]` |

---

## 5. Langkah Reproduksi

1. `[Langkah 1 — Persiapan state / Victim Lifecycle Seeding dengan vm.prank(victim)]`
2. `[Langkah 2 — Eksekusi panggilan penyerang ke Path/File.ext:Lxx dengan parameter konkret]`
3. `[Langkah 3 — Pemicuan penyelesaian / ekstraksi nilai dan pemeriksaan perubahan saldo akhir]`

```bash
$ [Perintah setup lingkungan bila ada]
$ [Perintah persis menjalankan PoC, misal: FOUNDRY_JOBS=1 forge test --match-test test_FIND001_Exploit -vvv]
```

---

## 6. Keluaran Nyata (`BUKTI_SIMULASI`)

```text
$ [Perintah persis yang dijalankan]
[Tempelkan keluaran terminal yang BENAR-BENAR dijalankan apa adanya tanpa diringkas dan tanpa elipsis (...), termasuk log saldo Sebelum vs Sesudah dan baris [PASS]]
```

---

## 7. Dampak Kuantitatif

| Metrik | Nilai Eksak (Angka & Satuan Aset) | Sumber Bukti (`Path/File.ext:Lxx` / Query On-Chain / Log PoC) |
| :--- | :--- | :--- |
| **Dana / Kapasitas Berisiko (`Current` vs `Intended`)** | `[Angka Eksak]` | `[Query saldo kontrak / batas kapasitas desain di Path/File.ext:Lxx]` |
| **Biaya Serangan (Gas + Modal Hangus)** | `[Angka Eksak]` | `[Log eksekusi gas dari PoC di Bagian 6]` |
| **Keuntungan Bersih Penyerang / Kerugian Korban (`Net Delta`)** | `[Angka Eksak]` | `[Selisih saldo akhir dikurangi saldo awal pada log PoC]` |

---

## 8. Rekomendasi Perbaikan

[Penjelasan singkat perubahan kode minimal pada `Path/File.ext:Lxx-Lyy` yang menutup akar masalah tanpa merusak invarian lain.]

```diff
--- a/Path/File.ext
+++ b/Path/File.ext
@@ -xx,y +xx,z @@
- [Baris kode lama yang rentan]
+ [Baris kode baru yang sudah diperbaiki]
```

---

## 9. Yang TIDAK Diverifikasi

*Kejujuran batas verifikasi. Bagian ini wajib diisi — membiarkannya kosong berarti mengklaim kepastian 100% di luar cakupan uji.*

- [x] `[Contoh: Dampak interaksi dengan kontrak periferal di luar repositori ini yang belum ter-deploy pada blok fork belum diuji.]`
- [x] `[Contoh: Perilaku bot/keeper off-chain diasumsikan mengikuti logika standar event on-chain pada Path/File.ext:Lxx.]`
