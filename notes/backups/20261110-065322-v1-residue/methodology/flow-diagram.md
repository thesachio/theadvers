# FLOW-DIAGRAM — Peta Visual Siklus Vertikal, Rolling Batch, & Anti-Kompresi (theadvers v2.0)

Dokumen ini memvisualisasikan empat pilar mekanis dari arsitektur theadvers v2.0 yang bersifat Universal (Lintas Bahasa & Runtime):
1. Alur Makro Eksekusi Vertikal per Wilayah (sc-autopilot dari STAGE-0 hingga FINAL-SWEEP).
2. Aliran Kandidat di Wadah Kanonik (04 s/d 09) & Mekanisme *Rolling Batch* (<= 5 [ACTIVE]).
3. Protokol Anti-Kompresi Konteks (--context-packet, @SLICE:STAGE-*, dan Isolasi Subagent).
4. Arsitektur *Drop-in Plugin* (1 File = 1 Item) & Sinkronisasi Otomatis _ROUTER.md.

---

## 1. Diagram Alur Makro: sc-autopilot & Siklus Vertikal per Wilayah (A–F)

Audit dilarang memproses seluruh repositori secara horizontal sekaligus. Setelah STAGE-0 memetakan 100% berkas sumber dalam *scope*, eksekusi berjalan vertikal menyelesaikan satu Wilayah Uang (R_i) dari Tahap A sampai Tahap F sebelum berpindah ke wilayah berikutnya (R_{i+1}).

flowchart TD
    Start(["MULAI AUDIT / sc-autopilot"]) --> Stage0["STAGE-0: Global Partitioning (L-PART)<br/>1. Rekonsiliasi 100% Berkas Scope di path-map.md<br/>2. Klasifikasi Tier 1 (Asset), Tier 2 (Valuation/Control/Latent), Tier 3 (Peripheral)<br/>3. Kunci Tier 3 1-Pass [LOCKED-TIER3]<br/>4. Bentuk Antrean Wilayah R_1..R_N di STATE.md berdasarkan EV (SOUL.md §3)"]
    Stage0 --> Gate0{"Gate 0 Lulus?<br/>(--gate 0)"}
    Gate0 -- "Gagal" --> Stage0
    Gate0 -- "Lulus" --> PickRegion{"Masih ada Wilayah R_i<br/>berstatus [OPEN] di STATE.md?"}

    subgraph VerticalLoop ["Siklus Vertikal Wilayah Aktif R_i (Fresh Context Window)"]
        direction TB
        StageA["STAGE-A: Region Value & Facts (L-VALUE)<br/>- Petakan Current Balance + Intended Capacity di path-map.md<br/>- Ekstrak Fakta Verbatim (Path/File.ext:Lxx-Lyy) + Prerequisite Inversion Hint ke FACTS.md<br/>- Kunci: verify_segitiga.py --gate A"]
        StageB["STAGE-B: Region Path & 3-Edge (L-PATH)<br/>- Petakan [EDGE-ASSET], [EDGE-VALUATION], [EDGE-CONTROL/LATENT] di path-map.md<br/>- Tandai titik potong lintas-wilayah<br/>- Kunci: verify_segitiga.py --gate B"]
        StageC1["STAGE-C1: Gelombang 1 — Blind Adversarial Hunt<br/>- TANPA membuka _ROUTER.md / file plugin<br/>- Jalur aman -> 04-code-guarded.md<br/>- Anomali awal -> 05-raw-leads.md [WAVE-1-BLIND]<br/>- Sinyal lintas-modul -> RADAR.md [TOUCHES: Modul.simbol]<br/>- Kunci: verify_segitiga.py --gate C1"]
        StageC2["STAGE-C2: Gelombang 2 — Cross-Pollination & Queueing<br/>- Adu Inversi FACTS.md + Rantai RADAR.md + Lazy-Load _ROUTER.md<br/>- Gugur awal -> 04-code-guarded.md<br/>- Semua kandidat lolos Segitiga -> Tabel [QUEUED] di 05-raw-leads.md (Tanpa Plafon Total, Urut EV P1-P5)<br/>- Kunci: verify_segitiga.py --gate C2"]
        BatchPull["Tarik Rolling Batch ke Meja Operasi<br/>Ambil maks 5 kandidat [QUEUED] EV tertinggi -> Ubah jadi [ACTIVE] di 05-raw-leads.md"]
        StageD["STAGE-D: Prove Batch Aktif (L-PROVE)<br/>- Load plugin M-xxx & AF-xx spesifik kandidat [ACTIVE]<br/>- Bangun 3 Titik Bukti Segitiga (Jejak Kode :Lxx + Eksekusi Test/Matematika Konkret + Delta Nilai)<br/>- Kunci: verify_segitiga.py --gate D"]
        StageE["STAGE-E: Verdict Batch Aktif (L-VERDICT)<br/>- Adili semua [ACTIVE] ke 06 / 07 / 08 / 09 hingga [ACTIVE] == 0<br/>- Kunci: verify_segitiga.py --gate E"]
        CheckQueue{"Masih ada [QUEUED] > 0<br/>untuk Wilayah R_i?"}
        StageF["STAGE-F: Incremental Disclosure & Close Region<br/>- Tulis Submission-Ready Report di 09-confirmed-findings.md untuk semua temuan R_i<br/>- Kunci: verify_segitiga.py --close-region R_i<br/>- Tandai R_i = [CLOSED] di STATE.md & Lakukan Hard Context Flush"]

        StageA --> StageB --> StageC1 --> StageC2 --> BatchPull --> StageD --> StageE --> CheckQueue
        CheckQueue -- "Ya (Ambil Batch <= 5 berikutnya)" --> BatchPull
        CheckQueue -- "Tidak ([QUEUED]==0 & [ACTIVE]==0)" --> StageF
    end

    PickRegion -- "Ya (Aktifkan R_i dengan EV tertinggi)" --> StageA
    StageF --> PickRegion
    PickRegion -- "Tidak (Semua R_1..R_N == [CLOSED])" --> FinalSweep["FINAL-SWEEP: Cross-Region Chain Verification<br/>- Periksa seluruh sinyal [TOUCHES: ...] di RADAR.md lintas R_1..R_N<br/>- Uji rantai lintas-wilayah baru bila ada (Batch D -> E -> F)<br/>- Kunci Akhir: verify_segitiga.py --final"]
    FinalSweep --> Finish(["AUDIT SELESAI 100%"])

