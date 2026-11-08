# 05-raw-leads.md — Antrean Lead Aktif (METHODOLOGY-SEGITIGA)

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Antrean lead aktif — dipakai di **Tahap C → D**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

> Setiap lead WAJIB membawa **provenance lapis** `[LAPIS: VALUE|PATH|FLOW]` dan **tag bentuk
> serangan** `[AF-xx]` (GATE-C). Tanpa keduanya, entri ditolak.
> Urutan kerja = EV menurun (lihat `notes/money-ledger.md`), bukan urutan tulis.

**Status: 0 entri.**

---

## Format entri (wajib, jangan diubah)

```
## [LEAD-NNN] <judul satu baris> [STATUS -> BELUM|DITEMBUS|TETAP_AMAN|->0X]
- `[LAPIS: VALUE|PATH|FLOW]` `[AF-xx]` `[LOAD: M-xxx]`
- `File:Baris`: `<path>:<awal>-<akhir>` (wajib rentang utuh, bukan potongan)
- Hipotesis: <mekanisme, bukan gejala>
- Provenance: <bagaimana lead ini lahir — census VALUE / jahitan PATH / bedah FLOW>
- Guard: <statis/dinamis; bila statis, sebut apakah tembus 5 Jalur Permissionless>
- Delta State: <variabel yang berubah akibat serangan>
- EV kasar: <max(balance_now, throughput_path)> + asumsi yang dipakai
- Pot: <ID pot dari money-ledger> | Jahitan: <ID dari path-map>
- Strike: 0/3
- Status: BELUM
```

## Gerbang wajib sebelum entri ditulis

1. `[LAPIS]` + `[AF-xx]` terisi dan **konsisten** dengan gejala kode
   (routing cepat di `methodology/mod-attack-forms.md` §Routing gejala → bentuk).
2. `File:Baris` adalah **rentang utuh fungsi**, dibaca penuh (`read_file` ber-offset bila > 60 baris).
   `grep`/`sed` hanya untuk menemukan lokasi — DILARANG menyimpulkan isi dari potongan.
3. FACTS/RADAR **dibuka setelah** hipotesis buta lahir (`mod-technical-rules.md` §5).

---

*Belum ada entri. Tahap A belum dijalankan.*
