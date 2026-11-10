# [DOM-staking] Heuristik Domain: Staking, Distribusi Reward, Vesting, & Antrean Unstake Universal
- Classes: STAKING, REWARDS, VESTING, COOLDOWN, SLASHING
- Trigger Symptom: Modul mengunci aset untuk memperoleh bagian reward per-detik/per-epoch, melacak indeks rewardPerToken, atau memiliki antrean penarikan.
- Paired Items: M-001, M-007, M-009, AF-03, AF-05, AF-09

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Sinkronisasi Checkpoint Reward Pengguna: Setiap kali saldo *stake* pengguna berubah (melalui stake, unstake, transfer, atau slash), reward tertunda pengguna wajib dihitung dan userRewardPerTokenPaid wajib disamakan dengan indeks global terbaru sebelum saldo pengguna diubah.
2. Isolasi Token Staking vs Token Reward: Jika token yang di-*stake* sama dengan token reward, pembayaran reward tidak boleh menggerus pokok *stake* pengguna, dan pokok *stake* tidak boleh dihitung sebagai tambahan reward baru.

## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]`:
  - Jika bukti kepemilikan *stake* berupa token yang dapat dipindahkan (*transferable receipt token*), apakah fungsi transfer memperbarui rewardDebt untuk pengirim DAN penerima di Path/File.ext:Lxx-Lyy? Jika tidak, pengguna dapat memindahkan token antar-dua akun untuk mengklaim reward berulang kali (M-001 + M-010).
- `[EDGE-VALUATION]`:
  - Apa yang terjadi pada akumulasi waktu ketika totalStaked == 0? Apakah lastUpdateTime tetap dimajukan, atau reward selama periode kosong melompat sekaligus ke penyetor pertama yang masuk (AF-03 + AF-05)?
- `[EDGE-CONTROL/LATENT]`:
  - Apakah penyerang dapat memanggil stakeFor(korban, 1) untuk mereset waktu tunggu penarikan (*cooldown/lockup timer*) korban tanpa batas (AF-09)?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `STAKING / REWARDS`
- **Siklus aliran (L-PATH):** stake → akrual (indeks) → claim → unstake (cooldown) → withdraw
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «indeks akrual tak bisa di-smear sebelum stake»; «cooldown window tak bisa di-bypass»; «reward claim idempoten»
- **Aktor off-chain:**

  validator/orchestrator penghitung reward

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
