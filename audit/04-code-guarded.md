# 04-code-guarded.md — Guard Statis TERSANGKAL

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
