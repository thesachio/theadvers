#!/usr/bin/env python3
"""verify_segitiga.py — gate checker METHODOLOGY-SEGITIGA untuk theadvers.

Menguji aturan yang paling sering dilanggar:
  G1  setiap entri 05 punya [LAPIS: ...] dan [AF-xx]
  G2  setiap entri 05 punya File:Baris berupa RENTANG (awal-akhir), bukan satu baris
  G3  setiap entri 06 yang REJECTED_POC_FAILS / NEGATIVE_EV / DUST punya BUKTI_SIMULASI
  G4  setiap entri 07 punya blok PERCOBAAN dengan minimal satu keluaran nyata
  G5  setiap entri 09/08 punya BUKTI_SIMULASI
  G6  STATE.md <= 50 baris, scratchpad <= 10 baris
  G7  tidak ada file audit/*.md berukuran 0 byte
  G8  tag AF-xx yang dipakai ada di registry mod-attack-forms.md

Pakai: python3 tools/verify_segitiga.py [--audit-dir audit]
Exit 0 = semua gerbang PASS.
"""
import argparse
import re
import sys
from pathlib import Path

AF_REGISTRY = Path(__file__).resolve().parent.parent / "methodology" / "mod-attack-forms.md"
ENTRY_RE = re.compile(r"^## \[(LEAD|GUARD|RADAR)-", re.M)
LAPIS_RE = re.compile(r"\[LAPIS:\s*(VALUE|PATH|FLOW)\]")
AF_RE = re.compile(r"\[AF-(\d{2})\]")
CLASS_RE = re.compile(r"\[CLASS-([ABC])\]")
valid_class = {"A", "B", "C"}
RANGE_RE = re.compile(r"(\.sol|\.rs|\.move|\.ts):\d+[-–]\d+")
STRIKE_HARD = ("REJECTED_POC_FAILS", "REJECTED_NEGATIVE_EV", "REJECTED_DUST")


def strip_fenced(text):
    """Buang isi blok ```...``` agar format contoh tidak terbaca sebagai entri."""
    out, inside = [], False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else ln)
    return "\n".join(out)


def entries(text, fence=False):
    """Pecah markdown jadi blok per entri '## [..]'.

    fence=False: heading di dalam blok ``` diabaikan (dipakai untuk enumerasi entri).
    fence=True : heading di dalam blok ``` DIPERTAHANKAN beserta isinya
                 (dipakai untuk memeriksa keluaran PERCOBAAN/BUKTI_SIMULASI).

    Kedua jalur WAJIB menghasilkan jumlah blok yang sama untuk file yang sama, karena
    `fence=True` hanya menambah isi, bukan menambah entri. Heading di dalam fence
    tetapi BUKAN bagian dari entri nyata dibuang dengan menyelaraskan pada entri non-fence.
    """
    src = text if fence else strip_fenced(text)
    idx = [m.start() for m in ENTRY_RE.finditer(src)]
    out = []
    for i, start in enumerate(idx):
        end = idx[i + 1] if i + 1 < len(idx) else len(src)
        out.append(src[start:end])
    if not fence:
        return out
    # Selaraskan: buang blok fence yang heading-nya tidak ada di enumerasi non-fence.
    real = [strip_fenced(b) for b in entries(text, fence=False)]
    aligned = []
    for b in out:
        if any(strip_fenced(b).startswith(r[:60]) for r in real):
            aligned.append(b)
    return aligned


def has_real_output(block):
    """Blok PERCOBAAN/BUKTI_SIMULASI harus punya baris $ dan baris keluaran setelahnya."""
    lines = block.splitlines()
    seen_cmd = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("$ "):
            seen_cmd = True
            continue
        if seen_cmd and s and not s.startswith("#") and not s.startswith("- "):
            return True
        if seen_cmd and s.startswith("# ") and len(s) > 3:
            return True
    return False



