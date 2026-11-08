# 09-confirmed-findings.md — Bounty-Ready (Live Production)

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Wadah bounty-ready — dipakai di **Tahap F**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

Hanya untuk `VALID_ELIGIBLE`: PoC `[PASS]` pada fork state produksi (`FORK_LIVE`, atau
`FORK_DEPLOYED_HEAD` yang terbukti `LIVE_MATCH`), tanpa Fantasy Mock/Cheatcode,
dampak finansial nyata (Critical/High/Medium), lolos 11 Pernyataan Wajib
(`templates/VERDICT.md`).

**Status: 0 entri.**

---

## Format entri

```
## [LEAD-NNN] <judul>
- `[LAPIS: ...]` `[AF-xx]`
- **Severity:** <Critical|High|Medium> · **Mode Uji:** `FORK_LIVE` · **Tangga Bukti:** A
- **Lokasi:** `<path>:<awal>-<akhir>`
- **Mekanisme:** <rantai sebab-akibat dari baris kode ke kerugian>
- **Korban:** <siapa yang kehilangan uang; saldo terukur>
- **BUKTI_SIMULASI:**
  $ forge test --match-test test_LEADNNN -vvv
  # <keluaran asli>
- **Duplikat di run lama?** <hasil grep <run-lama> 05/06/08/09 + SUBMISSION_REPORT/INDEX.md>
```

---

*Belum ada entri.*
