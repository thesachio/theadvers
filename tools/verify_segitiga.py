#!/usr/bin/env python3
"""
verify_segitiga.py — Mesin Penegak Mekanis, Context Re-Hydrator, Plugin Router Sync, & Hermes Skill Sync
Arsitektur: theadvers v2.0 (Selaras penuh dengan TECHNICAL-REPORT.md, POC-PACKAGE.md, SUBMISSION-EMAIL.md, VERDICT.md, SCHEMA.md)
- Berkas kanonik di root audit berhenti di 09-confirmed-findings.md (indeks + metadata VERDICT.md + 3 Titik Bukti).
- Pada STAGE-F, setiap temuan valid FIND-xxx di 09-confirmed-findings.md wajib memiliki wadah folder:
  cases/<FIND-ID>/ yang berisi 3 berkas dengan standar penuh upstream:
    1. chat.md           (Standar SUBMISSION-EMAIL.md + ringkasan jejak lead-<id>.md)
    2. laporan-teknis.md (Standar 9-Bagian wajib TECHNICAL-REPORT.md)
    3. poc.md            (Standar 5-Bagian wajib POC-PACKAGE.md + Kontrol Positif)
- Alur tahap wajib 100% linear: STAGE-0 -> A -> B -> C1 -> C2 -> D -> E -> F (termasuk Zero-Batch Clean Pass).
- Mendukung argumen --audit-dir <dir> maupun positional <dir>.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
METHODOLOGY_FILE = REPO_ROOT / "methodology" / "METHODOLOGY-SEGITIGA.md"
SKILLS_DIR = REPO_ROOT / "skills"
VERDICT_TEMPLATE = REPO_ROOT / "templates" / "VERDICT.md"

CANONICAL_FILES = [
    "INTEL.md",
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

CASE_REQUIRED_FILES = [
    "chat.md",
    "laporan-teknis.md",
    "poc.md",
]

LAPORAN_TEKNIS_SECTIONS = [
    "## 1. Ringkasan",
    "## 2. Lokasi Kode",
    "## 3. Akar Masalah",
    "## 4. Prasyarat",
    "## 5. Langkah Reproduksi",
    "## 6. Keluaran Nyata",
    "## 7. Dampak Kuantitatif",
    "## 8. Rekomendasi Perbaikan",
    "## 9. Yang TIDAK Diverifikasi",
]

POC_SECTIONS = [
    "## 1. Lingkungan",
    "## 2. Perintah",
    "## 3. Keluaran yang Diharapkan",
    "## 4. Bila Gagal",
    "## 5. Kode Lengkap Proof-of-Concept",
]

CHAT_SECTIONS = [
    "## 1. PESAN PENGANTAR SIAP KIRIM",
    "## 2. PANDUAN TEMPEL CEPAT UNTUK PLATFORM",
    "## 3. JEJAK PENALARAN & RINGKASAN RIWAYAT UJI",
]

# ============================================================================
# ATURAN WADAH 06 / 07 / 08 / 09 (preferensi v1 yang ditegakkan mekanis)
# ============================================================================
SIX_EVIDENCE_CLASSES = (
    "REJECTED_POC_FAILS",
    "REJECTED_NEGATIVE_EV",
    "REJECTED_DUST",
)
SIX_STATIC_IMPOSSIBILITY = ("KS-1", "KS-2", "KS-3", "KS-4")
SIX_ALL_CLASSES = SIX_EVIDENCE_CLASSES + (
    "REJECTED_NO_VICTIM",
    "REJECTED_FANTASY_MOCK",
    "REJECTED_CHEATCODE",
    "REJECTED_PRIVILEGED_FANTASY",
    "REJECTED_GENESIS_MIRAGE",
    "REJECTED_NON_LIVE_INIT",
    "REJECTED_BY_DESIGN",
    "REJECTED_MISMATCH",
    "REJECTED_UNPROVEN_DEPLOYMENT",
)
DISPOSITIONS = ("NEXT_EXPLORE", "NEXT_MAINNET", "TOOL_BLOCKED", "ENV_ERROR")
EIGHT_LOW_CLASSES = ("PRE_LIVE_SCOPE", "ADMIN_ONLY", "LOW_NUISANCE")
NINE_FORBIDDEN_TANGGA = ("A-HEAD",)
NINE_FORBIDDEN_CYCLE = ("P1_PRE_DEPLOY", "P2_TESTNET_ONLY")

BUKTI_SIMULASI_RX = re.compile(r"BUKTI[ _]SIMULASI\s*:", re.IGNORECASE)
PERCOBAAN_RX = re.compile(r"PERCOBAAN\s*:", re.IGNORECASE)
DISPOSITION_RX = re.compile(r"Disposition\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Z_]+)`?")
LOW_CLASS_RX = re.compile(r"LOW_CLASS\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?(PRE_LIVE_SCOPE|ADMIN_ONLY|LOW_NUISANCE)")
POC_STATUS_RX = re.compile(r"POC_STATUS\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Za-z_]+)`?")
VERDICT_RX = re.compile(r"VERDICT\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Z_]+)`?")
TANGGA_RX = re.compile(r"TANGGA_BUKTI\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Za-z\-]+)`?")
CYCLE_RX = re.compile(r"CYCLE\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Za-z0-9_]+)`?")
CMD_RX = re.compile(r"^\s*\$\s+\S+")
FENCE_RX = re.compile(r"^\s*```")
# Status baris antrean 05 yang sah setelah STAGE-E memindahkan lead ke wadah
LEAD_STATUS_MOVED = (
    "[MOVED-TO-06]", "[MOVED-TO-07]", "[MOVED-TO-08]", "[MOVED-TO-09]",
    "[MOVED-06]", "[MOVED-07]", "[MOVED-08]", "[MOVED-09]",
)
LEAD_STATUS_OPEN = ("[QUEUED]", "[ACTIVE]")
LEAD_STATUS_RX = re.compile(r"\[(?:QUEUED|ACTIVE|MOVED(?:-TO)?-0[6-9])\]")
# --- Aturan fork live (proyek mainnet) ---
MODE_UJI_RX = re.compile(r"Mode Uji\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?(FORK_LIVE|FORK_TESTNET|FORK_DEPLOYED_HEAD|LOKAL)\b")
BLOCK_RX = re.compile(r"\bblock\s*[:=]\s*`?(\d{4,})")
VERSION_RELATION_RX = re.compile(r"VERSION_RELATION\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Z_]+)")
VERSION_RELATIONS = (
    "LIVE_IS_DEPLOYED_COMMIT",
    "LIVE_NEWER_THAN_HEAD",
    "HEAD_NEWER_THAN_LIVE",
    "LIVE_UNVERIFIED",
)
MODE_LIVE_OK = ("FORK_LIVE", "FORK_TESTNET")
PROJECT_STAGE_RX = re.compile(r"Deployment Stage\s*[:=]\s*`?(MAINNET|TESTNET|DEVNET)", re.IGNORECASE)
DEPLOYMENT_STAGES = ("MAINNET", "TESTNET", "DEVNET")
BLOCK_REF_RX = re.compile(r"Blok Referensi\s*[:=]\s*`?(\d{4,})")
REPO_URL_RX = re.compile(r"Specific GitHub Repo\s*[:=]\s*`?(\S+)")
COMMIT_RX = re.compile(r"Audited Commit\s*/?\s*Branch\s*[:=]\s*`?([^\n]+)")
LIVE_PROOF_RX = re.compile(r"Bukti Live\s*[:=]\s*(.+)")
INTEL_STATUS_RX = re.compile(r"Intel Status\s*[:=]\s*`?(COMPLETE|PARTIAL)")
# --- Rekonsiliasi deployment (deteksi kondisi live) ---
SIKLUS_VALUES = ("P1_PRE_DEPLOY", "P2_TESTNET_ONLY", "P3_LIVE_PARTIAL", "P4_LIVE_FULL")
ENTRYPOINT_VERDICTS = (
    "LIVE_MATCH",
    "HEAD_ONLY_PROVEN",
    "TESTNET_ONLY",
    "ENTRYPOINT_RELOCATED",
    "REGRESSION_FIXED",
    "ENV_ERROR",
    "IDENTITY_ONLY",
    "UNVERIFIABLE",
)
SIKLUS_RX = re.compile(r"SIKLUS\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Z0-9_]+)")
VERDICT_EP_RX = re.compile(r"VERDICT_ENTRYPOINT\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([A-Z_]+)")
DEPLOY_REPORT_RX = re.compile(r"DEPLOYMENT_REPORT\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([^\n`]+)")
# --- Per-lead: objek live & mode PoC (STAGE-D) ---
TARGET_OBJEK_RX = re.compile(r"TARGET_OBJEK\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([^\n`]+)")
DEPLOY_REPORT_LEAD_RX = re.compile(r"DEPLOY_REPORT\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?([^\n`]+)")
MODE_UJI_POC_RX = re.compile(r"MODE_UJI_POC\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?(FORK_LIVE|FORK_TESTNET|FORK_DEPLOYED_HEAD|LOKAL)\b")
FORKPOC_BLOCK_RX = re.compile(r"Fork PoC\s*(?:\*\*)?\s*:\s*[^\n]*?block\s*[:=]\s*`?(\d{4,})")
LEAD_ID_RX = re.compile(r"Lead ID\s*&\s*Judul\s*:\s*\[?(LEAD-[A-Za-z0-9_\-]+)")

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

ANCHOR_REGEX = re.compile(r"[A-Za-z0-9_./\-]+\.[A-Za-z0-9_]+:L?\d+")
RANGE_ANCHOR_REGEX = re.compile(r"[A-Za-z0-9_./\-]+\.[A-Za-z0-9_]+:L?\d+[-–]L?\d+")
HEADER_ID_REGEX = re.compile(r"^#\s+\[([A-Za-z0-9\-]+)\]\s+(.+)$")
META_LINE_REGEX = re.compile(r"^-\s+\*\*(Classes|Trigger Symptom|Paired Items)\*\*:\s*(.+)$")
META_LINE_REGEX_LENIENT = re.compile(r"^-\s+(?:\*\*)?(Classes|Trigger Symptom|Paired Items)(?:\*\*)?:\s*(.+)$")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")



PLACEHOLDER_MARKERS = (
    # Catatan: ID contoh ([CROSS-R1-01], [OBS-R1-01]) SENGAJA tidak dimasukkan sebagai penanda.
    # ID tidak membuktikan kebasian; yang membuktikan adalah sisa token kurung-siku template
    # seperti "[Jelaskan" / "[Path/File" / "[Tulis ". Memasukkan ID membuat agen yang menulis
    # ID contoh di template (persis seperti contohnya) selalu dianggap placeholder.

    "[Fact ID F-R1-xx",
    "[Contoh:",
    "[Tulis ",
    "[Uraikan",
    "[Jelaskan",
    "[Isi ",
    "[Nama ",
    "[Path/File",
    "FIND-001 |",
    "src/CoreVault.ext",
    "src/Liquidator.ext",
    "src/interfaces/ICore.ext",
    "[Nama Wilayah",
    "[Nama Klaster",
)


def is_placeholder_line(line: str) -> bool:
    """True bila baris masih memuat penanda contoh/placeholder template (bukan data audit nyata)."""
    s = line.strip()
    return any(marker in s for marker in PLACEHOLDER_MARKERS)


def has_real_wave_marker(text: str, marker: str, region: Optional[str] = None, other_markers: Tuple[str, ...] = ()) -> bool:
    """Marker gelombang ([WAVE-1-BLIND] / [WAVE-2-CROSS]) hanya dihitung bila muncul pada baris DATA nyata.

    Syarat baris data nyata:
    - bukan heading ('#'), bukan baris definisi bernomor ('1. `[WAVE-...]` ...'),
    - tidak memuat penanda placeholder template,
    - tidak memuat marker gelombang lain (baris contoh menyebut kedua gelombang sekaligus),
    - memiliki jangkar Path/File.ext:Lxx-Lyy (bukti empiris, bukan narasi),
    - bila region diberikan, baris harus menyebut wilayah tersebut (atau wilayah tidak terdeteksi).
    """
    for line in text.splitlines():
        if marker not in line:
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^\d+\.\s+`?\[WAVE-", stripped):
            continue
        if is_placeholder_line(stripped):
            continue
        if any(other in stripped for other in other_markers):
            continue
        if not RANGE_ANCHOR_REGEX.search(stripped) and not ANCHOR_REGEX.search(stripped):
            continue
        return True
    return False


GATE_ORDER = ["GATE-0", "GATE-A", "GATE-B", "GATE-C1", "GATE-C2", "GATE-D", "GATE-E"]


def normalize_gate_label(value: str) -> str:
    v = (value or "").strip().strip("`").upper()
    if not v or v == "NONE":
        return ""
    if not v.startswith("GATE-"):
        v = "GATE-" + v
    return v


def gate_passed_before(required_gate: str, state_text: str) -> bool:
    """Cek apakah gate prasyarat (atau gate yang lebih tinggi) sudah tercatat PASS di STATE.md.

    Monoton: GATE-A sah bila 'Last Passed Gate' bernilai GATE-A, GATE-B, GATE-C1, ... (sudah melewati A).
    """
    m = re.search(r"Last Passed Gate(?:\*\*)?:[ \t]*`?([A-Za-z0-9\-]+)`?", state_text)
    if not m:
        return False
    current = normalize_gate_label(m.group(1))
    if current == "FINAL":
        return True
    if current not in GATE_ORDER:
        return False
    required = normalize_gate_label(required_gate)
    if required not in GATE_ORDER:
        return False
    return GATE_ORDER.index(current) >= GATE_ORDER.index(required)


def strip_template_boilerplate(text: str) -> str:
    """Mengabaikan baris blockquote instruksi template (> ...) dan komentar contoh."""
    cleaned_lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(">") or s.startswith("*Diisi pada") or s.startswith("*Gandakan") or s.startswith("*Salin"):
            continue
        if "[ISI_" in s or "[Contoh:" in s or "[Nama " in s or "[Path/File" in s or "[Jelaskan" in s:
            continue
        if "[TEMPLATE-CONTOH" in s or "[Tulis " in s or "[Uraikan" in s or "[Kutipan" in s or "[Satu " in s:
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
        if "[TOUCHES: ...]" in s or "<...>" in s or s.startswith("|") and "[Tulis " in s:
            continue
        if "Dilarang" in s or "DILARANG" in s or "token kompresi" in s or "FORBIDDEN" in s or "elipsis" in s:
            continue
        # Keluaran terminal nyata boleh terpotong: hex bytecode (0x6080604052...), hash (abc123...),
        # atau baris "Bukti Live"/"BUKTI_SIMULASI" yang mengutip output apa adanya.
        if re.search(r"(0x[0-9a-fA-F]{8,}|\.{3}\s*[\w\]]|\w{8,}\.\.\.)", s) and not re.search(r"\b(dll|dst|etc)\.", s, re.I):
            continue
        if re.match(r"^-?\s*(Bukti Live|BUKTI_SIMULASI|\$ )", s):
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
        m_meta = META_LINE_REGEX.match(line) or META_LINE_REGEX_LENIENT.match(line)
        if not m_meta or m_meta.group(1) != key:
            errors.append(
                f"[{file_path.name}:L{idx+1}] Baris {idx+1} wajib diawali '- **{key}**: ...', ditemukan: '{line}'"
            )
        else:
            meta[key] = m_meta.group(2).strip()

    if errors:
        return None, errors
    return meta, []


def sync_skills_to_hermes_profile() -> None:
    hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    target_skills_root = hermes_home / "skills"
    if not SKILLS_DIR.exists():
        return

    try:
        target_skills_root.mkdir(parents=True, exist_ok=True)
        synced_skills = []
        for skill_folder in sorted(SKILLS_DIR.iterdir()):
            if skill_folder.is_dir() and (skill_folder / "SKILL.md").exists():
                dest = target_skills_root / skill_folder.name
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(skill_folder / "SKILL.md", dest / "SKILL.md")
                synced_skills.append(skill_folder.name)
        if synced_skills:
            print(f"[SKILL-SYNC-OK] {len(synced_skills)} skill disinkronkan ke {target_skills_root}: {', '.join(synced_skills)}")
    except Exception as exc:
        print(f"[SKILL-SYNC-WARN] Tidak dapat menyalin ke {target_skills_root}: {exc}")


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
        print(f"[ROUTER-SYNC-OK] {router_path.relative_to(REPO_ROOT)} ({len(parsed_items)} plugin terindeks)")

    sync_skills_to_hermes_profile()

    if all_errors:
        print("\n[SYNC-FAIL] Ditemukan kesalahan header plugin:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\n[PASS] Seluruh {synced_count} berkas _ROUTER.md dan profil skill berhasil disinkronkan.")
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
            cursor[m.group(1).strip()] = m.group(2).strip()
            continue
        # Format tanpa bold: "- Active Region: R_1 *(keterangan opsional)*"
        m2 = re.match(r"^-\s+([A-Za-z][A-Za-z0-9 ()/&\-]+?):[ \t]*`?([^`*\n]+?)`?[ \t]*(?:\*\(.*)?$", line.strip())
        if m2:
            cursor[m2.group(1).strip()] = m2.group(2).strip()
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


def parse_confirmed_findings(confirmed_text: str, region: Optional[str] = None) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    in_table = False
    for line in confirmed_text.splitlines():
        s = line.strip()
        if re.match(r"^\|\s*`?FIND-", s):
            # Baris data temuan: diterima walau tabel baru dimulai tanpa header berulang.
            in_table = True
        if s.startswith("| Finding ID"):
            in_table = True
            continue
        if in_table:
            if not s.startswith("|"):
                in_table = False
                continue
            if ":---" in s:
                continue
            cols = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cols) >= 9 and re.match(r"^\[?FIND-", cols[0]):
                row_region = cols[2]
                if region is None or row_region == region:
                    findings.append(
                        {
                            "id": cols[0],
                            "lead_id": cols[1],
                            "region": row_region,
                            "severity": cols[3],
                            "ev": cols[4],
                            "anchor": cols[5],
                            "module": cols[6],
                            "plugins": cols[7],
                            "case_dir": cols[8] if len(cols) > 8 else f"cases/{cols[0]}",
                        }
                    )
    return findings


def validate_case_folders(audit_dir: Path, findings: List[Dict[str, str]]) -> List[str]:
    """
    Memvalidasi bahwa setiap FIND-xxx memiliki folder cases/<FIND-ID>/ dengan 3 berkas:
    1. chat.md           (3 bagian wajib SUBMISSION-EMAIL + lead summary)
    2. laporan-teknis.md (9 bagian wajib TECHNICAL-REPORT.md + rentang File:Baris + keluaran nyata)
    3. poc.md            (5 bagian wajib POC-PACKAGE.md + Kontrol Positif + keluaran nyata)
    """
    errors: List[str] = []
    for f in findings:
        fid = f["id"]
        rel_case_dir = f.get("case_dir", "").strip() or f"cases/{fid}"
        if not rel_case_dir.startswith("cases/"):
            rel_case_dir = f"cases/{fid}"
        case_path = audit_dir / rel_case_dir
        if not case_path.exists() or not case_path.is_dir():
            errors.append(
                f"[CASE-FOLDER MISSING] Temuan {fid} (Wilayah {f['region']}) belum memiliki folder wadah '{rel_case_dir}/' di {audit_dir}."
            )
            continue

        for req_file in CASE_REQUIRED_FILES:
            f_path = case_path / req_file
            if not f_path.exists():
                errors.append(
                    f"[CASE-FILE MISSING] Folder '{rel_case_dir}/' untuk temuan {fid} belum memiliki berkas wajib '{req_file}'."
                )
                continue

            errors.extend(check_zero_compression(f_path))
            raw_content = read_text(f_path)
            cleaned = strip_template_boilerplate(raw_content)

            if len(cleaned.strip()) < 60:
                errors.append(
                    f"[CASE-FILE EMPTY] Berkas '{rel_case_dir}/{req_file}' masih kosong atau hanya berisi placeholder template."
                )

            if req_file == "laporan-teknis.md":
                for sec in LAPORAN_TEKNIS_SECTIONS:
                    if sec not in raw_content:
                        errors.append(
                            f"[LAPORAN-TEKNIS SECTION] '{rel_case_dir}/laporan-teknis.md' kehilangan bagian wajib '{sec}' (Standar 9-Bagian TECHNICAL-REPORT.md)."
                        )
                if not RANGE_ANCHOR_REGEX.search(cleaned):
                    errors.append(
                        f"[LAPORAN-TEKNIS RANGE] '{rel_case_dir}/laporan-teknis.md' wajib mencantumkan lokasi kode dalam format rentang 'Path/File.ext:Lxx-Lyy'."
                    )
                if "$ " not in cleaned:
                    errors.append(
                        f"[LAPORAN-TEKNIS OUTPUT] '{rel_case_dir}/laporan-teknis.md' Bagian 5/6 wajib memuat perintah '$ ...' dan keluaran eksekusi nyata."
                    )

            elif req_file == "poc.md":
                for sec in POC_SECTIONS:
                    if sec not in raw_content:
                        errors.append(
                            f"[POC SECTION] '{rel_case_dir}/poc.md' kehilangan bagian wajib '{sec}' (Standar 5-Bagian POC-PACKAGE.md)."
                        )
                if "$ " not in cleaned:
                    errors.append(
                        f"[POC CMD] '{rel_case_dir}/poc.md' wajib memuat perintah '$ ...' dan keluaran eksekusi nyata."
                    )
                if not re.search(r"KONTROL|kontrol positif|positive control", cleaned, re.IGNORECASE):
                    errors.append(
                        f"[POC POSITIVE-CONTROL] '{rel_case_dir}/poc.md' wajib menyertakan pengujian Kontrol Positif sesuai aturan POC-PACKAGE.md."
                    )

            elif req_file == "chat.md":
                for sec in CHAT_SECTIONS:
                    if sec not in raw_content:
                        errors.append(
                            f"[CHAT SECTION] '{rel_case_dir}/chat.md' kehilangan bagian wajib '{sec}' (Standar SUBMISSION-EMAIL.md)."
                        )
                if "Subject:" not in cleaned:
                    errors.append(
                        f"[CHAT SUBJECT] '{rel_case_dir}/chat.md' wajib memiliki baris 'Subject: [<Proyek>] <Severity> — <Judul <=70 karakter>'."
                    )

    return errors



# ============================================================================
# PENEGAK ATURAN 06 / 07 / 08 / 09
# ============================================================================


def split_entries(text: str, id_prefixes: Tuple[str, ...]) -> List[Tuple[str, List[str]]]:
    """Pecah berkas wadah menjadi entri. Entri dimulai oleh heading level 2/3 yang memuat ID berprefix.

    Heading di dalam blok kode (fence ```) diabaikan agar contoh template tidak dihitung sebagai entri.
    """
    entries: List[Tuple[str, List[str]]] = []
    current: Optional[Tuple[str, List[str]]] = None
    in_fence = False
    for line in text.splitlines():
        if FENCE_RX.match(line):
            in_fence = not in_fence
            if current is not None:
                current[1].append(line)
            continue
        if not in_fence and re.match(r"^#{2,3}\s+", line):
            title = line.strip()
            # Heading entri: memuat '[' sebelum ID, mis. "[NEXT-...]", "### VNE-... (Eks [LEAD-..])",
            # "### REF-..." — yang penting ID berprefix muncul SEBELUM kemunculan pertama ']'
            # (mencegah heading tabel seperti "(07-NEEDS-NEXT-STEP)" ikut dianggap entri).
            # Entri sah: ID berprefix berada di dalam tanda kurung siku, ATAU heading diawali ID itu sendiri.
            # Heading tabel seperti "## 1. TABEL ... (07-NEEDS-NEXT-STEP)" tidak memenuhi keduanya.
            body_after_hash = re.sub(r"^#{2,3}\s+", "", title)
            is_entry = False
            for pfx in id_prefixes:
                pat = re.escape(pfx) + r"-[A-Za-z0-9_\-]+"
                if re.search(r"\[\s*`?" + pat, body_after_hash):
                    is_entry = True
                    break
                if re.match(r"^`?" + pat, body_after_hash):
                    is_entry = True
                    break
            if is_entry:
                if current is not None:
                    entries.append(current)
                current = (title, [line])
                continue
        if current is not None:
            current[1].append(line)
    if current is not None:
        entries.append(current)
    return entries


def has_real_command_output(lines: List[str]) -> bool:
    """True bila ada baris perintah '$ ...' DI DALAM blok kode/luar fence, diikuti minimal satu baris
    keluaran nyata (bukan placeholder, bukan baris kosong, bukan komentar contoh)."""
    in_fence = False
    cmd_seen_at = -1
    for idx, line in enumerate(lines):
        if FENCE_RX.match(line):
            in_fence = not in_fence
            continue
        s = line.strip()
        if CMD_RX.match(s):
            cmd_seen_at = idx
            continue
        if cmd_seen_at >= 0 and idx > cmd_seen_at and s:
            if s.startswith("```") or s.startswith("#"):
                continue
            if re.search(r"\[(tempelkan|perintah eksak|log )", s, re.IGNORECASE):
                continue
            if s.startswith("[") and s.endswith("]"):
                continue
            return True
    return False


def validate_six(text: str) -> List[str]:
    """Aturan 06: kelas REJECTED_* + PAPER_REFUTATION guard (BUKTI_SIMULASI atau KS-n) + bukti fork."""
    errors: List[str] = []
    for title, body in split_entries(text, ("REF",)):
        joined = "\n".join(body)
        m_cls = re.search(r"\b(REJECTED_[A-Z_]+)\b", joined)
        if not m_cls:
            continue
        cls = m_cls.group(1)
        if cls not in SIX_ALL_CLASSES:
            errors.append(f"[06 KELAS] Entri '{title[:60]}' memakai kelas tidak dikenal: {cls}.")
            continue
        if cls in SIX_EVIDENCE_CLASSES:
            if not BUKTI_SIMULASI_RX.search(joined):
                errors.append(
                    f"[06 PAPER_REFUTATION] Entri '{title[:60]}' berkelas {cls} tanpa blok BUKTI_SIMULASI: — "
                    f"PAPER_REFUTATION_DETECTED (Pernyataan #11e). Wajib log test + Strike 3 Fuzz."
                )
            elif not has_real_command_output(body):
                errors.append(
                    f"[06 PAPER_REFUTATION] Entri '{title[:60]}' punya BUKTI_SIMULASI: tetapi tidak memuat "
                    f"perintah '$ ...' beserta keluarannya — PAPER_REFUTATION_DETECTED."
                )
        else:
            if not (BUKTI_SIMULASI_RX.search(joined) or any(k in joined for k in SIX_STATIC_IMPOSSIBILITY)):
                errors.append(
                    f"[06 BUKTI] Entri '{title[:60]}' berkelas {cls} wajib BUKTI_SIMULASI: (kelas ini bukan "
                    f"kemustahilan statis KS-1..KS-4)."
                )
        # Kegagalan pun wajib terjadi pada state nyata: FORK_LIVE harus menyebut blok.
        if BUKTI_SIMULASI_RX.search(joined):
            errors.extend(validate_fork_evidence(joined, body, "06", True))
    return errors


def validate_seven(text: str) -> List[str]:
    """Aturan 07: Disposition + PERCOBAAN berisi log nyata (LAZY_BAILOUT guard)."""
    errors: List[str] = []
    for title, body in split_entries(text, ("NEXT",)):
        joined = "\n".join(body)
        m_disp = DISPOSITION_RX.search(joined)
        if not m_disp:
            errors.append(
                f"[07 LAZY_BAILOUT] Entri '{title[:60]}' tanpa Disposition: — LAZY_BAILOUT_DETECTED "
                f"(wajib tepat satu dari {', '.join(DISPOSITIONS)})."
            )
        elif m_disp.group(1) not in DISPOSITIONS:
            errors.append(
                f"[07 DISPOSITION] Entri '{title[:60]}' memakai Disposition tidak sah: {m_disp.group(1)} "
                f"(sah: {', '.join(DISPOSITIONS)})."
            )
        if not PERCOBAAN_RX.search(joined):
            errors.append(
                f"[07 LAZY_BAILOUT] Entri '{title[:60]}' tanpa blok PERCOBAAN: — LAZY_BAILOUT_DETECTED "
                f"(PERCOBAAN bukan rencana; wajib perintah + log)."
            )
        elif not has_real_command_output(body):
            errors.append(
                f"[07 LAZY_BAILOUT] Entri '{title[:60]}' punya PERCOBAAN: tetapi tanpa perintah '$ ...' "
                f"beserta keluarannya — LAZY_BAILOUT_DETECTED."
            )
        m_tangga = TANGGA_RX.search(joined)
        if m_tangga and m_tangga.group(1).upper() in ("A", "A-HEAD"):
            errors.append(
                f"[07 TANGGA] Entri '{title[:60]}' memakai TANGGA_BUKTI {m_tangga.group(1)} — bukti yang sudah "
                f"PASS wajib ke 09 atau 08, bukan diparkir di 07."
            )
    return errors


def validate_eight(text: str) -> List[str]:
    """Aturan 08: LOW_CLASS tepat satu + POC_STATUS PASS + bukti mekanisme."""
    errors: List[str] = []
    for title, body in split_entries(text, ("VNE",)):
        joined = "\n".join(body)
        m_lc = LOW_CLASS_RX.search(joined)
        if not m_lc:
            errors.append(
                f"[08 LOW_CLASS] Entri '{title[:60]}' tanpa LOW_CLASS sah "
                f"(PRE_LIVE_SCOPE | ADMIN_ONLY | LOW_NUISANCE)."
            )
        m_poc = POC_STATUS_RX.search(joined)
        if not m_poc or m_poc.group(1).upper() != "PASS":
            errors.append(
                f"[08 MEKANISME] Entri '{title[:60]}' wajib POC_STATUS: PASS — 08 hanya untuk mekanisme yang "
                f"sudah terbukti; lead belum teruji milik 07 dengan PERCOBAAN:."
            )
        if not BUKTI_SIMULASI_RX.search(joined) or not has_real_command_output(body):
            errors.append(
                f"[08 BUKTI] Entri '{title[:60]}' wajib BUKTI_SIMULASI: berisi perintah '$ ...' + keluaran nyata."
            )
        if m_lc and m_lc.group(1) == "PRE_LIVE_SCOPE" and "KONTROL" not in joined.upper() and "poc" not in joined.lower():
            errors.append(
                f"[08 PRE_LIVE] Entri '{title[:60]}' berkelas PRE_LIVE_SCOPE wajib menyertakan rujukan kode PoC utuh."
            )
    return errors


def validate_nine(text: str) -> List[str]:
    """Aturan 09: TANGGA_BUKTI, DEPLOYMENT_MATCH, LIVE_IDENTITY, POC_STATUS; tolak A-HEAD & siklus pre-deploy."""
    errors: List[str] = []
    for title, body in split_entries(text, ("FIND",)):
        joined = "\n".join(body)
        m_t = TANGGA_RX.search(joined)
        if not m_t:
            errors.append(f"[09 TANGGA] Entri '{title[:60]}' tanpa TANGGA_BUKTI.")
        elif m_t.group(1).upper() in NINE_FORBIDDEN_TANGGA:
            errors.append(
                f"[09 TANGGA] Entri '{title[:60]}' memakai TANGGA_BUKTI A-HEAD — dilarang di 09 "
                f"(itu milik 08 PRE_LIVE_SCOPE)."
            )
        if "DEPLOYMENT_MATCH" not in joined or "LIVE_MATCH" not in joined:
            errors.append(f"[09 DEPLOYMENT] Entri '{title[:60]}' wajib DEPLOYMENT_MATCH: LIVE_MATCH.")
        if "LIVE_IDENTITY" not in joined:
            errors.append(f"[09 IDENTITY] Entri '{title[:60]}' wajib LIVE_IDENTITY terukur.")
        m_c = CYCLE_RX.search(joined)
        if m_c and m_c.group(1) in NINE_FORBIDDEN_CYCLE:
            errors.append(
                f"[09 CYCLE] Entri '{title[:60]}' memakai CYCLE: {m_c.group(1)} — dilarang di 09."
            )
        m_p = POC_STATUS_RX.search(joined)
        if not m_p or m_p.group(1).upper() != "PASS":
            errors.append(f"[09 POC] Entri '{title[:60]}' wajib POC_STATUS: PASS.")
        if not BUKTI_SIMULASI_RX.search(joined) or not has_real_command_output(body):
            errors.append(
                f"[09 BUKTI] Entri '{title[:60]}' wajib BUKTI_SIMULASI: berisi perintah '$ ...' + keluaran nyata."
            )
    return errors


def extract_lead_ids(text: str) -> List[str]:
    """Ambil seluruh ID lead (LEAD-...) yang muncul di tabel maupun kartu 05-raw-leads.md."""
    return sorted(set(re.findall(r"\bLEAD-[A-Za-z0-9_\-]+", text)))


def lead_ids_in_wadah(text: str, id_prefixes: Tuple[str, ...] = ()) -> List[str]:
    """Ambil ID lead yang menjadi SUBJEK entri wadah.

    Sumber otoritatif = heading entri sah (yang memuat ID berprefix). Rujukan "(Eks LEAD-...)" di
    badan entri atau di tabel indeks tidak dihitung, agar satu lead tidak tampak berada di dua wadah.
    """
    ids = set()
    for title, body in split_entries(text, id_prefixes):
        joined = title + "\n" + "\n".join(body[:40])
        m_subject = re.search(r"Eks\s+`?(LEAD-[A-Za-z0-9_\-]+)", title)
        if m_subject:
            ids.add(m_subject.group(1))
            continue
        for lid in re.findall(r"\bLEAD-[A-Za-z0-9_\-]+", title):
            ids.add(lid)
    return sorted(ids)


def validate_lead_traceability(leads_text: str, wadah_texts: Dict[str, str]) -> List[str]:
    """#11d: setiap lead di 05 wajib muncul di tepat satu wadah 06/07/08/09 (tidak boleh menguap)."""
    errors: List[str] = []
    leads = extract_lead_ids(leads_text)
    prefix_map = {
        "06-refuted-invalid.md": ("REF",),
        "07-needs-next-step.md": ("NEXT",),
        "08-valid-not-eligible.md": ("VNE",),
        "09-confirmed-findings.md": ("FIND",),
    }
    seen: Dict[str, List[str]] = {}
    for name, text in wadah_texts.items():
        for lid in lead_ids_in_wadah(text, prefix_map.get(name, ())):
            seen.setdefault(lid, []).append(name)
    for lid in leads:
        holders = seen.get(lid, [])
        if not holders:
            errors.append(
                f"[TRACE #11d] Lead {lid} hilang dari 05-raw-leads.md tetapi tidak tercatat di "
                f"06/07/08/09 mana pun — jejak lead wajib lengkap."
            )
        elif len(holders) > 1:
            errors.append(
                f"[TRACE #11d] Lead {lid} tercatat di lebih dari satu wadah: {', '.join(holders)} "
                f"(satu lead = satu putusan)."
            )
    return errors


def validate_lead_status(raw_leads_text: str) -> List[str]:
    """Status baris antrean 05 wajib salah satu: [QUEUED], [ACTIVE], [MOVED-TO-06..09]."""
    errors: List[str] = []
    in_tbl = False
    for line in raw_leads_text.splitlines():
        s = line.strip()
        if s.startswith("| Lead ID"):
            in_tbl = True
            continue
        if in_tbl:
            if not s.startswith("|"):
                in_tbl = False
                continue
            if ":---" in s or "[Path/File" in s or "[Jelaskan" in s:
                continue
            cols = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cols) >= 10 and LEAD_STATUS_RX.search(cols[0]) is None:
                status = cols[-1]
                if not any(st in status for st in LEAD_STATUS_OPEN + LEAD_STATUS_MOVED):
                    errors.append(
                        f"[05 STATUS] Lead {cols[0]} memakai status tidak sah: '{status}' "
                        f"(sah: [QUEUED], [ACTIVE], atau [MOVED-TO-06..09])."
                    )
    return errors


