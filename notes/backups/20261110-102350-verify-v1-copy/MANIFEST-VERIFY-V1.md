# Salinan Panjang v1 dari `verify/` — dipindah

Dibuat: 2026-11-10 10:23:50

## Alasan

Setelah aturan bukti 06/07/08/09 dipulihkan ke `templates/VERDICT.md` (21.702 B), dua berkas ini
di `verify/` menjadi **sumber kebenaran ganda** yang berisi istilah dan aturan v1:

| Berkas | Ukuran | Sisa istilah v1 |
| :--- | :--- | :--- |
| `VERDICT.md` | 47.111 B | 23x "Fase N", 2x `INTEL.md`, 1x "kesebelas", 3x rujukan `verify/SEVERITY-RUBRIC.md` & `verify/ingest.py` |
| `SEVERITY-RUBRIC.md` | 21.419 B | 1x "Fase N", 1x `INTEL.md`, 1x rujukan `verify/SEVERITY-RUBRIC.md` |

Tidak ada berkas hidup yang merujuk keduanya lagi (diverifikasi dengan sweep 77 berkas).

## Yang DIPERTAHANKAN di `verify/`

| Berkas | Alasan |
| :--- | :--- |
| `SCHEMA.md` | skema `MANIFEST.json` untuk repo inbox submission — dirujuk `templates/09-confirmed-findings.md` dan `README.md` |
| `ingest.py` | validator submission (gerbang `MECH-OK`) — dirujuk `README.md` |

## Catatan

`SCHEMA.md` menyebut `tools/ingest.py`, sedangkan lokasi nyatanya `verify/ingest.py`.
Perbedaan ini BELUM diperbaiki (menunggu keputusan): perbaiki teks skema, atau pindahkan
`ingest.py` ke `tools/`.

## Pemulihan

```bash
cp -r notes/backups/20261110-102350-verify-v1-copy/*.md <root-repo>/verify/
```
