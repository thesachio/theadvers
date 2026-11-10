# PROJECT INTELLIGENCE BRIEF — `INTEL.md` (Prasyarat STAGE-0 / theadvers v2.0)

> **Posisi berkas.** `INTEL.md` diletakkan **di root folder kerja audit**, sejajar dengan `STATE.md`.
> Ia diisi **sekali** di awal, dan **hanya diperbarui bila jaringan/deployment berubah**.
> Ia **bukan tahap baru** — ia **prasyarat `--gate 0`**. Selama INTEL belum sah, `--gate 0` FAIL
> dan STAGE-A tidak boleh dimulai.

> **Pembagian tugas (jangan dicampur).**
> - `INTEL.md` = **fakta proyek yang dapat ditunjuk**: identitas, URL, commit, jaringan, alamat, bukti live.
> - `STATE.md` = **posisi eksekusi**: wilayah aktif, stage, batch, antrean, gate terlewati.
> - `path-map.md` = **peta kode**: rekonsiliasi 100% berkas, Tier, Wilayah R_i, 3-edge.
>
> `INTEL.md` **DILARANG** memuat hipotesis kerentanan, status wilayah, atau hasil audit.

> **Hukum kejujuran.** Bila sesuatu tidak ditemukan, tulis `TIDAK_DITEMUKAN` **beserta alasannya**.
> DILARANG mengarang URL, mengisi nama auditor dari ingatan, atau menebak commit.
> `TIDAK_DITEMUKAN` adalah hasil yang sah; URL palsu menghancurkan seluruh laporan.

---

```markdown
# PROJECT INTELLIGENCE BRIEF

- Target Repo Path  : <path absolut proyek lokal>
- Last Updated     : <YYYY-MM-DD>
- Intel Status     : COMPLETE | PARTIAL (catat bagian yang belum ditemukan)
- Diverifikasi Oleh: <perintah yang dijalankan untuk membuktikan tiap URL/klaim>

## 0. Deployment Stage (WAJIB — menentukan Mode Uji seluruh audit)

- Deployment Stage : MAINNET | TESTNET | DEVNET
- Alasan/Landasan  : <1 baris: mengapa stage itu yang dipakai — rujuk Bukti Live di §5>
- Perubahan Stage  : <tanggal + alasan, bila pernah berubah; selain itu "belum pernah berubah">

## 1. Project Identity & Brief Overview
- Project Name : <Nama Resmi Proyek & Organisasi>
- Brief Overview : <1–3 kalimat ringkas mengenai fungsi dan mekanisme inti protokol>

## 2. Core Reference Links (Direct URLs Only)
- Main UI (dApp) : <URL langsung ke aplikasi web/UI utama tempat pengguna berinteraksi, atau TIDAK_DITEMUKAN>
- Official Docs  : <URL langsung ke dokumentasi teknis resmi, atau TIDAK_DITEMUKAN>
- Specific GitHub Repo : <URL langsung ke repositori GitHub spesifik yang menjadi target audit>
- Audited Commit / Branch : <branch> @ <commit_hash>

## 3. Bug Bounty Rules (Direct Link)
- Platform : <Docs Resmi | Immunefi | Cantina | Sherlock | Code4rena | CodeHawks | Lainnya | TIDAK_DITEMUKAN>
- Direct Bounty URL : <URL langsung ke halaman aturan/scope bug bounty spesifik proyek ini>
- High-Level Scope Note : <1–2 baris catatan faktual bila halaman bounty menyebut repo/kontrak/
  chain spesifik atau aturan pengecualian utama>

## 4. Past Audit Reports (Direct File/Report Links)
- [<Nama Auditor 1 — Tanggal/Tahun>](<URL langsung ke file PDF / repo / halaman laporan audit>) — Fokus/Versi: <singkat>
- [<Nama Auditor 2 — Tanggal/Tahun>](<URL langsung ke file PDF / repo / halaman laporan audit>) — Fokus/Versi: <singkat>
- *(Bila belum ditemukan laporan publik, ganti KEDUA baris di atas dengan:)*
  `TIDAK_DITEMUKAN — tidak ada laporan audit publik di docs/, folder audits/, maupun situs auditor.`
- *(Bila README hanya MENYEBUT adanya audit tanpa tautan:)*
  `TIDAK_DITEMUKAN — README menyebut "audit by X" tanpa tautan laporan (klaim tak terverifikasi).`

## 5. Deployment & Live Surface (fakta terukur, bukan asumsi)
- Chain / Network Aktif : <daftar nama + chainId yang benar-benar dipakai, atau TIDAK_DITEMUKAN>
- Kontrak Utama (alamat) : <alamat entrypoint/proxy + chain, atau TIDAK_DITEMUKAN>
- Implementation Aktif : <alamat impl di balik proxy (slot EIP-1967), atau "bukan proxy", atau TIDAK_DITEMUKAN>
- Blok Referensi      : <nomor blok terakhir saat INTEL disusun — dipakai sebagai titik fork awal>
- VERSION_RELATION    : LIVE_IS_DEPLOYED_COMMIT | LIVE_NEWER_THAN_HEAD | HEAD_NEWER_THAN_LIVE | LIVE_UNVERIFIED
- Bukti Live : <perintah `cast code` / `eth_getCode` / `getAccountInfo` + hasil ringkas yang membuktikan kode ter-deploy>

## 6. Catatan Ketiadaan (WAJIB bila Intel Status = PARTIAL)
| Butir | Status | Alasan + sumber dicoba | Dampak |
|---|---|---|---|
| UI | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak bila tak ditemukan> |
| Docs | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Repo | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Bounty | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Audits | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Deployment | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
- Ringkasan : <butir TIDAK_DITEMUKAN, atau "tidak ada — INTEL COMPLETE">
```

