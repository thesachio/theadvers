# [AF-04] Penyelipan Eksekusi via Callback, Hook, CPI, & Read-Only Reentrancy
- Classes: REENTRANCY, READ-ONLY-REENTRANCY, CALLBACK, CPI-STALE-ACCOUNT
- Trigger Symptom: Terdapat panggilan eksternal, pengiriman aset native/token ber-hook, callback flash/swap, atau CPI sebelum state lokal/lintas-modul selesai diperbarui.
- Paired Items: M-003, M-010, CHAIN-reentrancy-valuation

---

## 1. Mekanisme Serangan Universal
Saat Modul A menyerahkan kendali eksekusi ke luar (melalui pengiriman koin native, hook token, callback, atau Cross-Program Invocation) di tengah-tengah fungsi, penyerang menyelipkan panggilan balik ke Modul A (atau ke Modul B yang membaca state Modul A) ketika variabel state masih belum sinkron dengan saldo aset.
## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Petakan Jendela State Kotor (*Dirty State Window*) di `Path/File.ext:Lxx-Lyy`:
   - Tulis kondisi variabel pada baris tepat sebelum panggilan keluar (Baris X) vs baris pembaruan state yang baru terjadi sesudahnya (Baris Y).
2. Bangun Jembatan Penyelipan (*Interleaving Call*):
   - Jika Modul A memiliki *reentrancy guard* lokal, periksa RADAR.md untuk menemukan Modul B yang memanggil fungsi *view*/valuasi Modul A tanpa memeriksa kunci *reentrancy* Modul A (*Read-Only Reentrancy*).
   - Pada arsitektur berbasis akun seperti Solana/Rust, buktikan bahwa setelah CPI mengubah saldo akun di *storage*, fungsi pemanggil masih menggunakan nilai *deserialized struct* di memori yang belum di-reload().
3. Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika pola *Checks-Effects-Interactions* (CEI) sudah dipatuhi penuh, pengunci *mutex* bersifat global lintas-modul yang berinteraksi, atau aset yang ditransfer terbukti tidak memiliki mekanisme hook/callback sama sekali.

## 3. Bentuk Serangan (Cara Menyerang) — dari Registry v1

- **[BENTUK-07] Penyerahan Kontrol di Tengah State Timpang** — baca-ke-lokal → interaksi eksternal/CPI/callback → tulis-balik lokal basi. PoC wajib urutan baca→interaksi→tulis-balik.
- **[BENTUK-04] Racun State Dulu, Korban Eksekusi Terakhir** — bila `nonReentrant` lokal menutup jalur reentrancy, racuni state lebih dulu lewat jalur permissionless, lalu biarkan aktor berizin (keeper/relayer) menjalankan rutinitasnya. **Tidak butuh reentrancy sama sekali.**
- **[BENTUK-03] Bundler Transaksi** — N sub-panggilan dalam satu konteks luar (multicall/PTB).

Rujuk `M-005` Jalur 3, `M-009`, `POV-CALL-01`.