def deployment_stage(audit_dir: Path) -> Optional[str]:
    """Baca Deployment Stage dari INTEL.md (primer); STATE.md hanya cadangan.

    TIDAK ADA default diam-diam: stage yang tidak dinyatakan = None, dan gate harus menolak.
    """
    for fname in ("INTEL.md", "STATE.md"):
        fp = audit_dir / fname
        if not fp.exists():
            continue
        m = PROJECT_STAGE_RX.search(fp.read_text(encoding="utf-8"))
        if m:
            return m.group(1).upper()
    return None


def project_is_mainnet(audit_dir: Path) -> bool:
    """True hanya bila Deployment Stage benar-benar dinyatakan MAINNET.

    Stage yang tidak dinyatakan TIDAK dianggap mainnet; validate_intel() yang menolaknya.
    """
    return deployment_stage(audit_dir) == "MAINNET"


def validate_fork_evidence(joined: str, body: List[str], label: str, mainnet: bool) -> List[str]:
    """Aturan fork: mode uji wajib disebut; FORK_LIVE wajib blok; 09 wajib live."""
    errors: List[str] = []
    m_mode = MODE_UJI_RX.search(joined)
    if not m_mode:
        errors.append(f"[{label} FORK] Entri '{joined.splitlines()[0][:60]}' tanpa 'Mode Uji:' — bukti fork wajib dinyatakan.")
        return errors
    mode = m_mode.group(1)
    if mode in ("FORK_LIVE", "FORK_TESTNET"):
        block_line = next((l for l in body if BLOCK_RX.search(l)), "")
        if not block_line:
            errors.append(
                f"[{label} FORK] Entri '{joined.splitlines()[0][:60]}' memakai {mode} tanpa nomor blok "
                f"(butuh 'block: <n>') — fork tanpa blok tidak dapat direproduksi."
            )
    return errors


