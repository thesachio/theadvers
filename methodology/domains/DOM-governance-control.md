# [DOM-governance-control] Heuristik Domain: Tata Kelola, Voting, Timelock, Upgrade, & Modul Darurat Universal
- Classes: GOVERNANCE, VOTING, TIMELOCK, ACCESS-CONTROL, EMERGENCY
- Trigger Symptom: Modul menghitung bobot suara (*voting power*), mengeksekusi proposal/timelock, mengelola *pause/unpause*, atau mengatur parameter sistem.
- Paired Items: M-005, M-006, M-009, AF-01, AF-07, AF-09

---

## 1. Invariant Nilai Inti (L-VALUE & FACTS.md)
1. Isolasi Snapshot Suara: Bobot suara (*voting power*) untuk sebuah proposal atau distribusi epoch wajib dibaca dari snapshot blok/waktu masa lalu sebelum proposal dibuat, bukan dari saldo saat ini yang dapat dipinjam kilat atau dipindah-tangankan antar-akun.
2. Keutuhan Siklus Proposal & Darurat: Proposal yang dibatalkan atau gagal tidak boleh dapat dieksekusi, dan mode darurat (*pause*) tidak boleh mengunci fungsi penyelamatan yang justru dibutuhkan untuk memulihkan sistem.

## 2. Titik Rawan pada 3-Edge (STAGE-B & STAGE-C2)
- `[EDGE-ASSET]` & `[EDGE-VALUATION]`:
  - Apakah pendelegasian suara (*delegate*) saat memindahkan token otomatis mengurangi suara delegasi lama dan menambah suara delegasi baru di Path/File.ext:Lxx-Lyy (M-001)?
  - Apakah kuorum dihitung dari totalSupply saat eksekusi yang bisa dimanipulasi naik/turun untuk menggagalkan atau meloloskan proposal?
- `[EDGE-CONTROL/LATENT]`:
  - Apakah satu pengguna dapat membuat proposal sampah tanpa batas untuk memenuhi slot antrean aktif dan memblokir proposal sah (AF-09)?
  - Apakah fungsi inisialisasi implementasi baru pada pola proxy/upgradeable dibiarkan terbuka tanpa penguncian konstruktor (AF-07)?

## 3. Siklus Aliran & Invarian Senyap (dari Registry Domain v1)

- **Domain:** `GOVERNANCE / CONTROL`
- **Siklus aliran (L-PATH):** usul → snapshot suara → voting → antre timelock → eksekusi → (darurat) pause/unpause → upgrade
- **Invarian senyap (asumsi yang TIDAK di-assert — target serangan):** «voting power dibaca dari snapshot masa lalu, bukan saldo saat ini»; «proposal batal/gagal tidak bisa dieksekusi»; «pause tidak mengunci fungsi penyelamatan»; «slot antrean tidak bisa dibanjiri proposal sampah»
- **Aktor off-chain:**

  indexer suara, eksekutor timelock, multisig/guardian

Rujuk `FACTS.md` domain terkait untuk mencatat mana dari invarian senyap ini yang **terbukti ditegakkan** oleh kode dan mana yang **TIDAK ditegakkan**.
