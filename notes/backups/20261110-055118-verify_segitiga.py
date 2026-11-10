#!/usr/bin/env python3
"""
verify_segitiga.py — Mesin Penegak Mekanis, Context Re-Hydrator, & Plugin Router Sync
Arsitektur: theadvers v2.0 (Universal Language-Agnostic, Drop-in Plugin, Rolling Batch, Zero-Compression)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
METHODOLOGY_FILE = REPO_ROOT / "methodology" / "METHODOLOGY-SEGITIGA.md"
VERDICT_TEMPLATE = REPO_ROOT / "templates" / "VERDICT.md"

CANONICAL_FILES = [
    "STATE.md",
    "FACTS.md",
    "RADAR.md",
    "path-map.md",
    "04-code-guarded.md",
    "05-raw-leads.md",
    "06-refuted-invalid.md",
    "07-needs-next-step.md",
    "08-valid-not-eligible.md",
    "09-confirmed-findings.md",
]

PLUGIN_SPECS = [
    {
        "name": "Metode Bedah Universal",
        "dir": REPO_ROOT / "references" / "methods",
        "prefix": "M-",
        "router_title": "# _ROUTER — Indeks Otomatis Metode Bedah Universal (`references/methods/`)",
        "rel_dir": "references/methods/",
    },
    {
        "name": "Bentuk Serangan Uji Universal",
        "dir": REPO_ROOT / "methodology" / "attack-forms",
        "prefix": "AF-",
        "router_title": "# _ROUTER — Indeks Otomatis Bentuk Serangan Uji Universal (`methodology/attack-forms/`)",
        "rel_dir": "methodology/attack-forms/",
    },
    {
        "name": "Heuristik Domain Universal",
        "dir": REPO_ROOT / "methodology" / "domains",
        "prefix": "DOM-",
        "router_title": "# _ROUTER — Indeks Otomatis Heuristik Domain Universal (`methodology/domains/`)",
        "rel_dir": "methodology/domains/",
    },
    {
        "name": "Sudut Pandang Aktor Universal",
        "dir": REPO_ROOT / "references" / "pov",
        "prefix": "POV-",
        "router_title": "# _ROUTER — Indeks Otomatis Sudut Pandang Aktor Universal (`references/pov/`)",
        "rel_dir": "references/pov/",
    },
    {
        "name": "Pola Serangan Berantai Universal",
        "dir": REPO_ROOT / "references" / "chains",
        "prefix": "CHAIN-",
        "router_title": "# _ROUTER — Indeks Otomatis Pola Serangan Berantai Universal (`references/chains/`)",
        "rel_dir": "references/chains/",
    },
]

FORBIDDEN_COMPRESSION_PATTERNS = [
    (r"(?<!\.)\.\.\.(?!\.)", "elipsis pemotongan malas ('...')"),
    (r"\bdll\.", "singkatan kompresi malas ('dll.')"),
    (r"\bdst\.", "singkatan kompresi malas ('dst.')"),
    (r"\betc\.", "singkatan kompresi malas ('etc.')"),
    (r"\band so on\b", "frasa kompresi malas ('and so on')"),
    (r"\brest of logic\b", "frasa kompresi malas ('rest of logic')"),
    (r"\brest of code\b", "frasa kompresi malas ('rest of code')"),
    (r"\bdan seterusnya\b", "frasa kompresi malas ('dan seterusnya')"),
]

ANCHOR_REGEX = re.compile(r"[A-Za-z0-9_./\-]+\.[A-Za-z0-9_]+:L\d+")
HEADER_ID_REGEX = re.compile(r"^#\s+\[([A-Za-z0-9\-]+)\]\s+(.+)$")
META_LINE_REGEX = re.compile(r"^-\s+\*\*(Classes|Trigger Symptom|Paired Items)\*\*:\s*(.+)$")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def strip_template_boilerplate(text: str) -> str:
    """Mengabaikan baris blockquote instruksi template (> ...) dan komentar contoh."""
    cleaned_lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(">") or s.startswith("*Diisi pada") or s.startswith("*Gandakan") or s.startswith("*Salin"):
            continue
        if "[ISI_" in s or "[Contoh:" in s or "[Nama " in s or "[Path/File" in s or "[Jelaskan" in s:
            continue
        if "[TEMPLATE-CONTOH" in s:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def check_zero_compression(file_path: Path) -> List[str]:
    """Mendeteksi token kompresi malas pada baris konten nyata (di luar instruksi template)."""
    errors: List[str] = []
    if not file_path.exists():
        return [f"Berkas tidak ditemukan: {file_path.name}"]

    raw_lines = file_path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(raw_lines, start=1):
        s = line.strip()
        if not s or s.startswith(">") or s.startswith("#") or s.startswith("*"):
            continue
        if "[Contoh:" in s or "[Path/File" in s or "[TEMPLATE-CONTOH" in s or "--match-test" in s:
            continue
        if "Dilarang" in s or "token kompresi" in s or "FORBIDDEN" in s:
            continue

        for pattern, label in FORBIDDEN_COMPRESSION_PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE):
                errors.append(
                    f"[{file_path.name}:L{idx}] Terdeteksi {label} yang melanggar Zero-Compression Law: '{s[:90]}'"
                )
    return errors


# ============================================================================
# 1. FITUR --sync: PEMINDAIAN HEADER 4-BARIS & PEMBANGUNAN OTOMATIS _ROUTER.md
# ============================================================================

def parse_plugin_header(file_path: Path) -> Tuple[Optional[Dict[str, str]], List[str]]:
    lines = [ln.strip() for ln in file_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) < 4:
        return None, [f"[{file_path.name}] Kurang dari 4 baris header metadata wajib."]

    m_title = HEADER_ID_REGEX.match(lines[0])
    if not m_title:
        return None, [
            f"[{file_path.name}:L1] Baris 1 wajib berformat '# [ID-PLUGIN] Judul', ditemukan: '{lines[0]}'"
        ]

    plugin_id, title = m_title.group(1).strip(), m_title.group(2).strip()
    meta: Dict[str, str] = {"id": plugin_id, "title": title, "file": file_path.name}
    expected_keys = ["Classes", "Trigger Symptom", "Paired Items"]
    errors: List[str] = []

    for idx, key in enumerate(expected_keys, start=1):
        line = lines[idx]
        m_meta = META_LINE_REGEX.match(line)
        if not m_meta or m_meta.group(1) != key:
            errors.append(
                f"[{file_path.name}:L{idx+1}] Baris {idx+1} wajib diawali '- **{key}**: ...', ditemukan: '{line}'"
            )
        else:
            meta[key] = m_meta.group(2).strip()

    if errors:
        return None, errors
    return meta, []


def sync_all_routers() -> int:
    all_errors: List[str] = []
    synced_count = 0

    for spec in PLUGIN_SPECS:
        folder: Path = spec["dir"]
        prefix: str = spec["prefix"]
        if not folder.exists():
            all_errors.append(f"Direktori plugin tidak ditemukan: {folder}")
            continue

        plugin_files = sorted(
            [p for p in folder.glob(f"{prefix}*.md") if p.name != "_ROUTER.md"]
        )
        parsed_items: List[Dict[str, str]] = []

        for pf in plugin_files:
            meta, errs = parse_plugin_header(pf)
            if errs:
                all_errors.extend(errs)
            elif meta:
                parsed_items.append(meta)

        if any(e for e in all_errors if folder.name in e):
            continue

        router_path = folder / "_ROUTER.md"
        rows = []
        for item in parsed_items:
            rows.append(
                f"| **`{item['id']}`** | `{item['file']}`<br/>{item['title']} | "
                f"{item['Classes']} | {item['Trigger Symptom']} | {item['Paired Items']} |"
            )

        router_content = (
            f"{spec['router_title']}\n\n"
            f"> **ATURAN LAZY-LOADING (`STAGE-C2` & `STAGE-D`)**:\n"
            f"> 1. Berkas ini di-generate secara otomatis oleh `python3 tools/verify_segitiga.py --sync` "
            f"dari 4 baris header setiap berkas `{prefix}*.md` di dalam folder `{spec['rel_dir']}`.\n"
            f"> 2. **Dilarang membuka seluruh berkas `{prefix}*` sekaligus**. Cocokkan kolom **Trigger Symptom** "
            f"dengan gejala kode di Wilayah Aktif `R_i`, lalu panggil `read_file` hanya pada berkas plugin yang relevan.\n"
            f"> 3. Untuk menambah item baru, cukup buat 1 berkas `{spec['rel_dir']}{prefix}<slug>.md` "
            f"dengan 4 baris header standar lalu jalankan `python3 tools/verify_segitiga.py --sync`.\n\n"
            f"| ID | Nama Plugin & Berkas (`{spec['rel_dir']}`) | Classes | Trigger Symptom *(Kapan Wajib Di-load?)* | Paired Items |\n"
            f"| :--- | :--- | :--- | :--- | :--- |\n"
            + "\n".join(rows)
            + "\n"
        )
        router_path.write_text(router_content, encoding="utf-8")
        synced_count += 1
        print(f"[SYNC-OK] {router_path.relative_to(REPO_ROOT)} ({len(parsed_items)} plugin terindeks)")

    if all_errors:
        print("\n[SYNC-FAIL] Ditemukan kesalahan header plugin:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\n[PASS] Seluruh {synced_count} berkas _ROUTER.md berhasil disinkronkan.")
    return 0


# ============================================================================
# 2. PARSER STATE.md & EKSTRAKTOR @SLICE DARI METHODOLOGY-SEGITIGA.md
# ============================================================================

def parse_state_cursor(state_text: str) -> Dict[str, str]:
    cursor: Dict[str, str] = {
        "Active Region": "NONE",
        "Current Stage": "STAGE-0",
        "Current Batch": "0",
        "Queued Leads Count (Active Region)": "0",
        "Active Leads Count (Active Batch)": "0",
        "Last Passed Gate": "NONE",
        "Next Exact Action": "",
    }
    for line in state_text.splitlines():
        m = re.match(r"^-\s+\*\*(.+?)\*\*:\s*`?([^`*\n]+)`?", line.strip())
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            cursor[key] = val
    return cursor


def parse_region_queue(state_text: str) -> List[Dict[str, str]]:
    regions: List[Dict[str, str]] = []
    in_table = False
    for line in state_text.splitlines():
        s = line.strip()
        if s.startswith("| Region ID"):
            in_table = True
            continue
        if in_table:
            if not s.startswith("|"):
                break
            if ":---" in s:
                continue
            cols = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cols) >= 5 and re.match(r"^R_\d+$", cols[0]):
                regions.append(
                    {
                        "id": cols[0],
                        "name": cols[1],
                        "ev": cols[2],
                        "files": cols[3],
                        "status": cols[4],
                    }
                )
    return regions


def extract_methodology_slice(stage: str) -> str:
    text = read_text(METHODOLOGY_FILE)
    if not text:
        return f"[PERINGATAN] {METHODOLOGY_FILE} tidak ditemukan."

    slice_key = stage.upper()
    if not slice_key.startswith("STAGE-") and slice_key != "FINAL-SWEEP":
        slice_key = f"STAGE-{slice_key}"

    pattern = re.compile(
        rf"<!--\s*@SLICE:{re.escape(slice_key)}:START\s*-->(.*?)<!--\s*@SLICE:{re.escape(slice_key)}:END\s*-->",
        re.DOTALL,
    )
    m = pattern.search(text)
    if m:
        return m.group(1).strip()
    return f"[INFO] Slice untuk {slice_key} tidak ditemukan; pastikan Current Stage bernilai STAGE-0..STAGE-F atau FINAL-SWEEP."


def extract_region_facts(facts_text: str, region: str) -> List[str]:
    matches = []
    for line in facts_text.splitlines():
        s = line.strip()
        if s.startswith("|") and f"`{region}`" in s or re.search(rf"\|\s*{re.escape(region)}\s*\|", s):
            if "[Path/File" not in s and "[Tulis " not in s:
                matches.append(s)
    return matches


def extract_radar_signals(radar_text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    rows = []
    touches_map: Dict[str, List[str]] = {}
    for line in radar_text.splitlines():
        s = line.strip()
        if s.startswith("|") and "[TOUCHES:" in s and "[Path/File" not in s:
            rows.append(s)
            for t in re.findall(r"\[TOUCHES:\s*([^\]]+)\]", s):
                t_clean = t.strip()
                touches_map.setdefault(t_clean, []).append(s)
    return rows, touches_map


def parse_leads_table_and_cards(raw_leads_text: str, region: Optional[str] = None) -> Tuple[List[Dict[str, str]], List[str]]:
    """Mengembalikan (daftar baris tabel antrean di Bagian 2, daftar blok kartu [ACTIVE] di Bagian 3)."""
    queued_rows: List[Dict[str, str]] = []
    in_queue_table = False

    for line in raw_leads_text.splitlines():
        s = line.strip()
        if s.startswith("| Lead ID"):
            in_queue_table = True
            continue
        if in_queue_table:
            if not s.startswith("|"):
                if s.startswith("## 3."):
                    in_queue_table = False
                continue
            if ":---" in s or "[Path/File" in s or "[Jelaskan" in s:
                continue
            cols = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cols) >= 10:
                row_region = cols[1]
                if region is None or row_region == region:
                    queued_rows.append(
                        {
                            "id": cols[0],
                            "region": row_region,
                            "ev": cols[2],
                            "anchor": cols[3],
                            "target": cols[4],
                            "summary": cols[5],
                            "method": cols[6],
                            "af": cols[7],
                            "extra": cols[8],
                            "status": cols[9],
                        }
                    )

    # Ekstrak kartu di Bagian 3 yang benar-benar berstatus [ACTIVE]
    active_cards: List[str] = []
    sec3_split = re.split(r"^##\s+3\.\s+BLOK MEJA OPERASI", raw_leads_text, flags=re.MULTILINE)
    if len(sec3_split) > 1:
        sec3 = sec3_split[1]
        card_chunks = re.split(r"^###\s+", sec3, flags=re.MULTILINE)
        for chunk in card_chunks[1:]:
            if "[TEMPLATE-CONTOH" in chunk:
                continue
            if re.search(r"Status Saat Ini\*\*:\s*`?\[ACTIVE\]`?", chunk):
                if region is None or re.search(rf"Region\s*&\s*EV\s*Rank\*\*:\s*`?{re.escape(region)}\b", chunk):
                    active_cards.append("### " + chunk.strip())

    return queued_rows, active_cards


# ============================================================================
# 3. FITUR --context-packet: SUNTIKAN PAKET KONTEKS SEGAR KE TERMINAL AGEN
# ============================================================================

def print_context_packet(audit_dir: Path, override_region: Optional[str] = None) -> int:
    state_path = audit_dir / "STATE.md"
    if not state_path.exists():
        print(f"[ERROR] STATE.md tidak ditemukan di {audit_dir}", file=sys.stderr)
        return 1

    state_text = read_text(state_path)
    cursor = parse_state_cursor(state_text)
    regions = parse_region_queue(state_text)

    active_region = override_region or cursor.get("Active Region", "NONE")
    current_stage = cursor.get("Current Stage", "STAGE-0")

    raw_leads_text = read_text(audit_dir / "05-raw-leads.md")
    q_rows, active_cards = parse_leads_table_and_cards(
        raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
    )
    queued_now = [r for r in q_rows if "[QUEUED]" in r["status"]]

    print("=" * 88)
    print("PAKET KONTEKS SEGAR (JIT CONTEXT RE-HYDRATION PACKET) — THEADVERS v2.0")
    print("=" * 88)
    print(f"- Audit Directory           : {audit_dir}")
    print(f"- Active Region             : {active_region}")
    print(f"- Current Stage             : {current_stage}")
    print(f"- Current Batch             : {cursor.get('Current Batch', '0')}")
    print(f"- Queued Leads (Disk Count) : {len(queued_now)}")
    print(f"- Active Leads (Disk Count) : {len(active_cards)} (Batas Maksimal: 5 per Batch)")
    print(f"- Last Passed Gate          : {cursor.get('Last Passed Gate', 'NONE')}")
    print(f"- Next Exact Action         : {cursor.get('Next Exact Action', '-')}")

    if regions:
        print("\n--- STATUS ANTREAN WILAYAH UANG (R_1 .. R_N) ---")
        for r in regions:
            marker = ">> ACTIVE <<" if r["id"] == active_region else r["status"]
            print(f"  * {r['id']} ({r['ev']}) [{marker}] : {r['name']} | Berkas: {r['files']}")

    print("\n" + "=" * 88)
    print(f"ATURAN WAJIB TAHAP AKTIF ({current_stage}) DARI METHODOLOGY-SEGITIGA.md")
    print("=" * 88)
    print(extract_methodology_slice(current_stage))

    facts_text = read_text(audit_dir / "FACTS.md")
    if active_region not in ("NONE", ""):
        region_facts = extract_region_facts(facts_text, active_region)
        print("\n" + "-" * 88)
        print(f"FAKTA VERBATIM & INVERSI PRASYARAT WILAYAH {active_region} (FACTS.md): {len(region_facts)} baris")
        print("-" * 88)
        for rf in region_facts[:25]:
            print(f"  {rf}")

    radar_text = read_text(audit_dir / "RADAR.md")
    radar_rows, touches_map = extract_radar_signals(radar_text)
    collisions = {k: v for k, v in touches_map.items() if len(v) >= 2}
    print("\n" + "-" * 88)
    print(f"SINYAL RADAR LINTAS-MODUL ({len(radar_rows)} sinyal total, {len(collisions)} tabrakan [TOUCHES])")
    print("-" * 88)
    if collisions:
        print("  [!] TABRAKAN [TOUCHES] TERDETEKSI (WAJIB UJI RANTAI DI C2 / FINAL-SWEEP):")
        for sym, lines in collisions.items():
            print(f"      * [TOUCHES: {sym}] disentuh oleh {len(lines)} entri radar.")
    else:
        for rr in radar_rows[:10]:
            print(f"  {rr}")

    # Injeksi khusus per tahap
    if current_stage.upper() == "STAGE-C1":
        print("\n" + "!" * 88)
        print("PERINGATAN KERAS STAGE-C1 (BLIND ADVERSARIAL HUNT):")
        print("DILARANG MEMBUKA _ROUTER.md ATAU MEMBACA FILE PLUGIN M-xxx / AF-xx PADA TAHAP INI!")
        print("Gunakan murni L-VALUE dan L-PATH Wilayah Aktif serta catat sinyal [TOUCHES: ...] ke RADAR.md.")
        print("!" * 88)

    elif current_stage.upper() in ("STAGE-C2", "FINAL-SWEEP"):
        print("\n" + "=" * 88)
        print("INJEKSI OTOMATIS INDEKS _ROUTER.md UNTUK STAGE-C2 / FINAL-SWEEP (LAZY-LOADING)")
        print("=" * 88)
        for spec in PLUGIN_SPECS:
            router_file = spec["dir"] / "_ROUTER.md"
            if router_file.exists():
                print(f"\n### [{spec['name']}] ({spec['rel_dir']}_ROUTER.md)")
                for ln in router_file.read_text(encoding="utf-8").splitlines():
                    if ln.startswith("|"):
                        print(ln)

    elif current_stage.upper() == "STAGE-D":
        print("\n" + "=" * 88)
        print("KANDIDAT [ACTIVE] DI MEJA OPERASI & PLUGIN YANG WAJIB DI-LOAD (STAGE-D)")
        print("=" * 88)
        assigned_ids = set()
        for r in q_rows:
            if "[ACTIVE]" in r["status"]:
                print(f"  * {r['id']} ({r['ev']}) | {r['anchor']} | Method: {r['method']} | AF: {r['af']}")
                for tok in re.findall(r"\b(?:M-\d+|AF-\d+|DOM-[a-z0-9\-]+|POV-[a-z0-9\-]+|CHAIN-[a-z0-9\-]+)\b",
                                      f"{r['method']} {r['af']} {r['extra']}"):
                    assigned_ids.add(tok)
        if assigned_ids:
            print(f"\n  -> Baca berkas plugin berikut untuk membuktikan batch ini: {', '.join(sorted(assigned_ids))}")

    elif current_stage.upper() == "STAGE-E":
        print("\n" + "=" * 88)
        print(" pengingat HUKUM ACARA PENGADILAN BUKTI (templates/VERDICT.md)")
        print("=" * 88)
        print("  - Pindahkan seluruh kandidat [ACTIVE] dari 05-raw-leads.md ke:")
        print("    * 06-refuted-invalid.md   (jika PoC gagal / terbantahkan saat uji)")
        print("    * 07-needs-next-step.md   (jika butuh verifikasi state on-chain live / eksternal)")
        print("    * 08-valid-not-eligible.md (jika valid teknis namun out-of-scope / known / trusted role)")
        print("    * 09-confirmed-findings.md (jika lulus 3 Titik Bukti Segitiga utuh)")
        print("  - Setelah STAGE-E selesai, jumlah [ACTIVE] di 05-raw-leads.md WAJIB == 0.")

    print("=" * 88)
    return 0


# ============================================================================
# 4. PENEGAK GERBANG TAHAP (--gate 0|A|B|C1|C2|D|E, --close-region, --final)
# ============================================================================

def validate_gate(gate: str, audit_dir: Path, override_region: Optional[str] = None) -> int:
    gate = gate.upper().replace("STAGE-", "")
    errors: List[str] = []

    state_text = read_text(audit_dir / "STATE.md")
    cursor = parse_state_cursor(state_text)
    regions = parse_region_queue(state_text)
    active_region = override_region or cursor.get("Active Region", "NONE")

    path_map_text = read_text(audit_dir / "path-map.md")
    facts_text = read_text(audit_dir / "FACTS.md")
    radar_text = read_text(audit_dir / "RADAR.md")
    guarded_text = read_text(audit_dir / "04-code-guarded.md")
    raw_leads_text = read_text(audit_dir / "05-raw-leads.md")

    # Sabuk Anti-Kompresi selalu diperiksa pada berkas utama yang relevan
    for fname in CANONICAL_FILES:
        fpath = audit_dir / fname
        if fpath.exists():
            errors.extend(check_zero_compression(fpath))

    if gate == "0":
        # Cek Tabel Rekonsiliasi di path-map.md
        reconciled_rows = []
        tier3_rows = []
        for line in path_map_text.splitlines():
            s = line.strip()
            if s.startswith("|") and ("TIER-1" in s or "TIER-2" in s or "TIER-3" in s):
                if "[src/" in s or "[Bahasa]" in s:
                    continue
                reconciled_rows.append(s)
                if "TIER-3" in s:
                    tier3_rows.append(s)

        if not reconciled_rows:
            errors.append("[GATE-0] Tabel Rekonsiliasi 100% Berkas di path-map.md masih kosong / masih berisi contoh template.")
        for t3 in tier3_rows:
            if "[LOCKED-TIER3]" not in t3 or not ANCHOR_REGEX.search(t3):
                errors.append(f"[GATE-0] Berkas TIER-3 wajib memiliki tag [LOCKED-TIER3] dan jangkar baris ':Lxx': {t3}")

        real_regions = [r for r in regions if "[Nama " not in r["name"] and "[Path/File" not in r["files"]]
        if not real_regions:
            errors.append("[GATE-0] Tabel Antrean Wilayah Uang (R_1..R_N) di STATE.md belum diisi dengan wilayah nyata.")

    elif gate == "A":
        if active_region in ("NONE", ""):
            errors.append("[GATE-A] Active Region di STATE.md belum diset ke R_i.")
        else:
            region_facts = extract_region_facts(facts_text, active_region)
            if not region_facts:
                errors.append(f"[GATE-A] Belum ada fakta verbatim untuk Wilayah {active_region} di FACTS.md.")
            for rf in region_facts:
                if not ANCHOR_REGEX.search(rf):
                    errors.append(f"[GATE-A] Baris fakta Wilayah {active_region} di FACTS.md tidak memiliki jangkar Path/File.ext:Lxx: {rf}")
            if active_region not in strip_template_boilerplate(path_map_text):
                errors.append(f"[GATE-A] Bagian L-VALUE untuk Wilayah {active_region} belum diisi di path-map.md.")

    elif gate == "B":
        cleaned_pm = strip_template_boilerplate(path_map_text)
        for edge_tag in ("[EDGE-ASSET]", "[EDGE-VALUATION]", "[EDGE-CONTROL/LATENT]"):
            if edge_tag not in cleaned_pm:
                errors.append(f"[GATE-B] Pemetaan {edge_tag} belum ditemukan (atau masih berupa contoh template) di path-map.md.")
        for line in cleaned_pm.splitlines():
            if any(t in line for t in ("[EDGE-ASSET]", "[EDGE-VALUATION]", "[EDGE-CONTROL/LATENT]")):
                if not ANCHOR_REGEX.search(line):
                    errors.append(f"[GATE-B] Entri Edge wajib memiliki jangkar Path/File.ext:Lxx: {line.strip()}")

    elif gate == "C1":
        cleaned_guarded = strip_template_boilerplate(guarded_text)
        cleaned_leads = strip_template_boilerplate(raw_leads_text)
        has_guarded = bool(ANCHOR_REGEX.search(cleaned_guarded))
        has_wave1 = "[WAVE-1-BLIND]" in cleaned_leads and bool(ANCHOR_REGEX.search(cleaned_leads))
        if not (has_guarded or has_wave1):
            errors.append(
                f"[GATE-C1] Wilayah {active_region} belum memiliki catatan berjangkar ':Lxx' di 04-code-guarded.md maupun [WAVE-1-BLIND] di 05-raw-leads.md."
            )
        radar_rows, _ = extract_radar_signals(radar_text)
        if not radar_rows:
            errors.append("[GATE-C1] RADAR.md belum memiliki sinyal lintas-modul dengan tag [TOUCHES: NamaModul.simbol] dan jangkar ':Lxx'.")

    elif gate == "C2":
        cleaned_leads = strip_template_boilerplate(raw_leads_text)
        if "[WAVE-2-CROSS]" not in cleaned_leads:
            errors.append(f"[GATE-C2] Dokumentasi penyilangan [WAVE-2-CROSS] untuk Wilayah {active_region} belum tercatat di 05-raw-leads.md.")
        q_rows, _ = parse_leads_table_and_cards(raw_leads_text, None if active_region == "NONE" else active_region)
        for r in q_rows:
            if not ANCHOR_REGEX.search(r["anchor"]):
                errors.append(f"[GATE-C2] Kandidat {r['id']} tidak memiliki jangkar Path/File.ext:Lxx pada kolom Verbatim Anchor.")
            if not re.match(r"^P[1-5]$", r["ev"]):
                errors.append(f"[GATE-C2] Kandidat {r['id']} wajib memiliki EV Rank P1..P5 (SOUL.md §3), ditemukan: '{r['ev']}'.")
            if not re.search(r"\bM-\d{3}\b", r["method"]):
                errors.append(f"[GATE-C2] Kandidat {r['id']} wajib dipasangi ID Metode valid (M-xxx), ditemukan: '{r['method']}'.")
            if not re.search(r"\bAF-\d{2}\b", r["af"]):
                errors.append(f"[GATE-C2] Kandidat {r['id']} wajib dipasangi ID Attack Form valid (AF-xx), ditemukan: '{r['af']}'.")

    elif gate == "D":
        _, active_cards = parse_leads_table_and_cards(
            raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        if len(active_cards) > 5:
            errors.append(
                f"[GATE-D] Pelanggaran Rolling Batch! Terdapat {len(active_cards)} kartu [ACTIVE] di 05-raw-leads.md (Maksimal 5 per Batch)."
            )
        if len(active_cards) == 0:
            errors.append("[GATE-D] Tidak ada kartu berstatus [ACTIVE] di Bagian 3 05-raw-leads.md untuk dibuktikan.")
        for card in active_cards:
            for titik in ("Titik 1", "Titik 2", "Titik 3"):
                if titik not in card:
                    errors.append(f"[GATE-D] Kartu [ACTIVE] kehilangan komponen '{titik}' pada Bukti Segitiga.")
            if not ANCHOR_REGEX.search(card):
                errors.append("[GATE-D] Kartu [ACTIVE] tidak memiliki jangkar kode Path/File.ext:Lxx.")

    elif gate == "E":
        q_rows, active_cards = parse_leads_table_and_cards(
            raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        active_in_table = [r for r in q_rows if r["status"] == "[ACTIVE]"]
        if active_cards or active_in_table:
            errors.append(
                f"[GATE-E] Meja operasi 05-raw-leads.md belum bersih! Masih ada {len(active_cards)} kartu [ACTIVE] dan {len(active_in_table)} baris tabel berstatus [ACTIVE]. Pindahkan semuanya ke wadah 06/07/08/09."
            )

    else:
        errors.append(f"Nama gate tidak dikenal: '{gate}'. Gunakan 0, A, B, C1, C2, D, atau E.")

    if errors:
        print(f"\n[GATE-{gate} FAIL] Ditemukan {len(errors)} pelanggaran:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"[GATE-{gate} PASS] Seluruh syarat mekanis dan Zero-Compression Law untuk Gate {gate} terpenuhi.")
    return 0


def validate_close_region(region: str, audit_dir: Path) -> int:
    errors: List[str] = []
    for fname in CANONICAL_FILES:
        fpath = audit_dir / fname
        if fpath.exists():
            errors.extend(check_zero_compression(fpath))

    raw_leads_text = read_text(audit_dir / "05-raw-leads.md")
    q_rows, active_cards = parse_leads_table_and_cards(raw_leads_text, region)
    remaining_queued = [r for r in q_rows if "[QUEUED]" in r["status"]]
    remaining_active = [r for r in q_rows if "[ACTIVE]" in r["status"]]

    if remaining_queued or remaining_active or active_cards:
        errors.append(
            f"[CLOSE-REGION {region} FAIL] Wilayah {region} masih menyisakan {len(remaining_queued)} [QUEUED] dan "
            f"{len(remaining_active) + len(active_cards)} [ACTIVE] di 05-raw-leads.md. Kuras habis dengan siklus D->E terlebih dahulu."
        )

    confirmed_text = strip_template_boilerplate(read_text(audit_dir / "09-confirmed-findings.md"))
    for line in confirmed_text.splitlines():
        s = line.strip()
        if s.startswith("|") and re.search(rf"\|\s*`?{re.escape(region)}`?\s*\|", s):
            if "[DRAFT-E]" in s or "[SUBMISSION-READY]" not in s:
                errors.append(
                    f"[CLOSE-REGION {region} FAIL] Temuan Wilayah {region} di 09-confirmed-findings.md belum berstatus [SUBMISSION-READY]: {s}"
                )

    if errors:
        print(f"\n[CLOSE-REGION {region} FAIL] Ditemukan {len(errors)} penghalang penutupan wilayah:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"[CLOSE-REGION {region} PASS] Wilayah {region} bersih ([QUEUED]==0, [ACTIVE]==0, Disclosure 09 siap). "
        f"Silakan set {region} = [CLOSED] di STATE.md dan lakukan Hard Context Flush."
    )
    return 0


def validate_final(audit_dir: Path) -> int:
    errors: List[str] = []
    for fname in CANONICAL_FILES:
        fpath = audit_dir / fname
        if not fpath.exists():
            errors.append(f"[FINAL] Berkas kanonik hilang: {fname}")
        else:
            errors.extend(check_zero_compression(fpath))

    state_text = read_text(audit_dir / "STATE.md")
    regions = [r for r in parse_region_queue(state_text) if "[Nama " not in r["name"]]
    if not regions:
        errors.append("[FINAL] Tidak ada wilayah uang yang terdaftar di STATE.md.")
    for r in regions:
        if "[CLOSED]" not in r["status"]:
            errors.append(f"[FINAL] Wilayah {r['id']} belum berstatus [CLOSED] di STATE.md (status: {r['status']}).")

    raw_leads_text = read_text(audit_dir / "05-raw-leads.md")
    q_rows, active_cards = parse_leads_table_and_cards(raw_leads_text, None)
    rem_q = [r for r in q_rows if "[QUEUED]" in r["status"]]
    rem_a = [r for r in q_rows if "[ACTIVE]" in r["status"]]
    if rem_q or rem_a or active_cards:
        errors.append(
            f"[FINAL] 05-raw-leads.md belum bersih! Tersisa {len(rem_q)} [QUEUED] dan {len(rem_a) + len(active_cards)} [ACTIVE]."
        )

    confirmed_text = strip_template_boilerplate(read_text(audit_dir / "09-confirmed-findings.md"))
    for line in confirmed_text.splitlines():
        s = line.strip()
        if s.startswith("|") and "FIND-" in s and "[SUBMISSION-READY]" not in s:
            errors.append(f"[FINAL] Terdapat temuan di 09-confirmed-findings.md yang belum [SUBMISSION-READY]: {s}")

    if errors:
        print(f"\n[FINAL VERIFICATION FAIL] Ditemukan {len(errors)} masalah:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("[FINAL VERIFICATION PASS] Seluruh wilayah [CLOSED], 05-raw-leads.md bersih (0), bebas kompresi, dan laporan 09 siap kirim!")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Penegak Mekanis & Context Injector Metode Segitiga (theadvers v2.0)"
    )
    parser.add_argument("--sync", action="store_true", help="Sinkronkan seluruh _ROUTER.md dari header 4-baris file plugin.")
    parser.add_argument("--context-packet", action="store_true", help="Cetak paket pemulihan konteks segar dari disk & @SLICE.")
    parser.add_argument("--gate", type=str, help="Validasi gerbang tahap: 0, A, B, C1, C2, D, atau E.")
    parser.add_argument("--close-region", type=str, metavar="R_i", help="Validasi penutupan Wilayah R_i (usai Tahap F).")
    parser.add_argument("--final", action="store_true", help="Validasi penutupan akhir seluruh wilayah & Cross-Region Final Sweep.")
    parser.add_argument("--region", type=str, help="Override ID wilayah aktif (opsional, misal R_1).")
    parser.add_argument("audit_dir", nargs="?", help="Path ke direktori kerja audit.")

    args = parser.parse_args()

    if args.sync:
        return sync_all_routers()

    if not args.audit_dir:
        parser.print_help()
        return 1

    audit_path = Path(args.audit_dir).resolve()
    if not audit_path.exists():
        print(f"[ERROR] Direktori audit tidak ditemukan: {audit_path}", file=sys.stderr)
        return 1

    if args.context_packet:
        return print_context_packet(audit_path, args.region)

    if args.gate:
        return validate_gate(args.gate, audit_path, args.region)

    if args.close_region:
        return validate_close_region(args.close_region, audit_path)

    if args.final:
        return validate_final(audit_path)

    # Default jika hanya dipanggil dengan path direktori audit: tampilkan context-packet
    return print_context_packet(audit_path, args.region)


if __name__ == "__main__":
    sys.exit(main())