def validate_nine_fork(audit_dir: Path, text: str) -> List[str]:
    """Aturan 09 pada proyek mainnet: FORK_LIVE wajib, VERSION_RELATION wajib, LIVE_UNVERIFIED dilarang."""
    errors: List[str] = []
    mainnet = project_is_mainnet(audit_dir)
    for title, body in split_entries(text, ("FIND",)):
        joined = "\n".join(body)
        errors.extend(validate_fork_evidence(joined, body, "09", mainnet))
        m_mode = MODE_UJI_RX.search(joined)
        allowed = "FORK_LIVE" if mainnet else "FORK_TESTNET"
        if m_mode and m_mode.group(1) != allowed:
            # 09 wajib bukti pada state yang benar-benar berjalan DAN sesuai sifat proyek:
            # mainnet -> FORK_LIVE ; testnet/devnet -> FORK_TESTNET. Mode lain tidak sah di 09.
            errors.append(
                f"[09 FORK] Entri '{title[:60]}' memakai Mode Uji {m_mode.group(1)} — 09 wajib {allowed} "
                f"(FORK_DEPLOYED_HEAD / LOKAL / mode lain tidak sah di 09)."
            )
        m_vr = VERSION_RELATION_RX.search(joined)
        if not m_vr:
            errors.append(f"[09 VERSION] Entri '{title[:60]}' wajib VERSION_RELATION (§2c).")
        elif m_vr.group(1) not in VERSION_RELATIONS:
            errors.append(f"[09 VERSION] Entri '{title[:60]}' memakai VERSION_RELATION tidak sah: {m_vr.group(1)}.")
        elif m_vr.group(1) == "LIVE_UNVERIFIED":
            errors.append(f"[09 VERSION] Entri '{title[:60]}' memakai LIVE_UNVERIFIED — dilarang di 09.")
    return errors


