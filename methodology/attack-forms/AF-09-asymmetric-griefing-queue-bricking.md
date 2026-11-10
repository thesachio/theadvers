# [AF-09] Pembekuan Antrean/Batch, Blacklist/Revert Trap, & DoS Asimetris
- Classes: QUEUE-BRICKING, PUSH-PAYMENT-DOS, DUST-GRIEFING, UNBOUNDED-LOOP
- Trigger Symptom: Fungsi penarikan/likuidasi/settlement memproses banyak pengguna sekaligus, mengirim aset secara *push*, atau bergantung pada kondisi state yang rapuh.
- Paired Items: M-006, M-009, POV-griefer

---

## 1. Mekanisme Serangan Universal
Penyerang menyisipkan satu entri beracun berbiaya sangat murah ke dalam antrean, batch penyelesaian, lelang, atau posisi bersama sehingga fungsi kritis protokol selalu *revert* dan membekukan dana pengguna lain atau menggagalkan likuidasi (Prioritas EV `P3`).

## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Cari Titik Kegagalan Tunggal dalam Koleksi/Antrean di `Path/File.ext:Lxx-Lyy`:
   - Periksa apakah loop pemrosesan batch melakukan panggilan transfer eksternal tanpa try/catch atau tanpa pola *pull-over-push*.
   - Periksa apakah penyerang dapat mendaftarkan penerima berupa kontrak yang selalu *revert* saat menerima aset, atau akun token yang dibekukan (*blacklisted* seperti USDC/USDT).
2. Uji *Dust Reset* & *Capacity Exhaustion***:
   - Uji apakah fungsi `depositFor(victim, 1)` atau `transfer(victim, 1)` memperpanjang waktu kunci (*lockup timestamp*) korban tanpa izin korban.
   - Uji apakah batas kuota antrean global dapat dipenuhi oleh ribuan transaksi mikro bernilai `1 wei`.
3. **Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika kegagalan satu elemen diisolasi (dilewati/dicatat sebagai klaim tertunda), terdapat batas minimum ekonomi (*minimum deposit/stake*) yang mahal bagi penyerang, dan pengatur waktu hanya berubah jika dipanggil oleh pemilik akun sendiri.
