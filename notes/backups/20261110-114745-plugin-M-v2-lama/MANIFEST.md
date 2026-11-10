# MANIFEST — plugin M-* v2 lama (10 berkas) diarsipkan

Alasan: isi diserap ke 10 plugin ber-nama v1 (keputusan B3). Berkas lama

tidak dihapus agar konsep v2 yang unik tetap dapat diverifikasi sumbernya.

| Berkas | SHA-256 | Konsep unik yang diserap ke |
| :--- | :--- | :--- |
| `M-001-invariant-value-conservation.md` | `48393bb5d288815b` | M-002 (konservasi nilai = ΔExpected vs ΔActual) |
| `M-002-precision-rounding-scaling.md` | `252233c7d27122a1` | M-002 (sumber asimetri: pembulatan) + M-007 (loop) |
| `M-003-state-transition-ordering.md` | `dd4cc143fd781d9e` | M-002 (sumber asimetri: urutan) + M-006 Prinsip A |
| `M-004-valuation-exchange-rate-oracle.md` | `59cfd3267b2e5b38` | M-004 (valuasi/oracle = View-vs-Write) |
| `M-005-authority-capability-access.md` | `9eedbc973b8ce2fd` | M-005 (otoritas) + M-008 (seam) + M-005 5 Jalur |
| `M-006-liquidation-dispute-latent.md` | `6dc1f09b1fc85d44` | M-001 (sink) + M-003 (self-liquidation) + M-009 |
| `M-007-boundary-zero-extreme-state.md` | `2a3d9b54707f669a` | M-002 (kondisi ekstrem) + M-003 (dust) + M-007 |
| `M-008-offchain-signature-proof-relay.md` | `05993a8040111b4f` | M-008 (hulu off-chain: signature/Merkle/ZK/relayer) |
| `M-009-asymmetric-dos-griefing-locking.md` | `08bd37cba1820bcd` | M-009 (asimetri pause/penalti, antrean, batas waktu) |
| `M-010-cross-module-shared-state-chain.md` | `d67c0f6e4d1a43d9` | M-010 (sinyal [TOUCHES], state lintas-modul) |