def validate_eight_fork(text: str) -> List[str]:
    """Aturan 08: PRE_LIVE_SCOPE wajib FORK_DEPLOYED_HEAD + HEAD_NEWER_THAN_LIVE."""
    errors: List[str] = []
    for title, body in split_entries(text, ("VNE",)):
        joined = "\n".join(body)
        if "PRE_LIVE_SCOPE" not in joined:
            continue
        m_mode = MODE_UJI_RX.search(joined)
        if m_mode and m_mode.group(1) == "FORK_LIVE":
            errors.append(
                f"[08 FORK] Entri '{title[:60]}' berkelas PRE_LIVE_SCOPE tetapi Mode Uji FORK_LIVE — "
                f"kode yang sudah live wajib ke 09, bukan 08."
            )
        m_vr = VERSION_RELATION_RX.search(joined)
        if not m_vr or m_vr.group(1) != "HEAD_NEWER_THAN_LIVE":
            errors.append(
                f"[08 VERSION] Entri '{title[:60]}' berkelas PRE_LIVE_SCOPE wajib "
                f"VERSION_RELATION: HEAD_NEWER_THAN_LIVE."
            )
    return errors


def validate_intel(audit_dir: Path) -> List[str]:
    """INTEL.md = prasyarat --gate 0. Menagih identitas, jaringan, dan bukti live.

    Dipanggil dari --gate 0 (bukan tahap baru), sesuai keputusan: INTEL diisi sekali di awal.
    """
    errors: List[str] = []
    ip = audit_dir / "INTEL.md"
    if not ip.exists():
        errors.append(
            "[INTEL MISSING] INTEL.md belum ada di root folder audit — INTEL adalah prasyarat STAGE-0 "
            "(salin dari templates/INTEL.md lalu isi)."
        )
        return errors

    text = ip.read_text(encoding="utf-8")
    cleaned = strip_template_boilerplate(text)

    # Batasi pembacaan ke blok §0 agar prosa aturan ("Deployment Stage DILARANG ...") tidak ikut terbaca.
    sec0 = ""
    lines_all = text.splitlines()
    for idx, line in enumerate(lines_all):
        if re.match(r"^#{2,3}\s*0\.\s*Deployment Stage", line.strip()):
            for nxt in lines_all[idx + 1:]:
                if re.match(r"^#{2,3}\s", nxt):
                    break
                sec0 += nxt + "\n"
            break
    m_stage = PROJECT_STAGE_RX.search(sec0)
    if not m_stage:
        errors.append(
            "[INTEL STAGE] 'Deployment Stage' belum diisi — wajib MAINNET | TESTNET | DEVNET "
            "(tidak ada default; nilai ini menentukan Mode Uji seluruh audit)."
        )
        stage = None
    else:
        stage = m_stage.group(1).upper()
        if stage not in DEPLOYMENT_STAGES:
            errors.append(f"[INTEL STAGE] Deployment Stage tidak sah: {stage}.")

    # Resolusi repo & commit
    m_repo = REPO_URL_RX.search(text)
    if not m_repo or "TIDAK_DITEMUKAN" in m_repo.group(1) or m_repo.group(1).strip() in ("", "<URL"):
        errors.append(
            "[INTEL REPO] 'Specific GitHub Repo' wajib URL langsung (atau TIDAK_DITEMUKAN + alasan di §6)."
        )
    m_commit = COMMIT_RX.search(text)
    if not m_commit or not re.search(r"\b[0-9a-f]{7,40}\b", m_commit.group(1)):
        errors.append(
            "[INTEL COMMIT] 'Audited Commit / Branch' wajib memuat hash commit nyata "
            "(hasil git rev-parse), bukan 'latest'/'main'."
        )

    # Bukti live wajib, terutama untuk MAINNET
    m_proof = LIVE_PROOF_RX.search(text)
    proof_val = m_proof.group(1).strip() if m_proof else ""
    # Bukti sah harus memuat artefak konkret: output hex 0x..., ukuran bytecode, atau angka lamport/akun.
    proof_ok = (
        bool(proof_val)
        and "TIDAK_DITEMUKAN" not in proof_val
        and re.search(r"(0x[0-9a-fA-F]{16,}|\b\d{3,}\s*(?:bytes|byte)\b|lamports?|non-?kosong|non-?empty)", proof_val) is not None
    )
    if not proof_ok:
        errors.append(
            "[INTEL LIVE] 'Bukti Live' kosong — wajib perintah cast code/eth_getCode + hasil ringkas "
            "yang membuktikan kode ter-deploy."
        )
    elif stage == "MAINNET":
        m_block = BLOCK_REF_RX.search(text)
        if not m_block:
            errors.append(
                "[INTEL BLOCK] Deployment Stage MAINNET wajib mencantumkan 'Blok Referensi' "
                "(nomor blok terakhir) — dipakai sebagai titik fork di STAGE-D."
            )

    # Konsistensi Intel Status dengan §6
    m_status = INTEL_STATUS_RX.search(text)
    if m_status and m_status.group(1).upper() == "COMPLETE":
        rows = [l for l in text.splitlines() if l.strip().startswith("|") and "TIDAK_DITEMUKAN" in l]
        if rows:
            errors.append(
                "[INTEL STATUS] 'Intel Status: COMPLETE' tidak sah — tabel §6 masih memuat "
                "TIDAK_DITEMUKAN. Turunkan ke PARTIAL."
            )
    return errors


