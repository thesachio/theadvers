#!/usr/bin/env python3
"""bind_references.py — tempel blok PERAN per berkas referensi.

Kontrak eksplisit: tiap ref-*.md menjelaskan
  (a) peran & tahap utama,
  (b) tahap lain yang juga memakainya,
  (c) kontribusi ke sumbu lead ([LAPIS] / [CLASS] / [AF]),
  (d) kapan TIDAK dibuka (hemat token).

Dijalankan ulang = idempoten (blok lama diganti, bukan ditumpuk).
"""
import re
import sys
from pathlib import Path

BEGIN = "<!-- SEGITIGA-PERAN:BEGIN -->"
END = "<!-- SEGITIGA-PERAN:END -->"

# slugs: (peran, tahap_utama, tahap_lain, sumbu, kapan_tidak)
P = {
 "ref-method-registry": (
   "**Metode bedah inti** — registry M-001..M-010 + 5 Jalur Permissionless + CLASS-A/B/C.",
   "C (`L-FLOW`)",
   "B (menentukan kelas jahitan), D (routing uji), F (ambang gugur)",
   "`[CLASS-x]` (paket metode wajib) + `[LOAD: M-xxx]`",
   "Tidak perlu dibuka berulang kali — baca sekali per audit, lalu rujuk ID."),
 "ref-attacker-pov": (
   "**Router gejala → POV.** Satu-satunya pintu ke katalog POV; mencegah memuat 4 katalog sekaligus.",
   "C (`L-FLOW`)",
   "B (gejala jahitan), E (gejala off-chain)",
   "`[LOAD: POV-XX]`",
   "Jangan dibuka bila gejala kode belum terlihat — ia router, bukan bacaan."),
 "ref-pov-call": (
   "**Katalog POV**: penyerahan kontrol, subcall, callback, otoritas.",
   "C (`L-FLOW`)",
   "D (routing skenario PoC)",
   "`[LOAD: POV-CALL-xx]`",
   "Hanya dibuka bila router `ref-attacker-pov.md` menunjuk ke sini."),
 "ref-pov-defi": (
   "**Katalog POV**: oracle, likuidasi, bad debt, self-liquidation.",
   "C (`L-FLOW`)",
   "D (skenario Victim Seeding)",
   "`[LOAD: POV-DEFI-xx]`",
   "Hanya dibuka bila gejala DeFi/likuidasi muncul."),
 "ref-pov-math": (
   "**Katalog POV**: indeks akrual, inverse rounding, fee multi-hop.",
   "C (`L-FLOW`)",
   "B (jalur akrual antar-hop), D (fuzz parameter)",
   "`[LOAD: POV-MATH-xx]`",
   "Hanya dibuka bila ada aritmetika/akrual/pembulatan."),
 "ref-pov-chain": (
   "**Katalog POV**: EVM multicall, Solana CPI, Move PTB, TON async.",
   "C (`L-FLOW`)",
   "B (jahitan ASYNC — zona utama), D (harness per rantai)",
   "`[LOAD: POV-EVM/SOL/MOVE/TON-xx]`",
   "Hanya dibuka untuk rantai yang terdeteksi (lihat §3 berkas ini)."),
 "ref-calls-tokens-reentrancy": (
   "**Checklist**: token non-standar, hook, reentrancy, otoritas eksternal.",
   "C (`L-FLOW`)",
   "B (edge yang membawa callback)",
   "Konteks untuk `[AF-07]`, `[AF-10]`",
   "Tidak perlu bila pot tidak menyentuh token eksternal/callback."),
 "ref-math-and-vaults": (
   "**Checklist**: pembulatan, share accounting, konservasi nilai.",
   "C (`L-FLOW`)",
   "A (satuan & desimal saat census), D (fuzz batas)",
   "Konteks untuk `[AF-08]`",
   "Tidak perlu bila tidak ada share/vault/konversi."),
 "ref-defi-oracles-liquidation": (
   "**Checklist**: oracle staleness, manipulasi harga, jalur likuidasi.",
   "C (`L-FLOW`)",
   "B (valuasi vs eksekusi = jahitan), D (sandwich)",
   "Konteks untuk `[AF-09]`",
   "Tidak perlu bila pot tidak membaca harga eksternal."),
 "ref-chain-evm-tron": (
   "**Tooling rantai**: census, parity, batas RPC untuk EVM/Tron.",
   "A (`L-VALUE`)",
   "B, C, D, F (parity)",
   "Menentukan bentuk `File:Baris` & cara probe",
   "Tidak dibuka untuk target non-EVM."),
 "ref-chain-solana": (
   "**Tooling rantai**: account model, CPI, `.reload()`, batas Helius.",
   "A (`L-VALUE`)",
   "B, C, D, F",
   "Menentukan apakah lead valid di SVM",
   "Tidak dibuka untuk target non-Solana."),
 "ref-chain-sui-move": (
   "**Tooling rantai**: objek, capability, PTB.",
   "A (`L-VALUE`)",
   "B, C, D, F",
   "Menentukan apakah lead valid di Move",
   "Tidak dibuka untuk target non-Move."),
 "ref-chain-ton-async": (
   "**Tooling rantai**: model aktor asinkron, bounce, `recv_internal`.",
   "A (`L-VALUE`)",
   "B (zona ASYNC), C, D, F",
   "Menentukan apakah lead valid di TON",
   "Tidak dibuka untuk target non-TON."),
 "ref-test-evm-advanced": (
   "**Harness uji**: Tier 1-5 (fuzz stateful, differential, halmos).",
   "D (`SIMULASI`)",
   "F (menilai bukti)",
   "Menentukan Strike 3 valid atau tidak",
   "Tidak dibuka saat masih di Tahap A-C."),
 "ref-test-multichain-advanced": (
   "**Harness uji**: Tier 6 (Solana/Sui/TON).",
   "D (`SIMULASI`)",
   "F",
   "Menentukan Strike 3 valid atau tidak",
   "Tidak dibuka saat masih di Tahap A-C."),
 "ref-atomic-write": (
   "**Protokol penulisan**: anti-truncate, backup write-ahead, tulis atomik.",
   "**semua tahap** (aturan lintas-tahap)",
   "A-F — dipakai setiap kali menulis `audit/*.md`",
   "Tidak menyumbang sumbu; ia menjaga integritas artefak",
   "Wajib dibuka SEBELUM menulis apa pun; boleh dirujuk ulang singkat."),
}