---

## 2. Diagram Aliran Kandidat & Wadah Kanonik (04 s/d 09) dengan Sistem *Rolling Batch*

Diagram ini menunjukkan mengapa tidak ada satu pun bug valid yang terbuang karena batas kuota, sekaligus mengapa memori agen tidak pernah sesak di Tahap D:
- Di 05-raw-leads.md, tabel `[QUEUED]` bersifat tanpa plafon total (menampung berapa pun kandidat yang lolos saringan kualitas Segitiga).
- Namun meja operasi `[ACTIVE-BATCH]` dibatasi keras maksimal 5 kandidat `[ACTIVE]` per siklus pembuktian D -> E.

flowchart LR
    subgraph Hunt ["Tahap C (L-HUNT di Wilayah R_i)"]
        C1["C1: Blind Hunt<br/>(Observasi Murni)"]
        C2["C2: Cross-Pollination<br/>(Inversi FACTS + Rantai RADAR + _ROUTER.md)"]
        C1 --> C2
    end

    C1 -- "Sudah dijaga require/assert/constraint" --> W04["04-code-guarded.md<br/>(Jalur Terjaga Kode + Bukti :Lxx)"]
    C2 -- "Terpatahkan FACTS.md / Penjaga Kode" --> W04

    subgraph RawLeads ["05-raw-leads.md (Pusat Antrean & Meja Operasi Wilayah R_i)"]
        Queue["Tabel [QUEUED]<br/>- Kapasitas: TANPA PLAFON TOTAL<br/>- Syarat: Lolos Segitiga + Punya M-xxx & AF-xx<br/>- Urutan: Prioritas EV (P1 -> P5)"]
        Active["Blok [ACTIVE-BATCH]<br/>- Kapasitas: MAKSIMAL 5 [ACTIVE] per Batch<br/>- Fokus Pembuktian Tahap D"]
        Queue -- "Tarik maks 5 kandidat<br/>EV tertinggi per putaran" --> Active
    end

    C2 -- "Lolos Saringan Kualitas Segitiga" --> Queue

    Active --> Prove["Tahap D (L-PROVE)<br/>Uji 3 Titik Bukti Segitiga:<br/>1. Jejak Kode Eksak (:Lxx)<br/>2. PoC Test Runner / Hitungan Konkret<br/>3. Delta Nilai / Invariant Pecah"]

    Prove --> Verdict{"Tahap E (L-VERDICT)<br/>Pengadilan Bukti<br/>(templates/VERDICT.md)"}

    Verdict -- "PoC gagal / Terbantahkan saat uji" --> W06["06-refuted-invalid.md<br/>(Kandidat Gugur + Bukti Gagal :Lxx)"]
    Verdict -- "Butuh cek state live / komponen eksternal" --> W07["07-needs-next-step.md<br/>(Butuh Tindak Lanjut)"]
    Verdict -- "Teknis valid tapi Out-of-Scope / Known / Admin" --> W08["08-valid-not-eligible.md<br/>(Valid Tak Memenuhi Syarat Klaim)"]
    Verdict -- "Lulus 3 Titik Bukti Segitiga Utuh" --> W09["09-confirmed-findings.md<br/>(Temuan Sahih Terkonfirmasi)"]

    W09 --> StageF["Tahap F (L-DISCLOSURE Wilayah R_i)<br/>Lengkapi blok Submission-Ready Report<br/>selagi konteks R_i masih 100% segar"]

