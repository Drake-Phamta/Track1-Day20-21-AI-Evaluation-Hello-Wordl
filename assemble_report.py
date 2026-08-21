#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ghep deliverables/_parts/*.md -> deliverables/REPORT.md

Chay o T+125 (chi Tuan Anh chay). Muc dich: 3 nguoi viet 7 muc song song trong
7 file rieng -> khong ai cham vao REPORT.md -> git conflict = 0.

    python assemble_report.py            # ghep
    python assemble_report.py --check    # chi bao muc nao con cho trong, khong ghi file
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(ROOT, "deliverables", "_parts")
OUT = os.path.join(ROOT, "deliverables", "REPORT.md")

ORDER = ["01-input-grid", "02-dataset", "03-rubric", "04-routing",
         "05-calibration", "06-scorecard", "07-verdict"]

# dau hieu con la template chua dien
PLACEHOLDERS = [r"\(dan o day\)", r"\(dán ở đây\)", r"_{3,}", r"\|\s*\|\s*\|",
                r"^\s*\|\s*\.\.\.\s*\|", r"SHIP / CHƯA SHIP", r"Ship / Ship with conditions / Hold"]


def read(name):
    p = os.path.join(PARTS, name + ".md")
    if not os.path.exists(p):
        sys.exit("THIEU FILE: " + p)
    txt = io.open(p, encoding="utf-8").read()
    # bo dong banner OWNER
    return re.sub(r"^<!--\s*OWNER:.*?-->\s*\n+", "", txt, flags=re.S).strip()


def main():
    check_only = "--check" in sys.argv
    header = read("00-header")
    chunks, warn = [header], []

    for name in ORDER:
        body = read(name)
        chunks.append(body)
        hits = [p for p in PLACEHOLDERS if re.search(p, body, re.M)]
        if hits:
            warn.append("  [CHUA XONG] %s.md  <- con placeholder: %s" % (name, ", ".join(hits[:2])))

    doc = "\n\n---\n\n".join(chunks).rstrip() + "\n"

    for w in warn:
        print(w)
    print("--- %d/7 muc sach placeholder ---" % (7 - len(warn)))

    if check_only:
        return 1 if warn else 0

    io.open(OUT, "w", encoding="utf-8").write(doc)
    print("Da ghi %s (%d dong)" % (OUT, doc.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
