# [M-005] Guard-Inversion (Membalik Guard Kode Menjadi Target Manipulasi)
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Terdapat `require`/`if (...) revert`/`assert!`/`constraint` yang membandingkan dua kondisi turunan variabel, atau fungsi berizin (`onlyX`) yang memanggil keluar atau membaca state yang bisa disentuh pihak lain.
- Paired Items: AF-07, AF-08, M-008, M-009, POV-unprivileged

---

## 1. Inti Metode

Guard bukan tembok mati, melainkan **rumus yang bergantung pada variabel pembentuknya**. Jika variabel pembentuknya dapat digeser sebelum guard dieksekusi, guard tersebut dapat **ditembus** — atau justru dipakai sebagai **senjata DoS** terhadap pengguna lain.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Dekomposisi guard.** Untuk setiap `require(X >= Y)` atau `if (...) revert`: identifikasi **seluruh** variabel penyusun `X` dan `Y`, beserta `Path/File.ext:Lxx-Lyy` masing-masing.
2. **Uji pergeseran.** Berdasarkan `FACTS.md`: bisakah fungsi publik lain (satu entitas pada `CLASS-A`, atau entitas lain / flashloan / donasi / callback pada `CLASS-B`/`CLASS-C`) mengubah `X` atau `Y` sesaat sebelum baris guard dieksekusi?
3. **Untuk guard izin/struktural statis** (variabel permission `immutable` atau dikunci admin): **DILARANG berhenti hanya dengan menulis "variabel hanya bisa diubah admin"**. Wajib uji terhadap 5 Jalur Permissionless di bawah.

## 3. Lima Jalur Permissionless (wajib diuji sebelum status `TERSANGKAL`)

Inilah definisi operasional `TERSANGKAL` di `04-code-guarded.md` — guard hanya boleh dicatat sebagai terjaga bila **tidak tembus kelima jalur** ini.

| # | Nama | Pertanyaan uji | Metode |
| :--- | :--- | :--- | :--- |
| **1** | **Mutasi Variabel Guard** | Apakah ada fungsi publik / inisialisasi ulang / celah akses yang dapat mengubah variabel pembentuk guard itu sendiri? | `M-005` |
| **2** | **Pemicuan via Entitas Hulu** | Apakah pemegang izin adalah kontrak hulu (Router, Manager, Hub, Vault, Forwarder) yang punya titik masuk publik sehingga pengguna tak berizin dapat memicunya? | `M-008` |
| **3** | **Peracunan State Input** | Apakah di dalam tubuh fungsi berizin (Keeper, Relayer, Solver, Operator) ada pembacaan state/saldo/antrean/array yang nilainya bisa dimanipulasi pihak tak berizin — membajak hasil eksekusi rutin atau memicu DoS revert permanen saat eksekutor sah menjalankannya? | `M-005`, `M-009` |
| **4** | **Eskalasi Lintas-Kontrak pada `nonReentrant` & Asimetri `whenNotPaused`** | Apakah `nonReentrant` hanya mengunci mutex lokal sementara panggilan keluar membiarkan kontrak pasangan/`view` membaca state timpang? Apakah `whenNotPaused` memblokir fungsi penyelamatan diri (`repay`, `addCollateral`, `cancel`) tetapi membiarkan fungsi penalti (`liquidate`, `slash`) tetap berjalan? | `POV-call` / `M-009` |
| **5** | **Cross-Whitelist Confusion & Unchecked Callback Initiator** | Apakah `isWhitelisted[x]` tidak memverifikasi kecocokan pasangan aset (`pool.token() == asset`)? Apakah callback (`onFlashLoan`, `swapCallback`, `onERC721Received`, `lzReceive`) hanya memeriksa `msg.sender` tanpa memeriksa `initiator`/`srcSender`? | `M-008` |

**Aturan keras:** guard statis yang **TEMBUS** salah satu jalur di atas **DILARANG** masuk `04-code-guarded.md` — wajib ke `05-raw-leads.md` sebagai lead.

## 4. Routing Simulasi

- Guard dengan variabel yang **tidak bisa** diubah penyerang → hanya boleh gugur ke `06` (`REJECTED_PRIVILEGED_FANTASY`) bila hipotesis **murni** menuntut Admin/Pemilik sah menyuntikkan parameter bunuh diri **di luar** batas validasi kode.
- Bila hipotesis bekerja melalui salah satu dari 5 Jalur Permissionless — atau merupakan **Valid-Range Config Brick** (admin menyetel parameter di dalam `require(MIN..MAX)` yang sah namun merusak perhitungan/membekukan dana) — hipotesis itu **100% VALID** dan wajib dibuatkan PoC.
- Guard **dinamis/matematis/state-dependent** (saldo, rasio share, waktu, harga, panjang array) → **DILARANG ditolak di atas kertas**; wajib simulasi + **Strike 3 Fuzzing**.

## 5. Kapan Status `TERSANGKAL` Sah

Hanya bila: (a) kelima jalur diuji satu per satu, (b) tiap jalur punya alasan tertutup yang merujuk `Path/File.ext:Lxx-Lyy`, dan (c) tidak ada jalur yang lulus. Dicatat di `04-code-guarded.md` dengan bukti per jalur.
