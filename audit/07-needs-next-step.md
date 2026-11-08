# 07-needs-next-step.md — Belum Tuntas Diuji

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Wadah belum tuntas — dipakai di **Tahap D → F**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

**Target akhir: 0 entri.** Tujuan file ini adalah menjadi **kosong** di akhir run.

**Status: 0 entri.**

Entri hanya sah untuk tiga kondisi: `NEXT_EXPLORE` (mentok timeout fuzzing/Halmos),
`NEXT_MAINNET` (rantai tanpa RPC/explorer publik), `TOOL_BLOCKED` (gagal setelah
3-Step Self-Healing: flag/toolchain → harness minimal → fallback RPC).

`LAZY_BAILOUT_DETECTED` = entri tanpa bukti usaha. Dilarang memarkir lead yang bisa
diselesaikan sesi ini.

---

## Format entri

```
## [LEAD-NNN] <judul> — <NEXT_EXPLORE|NEXT_MAINNET|TOOL_BLOCKED>
- `[LAPIS: ...]` `[AF-xx]`
- Disposition: <apa yang sudah dicoba dan kenapa belum selesai>
- PERCOBAAN:
  $ <perintah 1>
  # <keluaran asli>
  $ <perintah 2>
  # <keluaran asli>
```

---

*Belum ada entri.*
