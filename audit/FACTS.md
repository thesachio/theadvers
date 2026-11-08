# FACTS.md — Fakta Mekanisme Terverifikasi (Falsifier, BUKAN Generator)

**Posisi baru (METHODOLOGY-SEGITIGA §6):** file ini dibuka **SETELAH** hipotesis buta lahir
di Tahap C, murni sebagai falsifier. DILARANG dipakai sebagai sumber ide utama.

**Kontaminasi yang dicegah:** run 1-2 membangun FACTS di awal. FACTS itu memuat pemahaman
yang diturunkan dari lead lama, sehingga mewariskan kerangka berpikir lama ke run 3.
Karena itu run 3 **membangun ulang dari nol**.

**Status: 0 domain terisi — Tahap A belum dijalankan.**

---

## Tujuh komponen wajib per domain

| Komponen | Isi | Batas |
|---|---|---|
| `BERKAS` | kunci pencarian (nama file/kontrak) | — |
| `MEKANISME` | bagaimana domain bekerja | ≤12 baris/domain |
| `CHAINING` | state yang bertahan lintas-hop | — |
| `DATA` | tipe / satuan / nilai sentinel | — |
| `INVARIAN` | invarian + penegaknya, atau `TIDAK ditegakkan` | — |
| `LINGKUNGAN` | klasifikasi otoritas ber-tag `[chain:alamat]` | — |
| `ASUMSI` | asumsi yang dipegang, ditandai bila rapuh | — |

**DILARANG** memuat hipotesis (itu `05`) dan status deployment
(`CYCLE`/`ENTRYPOINT`/`Mode Uji` — itu `notes/deploy-parity-*.json`).

---

## Format blok domain

```
### D1: <nama-domain>
- BERKAS: <file utama>
- MEKANISME: <1-3 baris>
- CHAINING: <state lintas-hop>
- DATA: <tipe/satuan/sentinel>
- INVARIAN: <invarian> — penegak: <kode atau TIDAK ditegakkan>
- LINGKUNGAN: <peran> = <alamat> [chain:<id>]
- ASUMSI: <asumsi>
```

---

*Belum ada domain.*