def validate_deployment_report(joined: str, body: List[str], label: str, audit_dir: Path,
                               allow_siklus: Tuple[str, ...], allow_ep: Tuple[str, ...]) -> List[str]:
    """DEPLOYMENT_REPORT wajib menunjuk artefak deploy_parity yang benar-benar ada.

    Mencegah wadah 06/08/09 dipilih di atas asumsi 'kontrak belum live'.
    """
    errors: List[str] = []
    head = joined.splitlines()[0][:60] if joined else "?"
    m_rep = DEPLOY_REPORT_RX.search(joined)
    if not m_rep:
        errors.append(
            f"[{label} DEPLOY] Entri '{head}' tanpa DEPLOYMENT_REPORT — jalankan "
            f"tools/deploy_parity.py --out <audit-dir>/notes/deploy-parity-<ID>.json dulu."
        )
    else:
        raw = m_rep.group(1).strip()
        # Normalisasi: boleh path absolut, relatif audit-dir, atau relatif root.
        cands = [Path(raw)]
        if not Path(raw).is_absolute():
            cands += [audit_dir / raw, REPO_ROOT / raw]
        if not any(c.exists() for c in cands):
            errors.append(
                f"[{label} DEPLOY] Entri '{head}' menunjuk artefak yang tidak ada: {raw}"
            )

    m_s = SIKLUS_RX.search(joined)
    if not m_s:
        errors.append(f"[{label} DEPLOY] Entri '{head}' tanpa SIKLUS (P1..P4).")
    elif m_s.group(1) not in SIKLUS_VALUES:
        errors.append(f"[{label} DEPLOY] Entri '{head}' memakai SIKLUS tidak sah: {m_s.group(1)}.")
    elif m_s.group(1) not in allow_siklus:
        errors.append(
            f"[{label} DEPLOY] Entri '{head}' memakai SIKLUS {m_s.group(1)} — wadah {label} hanya sah untuk "
            f"{', '.join(allow_siklus)}."
        )

    m_ep = VERDICT_EP_RX.search(joined)
    if not m_ep:
        errors.append(f"[{label} DEPLOY] Entri '{head}' tanpa VERDICT_ENTRYPOINT.")
    elif m_ep.group(1) not in ENTRYPOINT_VERDICTS:
        errors.append(f"[{label} DEPLOY] Entri '{head}' memakai VERDICT_ENTRYPOINT tidak sah: {m_ep.group(1)}.")
    elif m_ep.group(1) not in allow_ep:
        errors.append(
            f"[{label} DEPLOY] Entri '{head}' memakai VERDICT_ENTRYPOINT {m_ep.group(1)} — tidak sah untuk "
            f"wadah {label} (sah: {', '.join(allow_ep)})."
        )
    return errors


# SIKLUS -> MODE_UJI_POC yang sah (PoC dibangun pada kondisi yang relevan)
SIKLUS_TO_MODE = {
    "P4_LIVE_FULL": ("FORK_LIVE",),
    "P3_LIVE_PARTIAL": ("FORK_LIVE",),
    "P2_TESTNET_ONLY": ("FORK_TESTNET",),
    "P1_PRE_DEPLOY": ("FORK_DEPLOYED_HEAD", "LOKAL"),
}
# MODE_UJI_POC yang sah menurut Deployment Stage proyek (INTEL §0)
STAGE_TO_MODE = {
    "MAINNET": ("FORK_LIVE", "FORK_DEPLOYED_HEAD", "LOKAL"),
    "TESTNET": ("FORK_TESTNET", "FORK_DEPLOYED_HEAD", "LOKAL"),
    "DEVNET": ("FORK_TESTNET", "FORK_DEPLOYED_HEAD", "LOKAL"),
}