def block(slug: str) -> str | None:
    if slug not in P:
        return None
    peran, utama, lain, sumbu, tidak = P[slug]
    return (
        f"{BEGIN}\n"
        f"**Peran.** {peran}\n\n"
        f"- **Tahap utama:** {utama}\n"
        f"- **Juga dipakai di:** {lain}\n"
        f"- **Kontribusi ke lead:** {sumbu}\n"
        f"- **Kapan TIDAK dibuka:** {tidak}\n"
        f"{END}\n\n"
    )


def main():
    root = Path("references")
    missing, done = [], 0
    for p in sorted(root.glob("ref-*.md")):
        slug = p.stem
        blk = block(slug)
        if blk is None:
            missing.append(slug)
            continue
        t = p.read_text(encoding="utf-8")
        # buang blok peran lama bila ada
        t = re.sub(r"<!-- SEGITIGA-PERAN:BEGIN -->.*?<!-- SEGITIGA-PERAN:END -->\n\n?",
                   "", t, flags=re.S)
        # sisipkan tepat sebelum blok SEGITIGA-BINDING (atau setelah judul H1)
        anchor = "<!-- SEGITIGA-BINDING -->"
        if anchor in t:
            t = t.replace(anchor, blk + anchor, 1)
        else:
            lines = t.splitlines(keepends=True)
            i = 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            t = "".join(lines[:i]) + blk + "".join(lines[i:])
        tmp = p.with_suffix(".md.tmp")
        tmp.write_text(t, encoding="utf-8")
        tmp.replace(p)
        done += 1
    print(f"blok peran ditulis: {done} berkas")
    if missing:
        print("TANPA PETA (perlu ditambahkan ke P):")
        for s in missing:
            print("  ", s)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
