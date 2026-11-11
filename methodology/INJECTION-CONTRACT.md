# INJECTION CONTRACT — Apa yang WAJIB Benar-Benar Tersuntik ke Konteks Agen

> Dokumen ini mengikat `tools/verify_segitiga.py --context-packet`. Tujuannya satu:
> **informasi yang sudah ditulis di disk harus benar-benar masuk ke konteks agen** —
> bukan sekadar ada di dokumen lalu disebut namanya saja (*masking*).

---

## 1. Definisi

| Istilah | Arti |
| :--- | :--- |
| **Tersuntik** | Isi nyata (baris fakta, path berkas, kutipan bekal) tercetak oleh `--context-packet` pada tahap yang tepat, dan dapat dibaca agen tanpa menebak. |
| **Masking** | Paket konteks hanya menyebut *nama* (mis. "Baca M-001, AF-01") tanpa path nyata, tanpa isi bekal, tanpa baris fakta — sehingga agen harus menebak atau melewatkannya. |
| **Label palsu** | ID plugin yang ditulis di kandidat/kartu tetapi tidak menunjuk berkas yang ada (mis. `M-999`). Ini masking tingkat gate. |

**Aturan keras:** label yang tidak menunjuk berkas nyata = DITOLAK gate. `[NO-CATALOG]` sah bila katalog memang tidak punya gejala yang cocok.

---

## 2. Matriks Kontrak per Tahap

| Tahap | WAJIB tersuntik | Sumber | Penegak mekanis |
| :--- | :--- | :--- | :--- |
| `STAGE-0` | potongan `@SLICE:STAGE-0` + kursor STATE | METHODOLOGY + STATE | `--gate 0` |
| `STAGE-A` | slice A + daftar berkas Wilayah R_i | METHODOLOGY + path-map | `--gate A` |
| `STAGE-B` | slice B + peta 3-Edge R_i | METHODOLOGY + path-map | `--gate B` |
| `STAGE-C1` | slice C1 + **PERINGATAN BLIND**; `_ROUTER` **DILARANG** muncul | METHODOLOGY | `--gate C1` (output) + pemeriksaan paket |
| `STAGE-C2` | slice C2 + baris **FACTS R_i** (dengan penanda bila dipotong) + sinyal **RADAR** + **baris tabrakan `[TOUCHES]`** (bahan CPAIR) + **5 tabel `_ROUTER`** (ID/AF/POV/CHAIN + Trigger Symptom + Paired Items) + **instruksi perakitan C2→D** | FACTS, RADAR, 5 router | `--gate C2` (label resolve) |
| `STAGE-D` | slice D + per kartu `[ACTIVE]`: `Batch ID`, `TARGET_OBJEK`, `MODE_UJI_POC`, `Fork PoC`, **blok Bekal Uji utuh**, **path berkas plugin asli**, **baris fakta `F-R`**, **baris radar `CPAIR`**, **JEJAK C2** (baris `[QUEUED]` asal + peringatan bila token C2 hilang dari bekal) | `05` §3 + FACTS + RADAR + repo plugin | `--gate D` (bekal + resolve) |
| `STAGE-E` | slice E + hukum acara wadah | METHODOLOGY + VERDICT | `--gate E` |
| `STAGE-F` | slice F + daftar temuan R_i + kewajiban `cases/<ID>/` | 09 + templates/case | `--close-region` |
| `FINAL-SWEEP` | slice FINAL-SWEEP + 5 tabel `_ROUTER` | METHODOLOGY + router | `--final` |

---

## 3. Anti-Masking: Empat Uji yang Ditegakkan

1. **Bekal wajib ada di kartu `[ACTIVE]`.** `--gate D` menolak kartu tanpa baris `Bekal Uji` — karena tanpa blok itu, paket konteks tidak punya apa pun untuk disuntikkan.
2. **Setiap label wajib menunjuk berkas nyata.** `M-xxx` / `AF-xx` / `POV-*` / `CHAIN-*` / `DOM-*` di baris `[QUEUED]` maupun kartu `[ACTIVE]` di-resolusi ke path asli; yang tidak ditemukan = FAIL. `[NO-CATALOG]` dikecualikan.
3. **Paket mencetak ringkasan suntikan.** Di akhir `STAGE-D`, paket menghitung: kartu aktif, bekal tersuntik, plugin path ter-resolve, baris fakta, baris radar — dan menyatakan `STATUS: OK` / `STATUS: GAGAL` agar agen/manusia bisa memverifikasi tanpa menebak.
4. **C1 tetap buta katalog.** Paket `STAGE-C1` tidak boleh memuat tabel `_ROUTER`; kolom Inversi Prasyarat ditandai sebagai bahan `STAGE-C2`.
5. **Pemotongan harus terlihat.** Bila fakta/radar melebihi batas tampil, paket mencetak `[DIPOTONG] menampilkan X dari Y` — bukan memotong diam-diam.
6. **Drift C2→D harus terlihat.** Kartu `[ACTIVE]` mencetak `JEJAK C2` dari baris `[QUEUED]` asalnya; token POV/CHAIN/DOM yang tercatat di C2 tetapi hilang dari Bekal Uji memicu peringatan (bukan kegagalan otomatis — agen boleh mengganti dengan alasan).

---

## 4. Alur Data yang Benar (C2 → D)

```
STAGE-C2  konsultasi katalog (5 _ROUTER)  →  catat hasil di kolom Method/AF
          (ID cocok, atau [NO-CATALOG])      →  tulis blok Bekal Uji di kartu saat tarik batch
                                                        │
STAGE-D   paket konteks mencetak:                       ▼
          • blok Bekal Uji (kutipan utuh)
          • path berkas plugin asli  (M/AF/POV/CHAIN/DOM)
          • baris fakta FACTS (F-R*) sebagai pagar tipe data/desimal/sentinel
          • baris RADAR ([TOUCHES]/CPAIR*) sebagai rantai lintas-modul
          → agen membangun PoC dengan bekal itu, bukan menebak.
```

**Yang dilarang:** menulis "Baca M-001 dan AF-01" tanpa path, atau mengandalkan ingatan C2 yang tidak pernah sampai ke D.