---

## Aturan pengisian (mengikat)

1. **URL harus langsung.** `https://docs.protokol.xyz/security` ✅ — bukan `https://docs.protokol.xyz` bila halaman itu tidak memuat aturan buruannya. DILARANG menaruh URL mesin pencari.
2. **Setiap URL wajib dibuktikan hidup** pada sesi yang sama (`curl -sI` → status 200/30x, atau pembacaan halaman). Catat perintahnya di baris `Diverifikasi Oleh`. URL mati → `TIDAK_DITEMUKAN`.
3. **Commit wajib dipin.** `Audited Commit / Branch` harus berisi hash hasil `git rev-parse`, bukan "latest". Ini input langsung untuk `VERSION_RELATION` di `templates/VERDICT.md` §2c.
4. **Dilarang mengarang nama auditor.** Bila repo/docs menyebut "audit oleh X" tanpa tautan laporan, tulis `TIDAK_DITEMUKAN` di §4 dan sebutkan klaim tak terverifikasi itu di §6.
5. **§5 bersifat terukur.** Deployment dinyatakan ada hanya bila ada `eth_getCode`/`cast code` non-kosong atau transaksi deploy. "Seharusnya live" bukan bukti.
6. **§6 tidak boleh kosong** bila `Intel Status = PARTIAL`. Bagian inilah yang melindungi audit dari klaim berlebih di STAGE-E/F.

### Aturan khusus §0 — `Deployment Stage`

`Deployment Stage` **menentukan Mode Uji seluruh audit**, jadi ia wajib dinyatakan, bukan disimpulkan:

| `Deployment Stage` | Artinya | Akibat pada audit |
| :--- | :--- | :--- |
| `MAINNET` | protokol berjalan di jaringan produksi publik | `09` wajib `Mode Uji: FORK_LIVE`; `FORK_TESTNET`/`FORK_DEPLOYED_HEAD`/`LOKAL` **tidak sah** di `09` |
| `TESTNET` | protokol hanya berjalan di testnet publik (belum produksi) | `09` wajib `Mode Uji: FORK_TESTNET`; `FORK_LIVE` tidak sah |
| `DEVNET` | jaringan pengembangan privat/terbatas | `09` wajib `Mode Uji: FORK_TESTNET` (fork devnet); dicatat eksplisit di laporan |

