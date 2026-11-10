# [M-009] Bedah Penguncian Nilai, Insolvensi, & DoS Asimetris Universal
- Classes: DOS, GRIEFING, VALUE-LOCKING, INSOLVENCY
- Trigger Symptom: Terdapat antrean penarikan, loop atas koleksi dinamis, pengiriman paksa ke penerima (*push payment*), ketergantungan pada saldo eksak (==), atau prasyarat yang dapat diblokir pihak ketiga.
- Paired Items: AF-09, AF-05, POV-griefer

---

## 1. Inti Metode Bedah
M-009 menguji apakah pelaku dengan modal minimal dapat membekukan dana pengguna lain, menggagalkan penyelesaian batch/likuidasi, atau merusak asumsi kesetaraan state secara permanen (Prioritas EV `P3`).
## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Audit Kegagalan Pengiriman Berantai (*Push-Payment & Batch Revert*):
   - Cari setiap fungsi penyelesaian (*settlement*, distribusi reward, pengembalian dana lelang, pemrosesan antrean penarikan) di Path/File.ext:Lxx-Lyy yang memproses banyak penerima dalam satu transaksi.
   - Jika satu penerima menolak menerima aset (kontrak tanpa receive/fallback, akun masuk daftar hitam *blacklist*, atau akun ditutup), apakah seluruh batch ikut *revert* dan mengunci dana pengguna lain?
2. Audit Ketergantungan Kesetaraan Kaku & Pemblokiran Prasyarat (*Strict Equality & Dust Griefing*):
   - Cari pemeriksaan dengan operator == pada saldo/state atau syarat require(totalDebt == 0) untuk menutup/meng-upgrade modul.
   - Uji apakah penyerang dapat mengirimkan 1 wei / 1 unit secara langsung (atau menyetor *dust* atas nama korban) untuk menggagalkan syarat tersebut atau mereset pengatur waktu (*cooldown timer*) korban secara berulang.
3. Audit Pembengkakan Struktur Data (*Unbounded Loop / Storage Bloat*):
   - Apakah pengguna tanpa izin dapat menambahkan elemen ke dalam array/antrean/peta yang nantinya wajib diiterasi oleh fungsi kritis (withdraw, liquidate, distribute) hingga melampaui batas komputasi/gas blok?

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Tunjukkan tindakan penyerang berbiaya rendah beserta baris kode di Path/File.ext:Lxx-Lyy yang menyebabkan fungsi penarikan/likuidasi selalu gagal (*permanent atau repeatable brick*).
