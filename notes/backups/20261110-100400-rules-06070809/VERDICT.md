# VERDICT — Standar Pengadilan Bukti & Pemisahan Wadah Kanonik (theadvers v2.0)

Dokumen ini adalah hukum acara pengadilan bukti pada Tahap E (`STAGE-E`) dan Tahap F (`STAGE-F`). Tidak ada satu pun kandidat dari 05-raw-leads.md yang boleh naik ke 09-confirmed-findings.md tanpa melewati pengujian ketat di bawah ini.

---

## 1. Syarat Mutlak Tiga Titik Bukti Segitiga (L-PROVE)

Sebuah kandidat hanya sah disebut Temuan Terkonfirmasi (`09-confirmed-findings.md`) apabila ketiga titik berikut terbukti secara simultan dan tertulis tanpa pemotongan logika:

1. Titik 1 — Jejak Kode Eksak & Keterjangkauan Jalur (`L-PATH` Verified):
   - Menyebutkan titik masuk publik/eksternal/instruksi/handler yang nyata (Path/File.ext:Lxx-Lyy).
   - Menunjukkan urutan pemanggilan hingga titik mutasi state/aset/valuasi (Path/File.ext:Lxx-Lyy).
   - Membuktikan bahwa seluruh penjaga kode (require, assert, ensure, *signer/account/capability check*, modifier) di sepanjang jalur tersebut benar-benar dapat dilewati oleh pelaku sesuai model ancaman.

2. Titik 2 — Bukti Eksekusi Konkret atau Jejak Matematika Eksak (`L-PROVE` Verified):
   - Standar Utama (Eksekusi Nyata): Hasil uji yang dapat direproduksi pada *test runner* ekosistem terkait (forge test, cargo test, move test, snforge, pytest, go test, atau harness simulasi), ATAU
   - Standar Setara (Jejak Matematika/State Konkret): Perhitungan angka konkret langkah demi langkah pada setiap baris ekspresi kode (dengan nilai awal, nilai input, hasil pembulatan/pembagian integer, dan nilai akhir yang terukur eksak).
   - Larangan: Narasi spekulatif seperti *"bisa menyebabkan overflow/kerugian"* tanpa angka konkret atau tanpa eksekusi dinyatakan BATAL DEMI HUKUM.

3. Titik 3 — Delta Nilai Terukur & Kerusakan Invariant (`L-VALUE` Verified):
   - Menunjukkan perubahan terukur pada saldo, hak klaim, kolateral, kapasitas nilai (*intended capacity*), atau pembekuan state (State Sebelum vs State Sesudah).
   - Menunjuk minimal satu invariant dari FACTS.md atau path-map.md yang terbukti pecah.

---

## 2. Matriks Keputusan Wadah Kanonik (04 / 06 / 07 / 08 / 09)
| Kondisi Hasil Pemeriksaan | Wadah Tujuan Wajib | Kapan Dipindahkan | Kewajiban Catatan Verbatim |
| :--- | :--- | :--- | :--- |
| Jalur/ide sudah tertahan oleh penjaga kode (require/assert/constraint/fakta FACTS.md) saat penyempitan awal. | `04-code-guarded.md` | STAGE-C1 atau STAGE-C2 | Kutip Path/File.ext:Lxx-Lyy dan ekspresi penjaga yang membuat jalur tersebut aman. |
| Kandidat masuk meja operasi 05-raw-leads.md, tetapi saat diuji di STAGE-D PoC gagal, hitungan membuktikan tidak ada dampak, atau tertahan penjaga kode yang baru terlihat saat eksekusi. | `06-refuted-invalid.md` | STAGE-E | Kutip Path/File.ext:Lxx-Lyy, hasil gagal PoC/hitungan, dan alasan teknis mengapa eksploitasi patah. |
| Logika kode mendukung serangan, tetapi kepastian eksploitasi bergantung pada data yang tidak ada di repositori lokal (state on-chain live, parameter deployment, komponen off-chain tertutup). | `07-needs-next-step.md` | STAGE-E | Kutip Path/File.ext:Lxx-Lyy, bukti yang sudah terkumpul, dan daftar langkah verifikasi lanjut yang spesifik. |
| Perilaku benar-benar terjadi secara teknis, tetapi berada di luar *scope*, termasuk *known issue* resmi, membutuhkan admin/governance jujur berbuat jahat, atau di bawah ambang kelayakan. | `08-valid-not-eligible.md` | STAGE-E | Kutip Path/File.ext:Lxx-Lyy, mekanisme teknisnya, dan alasan mengapa ia tidak memenuhi syarat klaim utama. |
| Ketiga titik Bukti Segitiga terbukti utuh, berada dalam *scope*, dan melanggar invariant nilai/kontrol tanpa asumsi palsu. | `09-confirmed-findings.md` | STAGE-E (Bukti) & STAGE-F (Laporan Siap-Kirim) | Masukkan seluruh 3 Titik Bukti Segitiga di STAGE-E, lalu lengkapi blok *Submission-Ready Disclosure* pada STAGE-F. |

---

## 3. Checklist Penolakan Otomatis (Anti-Halusinasi & Anti-Kompresi)

Sebelum memindahkan kandidat ke 09-confirmed-findings.md, pastikan seluruh jawaban di bawah ini adalah YA:

- [ ] Apakah seluruh berkas dan fungsi yang dikutip benar-benar ada di kode sumber dalam *scope* (bukan hasil tebakan nama fungsi)?
- [ ] Apakah nomor baris (Path/File.ext:Lxx-Lyy) telah diperiksa ulang langsung terhadap berkas sumber asli?
- [ ] Apakah bukti bebas dari token kompresi terlarang (..., dll., dst., etc., and so on, rest of logic, rest of code)?
- [ ] Apakah pelaku serangan tidak membutuhkan hak istimewa (*admin/owner/governance*) yang di luar model ancaman?
- [ ] Apakah biaya/prasyarat serangan realistis dibanding dampak kerusakan atau pencurian nilai yang dihasilkan?
