# 04-CODE-GUARDED — Wadah Jalur & Hipotesis Terjaga Kode (STAGE-C1 & STAGE-C2)

> ATURAN PENGISIAN (`ZERO-COMPRESSION LAW`):
> 1. Wadah ini mencatat setiap jalur ([EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT]) atau hipotesis serangan di Tahap C (C1 maupun C2) yang setelah diperiksa terbukti sudah dijaga secara rapat oleh kode.
> 2. Mencatat jalur terjaga secara presisi mencegah agen atau Subagent berikutnya memeriksa ulang jalur buntu yang sama di putaran lain.
> 3. Setiap entri wajib menyertakan jangkar verbatim `Path/File.ext:Lxx-Lyy` dan ekspresi kode penjaganya. Dilarang memakai token kompresi (..., dll., dst., etc., rest of logic).
> 4. **Wadah ini HANYA untuk guard statis/struktural.** Guard dinamis/matematis (rasio, pembulatan, saldo, waktu, panjang array, harga) **DILARANG** di sini — wajib ke `05-raw-leads.md` untuk diuji di STAGE-D.

---

## 1. DEFINISI `TERSANGKAL` — 5 Jalur Permissionless (WAJIB)

Status `TERSANGKAL` hanya sah bila guard terbukti **tidak tembus kelima jalur** di bawah. Definisi operasional lengkap: `references/methods/M-005-guard-inversion.md` §3.

| # | Nama Jalur | Pertanyaan Uji Wajib |
| :--- | :--- | :--- |
| **J1** | Mutasi Variabel Guard | Apakah ada fungsi publik / inisialisasi ulang / celah akses yang dapat mengubah variabel pembentuk guard itu sendiri? |
| **J2** | Pemicuan via Entitas Hulu | Apakah pemegang izin adalah kontrak hulu (Router, Manager, Hub, Vault, Forwarder) yang punya titik masuk publik sehingga pengguna tak berizin dapat memicunya? |
| **J3** | Peracunan State Input | Apakah di dalam tubuh fungsi berizin (Keeper, Relayer, Solver, Operator) ada pembacaan state/saldo/antrean/array yang nilainya bisa dimanipulasi pihak tak berizin — membajak hasil eksekusi rutin atau memicu DoS revert permanen saat eksekutor sah menjalankannya? |
| **J4** | Eskalasi Lintas-Kontrak (`nonReentrant`) & Asimetri `whenNotPaused` | Apakah `nonReentrant` hanya mengunci mutex lokal sementara panggilan keluar membiarkan kontrak pasangan/`view` membaca state timpang? Apakah `whenNotPaused` memblokir fungsi penyelamatan diri (`repay`, `addCollateral`, `cancel`) tetapi membiarkan fungsi penalti (`liquidate`, `slash`) tetap berjalan? |
| **J5** | Cross-Whitelist Confusion & Callback `initiator` | Apakah `isWhitelisted[x]` tidak memverifikasi kecocokan pasangan aset (`pool.token() == asset`)? Apakah callback (`onFlashLoan`, `swapCallback`, `onERC721Received`, `lzReceive`) hanya memeriksa `msg.sender` tanpa memeriksa `initiator`/`srcSender`? |

**Aturan keras:** guard yang **TEMBUS** salah satu jalur **DILARANG** masuk wadah ini — wajib ke `05-raw-leads.md` sebagai lead, dengan tag `[TEMBUS-Jn]`.

---

## 2. TABEL JALUR TERJAGA KODE PER WILAYAH (R_1 .. R_N)

| Guard ID | Region (R_i) | Gelombang (C1-BLIND / C2-CROSS) | Titik Masuk & Simbol (NamaModul.namaFungsi) | Hipotesis Serangan yang Diuji | Jangkar Penjaga Kode (Path/File.ext:Lxx-Lyy) | Status | Metode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| GUARD-R1-01 | R_1 | C1-BLIND | [NamaModul.namaFungsi] | [Contoh: Mencoba menarik melebihi saldo share melalui pembulatan ke atas] | [Path/File.ext:L88-L94] | TERSANGKAL | M-005 |

**Nilai `Status` yang sah:** `TERSANGKAL` (lolos J1–J5) · `TEMBUS-J1` … `TEMBUS-J5` (tembus satu jalur → **pindahkan entri ini ke `05-raw-leads.md`**, jangan ditinggal di sini).

---

## 3. TABEL UJI 5 JALUR PER GUARD (WAJIB LENGKAP)

Setiap GUARD berstatus `TERSANGKAL` di §2 **wajib** punya tepat **5 baris** di bawah. Satu baris per jalur. Baris yang kosong = entri tidak sah.

| Guard ID | Jalur | Hasil (TERTUTUP / TEMBUS) | Alasan / Jangkar Bukti (Path/File.ext:Lxx-Lyy) | Metode Terkait |
| :--- | :--- | :--- | :--- | :--- |
| GUARD-R1-01 | J1 | TERTUTUP | [Variabel guard `immutable`, tidak ada setter — Path/File.ext:L12] | M-005 |
| GUARD-R1-01 | J2 | TERTUTUP | [Pemegang izin adalah EOA tunggal, bukan kontrak hulu — Path/File.ext:L31] | M-008 |
| GUARD-R1-01 | J3 | TERTUTUP | [Fungsi berizin tidak membaca state yang bisa ditulis publik — Path/File.ext:L88-L94] | M-005, M-009 |
| GUARD-R1-01 | J4 | TERTUTUP | [Tidak ada panggilan keluar; `whenNotPaused` tidak menutup fungsi penyelamatan — Path/File.ext:L52] | POV-CALL-01 |
| GUARD-R1-01 | J5 | TERTUTUP | [N/A: tidak ada callback/whitelist di jalur ini — terbukti tanpa panggilan keluar pada Path/File.ext:L1-L200] | M-008 |

Aturan tabel ini:
- `TERTUTUP` wajib menyebut **alasan + jangkar `Path/File.ext:Lxx-Lyy`**. Alasan tanpa jangkar = tidak sah.
- `TEMBUS` pada jalur mana pun → status di §2 berubah menjadi `TEMBUS-Jn`, dan entri **dipindahkan ke `05-raw-leads.md`**.
- Dilarang menulis "sudah dijaga admin" atau "hanya owner" sebagai alasan `TERTUTUP` — itu **klaim**, bukan bukti; uji J1–J2 dulu.