---

## 3. Diagram Protokol Anti-Kompresi Konteks (*JIT Context Re-Hydration & Subagent Staging*)

Untuk mengatasi penyakit agen AI yang sering mengompres riwayat percakapan (*auto-compaction amnesia*) atau melupakan aturan methodology/METHODOLOGY-SEGITIGA.md di tengah sesi panjang, setiap awal tahap wajib menjalankan --context-packet.
sequenceDiagram
    autonumber
    participant Orch as Parent Orchestrator / sc-autopilot
    participant Disk as Disk Workspace (STATE, FACTS, RADAR, 04..09)
    participant Script as tools/verify_segitiga.py
    participant Method as methodology/METHODOLOGY-SEGITIGA.md
    participant Sub as Subagent (Fresh Context Window)

    Orch->>Disk: 1. Write-Ahead Checkpoint ke STATE.md (Set Region R_i, Stage, Batch)
    Orch->>Script: 2. Jalankan: verify_segitiga.py --context-packet <audit-dir>
    Script->>Disk: 3. Baca posisi aktif dari STATE.md + Fakta R_i (FACTS.md) + Sinyal [TOUCHES] (RADAR.md)
    Script->>Method: 4. Ekstrak blok aturan aktif (<!-- @SLICE:STAGE-X -->)
    Script-->>Orch: 5. Cetak Paket Konteks Segar ke baris paling bawah terminal agen

    alt Eksekusi via Subagent Terisolasi
        Orch->>Sub: 6. Kirim Prompt + Suntikkan Output --context-packet secara verbatim
        Sub->>Sub: 7. Bedah berkas sumber Wilayah R_i (Tanpa polusi memori wilayah lama)
        Sub->>Disk: 8. Tulis ke notes/staging-<region>-<stage>-<item>.md (Diawali ## STAGING MANIFEST <= 16 baris)
        Orch->>Disk: 9. Baca & verifikasi file staging, lalu gabungkan (merge) ke berkas utama (FACTS/RADAR/04..09)
    else Eksekusi Langsung oleh Orchestrator
        Orch->>Disk: 6b. Tulis hasil berjangkar verbatim (Path/File.ext:Lxx-Lyy) ke berkas utama
    end

    Orch->>Script: 10. Jalankan: verify_segitiga.py --gate <stage> <audit-dir>
    Script->>Disk: 11. Cek kelengkapan syarat tahap + Deteksi Token Kompresi Terlarang (..., dll, dst, etc, rest of logic)
    Script-->>Orch: 12. Status PASS (Lanjut tahap berikutnya) atau FAIL (Perbaiki catatan)

---

## 4. Diagram Arsitektur *Drop-in Plugin* (1 File = 1 Item) & Lazy-Loading _ROUTER.md

Menambah atau merevisi metode bedah (misal M-011), bentuk serangan (AF-11), domain (DOM-xx), sudut pandang (POV-xx), atau pola rantai (CHAIN-xx) hanya memerlukan perubahan pada 1 berkas mandiri.

flowchart TD
    subgraph PluginFolders ["Lima Folder Drop-in Plugin (1 File = 1 Item Mandiri)"]
        M["references/methods/<br/>M-001..M-xxx.md"]
        AF["methodology/attack-forms/<br/>AF-01..AF-xx.md"]
        DOM["methodology/domains/<br/>DOM-*.md"]
        POV["references/pov/<br/>POV-*.md"]
        CHAIN["references/chains/<br/>CHAIN-*.md"]
    end

    Header["Kontrak Header 4-Baris Wajib di Tiap File:<br/>1. # [ID] Nama Plugin<br/>2. - **Classes**: ...<br/>3. - **Trigger Symptom**: ...<br/>4. - **Paired Items**: ..."] --> PluginFolders

    PluginFolders --> Sync["python3 tools/verify_segitiga.py --sync<br/>(Memindai header 4-baris & memvalidasi format)"]

    Sync --> Routers["5 Berkas Indeks Otomatis (_ROUTER.md):<br/>- references/methods/_ROUTER.md<br/>- methodology/attack-forms/_ROUTER.md<br/>- methodology/domains/_ROUTER.md<br/>- references/pov/_ROUTER.md<br/>- references/chains/_ROUTER.md"]

    Routers -- "Disuntikkan otomatis saat STAGE-C2" --> Wave2["Tahap C2 (Cross-Pollination Wilayah R_i)<br/>Agen hanya membaca tabel ringkas _ROUTER.md<br/>dan mencocokkan kolom Trigger Symptom"]

    Wave2 -- "Lazy-Load (read_file hanya 2-3 plugin yang cocok)" --> Selected["File Plugin Spesifik yang Terpilih<br/>(Misal M-003 + AF-04 untuk Kandidat di R_i)"]
    Selected --> StageD["Digunakan secara fokus pada Tahap D (Prove Batch Aktif)<br/>tanpa membanjiri context window"]

---

## 5. Tabel Ringkasan Transisi Status & Gerbang Penegak
| Tahap Aktif | Blok Slice yang Di-load | Berkas Utama yang Diubah | Perintah Kunci Gate | Kondisi Wajib Sebelum Pindah |
| :--- | :--- | :--- | :--- | :--- |
| `STAGE-0` | @SLICE:STAGE-0 | path-map.md, STATE.md | --gate 0 | 100% berkas sumber masuk Tier 1/2/3, Tier 3 [LOCKED-TIER3], antrean R_1..R_N berstatus [OPEN]. |
| `STAGE-A` | @SLICE:STAGE-A | path-map.md, FACTS.md | --gate A | Seluruh modul R_i punya Current Balance + Intended Capacity dan fakta verbatim :Lxx + inversi. |
| `STAGE-B` | @SLICE:STAGE-B | path-map.md | --gate B | Blok R_i memiliki ketiga jalur: [EDGE-ASSET], [EDGE-VALUATION], dan [EDGE-CONTROL/LATENT]. |
| `STAGE-C1` | @SLICE:STAGE-C1 | 04-code-guarded.md, 05-raw-leads.md, RADAR.md | --gate C1 | Observasi buta tercatat tanpa membuka plugin; sinyal lintas-modul memiliki tag [TOUCHES: ...]. |
| `STAGE-C2` | @SLICE:STAGE-C2 | 04-code-guarded.md, 05-raw-leads.md | --gate C2 | Penyilangan selesai; seluruh kandidat lolos Segitiga masuk tabel [QUEUED] dengan EV + M-xxx & AF-xx. |
| `STAGE-D` | @SLICE:STAGE-D | 05-raw-leads.md | --gate D | Maksimal 5 kandidat [ACTIVE] memiliki 3 titik Bukti Segitiga lengkap tanpa token kompresi. |
| `STAGE-E` | @SLICE:STAGE-E | 05, 06, 07, 08, 09 | --gate E | Seluruh kandidat batch dipindahkan ke 06/07/08/09 hingga [ACTIVE] == 0. Jika [QUEUED] > 0, ulangi ke STAGE-D. |
| `STAGE-F` | @SLICE:STAGE-F | 09-confirmed-findings.md, STATE.md | --close-region R_i | [ACTIVE] == 0 & [QUEUED] == 0 untuk R_i; seluruh temuan R_i di 09 sudah *Submission-Ready*; R_i = [CLOSED]. |
| `FINAL-SWEEP` | @SLICE:FINAL-SWEEP | RADAR.md, 05..09, STATE.md | --final | Semua R_1..R_N == [CLOSED], rantai lintas-wilayah teruji, bebas token kompresi di seluruh berkas. |
