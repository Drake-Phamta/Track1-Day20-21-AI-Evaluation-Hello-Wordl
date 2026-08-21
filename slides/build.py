# -*- coding: utf-8 -*-
"""Sinh slides/index.html tu du lieu THAT trong deliverables/evidence/.

    python slides/build.py

Doc: dataset-v1.jsonl, results-v1.jsonl, labels.csv, verdicts-v3-vs-gold.jsonl
Ghi: slides/index.html  (self-contained, khong CDN tru Google Fonts)

Chay lai script nay moi khi so lieu doi — dung sua tay index.html.
"""
import io, json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EV = os.path.join(ROOT, "deliverables", "evidence")
sys.path.insert(0, os.path.join(ROOT, "tutor"))
import tutor  # noqa


def jsonl(name):
    return [json.loads(l) for l in io.open(os.path.join(EV, name), encoding="utf-8") if l.strip()]


def contiguous(n, h):
    return True if not n else any(h[i:i + len(n)] == n for i in range(len(h) - len(n) + 1))


secs = {(s["doc_id"], s["section_id"]): s for s in tutor.load_corpus()}
ds = {r["scenario_id"]: r for r in jsonl("dataset-v1.jsonl")}
res = {r["scenario_id"]: r for r in jsonl("results-v1.jsonl")}
ver = {r["scenario_id"]: r for r in jsonl("verdicts-v3-vs-gold.jsonl")}

labels, notes = {}, {}
for i, line in enumerate(io.open(os.path.join(EV, "labels.csv"), encoding="utf-8")):
    if i == 0 or not line.strip():
        continue
    p = line.rstrip("\n").split(",", 2)
    labels[p[0]] = p[1]
    notes[p[0]] = p[2] if len(p) > 2 else ""

cases = []
for sid in ds:
    d, r = ds[sid], res[sid]
    o = r.get("output") or {}
    srcs = []
    for s in (o.get("sources") or []):
        key = (s.get("doc_id"), s.get("section_id"))
        sec = secs.get(key)
        q = s.get("quote") or ""
        if not sec:
            st = "missing"          # section khong ton tai -> bia nguon
        else:
            qt, bt = tutor.tokens(q), tutor.tokens(sec["text"])
            st = ("verbatim" if contiguous(qt, bt)
                  else "stitched" if set(qt).issubset(set(bt))
                  else "foreign")   # co tu khong co trong section (vd quote da dich)
        srcs.append({"d": key[0], "s": key[1], "q": q, "st": st})
    sl = d["metadata"].get("slide")
    cases.append({
        "id": sid,
        "q": d["input"],
        "exp": d["expected_scope"],
        "slide": (sl["id"] + " — " + sl["title"]) if sl else None,
        "scope": o.get("scope"),
        "ans": (o.get("answer") or "")[:900],
        "src": srcs,
        "fu": [str(x) for x in (o.get("followup_questions") or [])],
        "hum": labels.get(sid), "note": notes.get(sid, ""),
        "judge": (ver.get(sid) or {}).get("verdict"),
        "jr": ((ver.get(sid) or {}).get("rationale") or "")[:320],
        "lat": r.get("latency_s"), "cost": r.get("cost_usd"),
        "kb": 2 if len(r.get("retrieved") or []) == 10 else 1,
    })
cases.sort(key=lambda c: c["id"])

lat = [c["lat"] for c in cases]
data = {
    "cases": cases,
    "stats": {
        "n": len(cases),
        "cost": round(sum(c["cost"] for c in cases), 4),
        "secs": round(sum(lat), 1),
        "latMed": sorted(lat)[len(lat) // 2],
        "tok": sum((res[c["id"]]["usage"] or {}).get("total_tokens", 0) for c in cases),
        "kb2": sum(1 for c in cases if c["kb"] == 2),
        "human": dict(Counter(c["hum"] for c in cases)),
        "judgeAgree": sum(1 for c in cases if c["judge"] == c["hum"]),
    },
}

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
# Chuoi "</script>" trong noi dung tutor se dong som the <script> -> phai cat ra.
payload = payload.replace("</", "<\\/")

tpl = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = tpl.replace("__DATA__", payload)
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(out)

print("da ghi slides/index.html  (%d case, %.1f KB)" % (len(cases), len(out) / 1024))
print("  human:", data["stats"]["human"], "| judge khop nhan vang: %d/20" % data["stats"]["judgeAgree"])
