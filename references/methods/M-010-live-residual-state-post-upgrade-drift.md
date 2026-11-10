# [M-010] Live Residual State, Delegated Authority, & Post-Upgrade Drift
- Classes: CLASS-A (proxy/upgraded contract mandiri), CLASS-B, CLASS-C
- Trigger Symptom: Kontrak berupa proxy/upgradeable, punya komponen perantara (Router/Helper/Migrator/Adapter), menerima `approve`/delegation, atau pernah mengalami migrasi/upgrade.
- Paired Items: AF-04, AF-10, M-006, M-008, DOM-bridge-offchain

---

## 1. Inti Metode

Auditor menguji pada *sandbox* kosong (`setUp()` bersih), sedangkan sistem produksi membawa **state sisa dan riwayat migrasi yang nyata**. Jangan kunci metode ini pada istilah EVM (`allowance`, `cast call`, slot proxy) — ada lima konsep general lintas-rantai:

1. **Allowance / Approval** yang masih aktif dari pengguna ke kontrak perantara
2. **Delegated Authority / Capability** yang belum dicabut setelah sesi selesai
3. **Residual Balance / Asset Object** yang mengendap di kontrak/akun/objek perantara
4. **Stale Configuration** yang tidak lagi sesuai dengan modul baru
5. **Storage Slot / Object Field / Account Data / Actor State** yang tidak sinkron atau belum terinisialisasi setelah upgrade/migrasi

Metode ini juga menampung **serangan rantai lintas-modul** (konsep v2, `[TOUCHES]`): state sisa satu modul dibaca modul lain yang menganggapnya final.

## 2. Tabel Padanan Lintas-Rantai

| Konsep general | EVM / Tron | Solana (SVM) | Move (Sui/Aptos) | TON |
| :--- | :--- | :--- | :--- | :--- |
| **Otorisasi / Capability tertunda** | `allowance`, `approve`, `Permit2`, `operator` | delegated authority pada Token Account / PDA signer | capability tertunda / dipinjamkan / tidak dihancurkan | otoritas admin/wallet yang masih terikat kontrak lama |
| **Residual balance / asset object** | ERC20/ETH mengendap di Router/Helper/Migrator | lamport / SPL token mengendap di PDA perantara | `Coin<T>` / asset object tertinggal di shared object | saldo TON / Jetton tersisa di actor perantara |
| **State drift pasca-upgrade** | slot proxy EIP-1967, variabel `V2` baru masih `0` | skema Account data lama vs program baru | `dynamic_field` / versi `Package` tidak sinkron | skema storage `c4` / konfigurasi actor pasca-`set_code` |
| **Alat baca state live (STAGE-D)** | `cast call`, `cast storage`, `eth_getStorageAt` | `getAccountInfo`, `solana account` | `sui client object`, `getDynamicFields` | Toncenter / Liteclient `getAccountState`, `runGetMethod` |

## 3. Prosedur Bedah (STAGE-C1 & STAGE-C2)

1. **Delegated authority & residual asset.** Apakah komponen perantara punya panggilan eksternal terbuka (`call`, `transferFrom`, `sweep`, `swap`, CPI, fungsi publik terbuka) yang dapat menarik aset tertinggal atau menyedot otorisasi pengguna aktif?
2. **Post-upgrade / migration drift.** Setelah upgrade, apakah ada field baru yang belum diinisialisasi, nilai lama yang dibaca dengan makna baru, atau modul baru membaca state modul lama yang sudah tidak relevan?
3. **Sinyal `[TOUCHES]`.** Untuk setiap state yang ditulis modul A dan dibaca modul B, tanyakan apakah B mengasumsikan state itu final padahal A bisa mengubahnya belakangan.
4. **Uji di state nyata.** Semua hipotesis di metode ini wajib diuji pada `FORK_LIVE` dengan *state sisa* — bukan di `setUp()` kosong.

## 4. Syarat Bukti (STAGE-D)

- **Titik 1:** entrypoint perantara/upgrade + state yang dibaca lintas-modul, `Path/File.ext:Lxx-Lyy`.
- **Titik 2:** PoC pada fork live dengan state sisa nyata (allowance aktif, saldo mengendap, atau field belum terinisialisasi) — bukan state yang disuntikkan `vm.store`.
- **Titik 3:** nilai terukur yang berpindah/terkunci + invariant yang pecah.

## 5. Routing Simulasi

- Wajib `Mode Uji: FORK_LIVE` + blok fork (lihat `templates/VERDICT.md` §2b). Menguji drift di `setUp()` kosong **tidak membuktikan apa pun** — state sisa adalah inti metodenya.
- `vm.store`/`vm.etch` untuk **mengarang** state sisa = `REJECTED_CHEATCODE`. State sisa harus berasal dari fork nyata.

## 6. Kapan Metode Ini TIDAK Dipakai

- Tidak ada proxy/upgrade, tidak ada komponen perantara, dan tidak ada allowance/delegation yang tersisa.
- State lintas-modul terbukti tidak pernah dibaca ulang setelah modul lain menulisnya (dibuktikan dengan pelacakan pembaca, bukan asumsi).
