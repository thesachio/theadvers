# [POV-CALL-02] Sudut Pandang: Subcall Success/Failure State Divergence
- Classes: CLASS-B (Pemanggil ↔ Target Subcall), CLASS-C (Multi-Entity Batch Settlement)
- Trigger Symptom: Kontrak membungkus panggilan eksternal dengan `try/catch`, `.call()` tanpa `require(success)`, atau mengabaikan kegagalan sub-eksekusi lalu melanjutkan mutasi state berbeda antara cabang sukses vs gagal.
- Paired Items: M-002, M-008, M-009, AF-04, AF-09, POV-griefer

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang mengendalikan alamat target sub-panggilan (kontrak `receiver`/`to`/callback), atau yang dapat mengatur takaran gas transaksi induk secara presisi (aturan 63/64 EIP-150).

## 2. Gejala di Kode

1. **Divergensi state antar-cabang (prinsip universal).** Cabang sukses (`try` / `if (success)`) dan cabang gagal (`catch` / `else`) memutasi state secara **tidak simetris** — misal cabang gagal melewati pemotongan penalti, membatalkan penyitaan kewajiban, atau memberi jalur keluar tanpa beban. Berlaku untuk **setiap isolasi sub-eksekusi**, termasuk penanganan fallback/error, *partial settlement* lintas modul, atau lanjutan eksekusi setelah panggilan antar-komponen gagal.
2. **Returnbombing (manifestasi khusus EVM).** `.call()` ke alamat yang dikendalikan pemanggil menyalin nilai balik ke `bytes memory` atau menangkap `catch (bytes memory reason)` **tanpa membatasi ukuran returndata di level assembly**, sehingga biaya ekspansi memori dibebankan ke pemanggil.

### Padanan non-EVM

| Runtime | Bentuk |
| :--- | :--- |
| Solana | CPI yang gagal lalu dilanjutkan tanpa menggulung state; `Result` yang diabaikan |
| Move | `abort`/error yang ditangkap lalu jalur sukses tetap diambil |
| TON | eksekusi lanjutan setelah pesan gagal terkirim; penanganan `ok:false` yang tidak membalik state |

## 3. Rangkaian Serangan

1. **Siapkan:** penyerang mengatur kontraknya sebagai target/callback, atau mengatur takaran gas transaksi induk secara presisi.
2. **Picu:** untuk divergensi state — buat sub-panggilan gagal (revert di penerima, atau kehabisan gas di sub-konteks) agar eksekusi masuk `catch`/`!success`. Untuk returnbombing — kembalikan payload memori raksasa pada returndata.
3. **Ekstraksi:** transaksi induk tetap berhasil dengan state menguntungkan dari cabang gagal, atau seluruh gas pemanggil terkuras oleh biaya ekspansi memori kuadratik sebelum `catch` sempat menyelamatkan (DoS permanen pada likuidasi/penyelesaian).

## 4. Auditor Blindspot

Auditor menganggap keberadaan `try/catch` atau `.call{gas: X}()` sudah otomatis menjamin keamanan dari kegagalan pihak ketiga, sehingga **tidak membandingkan selisih akuntansi antara cabang sukses vs gagal**, dan lupa bahwa biaya penyalinan returndata ke memori dibebankan ke pemanggil.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila cabang sukses dan gagal terbukti memutasi state **identik** (dibuktikan baris demi baris dengan kutipan kedua cabang), dan returndata dibatasi ukurannya di level assembly.
- **Wajib PoC** bila ada asimetri state: tulis dua jalur — sukses dan gagal — lalu bandingkan delta per variabel.
- Untuk returnbombing: PoC wajib mengukur konsumsi gas aktual (`gasleft()` sebelum/sesudah) agar DoS terbukti terukur, bukan dugaan.