def pair(es, esf, tag, fails):
    """Pasangkan enumerasi entri dengan blok ber-fence. Panjang beda = FAIL keras,
    karena zip() diam-diam membandingkan blok yang salah (bug nyata pada versi awal)."""
    if len(es) != len(esf):
        fails.append(f"TOOL: {tag} enumerasi {len(es)} != fence {len(esf)} — parser tak sejajar")
        return list(zip(es, es))
    return list(zip(es, esf))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", default="audit")
    args = ap.parse_args()
    ad = Path(args.audit_dir)
    fails, warns, stats = [], [], {}

    # G8: registry AF yang sah
    valid_af = set()
    if AF_REGISTRY.exists():
        valid_af = set(re.findall(r"\[AF-(\d{2})\]", AF_REGISTRY.read_text()))
    else:
        warns.append(f"G8: registry AF tidak ditemukan di {AF_REGISTRY}")

    # G1 + G2: leads
    p05 = ad / "05-raw-leads.md"
    if p05.exists():
        es = entries(p05.read_text())
        stats["05"] = len(es)
        for e in es:
            title = e.splitlines()[0][:80]
            if not LAPIS_RE.search(e):
                fails.append(f"G1: {title} -> tanpa tag [LAPIS: VALUE|PATH|FLOW]")
            afs = AF_RE.findall(e)
            if not afs:
                fails.append(f"G1: {title} -> tanpa tag [AF-xx]")
            for af in afs:
                if valid_af and af not in valid_af:
                    fails.append(f"G8: {title} -> [AF-{af}] tidak ada di registry")
            # G9: CLASS wajib (sumbu lama yang tetap mengikat — menentukan paket metode)
            classes = CLASS_RE.findall(e)
            if not classes:
                fails.append(f"G9: {title} -> tanpa tag [CLASS-A|CLASS-B|CLASS-C]")
            for c in set(classes):
                if c not in valid_class:
                    fails.append(f"G9: {title} -> [CLASS-{c}] bukan nilai sah")
            if not RANGE_RE.search(e):
                fails.append(f"G2: {title} -> File:Baris bukan rentang (awal-akhir)")

    # G3: refuted wajib bukti
    p06 = ad / "06-refuted-invalid.md"
    if p06.exists():
        raw6 = p06.read_text()
        es = entries(raw6)
        esf = entries(raw6, fence=True)
        stats["06"] = len(es)
        for e, ef in pair(es, esf, '06', fails):
            if any(k in e for k in STRIKE_HARD):
                if "BUKTI_SIMULASI" not in ef:
                    fails.append(f"G3: {e.splitlines()[0][:80]} -> butuh BUKTI_SIMULASI")
                elif not has_real_output(ef):
                    fails.append(f"G3: {e.splitlines()[0][:80]} -> BUKTI_SIMULASI tanpa keluaran nyata")

    # G4: 07 wajib PERCOBAAN
    p07 = ad / "07-needs-next-step.md"
    if p07.exists():
        raw7 = p07.read_text()
        es = entries(raw7)
        esf = entries(raw7, fence=True)
        stats["07"] = len(es)
        if es:
            warns.append(f"G4: 07 berisi {len(esf)} entri (target akhir = 0)")
        for e, ef in pair(es, esf, '07', fails):
            if "PERCOBAAN" not in ef or not has_real_output(ef):
                fails.append(f"G4: {e.splitlines()[0][:80]} -> PERCOBAAN tanpa keluaran nyata")

    # G5: 08/09 wajib bukti
    for name in ("08-valid-not-eligible.md", "09-confirmed-findings.md"):
        p = ad / name
        if not p.exists():
            continue
        raw = p.read_text()
        es = entries(raw)
        esf = entries(raw, fence=True)
        stats[name[:2]] = len(es)
        for e, ef in pair(es, esf, name, fails):
            if "BUKTI_SIMULASI" not in ef or not has_real_output(ef):
                fails.append(f"G5: {name} {e.splitlines()[0][:60]} -> butuh BUKTI_SIMULASI nyata")

    # G6: STATE
    pst = ad / "STATE.md"
    if pst.exists():
        txt = pst.read_text()
        n = len(txt.splitlines())
        if n > 50:
            fails.append(f"G6: STATE.md {n} baris (maks 50)")
        m = re.search(r"## 4\..*?(?=\n## |\Z)", txt, re.S)
        if m:
            inner = [l for l in m.group(0).splitlines()[1:] if l.strip().startswith("-")]
            if len(inner) > 10:
                fails.append(f"G6: scratchpad {len(inner)} baris (maks 10)")

    # G7: file kosong
    for p in sorted(ad.glob("*.md")):
        if p.stat().st_size == 0:
            fails.append(f"G7: {p.name} 0 byte")

    # G10: istilah warisan di artefak audit (regresi terminologi)
    # Sengaja hanya memeriksa audit/*.md — dokumen pemetaan (AUTOPILOT-MAPPING, _INDEX-SEGITIGA)
    # memang WAJIB menyebut nama lama, dan referensi menjelaskannya di blok padanan.
    LEGACY = re.compile(r"\bFase [0-4]\b|\bPutaran [12]\b|\bunit `S-\d+`\b|`0[0-3]-[a-z-]+\.md`|`00b-[a-z-]+\.md`")
    EXEMPT = re.compile(r"Padanan istilah|→ \*\*Tahap|Peran berkas|SEGITIGA-BINDING")
    for p in sorted(ad.rglob("*.md")):
        for i, ln in enumerate(p.read_text().splitlines(), 1):
            if LEGACY.search(ln) and not EXEMPT.search(ln):
                fails.append(f"G10: {p.relative_to(ad)}:{i} istilah warisan -> {ln.strip()[:70]}")
                break

    # G11: setiap berkas referensi wajib punya blok PERAN (bukan header seragam)
    refdir = Path(__file__).resolve().parent.parent / "references"
    if refdir.is_dir():
        for rp in sorted(refdir.glob("ref-*.md")):
            body = rp.read_text(encoding="utf-8")
            if "SEGITIGA-PERAN:BEGIN" not in body:
                fails.append(f"G11: {rp.name} tanpa blok SEGITIGA-PERAN (tahap peran tidak jelas)")
            elif "**Tahap utama:**" not in body:
                fails.append(f"G11: {rp.name} blok PERAN tanpa field Tahap utama")

    print("=== verify_segitiga ===")
    print("entri:", ", ".join(f"{k}={v}" for k, v in stats.items()) or "-")
    for w in warns:
        print("WARN ", w)
    for f in fails:
        print("FAIL ", f)
    print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
