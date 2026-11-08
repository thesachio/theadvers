# 06-refuted-invalid.md — Gugur Permanen

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Wadah gugur permanen — dipakai di **Tahap D → F**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

**Status: 0 entri.**

Hukum Anti-Paper-Refutation (#11e): setiap entri `REJECTED_POC_FAILS`,
`REJECTED_NEGATIVE_EV`, dan `REJECTED_DUST` **WAJIB** melampirkan blok `BUKTI_SIMULASI:`
berisi perintah `$ ...` + keluaran nyata. Penolakan kertas tanpa kode test memicu
`PAPER_REFUTATION_DETECTED`.

3-Stage Escalation sebelum mengunci di sini: Strike 1 (Manual + Victim Seeding) →
Strike 2 (Perbaikan Urutan + 3-Way Amplification) → Strike 3 (Mandatory Fuzz `testFuzz_`).
Kegagalan alat (compile, import, checksum, ABI) **bukan** strike.

---

## Format entri

```
## [LEAD-NNN] <judul> — REJECTED_<KELAS>
- `[LAPIS: ...]` `[AF-xx]`
- `File:Baris`: `<path>:<awal>-<akhir>`
- Alasan gugur: <mekanisme kegagalan>
- Strike: 3/3 (1 manual, 2 manual+amplifikasi, 3 fuzz)
- Kelas: REJECTED_FANTASY_MOCK | REJECTED_UNPROVEN_DEPLOYMENT | REJECTED_GENESIS_MIRAGE |
  REJECTED_NO_VICTIM | REJECTED_NEGATIVE_EV | REJECTED_CHEATCODE |
  REJECTED_PRIVILEGED_FANTASY | REJECTED_NON_LIVE_INIT | REJECTED_DUST |
  REJECTED_BY_DESIGN | REJECTED_MISMATCH | REJECTED_POC_FAILS
- BUKTI_SIMULASI:
  $ forge test --match-test test_LEADNNN -vv
  # <keluaran asli, tempel dari log>
- Duplikat di run lama? <hasil grep ke <run-lama>/audit/06>
```

---

*Belum ada entri.*
