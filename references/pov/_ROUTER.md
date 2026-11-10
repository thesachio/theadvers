# _ROUTER — Indeks Otomatis Sudut Pandang Aktor Universal (`references/pov/`)

> **ATURAN LAZY-LOADING (`STAGE-C2` & `STAGE-D`)**:
> 1. Berkas ini di-generate secara otomatis oleh `python3 tools/verify_segitiga.py --sync` dari 4 baris header setiap berkas `POV-*.md` di dalam folder `references/pov/`.
> 2. **Dilarang membuka seluruh berkas `POV-*` sekaligus**. Cocokkan kolom **Trigger Symptom** dengan gejala kode di Wilayah Aktif `R_i`, lalu panggil `read_file` hanya pada berkas plugin yang relevan.
> 3. Untuk menambah item baru, cukup buat 1 berkas `references/pov/POV-<slug>.md` dengan 4 baris header standar lalu jalankan `python3 tools/verify_segitiga.py --sync`.

| ID | Nama Plugin & Berkas (`references/pov/`) | Classes | Trigger Symptom *(Kapan Wajib Di-load?)* | Paired Items |
| :--- | :--- | :--- | :--- | :--- |
| **`POV-griefer`** | `POV-griefer.md`<br/>Sudut Pandang: Penyabotase Asimetris Bermodal Debu (*Low-Cost Griefer*) | GRIEFING, ASYMMETRIC-DOS, QUEUE-BLOCKER, BRICKING | Terdapat antrean bersama, pemrosesan batch, batas kuota global, *cooldown timer*, atau syarat kesetaraan saldo yang dapat diganggu pihak ketiga. | M-009, AF-09, DOM-staking, DOM-governance-control |
| **`POV-liquidator`** | `POV-liquidator.md`<br/>Sudut Pandang: Likuidator, Arbitrase Lelang, & Pemburu Insentif Penyitaan | LIQUIDATOR, AUCTION-BIDDER, SELF-LIQUIDATION, BAD-DEBT | Terdapat jalur likuidasi, lelang agunan, klaim bonus penalti, atau penutupan paksa posisi tidak sehat. | M-004, M-006, AF-06, DOM-lending |
| **`POV-malicious-integrator`** | `POV-malicious-integrator.md`<br/>Sudut Pandang: Kontrak/Token/Akun Pihak Ketiga Berbahaya & Callback Penjebak | MALICIOUS-TOKEN, HOOK-TRAP, SPOOFED-ACCOUNT, EXTERNAL-CALLBACK | Modul berinteraksi dengan token/aset/kontrak/akun/objek yang disuplai pengguna atau melakukan panggilan keluar (*external call*/CPI). | M-003, M-005, AF-04, AF-07 |
| **`POV-relayer-mev`** | `POV-relayer-mev.md`<br/>Sudut Pandang: Eksekutor Urutan Transaksi (MEV), Relayer, Keeper, & Solver | MEV-SEARCHER, RELAYER, KEEPER, ORDERING, INTENT-SOLVER | Hasil eksekusi bergantung pada urutan transaksi dalam blok, parameter *slippage/deadline*, tanda tangan pengguna, atau kiriman data relayer/keeper. | M-008, AF-05, AF-08, AF-10, DOM-bridge-offchain |
| **`POV-unprivileged`** | `POV-unprivileged.md`<br/>Sudut Pandang: Penyerang Eksternal Tanpa Izin & Modal Pinjaman Kilat | EXTERNAL-ATTACKER, FLASH-CAPITAL, PERMISSIONLESS | Terdapat fungsi publik/eksternal tanpa penjaga otoritas pada [EDGE-ASSET], [EDGE-VALUATION], atau [EDGE-CONTROL/LATENT]. | M-001, M-005, AF-01, AF-07 |
