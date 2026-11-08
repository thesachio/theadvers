# METHODOLOGY-DELTA — template untuk audit ulang pada kode yang sama

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Template audit ulang — dipakai di **sebelum Tahap A**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

**Kapan dokumen ini dipakai:** saat menjalankan audit ulang (run ke-2 dst.) pada target yang
**kodenya identik atau hampir identik** dengan run sebelumnya. Dokumen ini memaksa penulis
menjawab: *"apa yang membuat run ini beda, dan apa yang DILARANG diklaim?"*

Tanpa jawaban tertulis di sini, audit ulang adalah pengulangan deterministik yang membakar
anggaran untuk hasil yang sama.

---

## 1. Fakta yang wajib diverifikasi dulu (bukan asumsi)

Isi tabel ini dengan **perintah + keluaran nyata**. Kosong = belum diverifikasi.

| Klaim | Cara verifikasi | Hasil |
|---|---|---|
| Commit target vs run sebelumnya | `git fetch origin && git rev-parse HEAD origin/<branch>` + `git rev-list --count HEAD..origin/<branch>` | `-` |
| Run sebelumnya memakai lapis L-VALUE/PATH/FLOW? | `grep -c "LAPIS:" <run-lama>/audit/05-raw-leads.md` | `-` |
| Run sebelumnya memakai tag bentuk serangan? | `grep -c "AF-0" <run-lama>/audit/05-raw-leads.md` | `-` |
| Tahap E (offchain) pernah dijalankan? | `grep -rc "L-OFFCHAIN" <run-lama>/audit/notes/*.md` | `-` |
| Persebaran kerja run lama: EV-major atau unit-major? | urutan item di `<run-lama>/audit/STATE.md` + `audit/notes/path-map.md` (peta jahitan) | `-` |

## 2. Tiga pergeseran yang membenarkan run ulang

Run ulang hanya sah bila ada pergeseran **terukur**. Isi minimal satu; hapus yang tidak berlaku.

### (1) Urutan: EV-major, bukan unit-major
Bila run lama mengiterasi nomor unit (`S-01..S-n`), unit ber-EV rendah dikerjakan lebih dulu
dan pot terbesar dikerjakan saat ketajaman sesi sudah turun. Run baru mengurutkan dari
EV ledger (`notes/money-ledger.md`).

**Uji keterukuran:** bila anggaran terputus di titik mana pun, apakah porsi EV tertinggi
sudah selesai? Run lama tidak punya properti ini bila unit-major.

### (2) Blind spot L-PATH: kontrak zero-balance di jalur aliran
Bila run lama memakai saldo sebagai filter dominan, kontrak yang **tidak** menyimpan uang tapi
**dilalui** aliran dana (kelas handler sementara, gateway, adapter stateless) otomatis turun
prioritas — padahal di situ justru bug aliran lahir.

**Uji keterukuran:** jumlah jahitan dengan `balance_now ≈ 0` tapi `throughput_path > 0` yang
masuk antrean. Run lama: biasanya tidak dihitung sama sekali.

### (3) Tahap E (offchain) yang selama ini kosong
Bila scope bounty mencakup kode off-chain (bot, keeper, frontend, repository konfigurasi),
run lama yang hanya membaca kontrak akan melewatkan seluruh kelas ini.

**Uji keterukuran:** jumlah anomali on-chain yang berhasil direduksi menjadi akar kode.

## 3. Konsekuensi keras — yang DILARANG diklaim

1. **DILARANG** menyebut run ini "audit kode baru" bila commit target identik.
2. Temuan baru wajib dibuktikan sebagai **false negative run lama**:
   - tidak pernah muncul di `<run-lama>/audit/05-raw-leads.md`, DAN
   - hilang karena salah satu blind spot di §2, DAN
   - dibuktikan PoC nyata (bukan hipotesis).
3. **DILARANG** memakai `<run-lama>/audit/06-refuted-invalid.md` sebagai bukti bahwa sesuatu aman.
4. Angka **"0 temuan" adalah hasil yang sah** dan wajib dilaporkan apa adanya. Run ulang tidak
   diberi insentif mengarang temuan demi membenarkan metode baru.

## 4. Amnesia terkontrol — apa yang dibawa dan tidak

| Artefak | Dibawa? | Alasan |
|---|---|---|
| `STATE.md`, `05`-`09` run lama | **TIDAK** | mencegah anchoring ke hipotesis lama |
| `METHODOLOGY-SEGITIGA.md` + modul + `references/` | **YA** | ini metodenya |
| `templates/*` | **YA** | aturan penulisan & verdict |
| `target/PIN.md` | **YA** | reproduktibilitas |
| `FACTS.md` run lama | **TIDAK** (bangun ulang) | FACTS lama diturunkan dari lead lama — membawanya = anchoring |
| Daftar alamat/konfigurasi live run lama | **YA, diverifikasi ulang** | alamat & saldo bergerak; ukur ulang di Tahap A |

## 5. Gerbang anti-duplikat (dijalankan SEBELUM submit, bukan sebelum hunting)

```bash
RUN_LAMA=~/audits/<proyek>-run1
grep -n "<NamaFile>" $RUN_LAMA/audit/05-raw-leads.md
grep -n "<NamaFile>" $RUN_LAMA/audit/06-refuted-invalid.md
grep -n "<NamaFile>" $RUN_LAMA/audit/08-valid-not-eligible.md
grep -n "<NamaFile>" $RUN_LAMA/audit/09-confirmed-findings.md
```

- Hasil di `06` → **bukan temuan baru**. Butuh bukti baru material, jika tidak: buang.
- Hasil di `08`/`09` → kemungkinan duplikat submit. Cek tanggal kirim di `SUBMISSION_REPORT/INDEX.md`.

Alasan gerbang ini di **akhir**, bukan awal: menjalankannya di awal mengembalikan anchoring
yang justru ingin dihindari. Biayanya hanya satu grep.