def validate_lead_deploy(audit_dir: Path, active_cards: List[str]) -> List[str]:
    """Per lead [ACTIVE]: TARGET_OBJEK + artefak deploy_parity + MODE_UJI_POC konsisten.

    Tujuan: PoC dibangun pada kondisi yang RELEVAN — mainnet->FORK_LIVE, testnet/devnet->
    FORK_TESTNET, pre-deploy->FORK_DEPLOYED_HEAD/LOKAL.
    """
    errors: List[str] = []
    stage = deployment_stage(audit_dir)
    if stage is None:
        errors.append(
            "[GATE-D DEPLOY] Deployment Stage belum dinyatakan di INTEL.md §0 — Mode Uji PoC "
            "tidak dapat diverifikasi. Jalankan skill sc-pre-intel lebih dulu."
        )
        return errors

    for chunk in active_cards:
        body = chunk.splitlines()
        joined = "\n".join(body)
        head = body[0][:70] if body else "?"
        m_id = LEAD_ID_RX.search(joined)
        lead_id = m_id.group(1) if m_id else "LEAD-?"

        # a. objek on-chain yang diserang
        m_obj = TARGET_OBJEK_RX.search(joined)
        obj = (m_obj.group(1).strip() if m_obj else "")
        if not obj or "[" in obj or "<" in obj:
            errors.append(
                f"[GATE-D DEPLOY] {lead_id} tanpa TARGET_OBJEK — sebutkan chain:alamat objek yang diserang "
                f"(mis. ethereum:0xAbC…123) agar PoC dibangun pada objek nyata."
            )

        # b. artefak deploy_parity per lead wajib ADA di disk
        m_rep = DEPLOY_REPORT_LEAD_RX.search(joined)
        if not m_rep:
            errors.append(
                f"[GATE-D DEPLOY] {lead_id} tanpa DEPLOY_REPORT — jalankan tools/deploy_parity.py "
                f"--out <audit-dir>/notes/deploy-parity-{lead_id}.json sebelum --gate D."
            )
        else:
            raw = m_rep.group(1).strip()
            cands = [Path(raw)]
            if not Path(raw).is_absolute():
                cands += [audit_dir / raw, REPO_ROOT / raw]
            if not any(c.exists() for c in cands):
                errors.append(f"[GATE-D DEPLOY] {lead_id} menunjuk artefak yang tidak ada: {raw}")

        # c. SIKLUS wajib & sah
        m_s = SIKLUS_RX.search(joined)
        siklus = m_s.group(1) if m_s else None
        if not siklus:
            errors.append(f"[GATE-D DEPLOY] {lead_id} tanpa SIKLUS (P1..P4).")
        elif siklus not in SIKLUS_VALUES:
            errors.append(f"[GATE-D DEPLOY] {lead_id} memakai SIKLUS tidak sah: {siklus}.")

        # d. MODE_UJI_POC wajib & konsisten dengan SIKLUS
        m_mode = MODE_UJI_POC_RX.search(joined)
        mode = m_mode.group(1) if m_mode else None
        if not mode:
            errors.append(f"[GATE-D DEPLOY] {lead_id} tanpa MODE_UJI_POC.")
        elif siklus in SIKLUS_TO_MODE and mode not in SIKLUS_TO_MODE[siklus]:
            errors.append(
                f"[GATE-D DEPLOY] {lead_id}: SIKLUS {siklus} menuntut MODE_UJI_POC "
                f"{' / '.join(SIKLUS_TO_MODE[siklus])}, bukan {mode}."
            )

        # e. MODE_UJI_POC wajib konsisten dengan Deployment Stage proyek
        if mode and stage in STAGE_TO_MODE and mode not in STAGE_TO_MODE[stage]:
            errors.append(
                f"[GATE-D DEPLOY] {lead_id}: Deployment Stage {stage} (INTEL §0) tidak mengizinkan "
                f"MODE_UJI_POC {mode} — PoC akan dibangun pada kondisi yang tidak relevan."
            )

        # f. fork wajib menyebut blok bila mode fork live/testnet
        if mode in ("FORK_LIVE", "FORK_TESTNET") and not FORKPOC_BLOCK_RX.search(joined):
            errors.append(
                f"[GATE-D DEPLOY] {lead_id}: MODE_UJI_POC {mode} tanpa nomor blok pada baris "
                f"'Fork PoC' (butuh block: <n>)."
            )

    return errors


GUARD_ID_RX = re.compile(r"\bGUARD-(?:R\d+-)?\d+\b")
GUARD_STATUSES = {"TERSANGKAL"} | {f"TEMBUS-J{n}" for n in range(1, 6)}
JALUR_IDS = ("J1", "J2", "J3", "J4", "J5")


def _table_rows(text: str, header_probe: str) -> List[List[str]]:
    """Ambil baris tabel markdown setelah header memuat header_probe — BERHENTI di heading berikutnya.

    Tanpa berhenti di heading, tabel bagian 3 (5 kolom) ikut tertelan ke daftar baris
    bagian 2 (8 kolom) dan memicu salah baca jumlah kolom.
    """
    rows: List[List[str]] = []
    inside = False
    for line in text.splitlines():
        s = line.strip()
        if inside and s.startswith("#"):
            break
        if s.startswith("|") and header_probe in s:
            inside = True
            continue
        if inside:
            if not s.startswith("|"):
                inside = False
                continue
            if ":---" in s:
                continue
            rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


def _guard_table_rows(text: str) -> List[Tuple[List[str], bool]]:
    """Baris tabel GUARD di bagian 2, beserta penanda apakah headernya punya kolom Status.

    Dua tabel memakai awalan "Guard ID" (bagian 2 dan bagian 3), jadi probe harus
    membedakan lewat kolom lain: bagian 2 punya kolom Status/Metode, bagian 3 punya 'Jalur'.
    """
    out: List[Tuple[List[str], bool]] = []
    inside = False
    has_status = False
    for line in text.splitlines():
        s = line.strip()
        if inside and s.startswith("#"):
            break
        if s.startswith("|") and "Guard ID" in s:
            if "Jalur" in s:
                inside = False
                continue
            inside = True
            has_status = "Status" in s
            continue
        if inside:
            if not s.startswith("|"):
                inside = False
                continue
            if ":---" in s:
                continue
            out.append(([c.strip() for c in s.strip("|").split("|")], has_status))
    return out


def validate_four(guarded_text: str) -> List[str]:
    """04-code-guarded.md: status TERSANGKAL wajib didukung 5 baris uji jalur berjangkar.

    Alasan aturan ini ada: sebelumnya agen dapat menulis "dijaga onlyOwner" tanpa pernah
    menguji 4 jalur permissionless lainnya, lalu mengunci hipotesis yang sebenarnya tembus.
    """
    errors: List[str] = []
    if not guarded_text.strip():
        return errors

    # 1. Tabel utama: Guard ID + Status
    guards: Dict[str, str] = {}
    for cols, probe_hit_status in _guard_table_rows(guarded_text):
        gid = cols[0].strip("`* ")
        if not re.fullmatch(r"GUARD-(?:R\d+-)?\d+", gid):
            continue
        if not probe_hit_status or len(cols) < 8:
            # Format lama (tanpa kolom Status) dilarang dilewati diam-diam: entri seperti itu
            # tidak pernah mengklaim TERSANGKAL, tetapi juga tidak pernah membuktikannya.
            errors.append(
                f"[RULES-04] {gid}: tabel utama hanya punya {len(cols)} kolom tanpa kolom Status, "
                f"wajib 8 (… | Status | Metode). Tambahkan kolom Status "
                f"(TERSANGKAL / TEMBUS-J1..J5) dan tabel Uji 5 Jalur di bagian 3."
            )
            continue
        status = cols[6].strip("`* ").upper()
        guards[gid] = status
        if status not in GUARD_STATUSES:
            errors.append(
                f"[RULES-04] {gid} berstatus tidak sah '{status}'. Nilai sah: "
                f"TERSANGKAL atau TEMBUS-J1..TEMBUS-J5."
            )

    # 2. Tabel uji 5 jalur
    jalur_rows: Dict[str, Dict[str, List[str]]] = {}
    for cols in _table_rows(guarded_text, "| Jalur |"):
        if len(cols) < 4:
            continue
        gid, jalur = cols[0].strip("`* "), cols[1].strip("`* ").upper()
        if not re.fullmatch(r"GUARD-(?:R\d+-)?\d+", gid) or jalur not in JALUR_IDS:
            continue
        jalur_rows.setdefault(gid, {}).setdefault(jalur, []).append(cols[2] + " || " + cols[3])

    # 3. Setiap GUARD wajib punya 5 jalur
    for gid, status in guards.items():
        rows = jalur_rows.get(gid, {})
        hilang = [j for j in JALUR_IDS if j not in rows]
        if hilang:
            errors.append(
                f"[RULES-04] {gid} (status {status}) belum menguji jalur {', '.join(hilang)}. "
                f"Tabel 'Uji 5 Jalur' wajib berisi tepat 5 baris (J1..J5)."
            )
            continue
        for jalur in JALUR_IDS:
            for cell in rows[jalur]:
                hasil, _, alasan = cell.partition("||")
                hasil_u = hasil.strip("`* ").upper()
                if hasil_u not in ("TERTUTUP", "TEMBUS"):
                    errors.append(
                        f"[RULES-04] {gid} jalur {jalur}: hasil '{hasil.strip()}' tidak sah "
                        f"(TERTUTUP / TEMBUS)."
                    )
                if hasil_u == "TEMBUS" and status == "TERSANGKAL":
                    errors.append(
                        f"[RULES-04] {gid} berstatus TERSANGKAL padahal jalur {jalur} TEMBUS — "
                        f"guard ini DILARANG di 04; pindahkan ke 05-raw-leads.md dengan tag [TEMBUS-{jalur}]."
                    )
                if hasil_u == "TERTUTUP" and not ANCHOR_REGEX.search(alasan):
                    # Jangkar Path/File.ext:Lxx WAJIB pada setiap baris, termasuk yang berlabel N/A:
                    # ketiadaan jalur pun harus dibuktikan di berkas tertentu, bukan diklaim.
                    errors.append(
                        f"[RULES-04] {gid} jalur {jalur}: alasan TERTUTUP tanpa jangkar "
                        f"Path/File.ext:Lxx — alasan tanpa bukti tidak sah. Bila jalurnya memang "
                        f"tidak ada, tulis 'N/A' DAN sebut lokasi pembuktian ketiadaannya."
                    )

    return errors


