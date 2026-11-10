# [M-004] Patch-Scar, Periphery, & View-vs-Write Asymmetry
- Classes: CLASS-A, CLASS-B, CLASS-C
- Trigger Symptom: Ada fungsi utama dengan guard khusus yang tampak seperti tambalan audit, atau ada pasangan fungsi `view`/`preview` di samping fungsi tulis; jalur periferal (transfer, migrate, rescue, sweep, batch, hook) menyentuh variabel yang sama.
- Paired Items: AF-02, AF-06, M-002, DOM-oracle, POV-malicious-integrator

---

## 1. Inti Metode

Auditor cenderung lelah saat memeriksa jalur periferal dan fungsi pembacaan. Tambalan keamanan (*patch-scar*) atau pemotongan biaya yang dipasang di jalur utama **sering terlupa di jalur sampingan**, atau **berbeda rumus** antara fungsi baca vs fungsi tulis.

Metode ini juga menampung konsep **valuasi/kurs/oracle** (v2): harga, `share` rate, indeks bunga/reward adalah bentuk khusus dari asimetri `View` vs `Write` — nilai dibaca dengan satu rumus, diterapkan dengan rumus lain.

## 2. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Bedah *Patch-Scar*.** Jika fungsi utama memiliki `if`/`require`/`assert!` yang terlihat seperti tambalan audit, periksa apakah jalur sampingan yang menyentuh variabel sama **lupa dipasang tambalan**: `transfer`, `migrate`, `rescue`, `sweep`, `emergencyWithdraw`, `batch`, hook/callback.
2. **Desinkronisasi `View` vs `Write`.** Bandingkan baris demi baris rumus fungsi `view`/`preview`/getter dengan fungsi tulis pasangannya. Yang dicari: perbedaan arah pembulatan (`mulDivDown` vs `mulDivUp`), biaya yang dihitung di preview tetapi tidak dipotong di eksekusi, atau sumber angka berbeda (`balanceOf` vs variabel internal).
3. **Valuasi & oracle.** Bila kontrak membaca harga/kurs/indeks: periksa desimal, arah pembulatan, staleness (`updatedAt`), dan apakah fungsi kuotasi memakai rumus yang sama dengan fungsi eksekusi.
4. **Periferal tanpa uji.** Setiap entrypoint yang jarang dipakai tapi menyentuh nilai wajib diperiksa setara dengan jalur utama.

## 3. Syarat Bukti (STAGE-D)

- **Titik 1:** jalur periferal atau pasangan `view`/`write` + `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** dua angka berdampingan (hasil `view` vs hasil tulis) pada input yang sama, atau PoC jalur periferal setelah *Victim Seeding*.
- **Titik 3:** deviasi terukur + dampak (biaya hilang, kuotasi menyesatkan, kolateral salah nilai).

## 4. Routing Simulasi

- *Patch-Scar* pada jalur periferal → wajib PoC yang mengeksekusi jalur tersebut setelah *Victim Seeding*.
- **DILARANG menggugurkan ke `06` (`REJECTED_NO_VICTIM`) hanya karena `view`/`preview`/`quote` tidak dipanggil on-chain di kontrak yang sama.** Fungsi kuotasi publik sering dikonsumsi Router eksternal, Solver/Relayer off-chain, atau integrasi pihak ketiga. Selama rumus `View` dan `Write` terbukti menghasilkan angka berbeda di simulator, **WAJIB tulis PoC**. Gugur ke `06` hanya bila simulator membuktikan keduanya **100% identik di segala kondisi batas** (termasuk setelah Strike 3 Fuzz).

## 5. Kapan Metode Ini TIDAK Dipakai

- Tidak ada jalur periferal dan tidak ada fungsi pembacaan yang menyentuh nilai.
- `View` dan `Write` terbukti identik setelah fuzz menyeluruh (→ `06` `REJECTED_POC_FAILS`, wajib log).
