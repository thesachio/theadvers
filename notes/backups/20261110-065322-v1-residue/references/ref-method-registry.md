# REF-METHOD-REGISTRY — Jembatan Kompatibilitas ke Router Plugin (theadvers v2.0)
> PEMBERITAHUAN ARSITEKTUR MODULAR v2.0 (`1 FILE = 1 METODE`):
> Katalog metode bedah kini menggunakan arsitektur Drop-in Plugin di dalam direktori references/methods/.
> - Untuk melihat indeks ringkas seluruh metode (M-001 s/d M-xxx) beserta Trigger Symptom-nya, baca: `references/methods/_ROUTER.md`.
> - Untuk menambah atau merevisi metode bedah, buat atau ubah berkas mandiri references/methods/M-xxx-<slug>.md lalu jalankan python3 tools/verify_segitiga.py --sync.
> - Dilarang memuat seluruh berkas metode sekaligus ke dalam memori; gunakan _ROUTER.md untuk *lazy-loading* hanya metode yang cocok dengan gejala wilayah aktif.
