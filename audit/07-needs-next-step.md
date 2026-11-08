# 07-needs-next-step.md — Belum Tuntas Diuji

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
