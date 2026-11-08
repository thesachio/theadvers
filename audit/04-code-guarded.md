# 04-code-guarded.md — Guard Statis TERSANGKAL

<!-- SEGITIGA-BINDING -->
> **Peran berkas.** Wadah guard statis — dipakai di **Tahap C**. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

Hanya hipotesis yang dihentikan **Guard Statis/Struktural** (`onlyOwner`, `onlyRouter`,
`msg.sender == x`, `nonReentrant`, `whenNotPaused`, cek alamat `!= 0`) **dan** terbukti
tidak tembus 5 Jalur Permissionless.

**DILARANG** memasukkan guard dinamis/matematis (rasio, pembulatan, saldo, waktu, panjang
array) — itu milik `05`. **DILARANG** memasukkan guard statis yang TEMBUS salah satu jalur.

**Status: 0 entri.**

---

## Format entri

```
## [GUARD-NNN] <judul>
- `File:Baris`: `<path>:<awal>-<akhir>`
- Ekspresi guard: `<kode guard persis>`
- Variabel pembentuk: <state yang menentukan hasil guard>
- Uji 5 Jalur Permissionless: <hasil per jalur, J1..J5>
- Verdict: TERSANGKAL
```

---

*Belum ada entri.*
