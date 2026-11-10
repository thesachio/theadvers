# [M-006] Bedah Jalur Laten: Likuidasi, Lelang, Slashing, & Sengketa Universal
- Classes: LATENT-PATH, LIQUIDATION, AUCTION, DISPUTE, SLASHING
- Trigger Symptom: Terdapat modul likuidasi posisi tidak sehat, lelang penyitaan, penyelesaian sengketa (*dispute/challenge*), *slashing*, atau *emergency settlement*.
- Paired Items: AF-06, AF-09, POV-liquidator, DOM-lending

---

## 1. Inti Metode Bedah
M-006 berfokus pada jalur yang jarang dieksekusi dalam kondisi normal tetapi memegang kekuasaan mutlak untuk menyita dana, menghukum partisipan, atau menutup posisi secara paksa pada [EDGE-CONTROL/LATENT].
## 2. Langkah Bedah Operasional (STAGE-C2 & STAGE-D)
1. Uji Syarat Ambang Likuidasi / Slashing (*Health Factor & Threshold Audit*):
   - Periksa rumus kesehatan posisi di Path/File.ext:Lxx-Lyy: apakah perhitungan kesehatan sebelum dan sesudah likuidasi konsisten?
   - Dapatkah posisi yang sebenarnya sehat dilikuidasi karena keterlambatan pembaruan bunga/oracle atau manipulasi sesaat?
   - Setelah likuidasi sebagian (*partial liquidation*), apakah posisi korban justru menjadi lebih buruk atau menyisakan utang tanpa agunan (*bad debt*) yang tidak dihapusbukukan?
2. Uji Insentif & Pemblokiran Likuidator (*Unliquidatable Position / Self-Liquidation*):
   - Apakah pemilik posisi dapat melakukan likuidasi diri sendiri (*self-liquidation*) untuk mendapatkan diskon/bonus penyitaan dan melempar sisa utang buruk ke protokol?
   - Apakah posisi kecil (*dust position*) atau token yang memiliki daftar hitam (*blacklist*) / *revert-on-zero* dapat membuat fungsi likuidasi selalu *revert*, sehingga utang macet tidak pernah bisa dibersihkan?
3. Uji Permainan Waktu pada Lelang & Sengketa (*Auction / Dispute Window Manipulation*):
   - Pada mekanisme lelang atau jendela tantangan (*challenge period*): apakah penyerang dapat memblokir tawaran/tantangan sah di detik terakhir, memanipulasi harga penyelesaian, atau mengklaim kemenangan sengketa tanpa membakar jaminan (*bond*) lawan secara benar?

## 3. Syarat Bukti di STAGE-D (L-PROVE)
- Buktikan skenario konkret di mana posisi sehat tersita tidak sah, likuidasi macet permanen, atau likuidator/pemilik posisi mengekstrak nilai melebihi agunan yang seharusnya.
