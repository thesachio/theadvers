# 08-valid-not-eligible.md — Valid Mekanis, Tak Eligible

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Wadah valid-tak-eligible — dipakai di **Tahap F**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

**Eksklusif tulisan Tahap F (VERDICT).** Tahap D DILARANG menulis ke file ini.

Tiga alasan masuk sini: `PRE_LIVE_SCOPE (HEAD_ONLY_PROVEN)`, `ADMIN_ONLY`, `LOW_NUISANCE`.

**Status: 0 entri.**

---

## Format entri

```
## [LEAD-NNN] <judul> — <KELAS_08>
- `[LAPIS: ...]` `[AF-xx]`
- Severity: <Critical|High|Medium|Low> (rubrik: templates/SEVERITY-RUBRIC.md)
- Mode Uji: FORK_LIVE | FORK_DEPLOYED_HEAD | LOKAL
- Tangga Bukti: A | A-HEAD | B
- Alasan tak-eligible: <PRE_LIVE_SCOPE / ADMIN_ONLY / LOW_NUISANCE>
- BUKTI_SIMULASI:
  $ <perintah>
  # <keluaran asli>
```

---

*Belum ada entri.*
