# KLASIFIKASI — tiga sumbu yang berbeda (jangan dicampur)

Ini pertanyaan yang paling mudah salah dijawab, dan salah menjawabnya membuat
`delegate_task` memilih paket metode yang keliru.

## Jawaban singkat

Referensi lama memakai **CLASS-A/B/C** sebagai klasifikasi. Metode segitiga **tidak
menggantikannya** — ia menambah **satu sumbu baru** (`[LAPIS]`) dan mempertahankan dua
sumbu lama. Ketiganya **ortogonal**: sebuah lead memiliki ketiganya sekaligus.

| Sumbu | Menjawab pertanyaan | Nilai | Sumber | Kapan ditentukan |
|---|---|---|---|---|
| **1. LAPIS** (baru) | *Dari mana lead ini lahir?* | `VALUE` / `PATH` / `FLOW` | `methodology/mod-layers.md` | Tahap A/B/C, saat lead ditulis |
| **2. CLASS** (lama, wajib tetap) | *Berapa entitas & sepanjang apa alurnya?* | `CLASS-A` / `CLASS-B` / `CLASS-C` | `references/ref-method-registry.md` §1 | Tahap C, saat unit/jahitan diambil |
| **3. AF** (baru) | *Bagaimana cara menyerangnya?* | `AF-01` … `AF-10` | `methodology/mod-attack-forms.md` | Tahap C, setelah gejala kode terlihat |

Analoginya:

- **LAPIS** = *tim mana yang menemukan* (sensus nilai, peta aliran, bedah kode).
- **CLASS** = *seberapa besar panggungnya* (1 entitas / 2 entitas / rantai panjang).
- **AF** = *senjata apa yang dipakai*.

Ketiganya tidak saling menggantikan. Lead `[LAPIS: PATH] [CLASS-C] [AF-09]` berarti:
lahir dari peta aliran, panggungnya rantai multi-entitas panjang, dan diserang lewat
penyisipan asinkron.

## Mengapa CLASS tidak boleh dibuang

`ref-method-registry.md` §1 mengikat **paket metode wajib minimum per kelas**:

| Kelas | Paket metode |
|---|---|
| `CLASS-A` | M-001, M-002, M-003 (2 akun pada 1 kontrak), M-004, M-005, M-006 Prinsip B, M-007, M-008 (self-call), M-009, M-010 |
| `CLASS-B` | seluruh CLASS-A + M-003, M-006 Prinsip A+B, M-008, M-010 (residual authority) |
| `CLASS-C` | paket penuh M-001..M-010, penekanan M-003/M-004/M-005 lintas-kontrak/M-008/M-009/M-010 |

Tanpa CLASS, agen tidak tahu metode mana yang **wajib** dijalankan. Ini bukan soal
gaya — ia menentukan kelengkapan bedah.

**Peringatan tetap berlaku:** `CLASS-A < CLASS-B < CLASS-C` **bukan** urutan EV.
Satu vault `CLASS-A` bisa memegang 100% TVL. Urutan kerja tetap **EV menurun** dari
`money-ledger.md`.

## Yang berubah di segitiga (dan yang tidak)

### Berubah
- **Urutan kerja**: EV ledger, bukan nomor unit `S-n`.
- **Provenance wajib**: `[LAPIS]` harus ada supaya bisa diaudit "lead ini lahir dari lapis
  yang benar, atau dari tebakan".
- **Tag serangan wajib**: `[AF-xx]` memaksa agen menyebut mekanisme, bukan gejala.
- **CLASS-C pemicu**: kini sering lahir otomatis dari Tahap B (jahitan lintas-hop di
  `path-map.md`), bukan dari nomor unit.

### Tidak berubah
- Definisi CLASS-A/B/C dan paket metode wajibnya.
- Larangan menyimpulkan severity dari CLASS.
- 5 Jalur Permissionless, 4 Kondisi Batas, 5 Primitif Universal.

## Cara mengisi di `05-raw-leads.md`

```
## [LEAD-004] ...
- `[LAPIS: PATH]` `[CLASS-C]` `[AF-09]` `[LOAD: M-009]`
```

Kolom wajib kini **tiga**: `[LAPIS]`, `[CLASS-x]`, `[AF-xx]`.
`tools/verify_segitiga.py` G1 memeriksa `[LAPIS]` dan `[AF-xx]`; **G9** memeriksa
`[CLASS-x]`. Lead tanpa salah satunya ditolak.

## Jebakan yang harus dihindari

1. **Menganggap LAPIS menggantikan CLASS.** Tidak. `[LAPIS: FLOW]` tidak memberitahu
   berapa entitas yang terlibat.
2. **Menurunkan CLASS-C menjadi CLASS-A karena "hanya satu kontrak".** CLASS menghitung
   **entitas yang berinteraksi**, bukan jumlah berkas. Satu kontrak yang memanggil token,
   oracle, dan callback adalah `CLASS-C`.
3. **Memakai CLASS sebagai prioritas.** Itu pelanggaran urutan EV (lihat `SOUL.md` §3 butir 5).
4. **Menulis AF tanpa membaca registry.** `[AF-99]` akan ditolak G8 — tag harus ada di
   `mod-attack-forms.md`.
