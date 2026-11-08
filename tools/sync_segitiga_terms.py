#!/usr/bin/env python3
"""sync_segitiga_terms.py — selaraskan istilah warisan di references/ ke Tahap A-F.

Dijalankan sekali saat migrasi metode. Idempoten: aman dijalankan berulang.

Yang dikerjakan:
  1. Tempel blok header penerapan segitiga ke setiap ref-*.md (sekali saja).
  2. Ganti istilah fase lama -> tahap baru, TANPA mengubah nama ID (M-001, POV-xx, AF-xx).
  3. Laporkan sisa istilah warisan yang tidak bisa diganti otomatis (perlu tangan manusia).

Pakai:
  python3 tools/sync_segitiga_terms.py --refs references --dry-run
  python3 tools/sync_segitiga_terms.py --refs references
"""
import argparse
import re
import sys
from pathlib import Path

MARKER = "<!-- SEGITIGA-BINDING -->"

HEADER = """<!-- SEGITIGA-BINDING -->
> **Penerapan segitiga.** Berkas ini dipakai di **Tahap C (`L-FLOW`)** sebagai generator
> hipotesis. Padanan istilah: `Fase 2` → **Tahap C**, `Fase 3` → **Tahap D**,
> `Fase 4` → **Tahap F**, `Fase 1` → **Tahap A/B**, `Fase 0` → **Tahap A0**,
> `Putaran 1/2` → **Tahap C**, `unit S-n` → **pot/jahitan**.
> Rujukan berkas lama (`00b`, `01`, `02`, `03`) tidak dipakai lagi — lihat
> `references/_INDEX-SEGITIGA.md`. Tiga sumbu lead: `[LAPIS]` × `[CLASS-x]` × `[AF-xx]`.

"""

# Urutan penting: yang lebih spesifik lebih dulu.
REPLACEMENTS = [
    # Rujukan berkas lama -> artefak segitiga
        (r"`03-attack-surface-queue\.md`", "`audit/notes/path-map.md` (peta jahitan)"),
    (r"03-attack-surface-queue\.md", "path-map.md (peta jahitan)"),
    (r"00b-file-inventory\.md", "money-ledger.md (census)"),
    (r"00-project-map\.md", "PIN.md"),
    (r"01-threat-and-env\.md", "FACTS.md (LINGKUNGAN/DATA)"),
    (r"02-state-and-var-matrix\.md", "FACTS.md (DATA)"),
    (r"`00b-file-inventory\.md`", "`audit/notes/money-ledger.md` (census)"),
    (r"`00-project-map\.md`", "`target/PIN.md`"),
    (r"`01-threat-and-env\.md`", "`audit/FACTS.md` (LINGKUNGAN/DATA)"),
    (r"`02-state-and-var-matrix\.md`", "`audit/FACTS.md` (DATA)"),
    (r"\bunit antrean\b", "pot/jahitan"),
    (r"\bunit `S-n`\b", "pot/jahitan"),
    (r"\bunit `\[CLASS-A\]`\b", "pot/jahitan `[CLASS-A]`"),
    (r"\bunit `\[CLASS-([ABC])\]`\b", r"pot/jahitan `[CLASS-\1]`"),
    (r"\bunit `S-\d+`\b", "pot/jahitan"),
    # Fase -> Tahap
    (r"\bFase 0\b", "Tahap A0"),
    (r"\bFase 1\b", "Tahap A/B"),
    (r"\bFase 2\b", "Tahap C"),
    (r"\bFase 3\b", "Tahap D"),
    (r"\bFase 4\b", "Tahap F"),
    (r"\bPutaran 1\b", "Tahap C putaran bedah"),
    (r"\bPutaran 2\b", "Tahap C putaran sintesis"),
    # Penamaan langkah internal Fase 3 -> Tahap D
    (r"Langkah 1b\b", "Langkah D-1b"),
    (r"Langkah 1c\b", "Langkah D-1c"),
]


def apply_header(text: str) -> tuple[str, bool]:
    """Sisipkan header bila belum ada. Dijalankan SETELAH apply_terms supaya
    istilah di dalam header (yang memang menyebut nama lama) tidak ikut tergantikan."""
    if MARKER in text:
        return text, False
    lines = text.splitlines(keepends=True)
    insert_at = 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    return "".join(lines[:insert_at]) + HEADER + "".join(lines[insert_at:]), True


def _protect(text: str) -> tuple[str, list[str]]:
    """Keluarkan blok SEGITIGA-BINDING dari teks sebelum substitusi.

    Blok itu SENGAJA memuat nama lama (`Fase 2` → Tahap C). Tanpa perlindungan ini,
    substitusi memakan namanya sendiri dan alat jadi tidak idempoten.
    """
    store: list[str] = []
    def swap(m):
        store.append(m.group(0))
        return f"\x00PROT{len(store)-1}\x00"
    text = re.sub(r"<!-- SEGITIGA-BINDING -->.*?(?=\n\n)", swap, text, flags=re.S)
    return text, store


def _restore(text: str, store: list[str]) -> str:
    for i, blk in enumerate(store):
        text = text.replace(f"\x00PROT{i}\x00", blk)
    return text


def apply_terms(text: str) -> tuple[str, int]:
    text, store = _protect(text)
    n = 0
    for pat, rep in REPLACEMENTS:
        text, k = re.subn(pat, rep, text)
        n += k
    return _restore(text, store), n


LEFTOVER = re.compile(r"\bFase [0-9]\b|\bPutaran [12]\b|\bunit `S-\d+`\b|`0[0-3]-[a-z-]+\.md`|`00b-[a-z-]+\.md`")
# Baris yang memang menjelaskan padanan istilah (boleh memuat istilah lama)
EXEMPT = re.compile(r"Penerapan segitiga|Padanan istilah|→ \*\*Tahap")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", default="references")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = Path(a.refs)
    files = sorted(p for p in root.glob("ref-*.md"))
    if not files:
        files = sorted(p for p in root.glob("*.md") if not p.name.startswith("_"))
    if not files:
        print(f"Tidak ada ref-*.md di {root}")
        return 1

    total_hdr = total_terms = 0
    leftovers = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        orig = text
        text, n = apply_terms(text)
        text, added = apply_header(text)
        if text != orig and not a.dry_run:
            tmp = p.with_suffix(".md.tmp")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(p)          # atomik: tidak pernah truncate in-place
        total_hdr += int(added)
        total_terms += n
        for i, ln in enumerate(text.splitlines(), 1):
            if LEFTOVER.search(ln) and not EXEMPT.search(ln):
                leftovers.append((p.name, i, ln.strip()[:110]))

    verb = "[dry-run] " if a.dry_run else ""
    print(f"{verb}header ditempel : {total_hdr} berkas")
    print(f"{verb}istilah diganti: {total_terms} kemunculan")
    if leftovers:
        print(f"\nSISA MANUAL ({len(leftovers)}) — perlu ditinjau manusia:")
        for f, i, ln in leftovers[:40]:
            print(f"  {f}:{i}  {ln}")
        if len(leftovers) > 40:
            print(f"  ... dan {len(leftovers) - 40} lagi")
    else:
        print("\nTidak ada istilah warisan tersisa (di luar baris padanan).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
