# PATH-MAP — Rekonsiliasi 100% Berkas, Kapasitas Nilai (L-VALUE), & Peta 3-Edge (L-PATH) (theadvers v2.0)

> ATURAN CAKUPAN 100% & PENANGANAN SALDO `0`:
> 1. Pada STAGE-0, 100% berkas kode sumber dalam *scope*** wajib masuk ke **Bagian 1 (Tabel Rekonsiliasi). Tidak boleh ada satu pun berkas yang terlewat.
> 2. Berkas Tier 3 wajib dibuktikan 1-pass tidak menyimpan/memindahkan nilai atau kontrol dengan jangkar :Lxx sebelum diberi label [LOCKED-TIER3].
> 3. Pada STAGE-A, dilarang mengabaikan modul hanya karena Current Balance == 0; wajib ukur Intended Capacity & Latent Power-nya.
> 4. Pada STAGE-B, setiap Wilayah R_i wajib memetakan ketiga jenis jalur: `[EDGE-ASSET]`, `[EDGE-VALUATION]`, dan `[EDGE-CONTROL/LATENT]`.

---

## 1. TABEL REKONSILIASI 100% BERKAS SUMBER DALAM SCOPE (STAGE-0 / L-PART)

- Total Berkas Sumber dalam Scope: 0
- Total Tier 1 (`CORE-ASSET`): 0
- Total Tier 2 (`VALUATION-CONTROL-LATENT`): 0
- Total Tier 3 (`ISOLATED-PERIPHERAL`): 0

| No | Path Berkas Sumber (Path/File.ext) | Bahasa / Runtime | Klasifikasi Tier (TIER-1 / TIER-2 / TIER-3) | Alokasi Wilayah (R_1..R_N atau [LOCKED-TIER3]) | Peran Ekonomi / Bukti Isolasi 1-Pass (Path/File.ext:Lxx-Lyy wajib untuk Tier 3) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [src/CoreVault.ext] | [Bahasa] | TIER-1 | R_1 | [Menyimpan aset utama, mencetak/membakar share pengguna di :L20-L140] |
| 2 | [src/Liquidator.ext] | [Bahasa] | TIER-2 | R_1 | [Saldo awal 0, namun memiliki Intended Capacity mengeksekusi penyitaan kolateral di :L45-L110] |
| 3 | [src/interfaces/ICore.ext] | [Bahasa] | TIER-3 | [LOCKED-TIER3] | [1-Pass Verified: Hanya deklarasi antarmuka/tipe data di :L1-L60, 0 state & 0 logika eksekusi] |

---

## 2. RINGKASAN PARTISI WILAYAH UANG (R_1 .. R_N) & PERINGKAT EV (SOUL.md §3)

| Region ID | Nama Wilayah Uang | Peringkat EV (P1`–`P5) | Berkas Tier 1 & Tier 2 yang Tercakup | Titik Singgung dengan Wilayah Lain |
| :--- | :--- | :--- | :--- | :--- |
| R_1 | [Nama Wilayah 1] | P1 | [src/CoreVault.ext, src/Liquidator.ext] | [Memanggil harga dari R_2 di src/CoreVault.ext:L88] |

---

## 3. PETA VERTIKAL PER WILAYAH (STAGE-A: L-VALUE & STAGE-B: L-PATH)

*Gandakan sub-bagian 3.x di bawah ini untuk setiap Wilayah R_1, R_2, ..., R_N saat wilayah tersebut menjadi [ACTIVE].*

### 3.1 WILAYAH R_1 — [Nama Wilayah Uang]

#### A. Tabel Kapasitas Nilai & Kekuasaan Laten (STAGE-A / L-VALUE)

| Modul / Berkas (Path/File.ext) | Aset / Hak Klaim / State yang Dikelola | Current Balance / Initial State | Intended Capacity & Latent Power *(Kapasitas maksimal + hak mint/burn/sita/kontrol)* | Core Value Invariant & Jangkar Kode (Path/File.ext:Lxx-Lyy) |
| :--- | :--- | :--- | :--- | :--- |
| [src/CoreVault.ext] | [Token Kolateral & Share Vault] | [0 saat deploy] | [100% TVL pengguna; otoritas mint/burn share di :L50-L95] | [totalAssets() >= sum(shares * rate) pada src/CoreVault.ext:L100-L130] |

#### B. Pemetaan Jalur 3-Edge (STAGE-B / L-PATH)

1. `[EDGE-ASSET]` (Aliran Masuk, Perpindahan, Mint/Burn, & Keluar Aset):
   - [EDGE-ASSET] [src/CoreVault.ext:L50-L78] | [CoreVault.deposit -> mutasi saldo & pencetakan share] | [Aset berpindah dari pengirim ke vault; share dicetak ke penerima]
   - [EDGE-ASSET] [src/CoreVault.ext:L80-L115] | [CoreVault.withdraw -> pembakaran share & transfer keluar] | [Share dibakar sebelum/sesudah aset dikirim keluar]
2. `[EDGE-VALUATION]` (Perhitungan Harga, Kurs, Indeks, & Pembulatan Presisi):
   - [EDGE-VALUATION] [src/CoreVault.ext:L120-L145] | [CoreVault.convertToShares] | [Menghitung share = assets * totalSupply / totalAssets(); rawan pembulatan/manipulasi denominator]

3. `[EDGE-CONTROL/LATENT]` (Otorisasi, Likuidasi, Dispute, Callback, & Jembatan Off-Chain):
   - [EDGE-CONTROL/LATENT] [src/Liquidator.ext:L45-L92] | [Liquidator.liquidate] | [Jalur laten penyitaan kolateral saat health factor < 1e18; memanggil callback eksternal di :L79]
