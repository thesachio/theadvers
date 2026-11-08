# MOD-OFFCHAIN — Doktrin Bedah Aktor Luar (Tahap E, opsional)

Plug-in METHODOLOGY-SEGITIGA. **Kontrak ekstensi**: kebijakan baru = append satu blok.

## Prinsip inti

- **Bukti SELALU on-chain** — tidak ada laporan diterima tanpa manifestasi on-chain.
- **Bedah off-chain = mengubah "terlihat aneh" menjadi "ini barisnya, ini dampaknya"**, dan
  menangkap kelas bug yang tak pernah tampil di rantai: yang diam, yang bocor pelan, yang belum menembak.

## Pemicu bedah (bukan dibaca menyeluruh)

Bedah off-chain HANYA bila salah satu terpenuhi:

1. **Scope bounty memasukkan off-chain** (cek aturan bounty proyek — Across: eksplisit YA,
   termasuk bot & front-end).
2. **Anomali on-chain teramati**: dispute nyata, bundle gagal, pola fill menyimpang.
3. **Kelas ketiadaan aksi**: keeper/bot SEHARUSNYA bertindak tapi diam (tidak ada tx) —
   on-chain tak bisa membedakan diam-yang-benar vs diam-yang-bug; hanya kode yang bisa.

## Alur

```
1. Cek org GitHub proyek dulu ("tidak tersedia" sering = belum dicari)
2. Repo PUBLIK  → clone, bedah jalur yang memicu anomali (bukan seluruh repo)
3. Repo PRIVAT  → rekonstruksi blackbox dari event on-chain:
                  pola dispute/fill/bundle → model perilaku → deviasi = hipotesis
4. Temuan diajukan atas MANIFESTASI on-chain; severity diukur dari kerugian on-chain
```

## Batas-batas jujur

- Bug privat yang hanya merugikan OPERATOR-nya sendiri → self-inflicted → umumnya tidak dibayar
  bounty; catat, jangan klaim.
- Label `07`/`TOOL_BLOCKED` hanya bila BUKTI ON-CHAIN-nya tak terjangkau (RPC/explorer mati) —
  kehilangan source privat bukan alasan sah berhenti.
- Severity off-chain dinilai dari dampak ke PENGGUNA (bundle palsu menyapu pool = High), bukan
  dari parahnya bug logika (UI salah tampil = informational).

## Empat hal yang observasi on-chain TIDAK bisa (alasan bedah tetap bernilai)

1. **Atribusi akar** — on-chain = gejala; bounty butuh "bug di baris Y, rumus Z".
2. **Bug laten** — temukan SEBELUM menembak (potential impact = inti severity).
3. **Degradasi senyap** — bug yang membocorkan alur tanpa mematahkannya (underprice 1%/fill).
4. **Ketiadaan aksi** — absennya tx tidak bisa dibedakan dari keputusan benar.
