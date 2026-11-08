# RADAR.md — Sinyal Lintas-Domain (Append-Only)

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Sinyal lintas-domain — dipakai di **Tahap B–C**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

Observasi berpresisi `File:Baris` yang **belum layak jadi lead** — belum ada bukti
eksploitasi, tapi menunjukkan asimetri. Bukan `05` (belum teruji), bukan atestasi.

**Dua lapis, keduanya append murni:** Observasi (ditulis sekali) + Kejadian
(`PROMOTED`, `RESOLVED-*`, `TARGET-ADDED`, `REOPENED`, `EXHAUSTED`).

Sinyal **DILARANG** diparkir di sini bila sudah ada PoC `[PASS]` → wajib naik ke `05`.

**Status: 0 observasi.**

---

## Format observasi

```
## [RADAR-NNN] <asimetri satu baris>
- `File:Baris`: `<path>:<awal>-<akhir>`
- Asimetri: <harapan vs kenyataan>
- Pemicu: <kondisi yang membuatnya relevan>
- Tujuan: <unit/domain/stage yang berkepentingan>
- Status: OPEN
```

## Gerbang 3-Uji sebelum observasi diterima

1. Ada presisi `File:Baris` yang bisa dibuka ulang.
2. Bisa menyebutkan pemicu konkret (bukan "mungkin berbahaya").
3. Ada tujuan jelas (siapa yang akan memakai sinyal ini).

---

*Belum ada observasi.*
