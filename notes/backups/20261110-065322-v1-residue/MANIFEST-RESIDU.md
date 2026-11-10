# MANIFEST RESIDU v1 — dipindah dari workflow v2

Dibuat: 2026-11-10 06:53:31
Sumber: repo theadvers (cabang v2)

Berkas di bawah ini adalah sisa workflow lama (Segitiga + Offchain / 6 tahap A-F)
yang TIDAK dipakai lagi oleh workflow baru (theadvers v2.0 / STAGE-0..F + drop-in plugin).
Dipindah (bukan dihapus permanen) agar tetap dapat dirujuk bila ada bagian yang perlu dipulihkan.

| Berkas | Alasan tidak dipakai |
| :--- | :--- |
| `methodology/mod-layers.md` | L-VALUE/L-PATH/L-FLOW lapis v1 (diganti @SLICE STAGE-A/B/C) |
| `methodology/mod-attack-forms.md` | registry AF v1 (diganti methodology/attack-forms/AF-01..10) |
| `methodology/mod-domain-cartridges.md` | domain cartridges v1 (diganti methodology/domains/DOM-*) |
| `methodology/mod-chain-cartridges.md` | chain cartridges v1 (diganti references/chains/CHAIN-*) |
| `methodology/mod-offchain.md` | Tahap E offchain v1 (tidak ada padanan di v2) |
| `methodology/mod-technical-rules.md` | aturan teknis v1 (diserap ke AGENTS.md v2) |
| `methodology/flow-diagram.md` | diagram alur v1 (6 tahap A-F, bukan STAGE-0..F) |
| `methodology/attack-forms.md` | bridge v1 -> attack-forms/ |
| `methodology/domain-heuristics.md` | bridge v1 -> domains/ |
| `references/_INDEX-SEGITIGA.md` | matriks indeks v1 (dibaca tools/sync_segitiga_terms.py v1) |
| `references/README.md` | README referensi v1 (daftar 18 ref-*) |
| `templates/README.md` | README template v1 |
| `templates/MERGE-LOG.tsv` | merge log v1 (dipakai tools/merge_audit.py v1) |
| `templates/INTEL.md` | Fase 0 INTEL v1 (dipindah atas keputusan pengguna) |
| `AUTOPILOT-MAPPING.md` | peta Fase 1-4 -> Tahap A-F (istilah v1) |
| `CLASSIFICATION.md` | taksonomi LAPIS x CLASS x AF (v1) |
| `references/ref-method-registry.md` | bridge registry v1 (diganti references/methods/_ROUTER.md) |
| `references/ref-attacker-pov.md` | POV router v1 (diganti references/pov/_ROUTER.md) |
| `references/ref-pov-call.md` | katalog POV v1 |
| `references/ref-pov-chain.md` | katalog POV v1 |
| `references/ref-pov-defi.md` | katalog POV v1 |
| `references/ref-pov-math.md` | katalog POV v1 |
| `references/ref-calls-tokens-reentrancy.md` | checklist v1 |
| `references/ref-math-and-vaults.md` | checklist v1 |
| `references/ref-defi-oracles-liquidation.md` | checklist v1 |
| `references/ref-chain-evm-tron.md` | tooling chain v1 (router CHAIN v2 = pola serangan berantai) |
| `references/ref-chain-solana.md` | tooling chain v1 |
| `references/ref-chain-sui-move.md` | tooling chain v1 |
| `references/ref-chain-ton-async.md` | tooling chain v1 |
| `references/ref-test-evm-advanced.md` | harness v1 |
| `references/ref-test-multichain-advanced.md` | harness v1 |
| `references/ref-atomic-write.md` | protokol tulis v1 (aturan atomik kini di AGENTS.md v2) |
| `tools/bind_references.py` | alat v1: menyuntik blok SEGITIGA-BINDING ke ref-* (ref-* sudah pindah) |
| `tools/sync_segitiga_terms.py` | alat v1: sinkron istilah pada ref-* (ref-* sudah pindah) |
| `tools/merge_audit.py` | alat v1: staging/merge (v2 pakai notes/staging-*.md tanpa merge_audit) |
| `tools/verify07.py` | alat v1: gate LAZY_BAILOUT (v2 tidak punya kelas 07) |

## Pemulihan

```bash
cp -r notes/backups/20261110-065322-v1-residue/* <root-repo>/
```

## Yang DIPERTAHANKAN (masih dipakai workflow v2)

| Berkas | Dipakai oleh |
| :--- | :--- |
| `tools/verify_segitiga.py` | mesin gate v2 |
| `tools/deploy_parity.py` | dirujuk `templates/09-confirmed-findings.md` + `templates/case/laporan-teknis.md` |
| `verify/SCHEMA.md`, `verify/ingest.py` | dirujuk `templates/09-confirmed-findings.md` (gerbang MECH-OK) |
| `verify/VERDICT.md` | salinan standar 11 Pernyataan / #11e (47.111 B) |
| `verify/SEVERITY-RUBRIC.md` | dirujuk `templates/09-confirmed-findings.md` |
| `templates/TECHNICAL-REPORT.md`, `POC-PACKAGE.md`, `SUBMISSION-EMAIL.md`, `SEVERITY-RUBRIC.md` | standar `cases/<ID>/` |
