# [AF-08] Replay Tanda Tangan/Bukti Merkle-ZK, Pemalsuan Domain/Nonce, & Parameter Hijack
- Classes: SIGNATURE-REPLAY, MERKLE-PROOF, ZK-UNDERCONSTRAINED, NONCE-BYPASS
- Trigger Symptom: Terdapat verifikasi tanda tangan kriptografis, klaim berbasis Merkle/ZK proof, izin *permit/meta-transaction*, atau pesan lintas-rantai.
- Paired Items: M-005, M-008, DOM-bridge-offchain, POV-relayer-mev

---

## 1. Mekanisme Serangan Universal
Penyerang mengambil tanda tangan atau bukti kriptografis (Merkle/ZK) yang sah, lalu menggunakannya kembali (*replay*) di fungsi lain, di kontrak/rantai lain, setelah state di-reset, atau mengubah parameter fungsi yang tidak ikut diikat di dalam digest hash/bukti.
## 2. Langkah Konstruksi Bukti di STAGE-D (L-PROVE)
1. Bandingkan Parameter Fungsi vs Komponen Digest di `Path/File.ext:Lxx-Lyy`:
   - Tulis daftar seluruh argumen fungsi: (arg1, arg2, arg3, signature).
   - Tulis daftar argumen yang benar-benar dimasukkan ke dalam keccak256(abi.encode(...)) atau *public input* verifikator.
   - Jika ada argumen (seperti recipient, fee, token, nonce, chainId, verifyingContract) yang berada di luar hash, ubah argumen tersebut sambil tetap mengirim tanda tangan asli.
2. Uji Pemutaran Ulang (*Replay*) & Pemutusan DoS *Permit***:
   - Periksa apakah nonce dicatat per-pengguna dan langsung dinaikkan.
   - Sebaliknya, jika fungsi utama mewajibkan `permit` dalam satu transaksi tanpa blok `try/catch`, uji apakah penyerang dapat melakukan *front-run* mengeksekusi tanda tangan `permit` tersebut lebih dulu agar transaksi utama korban gagal karena nonce sudah terpakai.
3. **Kondisi Gugur ke `06-refuted-invalid.md`:
   Gugurkan jika seluruh parameter sensitif, domain separator (chainId + alamat modul), dan nonce satu-kali-pakai terikat penuh di dalam digest kriptografis.
