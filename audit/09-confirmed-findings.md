# 09-confirmed-findings.md — Bounty-Ready (Live Production)

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