def validate_wadah_rules(audit_dir: Path) -> List[str]:
    """Jalankan seluruh aturan 06/07/08/09 + jejak lead."""
    errors: List[str] = []
    texts = {}
    for name in ("06-refuted-invalid.md", "07-needs-next-step.md", "08-valid-not-eligible.md", "09-confirmed-findings.md"):
        path = audit_dir / name
        texts[name] = path.read_text(encoding="utf-8") if path.exists() else ""
    errors.extend(validate_six(texts["06-refuted-invalid.md"]))
    errors.extend(validate_seven(texts["07-needs-next-step.md"]))
    errors.extend(validate_eight(texts["08-valid-not-eligible.md"]))
    errors.extend(validate_nine(texts["09-confirmed-findings.md"]))
    guarded_path = audit_dir / "04-code-guarded.md"
    if guarded_path.exists():
        errors.extend(validate_four(guarded_path.read_text(encoding="utf-8")))
    errors.extend(validate_nine_fork(audit_dir, texts["09-confirmed-findings.md"]))
    errors.extend(validate_eight_fork(texts["08-valid-not-eligible.md"]))

    # Rekonsiliasi deployment: 09 hanya LIVE_MATCH/P4; 08 hanya pre-live/testnet/relocated.
    for title, body in split_entries(texts["09-confirmed-findings.md"], ("FIND",)):
        errors.extend(validate_deployment_report(
            "\n".join(body), body, "09", audit_dir,
            allow_siklus=("P4_LIVE_FULL",), allow_ep=("LIVE_MATCH",),
        ))
    for title, body in split_entries(texts["08-valid-not-eligible.md"], ("VNE",)):
        errors.extend(validate_deployment_report(
            "\n".join(body), body, "08", audit_dir,
            allow_siklus=("P1_PRE_DEPLOY", "P2_TESTNET_ONLY", "P3_LIVE_PARTIAL"),
            allow_ep=("HEAD_ONLY_PROVEN", "TESTNET_ONLY", "ENTRYPOINT_RELOCATED"),
        ))
    leads_text = (audit_dir / "05-raw-leads.md").read_text(encoding="utf-8") if (audit_dir / "05-raw-leads.md").exists() else ""
    errors.extend(validate_lead_status(leads_text))
    errors.extend(validate_lead_traceability(leads_text, texts))
    return errors


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
        if s.startswith("|") and (f"`{region}`" in s or re.search(rf"\|\s*{re.escape(region)}\s*\|", s)):
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
            # Toleran terhadap format bold maupun tidak: "- Status Saat Ini: [ACTIVE]" / "- **Status Saat Ini**: [ACTIVE]"
            if re.search(r"Status Saat Ini\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?\[ACTIVE\]`?", chunk):
                if region is None or re.search(
                    rf"Region\s*&\s*EV\s*Rank\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*`?{re.escape(region)}\b", chunk
                ):
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
    print(f"ATURAN WAJIB STAGE AKTIF ({current_stage}) DARI METHODOLOGY-SEGITIGA.md")
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
        print("DILARANG MEMBUKA _ROUTER.md ATAU MEMBACA FILE PLUGIN M-xxx / AF-xx PADA STAGE INI!")
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
        if not active_cards and not queued_now:
            print(f"  [INFO] Wilayah {active_region} memiliki 0 [QUEUED] dan 0 [ACTIVE] (Zero-Batch Clean Pass).")
            print("  -> Jalankan langsung: python3 tools/verify_segitiga.py --gate D <audit-dir> untuk lanjut ke STAGE-E.")
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
        print("PENGINGAT HUKUM ACARA PENGADILAN BUKTI (templates/VERDICT.md)")
        print("=" * 88)
        print("  - Pindahkan seluruh kandidat [ACTIVE] dari 05-raw-leads.md ke:")
        print("    * 06-refuted-invalid.md   (jika PoC gagal / terbantahkan saat uji)")
        print("    * 07-needs-next-step.md   (jika butuh verifikasi state on-chain live / eksternal)")
        print("    * 08-valid-not-eligible.md (jika valid teknis namun out-of-scope / known / trusted role)")
        print("    * 09-confirmed-findings.md (jika lulus 3 Titik Bukti Segitiga utuh)")
        print("  - Setelah STAGE-E selesai, jumlah [ACTIVE] di 05-raw-leads.md WAJIB == 0.")

    elif current_stage.upper() == "STAGE-F":
        confirmed_text = read_text(audit_dir / "09-confirmed-findings.md")
        region_findings = parse_confirmed_findings(
            confirmed_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        print("\n" + "=" * 88)
        print("WADAH KASUS STAGE-F: cases/<FIND-ID>/ (chat.md, laporan-teknis.md [9 Bagian], poc.md [5 Bagian + Kontrol Positif])")
        print("=" * 88)
        if not region_findings:
            print(f"  [INFO] Wilayah {active_region} memiliki 0 temuan di 09-confirmed-findings.md.")
            print(f"  -> Anda dapat langsung menjalankan: python3 tools/verify_segitiga.py --close-region {active_region} <audit-dir>")
        else:
            print(f"  [!] Ditemukan {len(region_findings)} temuan valid di 09-confirmed-findings.md untuk Wilayah {active_region}:")
            for rf in region_findings:
                cdir = rf["case_dir"]
                print(f"      * {rf['id']} ({rf['severity']}) -> Wajib buat folder '{cdir}/' berisi:")
                print(f"          1. {cdir}/chat.md           (Standar SUBMISSION-EMAIL.md + ringkasan lead)")
                print(f"          2. {cdir}/laporan-teknis.md (Standar 9-Bagian wajib TECHNICAL-REPORT.md)")
                print(f"          3. {cdir}/poc.md            (Standar 5-Bagian wajib POC-PACKAGE.md + Kontrol Positif)")

    print("=" * 88)
    return 0


# ============================================================================
# 4. PENEGAK GERBANG STAGE (--gate 0|A|B|C1|C2|D|E, --close-region, --final)
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
        # INTEL.md = prasyarat STAGE-0 (bukan tahap baru)
        errors.extend(validate_intel(audit_dir))

        # Cek Tabel Rekonsiliasi di path-map.md
        reconciled_rows = []
        tier3_rows = []
        for line in path_map_text.splitlines():
            s = line.strip()
            if s.startswith("|") and ("TIER-1" in s or "TIER-2" in s or "TIER-3" in s):
                if "[src/" in s or "[Bahasa]" in s or s.startswith("| No |"):
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

        # [GATE-0] Zero-Loss: setiap berkas TIER-1 / TIER-2 wajib dialokasikan ke minimal satu Wilayah R_i
        # di STATE.md. Tanpa aturan ini, berkas bernilai bisa hilang tanpa jejak karena tidak ada
        # yang menagih kesetaraan jumlah berkas Tier-1/2 vs berkas yang tercakup wilayah.
        allocated_files = set()
        for r in real_regions:
            for token in re.split(r"[,\s]+", r.get("files", "")):
                token = token.strip().strip("`[]")
                if "/" in token and "." in token:
                    allocated_files.add(token)

        unassigned = []
        for row in reconciled_rows:
            if "TIER-3" in row:
                continue
            for token in re.findall(r"[A-Za-z0-9_./\-]+\.[A-Za-z0-9_]+", row):
                if token.startswith("Path/"):
                    continue
                if token not in allocated_files:
                    unassigned.append(token)
        for token in sorted(set(unassigned)):
            errors.append(
                f"[GATE-0] Berkas Tier-1/Tier-2 '{token}' terdaftar di Tabel Rekonsiliasi path-map.md "
                f"tetapi tidak dialokasikan ke Wilayah mana pun di STATE.md (Zero-Loss Coverage)."
            )

    elif gate == "A":
        if not gate_passed_before("GATE-0", state_text):
            errors.append("[GATE-A] Prasyarat GATE-0 belum tercatat PASS di STATE.md (field 'Last Passed Gate').")
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
            has_real = False
            for line in cleaned_pm.splitlines():
                if edge_tag not in line:
                    continue
                stripped = line.strip()
                if stripped.startswith("#") or re.match(r"^\d+\.\s+`?\[EDGE-", stripped):
                    continue
                if is_placeholder_line(line):
                    continue
                has_real = True
                break
            if not has_real:
                errors.append(
                    f"[GATE-B] Pemetaan {edge_tag} belum ditemukan sebagai entri data nyata (bukan definisi/heading/contoh) di path-map.md."
                )
        for line in cleaned_pm.splitlines():
            if not any(t in line for t in ("[EDGE-ASSET]", "[EDGE-VALUATION]", "[EDGE-CONTROL/LATENT]")):
                continue
            stripped = line.strip()
            # Heading template & baris definisi (mis. "3. `[EDGE-CONTROL/LATENT]` (Otorisasi ...)") bukan entri data.
            if stripped.startswith("#") or re.match(r"^\d+\.\s+`?\[EDGE-", stripped):
                continue
            if is_placeholder_line(line):
                continue
            if not ANCHOR_REGEX.search(line):
                errors.append(f"[GATE-B] Entri Edge wajib memiliki jangkar Path/File.ext:Lxx: {stripped}")

    elif gate == "C1":
        if not gate_passed_before("GATE-B", state_text):
            errors.append("[GATE-C1] Prasyarat GATE-B belum tercatat PASS di STATE.md (field 'Last Passed Gate').")
        cleaned_guarded = strip_template_boilerplate(guarded_text)
        cleaned_leads = strip_template_boilerplate(raw_leads_text)
        real_guarded_lines = [
            ln for ln in cleaned_guarded.splitlines()
            if ANCHOR_REGEX.search(ln) and not is_placeholder_line(ln) and not ln.strip().startswith("#")
        ]
        has_guarded = bool(real_guarded_lines)
        has_wave1 = has_real_wave_marker(cleaned_leads, "[WAVE-1-BLIND]", active_region, other_markers=("[WAVE-2-CROSS]",))
        if not (has_guarded or has_wave1):
            errors.append(
                f"[GATE-C1] Wilayah {active_region} belum memiliki catatan berjangkar ':Lxx' di 04-code-guarded.md maupun [WAVE-1-BLIND] di 05-raw-leads.md."
            )
        radar_rows, _ = extract_radar_signals(radar_text)
        real_radar = [r for r in radar_rows if not is_placeholder_line(r)]
        if not real_radar:
            errors.append("[GATE-C1] RADAR.md belum memiliki sinyal lintas-modul NYATA dengan tag [TOUCHES: NamaModul.simbol] dan jangkar ':Lxx'.")

    elif gate == "C2":
        if not gate_passed_before("GATE-C1", state_text):
            errors.append("[GATE-C2] Prasyarat GATE-C1 belum tercatat PASS di STATE.md (field 'Last Passed Gate').")
        cleaned_leads = strip_template_boilerplate(raw_leads_text)
        if not has_real_wave_marker(cleaned_leads, "[WAVE-2-CROSS]", active_region, other_markers=("[WAVE-1-BLIND]",)):
            errors.append(
                f"[GATE-C2] Dokumentasi penyilangan [WAVE-2-CROSS] untuk Wilayah {active_region} belum tercatat sebagai baris data nyata di 05-raw-leads.md."
            )
        q_rows, _ = parse_leads_table_and_cards(raw_leads_text, None if active_region == "NONE" else active_region)
        if not q_rows:
            real_guarded_c2 = [
                ln for ln in strip_template_boilerplate(guarded_text).splitlines()
                if ANCHOR_REGEX.search(ln) and not is_placeholder_line(ln)
            ]
            if not real_guarded_c2:
                errors.append(
                    f"[GATE-C2] Wilayah {active_region}: tidak ada kandidat [QUEUED] dan 04-code-guarded.md tidak memuat jalur terjaga nyata. "
                    f"Penyilangan belum menghasilkan keputusan apa pun."
                )
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
        if not gate_passed_before("GATE-C2", state_text):
            errors.append("[GATE-D] Prasyarat GATE-C2 belum tercatat PASS di STATE.md (field 'Last Passed Gate').")
        _, active_cards = parse_leads_table_and_cards(
            raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        q_rows_d, _ = parse_leads_table_and_cards(
            raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        queued_now = [r for r in q_rows_d if "[QUEUED]" in r["status"]]

        if len(active_cards) > 5:
            errors.append(
                f"[GATE-D] Pelanggaran Rolling Batch! Terdapat {len(active_cards)} kartu [ACTIVE] di 05-raw-leads.md (Maksimal 5 per Batch)."
            )
        elif len(active_cards) == 0:
            if len(queued_now) > 0:
                errors.append(
                    f"[GATE-D] Masih ada {len(queued_now)} kandidat [QUEUED] untuk Wilayah {active_region}, tetapi 0 kartu [ACTIVE] di Bagian 3 05-raw-leads.md. Tarik maksimal 5 kandidat ke meja operasi terlebih dahulu."
                )
            else:
                cleaned_guarded_d = strip_template_boilerplate(guarded_text)
                if not ANCHOR_REGEX.search(cleaned_guarded_d):
                    errors.append(
                        f"[GATE-D] Wilayah {active_region} memiliki 0 lead, tetapi 04-code-guarded.md belum mencatat bukti jalur terjaga ':Lxx'."
                    )
        for card in active_cards:
            for titik in ("Titik 1", "Titik 2", "Titik 3"):
                if titik not in card:
                    errors.append(f"[GATE-D] Kartu [ACTIVE] kehilangan komponen '{titik}' pada Bukti Segitiga.")
            if not ANCHOR_REGEX.search(card):
                errors.append("[GATE-D] Kartu [ACTIVE] tidak memiliki jangkar kode Path/File.ext:Lxx.")

        # Per lead: objek on-chain + artefak deploy_parity + Mode Uji PoC yang relevan.
        errors.extend(validate_lead_deploy(audit_dir, active_cards))

    elif gate == "E":
        if not gate_passed_before("GATE-D", state_text):
            errors.append(
                "[GATE-E] Prasyarat GATE-D belum tercatat PASS di STATE.md (field 'Last Passed Gate'). "
                "STAGE-E tidak boleh disahkan bila STAGE-D belum pernah dijalankan."
            )
        q_rows, active_cards = parse_leads_table_and_cards(
            raw_leads_text, None if active_region in ("NONE", "CROSS-REGION") else active_region
        )
        active_in_table = [r for r in q_rows if r["status"] == "[ACTIVE]"]
        if active_cards or active_in_table:
            errors.append(
                f"[GATE-E] Meja operasi 05-raw-leads.md belum bersih! Masih ada {len(active_cards)} kartu [ACTIVE] dan {len(active_in_table)} baris tabel berstatus [ACTIVE]. Pindahkan semuanya ke wadah 06/07/08/09."
            )
        errors.extend(validate_wadah_rules(audit_dir))

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

    confirmed_text = read_text(audit_dir / "09-confirmed-findings.md")
    region_findings = parse_confirmed_findings(confirmed_text, region)
    errors.extend(validate_case_folders(audit_dir, region_findings))
    errors.extend(validate_wadah_rules(audit_dir))

    if errors:
        print(f"\n[CLOSE-REGION {region} FAIL] Ditemukan {len(errors)} penghalang penutupan wilayah:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"[CLOSE-REGION {region} PASS] Wilayah {region} bersih ([QUEUED]==0, [ACTIVE]==0, "
        f"dan {len(region_findings)} wadah cases/<FIND-ID>/ lengkap mematuhi standar TECHNICAL-REPORT, POC-PACKAGE, & SUBMISSION-EMAIL). "
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

    confirmed_text = read_text(audit_dir / "09-confirmed-findings.md")
    all_findings = parse_confirmed_findings(confirmed_text, None)
    errors.extend(validate_case_folders(audit_dir, all_findings))
    errors.extend(validate_wadah_rules(audit_dir))

    if errors:
        print(f"\n[FINAL VERIFICATION FAIL] Ditemukan {len(errors)} masalah:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"[FINAL VERIFICATION PASS] Seluruh wilayah [CLOSED], 05-raw-leads.md bersih (0), bebas kompresi, "
        f"dan seluruh {len(all_findings)} wadah cases/<FIND-ID>/ (chat.md, laporan-teknis.md, poc.md) terverifikasi utuh!"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Penegak Mekanis & Context Injector Metode Segitiga (theadvers v2.0)"
    )
    parser.add_argument("--intel", action="store_true", help="Audit khusus INTEL.md (prasyarat STAGE-0) tanpa gate tahap.")
    parser.add_argument("--rules", action="store_true", help="Audit khusus aturan wadah 06/07/08/09 + jejak lead (tanpa gate tahap).")
    parser.add_argument("--sync", action="store_true", help="Sinkronkan seluruh _ROUTER.md dan instal skill ke profil Hermes.")
    parser.add_argument("--context-packet", action="store_true", help="Cetak paket pemulihan konteks segar dari disk & @SLICE.")
    parser.add_argument("--gate", type=str, help="Validasi gerbang tahap: 0, A, B, C1, C2, D, atau E.")
    parser.add_argument("--close-region", type=str, metavar="R_i", help="Validasi penutupan Wilayah R_i (usai STAGE-F).")
    parser.add_argument("--final", action="store_true", help="Validasi penutupan akhir seluruh wilayah & Cross-Region Final Sweep.")
    parser.add_argument("--region", type=str, help="Override ID wilayah aktif (opsional, misal R_1).")
    parser.add_argument("--audit-dir", dest="audit_dir_flag", type=str, help="Path ke direktori kerja audit (flag --audit-dir).")
    parser.add_argument("audit_dir_pos", nargs="?", help="Path ke direktori kerja audit (argumen posisional).")

    args = parser.parse_args()

    if args.sync:
        return sync_all_routers()

    if args.intel:
        target_intel = args.audit_dir_flag or args.audit_dir_pos
        if not target_intel:
            parser.print_help()
            return 1
        intel_dir = Path(target_intel).resolve()
        intel_errors = validate_intel(intel_dir)
        if intel_errors:
            print(f"\n[INTEL FAIL] Ditemukan {len(intel_errors)} pelanggaran INTEL:", file=sys.stderr)
            for e in intel_errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        stage = deployment_stage(intel_dir)
        print(f"[INTEL PASS] INTEL.md sah — Deployment Stage: {stage}.")
        return 0

    if args.rules:
        target_rules = args.audit_dir_flag or args.audit_dir_pos
        if not target_rules:
            parser.print_help()
            return 1
        rules_dir = Path(target_rules).resolve()
        rule_errors = validate_wadah_rules(rules_dir)
        if rule_errors:
            print(f"\n[RULES FAIL] Ditemukan {len(rule_errors)} pelanggaran aturan wadah 06/07/08/09:", file=sys.stderr)
            for e in rule_errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print("[RULES PASS] Aturan 06/07/08/09 + jejak lead terpenuhi.")
        return 0

    target_dir = args.audit_dir_flag or args.audit_dir_pos
    if not target_dir:
        parser.print_help()
        return 1

    audit_path = Path(target_dir).resolve()
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