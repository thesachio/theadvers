# BOOTSTRAP — Memulai Audit di Sesi Baru

> Dibuat agar sesi baru tidak perlu membaca percakapan lama. Semua konteks ada di disk.

## 1. Yang sudah siap (tidak perlu diulang)
- Framework v2 lengkap di repo ini (`SOUL.md`, `AGENTS.md`, `methodology/`, `references/`, `templates/`, `tools/`).
- 52 plugin aktif (M 10, POV 15, CHAIN 10, AF 10, DOM 7), `_ROUTER.md` tersinkron.
- 8 skill `sc-*` sudah disinkronkan ke profil: `~/.hermes/profiles/adv/skills/` (termasuk `sc-autopilot` v2; salinan v1 usang sudah dipindah ke `notes/backups/`).

## 2. Langkah boot di sesi baru
1. Buat direktori audit proyek target:
   `mkdir -p projects/<target>/audit/notes`
   `cp templates/*.md projects/<target>/audit/`
2. Isi `INTEL.md` lewat skill `sc-pre-intel` (wajib: nama proyek, repo+commit, link bounty, **Deployment Stage: MAINNET/TESTNET/DEVNET**).
3. Jalankan packet konteks pertama:
   `python3 tools/verify_segitiga.py --context-packet projects/<target>/audit`
4. Mulai STAGE-0: inventaris 100% berkas ke `path-map.md`, partisi `R_1..R_N` di `STATE.md`, lalu:
   `python3 tools/verify_segitiga.py --gate 0 projects/<target>/audit`
5. Lanjut loop vertikal: A → B → C1 → C2 → batch D→E → F per wilayah; `--context-packet` di setiap tahap/ganti batch.

## 3. Aturan yang paling sering dilanggar (ingatkan diri)
- `--context-packet` WAJIB di awal setiap tahap — jangan mengandalkan ingatan percakapan.
- C1 blind: dilarang membuka `_ROUTER`/plugin.
- `[QUEUED]` boleh `[NO-CATALOG]`; jangan buang kandidat hanya karena tak cocok katalog.
- Plugin yang dipakai wajib punya baris `MATCH` §1.3 dengan kutipan verbatim — gate C2 memverifikasi.
- Batch maks 3, satu wilayah, satu `Batch ID` `<R_i>-B<nn>`; jangan pindah wilayah sebelum `[QUEUED]==0`.
- Kartu `[ACTIVE]` wajib blok `Bekal Uji` + M/AF yang menunjuk berkas nyata.

## 4. Perintah penegak
`--sync` · `--context-packet <dir>` · `--gate 0|A|B|C1|C2|D|E <dir>` · `--rules <dir>` · `--close-region <R_i> <dir>` · `--final <dir>`
