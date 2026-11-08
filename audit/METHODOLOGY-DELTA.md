# METHODOLOGY-DELTA — apa yang berubah dari run 1-2, dan apa konsekuensinya

Dokumen ini **wajib dibaca sebelum Tahap A dimulai**. Ia menjelaskan mengapa run ketiga
layak dijalankan padahal kode targetnya identik, dan apa yang **tidak** boleh diklaim.

## 1. Fakta yang diverifikasi (bukan asumsi)

| Klaim | Cara verifikasi | Hasil |
|---|---|---|
| Commit target identik dengan run 2 | `git fetch origin master && git rev-parse HEAD origin/master` + `git rev-list --count HEAD..origin/master` | identik, 0 commit baru |
| Run 1 dan run 2 punya HEAD berbeda | `git log --oneline -1` di `across/contracts` vs `across2/contracts` | `b1c4e862` vs `d0725ea0` |
| Metode lama **tidak** memakai provenance lapis | `grep -c "LAPIS:" across2/audit/05-raw-leads.md` | **0** |
| Metode lama **tidak** memakai tag bentuk serangan | `grep -c "AF-0" across2/audit/05-raw-leads.md` | **0** |
| Tahap E (offchain) **tidak pernah** dijalankan | `grep -rc "L-OFFCHAIN" across2/audit/notes/*.md` | **0 file** |
| Persebaran lead lama | `03-attack-surface-queue.md` run 2: 39 unit, 604 baris | unit-major (S-n), bukan EV-major |

## 2. Tiga pergeseran yang mendefinisikan run 3

### (1) Urutan: EV-major, bukan unit-major
Run 1-2 mengiterasi `S-01..S-39` mengikuti nomor unit di `03`. Akibatnya, unit ber-EV rendah
dikerjakan pagi hari dan pot terbesar (HubPool, $3,77 jt) dikerjakan belakangan saat
ketajaman sesi sudah turun. Run 3 mengurutkan berdasarkan **EV ledger** (`notes/money-ledger.md`):
uang termahal diledah di jam pertama.

**Uji keterukuran:** bila anggaran terputus di tahap mana pun, run 3 sudah menyelesaikan
porsi EV tertinggi. Run 1-2 tidak punya properti ini.

### (2) Blind spot L-PATH: kontrak zero-balance di jalur aliran
Run 1-2 memakai saldo sebagai filter dominan, sehingga kontrak yang **tidak** menyimpan uang
tapi **dilalui** aliran dana (kelas `MulticallHandler`, gateway sementara, adapter stateless)
otomatis turun prioritas — padahal justru di situ bug bridging lahir.

**Uji keterukuran:** jumlah jahitan dengan `balance_now ≈ 0` tapi
`throughput_path > 0` yang masuk antrean. Run 1-2: tidak dihitung sama sekali.

### (3) Tahap E (offchain) yang selama ini kosong
Scope bounty Across eksplisit mencakup sebagian besar kode repo termasuk bot & frontend
(`audit/INTEL.md` §3, sumber `docs.across.to/introduction/bug-bounty`). Run 1-2 tidak pernah
menjalankan Tahap E (bukti: 0 kemunculan `L-OFFCHAIN`) — termasuk tiga repo pendukung
`exclusive-relayer-configs`, `relayer-registration-repository`, `v5-token-pricing`.

**Uji keterukuran:** Tahap E dipicu anomali on-chain, bukan dibaca menyeluruh
(`methodology/mod-offchain.md`). Nilai run 3 diukur dari berapa anomali yang berhasil
direduksi menjadi akar kode.

## 3. Konsekuensi keras — apa yang DILARANG diklaim

1. **DILARANG** menyebut run ini "audit kode baru". Kode target tidak berubah.
2. Temuan baru wajib dibuktikan sebagai **false negative metode lama**, yaitu:
   - lead yang tidak pernah muncul di `across2/audit/05-raw-leads.md`, DAN
   - hilang karena salah satu dari tiga blind spot di §2, DAN
   - dibuktikan PoC nyata (bukan hipotesis).
3. **DILARANG** memakai `across2/audit/06-refuted-invalid.md` sebagai bukti bahwa sesuatu aman.
   Run 3 buta terhadapnya (amnesia terkontrol). Namun run 3 juga **dilarang** mengklaim
   sesuatu sebagai temuan baru bila sebenarnya itu lead yang sudah gugur — karena itu,
   sebelum submit, temuan WAJIB dicek silang ke `06`/`08` across2 (gerbang anti-duplikat).
4. Angka "0 temuan" adalah hasil yang sah dan **harus dilaporkan apa adanya**. Run 3 tidak
   diberi insentif untuk mengarang temuan demi membenarkan metode baru.

## 4. Amnesia terkontrol — apa yang dibawa dan tidak

| Artefak | Dibawa? | Alasan |
|---|---|---|
| `STATE.md`, `05`-`09` run 1-2 | **TIDAK** | mencegah penambatan (anchoring) ke hipotesis lama |
| `METHODOLOGY-SEGITIGA.md` + 6 modul | **YA** | ini metodenya |
| `templates/*` (STATE, 04-09, VERDICT, RUBRIC) | **YA** | aturan penulisan & verdict |
| `target/PIN.md` | **YA** | reproduktibilitas |
| `FACTS.md` run 2 | **TIDAK** (dibangun ulang) | FACTS lama memuat pemahaman turunan dari lead lama — membawanya = anchoring |
| Daftar alamat live dari `INTEL.md` run 2 | **YA, diverifikasi ulang** | alamat harus diukur ulang di Tahap A, bukan dipercaya |

## 5. Gerbang anti-duplikat (dijalankan SEBELUM submit, bukan sebelum hunting)

Pada saat temuan siap diajukan, jalankan pencocokan ke run sebelumnya:

```bash
# Apakah file yang sama pernah jadi lead di across2?
grep -n "<NamaFile.sol>" /home/ubuntu/.hermes/profiles/adv/workspace/projects/across2/audit/05-raw-leads.md
grep -n "<NamaFile.sol>" /home/ubuntu/.hermes/profiles/adv/workspace/projects/across2/audit/06-refuted-invalid.md
grep -n "<NamaFile.sol>" /home/ubuntu/.hermes/profiles/adv/workspace/projects/across2/audit/08-valid-not-eligible.md
```

- Hasil di `06` → **bukan temuan baru**. Wajib punya bukti baru material, jika tidak: buang.
- Hasil di `08` → kemungkinan duplikat submit. Cek tanggal kirim di `SUBMISSION_REPORT/INDEX.md`.
- Hasil di `09` → duplikat submit. Buang.

Alasan gerbang ini di akhir, bukan di awal: menjalankannya di awal akan mengembalikan
anchoring yang justru ingin dihindari. Biaya menjalankannya di akhir kecil (satu grep).