**Larangan:**
- `Deployment Stage` **DILARANG dikosongkan.** Tidak ada default diam-diam — INTEL tanpa §0 = `--gate 0` FAIL.
- `Deployment Stage: MAINNET` **DILARANG** bila §5 `Bukti Live` kosong. Mainnet tanpa bukti `cast code` non-kosong = klaim tanpa dasar.
- Perubahan stage (mis. `TESTNET → MAINNET`) **wajib** mengisi baris `Perubahan Stage` + tanggal, dan **mengulang** `--gate 0` untuk wilayah yang belum ditutup.

---

## Aturan Jujur per Bagian (WAJIB — "tidak ditemukan" bukan kegagalan)

Setiap bagian punya **cara sah mengatakan tidak ada**. Dilarang mengosongkan slot, dilarang mengisi dengan tebakan, dilarang memaksakan jawaban agar terlihat lengkap.

| Bagian | Bila TIDAK ditemukan, tulis PERSIS | DILARANG |
|---|---|---|
| 0 · Deployment Stage | **tidak boleh** — wajib salah satu dari tiga nilai | Mengosongkan, menebak, atau menyalin dari proyek lain |
| 1 · Project Name | `TIDAK_DITEMUKAN` diikuti sumber yang diperiksa (`README`/`git remote`) | Menebak nama dari nama folder |
| 1 · Brief Overview | `TIDAK_DITEMUKAN — tidak ada README/docs yang menjelaskan mekanisme` | Mengarang deskripsi dari pengetahuan umum/model |
| 2 · Main UI (dApp) | `TIDAK_DITEMUKAN` — protokol mungkin hanya kontrak/library tanpa UI | Menulis domain akar yang belum diuji |
| 2 · Official Docs | `TIDAK_DITEMUKAN` | Menulis URL hasil pencarian |
| 2 · Specific GitHub Repo | `TIDAK_DITEMUKAN` — bukan repo git / tanpa remote | Menebak `github.com/<org>/<nama>` dari nama proyek |
| 2 · Audited Commit | `TIDAK_DITEMUKAN` — bukan repo git | Menulis `latest`, `main`, atau hash karangan |
| 3 · Platform | `TIDAK_DITEMUKAN` | Mengisi `Immunefi` tanpa halaman bounty yang benar-benar ada |
| 3 · Direct Bounty URL | `TIDAK_DITEMUKAN` | Menunjuk beranda platform, bukan halaman proyek |
| 3 · High-Level Scope Note | `TIDAK_DITEMUKAN — tidak ada aturan scope tertulis` | **Menyimpulkan scope dari praktik umum** |
| 4 · Past Audit Reports | `TIDAK_DITEMUKAN` | Menaikkan *"disebut di README"* menjadi laporan |
| 5 · Chain / Kontrak / Impl / Blok / Bukti Live | `TIDAK_DITEMUKAN` per sub-baris | Menulis alamat tanpa `cast code` non-kosong |

### Empat hukum pengisian

1. **Satu alasan per ketiadaan.** `TIDAK_DITEMUKAN` saja tidak cukup — wajib disertai **alasan singkat + sumber yang sudah dicoba** di tabel §6. Tanpa itu, INTEL dianggap **tidak jujur**.
2. **"Gagal diakses" ≠ "tidak ada".** Bila penyebabnya 403/429/login/timeout, tulis `TIDAK_DITEMUKAN (batas akses: <penyebab>)`. DILARANG menyimpulkan aturan/laporan itu tidak eksis.
3. **Dilarang mengisi slot dengan asumsi.** Bila ragu, turunkan ke `TIDAK_DITEMUKAN`. Satu slot kosong yang jujur tidak merusak laporan; satu URL palsu membatalkan seluruhnya.
4. **Konsistensi wajib.** `Intel Status = COMPLETE` hanya sah bila **keenam** butir di tabel §6 berstatus `DITEMUKAN`. Satu saja `TIDAK_DITEMUKAN` ⇒ status **wajib** `PARTIAL`.
