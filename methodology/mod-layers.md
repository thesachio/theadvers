# MOD-LAYERS — Detail Tiga Lapis + Offchain (plug-in METHODOLOGY-SEGITIGA §1)

Kontrak ekstensi: lapis baru = append satu blok di bawah; core tidak disentuh.

## L-VALUE — Sensus nilai live (Tahap A)

**Pertanyaan**: di mana uangnya SEKARANG, dan bagaimana konfigurasi hidupnya?

- Enumerate semua kontrak ter-deploy × chain × token besar × native.
- Baca **lewat proxy** (bukan impl — storage impl kosong; pelajaran empiris dari run sebelumnya).
- Konfigurasi live yang wajib dicensus: owner/admin/crossDomainAdmin, whitelist token,
  messenger OFT/CCTP, pause flags, fee params, role holders (hasRole per role).
- Output: `notes/money-ledger.md` — EV terurut + status pot.
- Alat: `cast balance/call/storage`, `getAccountInfo` (Solana), `getObject` (Sui), `getAccountState` (TON).
- **GATE-A**: kontrak bernilai > ambang WAJIB masuk B/C. Keluarga mati-dini (dibunuh di sini,
  1 query, bukan lab): tidak ter-deploy, tidak ter-inisialisasi, konfigurasi kosong,
  role tak terpasang, saldo 0 DAN tidak di jalur aliran.

## L-PATH — Peta siklus aliran dana (Tahap B)

**Pertanyaan**: ke mana uang MENGALIR (bukan hanya mengendap)?

- Bangun peta siklus per domain cartridge (lihat mod-domain-cartridges.md): node = kontrak,
  edge = aliran dana (transfer/bridge/mint-burn/reward).
- Tiap jahitan (edge antar node) diberi `EV = max(balance_now, throughput_path)`.
- Khusus jahitan asinkron (bridge hop, message in-flight): tandai `ASYNC` — zona observasi khusus.
- Output: `notes/path-map.md` — daftar jahitan + EV + kelas (sinkron/asinkron) + aktor
  (on-chain/off-chain) tiap hop.
- **GATE-B**: kontrak zero-balance TAPI dilalui aliran WAJIB diburu (kelas MulticallHandler);
  cabang tanpa throughput dipangkas (uang terkonsentrasi di rute dominan — anti state-space blowup).

## L-FLOW — Bedah sink mutasi (Tahap C)

**Pertanyaan**: fungsi mana yang menggerakkan dana di tiap jahitan, dan siapa boleh memanggilnya?

- Per jahitan terpilih: baca fungsi UTUH (A0) dengan toolkit M-001..M-010 + POV router sebagai
  GENERATOR (tanya per pot: "POV mana yang muat di uang ini?" — bukan filter pasca-baca).
- Klasifikasi reachability: 5 Jalur Permissionless (registry M-005).
- FACTS/RADAR dibuka SETELAH hipotesis buta lahir — murni falsifier.
- Output: entri `05` ber-provenance `[LAPIS: VALUE|PATH|FLOW]` + `[CLASS-A|B|C]`
  + `[AF-xx]` + `[LOAD: M-xxx]`.
- `[CLASS-x]` **BUKAN** digantikan oleh `[LAPIS]`: CLASS menentukan paket metode wajib
  minimum (`ref-method-registry.md` §1), LAPIS hanya menandai asal lead. Lihat
  `CLASSIFICATION.md`.
- **GATE-C**: tiap lead punya provenance + tag AF; klaim negatif wajib kutip rentang baris utuh.

## L-OFFCHAIN — Bedah aktor luar (Tahap E, opsional) — detail di mod-offchain.md

- DIPICU anomali on-chain (dispute nyata, bundle gagal, pola fill aneh) atau kelas
  "ketiadaan aksi" (keeper diam saat seharusnya bertindak).
- Repo publik → baca; privat → rekonstruksi blackbox dari event.
- **GATE-E**: hanya bila scope bounty memasukkan off-chain ATAU manifestasi hanya berbentuk
  absennya transaksi. Bug yang hanya merugikan operatornya sendiri = self-inflicted (catat, jangan klaim).

## Matriks EV tiga lapis (ringkas)

| Lapis | Menemukan | Blind spot bawaan |
|---|---|---|
| L-VALUE | kerugian TERWUJUD (stuck funds, config brick) | kontrak zero-balance |
| L-FLOW | celah LATEN (drain, signature, guard) | tak pernah menanyakan saldo |
| L-PATH | kelas aliran (transient holder, mid-chain desync) | butuh peta aliran yang lengkap |
| L-OFFCHAIN | bug bot/keeper yang termanifestasi on-chain | bukti lemah bila repo privat |
