# [POV-EVM-01] Sudut Pandang: Multicall Context Reuse & Residual Authority Exploitation
- Classes: CLASS-A (Batch/Loop Internal), CLASS-B (Router/Multicall ↔ Target)
- Trigger Symptom: Kontrak mewarisi `Multicall` (`delegatecall`), memiliki loop batch, atau memakai `TSTORE`/`TLOAD`, SERTA memiliki fungsi yang membaca `msg.value` atau flag otorisasi sementara.
- Paired Items: M-003, M-007, M-010, AF-05, CHAIN-evm-tron, POV-unprivileged

---

## 1. Kemampuan & Sumber Daya Aktor

Penyerang tanpa izin yang menyusun payload batch dalam satu transaksi. Modal hanya `1 × X` nilai pembayaran, bukan `N × X`.

## 2. Gejala di Kode

Fungsi satuan memeriksa `require(msg.value == requiredAmount)` atau memakai `msg.value` untuk mencatat pembayaran **tanpa mengurangi penghitung global per-transaksi**, atau menetapkan flag sementara di *Transient Storage* yang tidak dihapus (`TSTORE(slot, 0)`) sebelum sub-eksekusi berikutnya dimulai.

Prinsip umumnya: **satu konteks luar (nilai pembayaran, otorisasi sementara, atau status sesi) dipakai ulang oleh N sub-panggilan** sementara kontrak menganggapnya sekali pakai.

### Padanan lintas-rantai

| Runtime | Bentuk |
| :--- | :--- |
| TVM (Tron) | perilaku `msg.value` identik dengan EVM |
| Solana | konteks instruksi/akun yang dipakai ulang di dalam satu transaksi |

## 3. Rangkaian Serangan

1. **Siapkan:** susun payload batch berisi N panggilan berulang ke fungsi pembayaran/pencetakan yang sama.
2. **Picu:** panggil fungsi pembungkus batch (multicall) sambil mengirim `msg.value` hanya sebesar 1 kali nilai pembayaran (`1 × X`).
3. **Ekstraksi:** karena setiap sub-panggilan `delegatecall` membaca konteks `msg.value` yang sama (`X`), kontrak mengkreditkan `N × X` kepada penyerang dengan modal hanya `1 × X`.

## 4. Auditor Blindspot

Auditor menguji fungsi pembayaran secara terpisah (1 transaksi = 1 panggilan) sehingga tidak pernah melihat bahwa **konteks luar dipakai ulang** oleh N sub-panggilan dalam satu transaksi.

## 5. Batas Realitas & Routing Simulasi (STAGE-D)

- **Gugur** bila fungsi pembayaran mengurangi penghitung global per-transaksi (mis. `msg.value` di-track dan dikonsumsi), atau flag transient storage selalu dihapus (`TSTORE(slot, 0)`) sebelum sub-eksekusi berikutnya.
- **Wajib PoC** dengan payload batch nyata: N panggilan, `msg.value` tunggal, ukur kredit vs pembayaran.
- Fuzz wajib mengacak jumlah N dan ukuran `X`, karena laba bertumbuh linear terhadap N.
