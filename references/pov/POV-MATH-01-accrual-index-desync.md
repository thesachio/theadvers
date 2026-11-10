# [POV-MATH-01] Sudut Pandang: Desinkronisasi Indeks Akrual pada Transfer/Mutasi Pokok
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Ada `globalIndex`/`userIndex`/`accruedPerShare` plus fungsi pemindah saldo/posisi 2-akun (`transfer`, `delegate`, `migrate`, `merge`, `split`).
- Paired Items: M-002, M-003, M-006, AF-02, POV-unprivileged

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang menguasai ≥2 akun/posisi pada kontrak yang sama, dengan modal sekecil mungkin. Tidak butuh flashloan — cukup satu posisi yang reward/utangnya belum di-*settle*.

## 2. Gejala di Kode

Fungsi pemindah saldo/posisi (`transfer`, `delegate`, `migrate`, `merge`) **tidak memanggil `_accrue`/`updateReward` pada kedua sisi** sebelum memindahkan pokok. Akibatnya:

- Indeks akrual milik pengirim dan penerima berada di titik waktu berbeda.
- Pokok yang dipindah "membawa" akrual yang salah, atau akrual ganda dipanen oleh penerima.

Urutan yang dicari: `pindah pokok` → `settle reward` (seharusnya `settle` → `pindah`).

## 3. Rangkaian Serangan

1. **Siapkan:** penyerang memegang dua posisi pada kontrak yang sama (dua akun, atau dua objek/posisi pada runtime Move).
2. **Picu:** pindahkan pokok antar-posisi ketika indeks global sedang bergerak (setelah ada akrual yang belum di-*settle*).
3. **Ekstraksi:** akrual dari posisi A terbawa ke posisi B, atau terhitung dua kali — reward/utang diambil melebihi hak.

## 4. Auditor Blindspot

Auditor menguji `transfer` dan `claim` sebagai dua fungsi terpisah. Yang tidak diuji adalah **jalur perpindahan pokok yang menyentuh akuntansi indeks**, karena tampak seperti operasi saldo murni tanpa akrual.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila fungsi pemindah terbukti memanggil akrual pada kedua sisi sebelum mutasi (`Path/File.ext:Lxx-Lyy` untuk kedua panggilan).
- **Wajib PoC** bila ada jalur yang memindahkan pokok tanpa akrual penuh. Uji dengan dua identitas (`Attacker_A`, `Attacker_B`) — PoC satu identitas tidak membuktikan apa pun.
- Fuzz wajib mengacak: selang waktu akrual, ukuran pokok, dan urutan `transfer` vs `claim`.
