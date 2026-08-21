# -*- coding: utf-8 -*-
"""Sinh slides/index.html tu du lieu THAT trong deliverables/evidence/.

    python slides/build.py

Doc: dataset-v1 + v2, results-v1 + v2-gateway, labels.csv + labels-v2-gateway.csv,
     verdicts-v3-vs-gold.jsonl, va 3 file labels-<ten>.csv de tinh agreement.
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


def csv2(name):
    lab, note = {}, {}
    for i, line in enumerate(io.open(os.path.join(EV, name), encoding="utf-8")):
        if i == 0 or not line.strip():
            continue
        p = line.rstrip("\n").split(",", 2)
        lab[p[0]] = p[1]
        note[p[0]] = p[2] if len(p) > 2 else ""
    return lab, note


def contiguous(n, h):
    return True if not n else any(h[i:i + len(n)] == n for i in range(len(h) - len(n) + 1))


secs = {(s["doc_id"], s["section_id"]): s for s in tutor.load_corpus()}
ver = {r["scenario_id"]: r for r in jsonl("verdicts-v3-vs-gold.jsonl")}
gold, gnote = csv2("labels.csv")
v2lab, v2note = csv2("labels-v2-gateway.csv")


def build(ds_file, res_file, labels, notes, tag):
    ds = {r["scenario_id"]: r for r in jsonl(ds_file)}
    res = {r["scenario_id"]: r for r in jsonl(res_file)}
    out = []
    for sid in ds:
        d, r = ds[sid], res[sid]
        o = r.get("output") or {}
        srcs = []
        for s in (o.get("sources") or []):
            key = (s.get("doc_id"), s.get("section_id"))
            sec = secs.get(key)
            q = s.get("quote") or ""
            if not sec:
                st = "missing"
            else:
                qt, bt = tutor.tokens(q), tutor.tokens(sec["text"])
                st = ("verbatim" if contiguous(qt, bt)
                      else "stitched" if set(qt).issubset(set(bt))
                      else "foreign")
            srcs.append({"d": key[0], "s": key[1], "q": q, "st": st})
        sl = d["metadata"].get("slide")
        out.append({
            "id": sid, "set": tag,
            "q": d["input"], "exp": d["expected_scope"],
            "slide": (sl["id"] + " — " + sl["title"]) if sl else None,
            "scope": o.get("scope"), "ans": (o.get("answer") or "")[:900],
            "src": srcs, "fu": [str(x) for x in (o.get("followup_questions") or [])],
            "hum": labels.get(sid), "note": notes.get(sid, ""),
            "judge": (ver.get(sid) or {}).get("verdict"),
            "jr": ((ver.get(sid) or {}).get("rationale") or "")[:320],
            "lat": r.get("latency_s"), "cost": r.get("cost_usd"),
            "kb": 2 if len(r.get("retrieved") or []) == 10 else 1,
        })
    return sorted(out, key=lambda c: c["id"])


v1 = build("dataset-v1.jsonl", "results-v1.jsonl", gold, gnote, "v1")
v2 = build("dataset-v2-extra.jsonl", "results-v2-gateway.jsonl", v2lab, v2note, "v2")
cases = v1 + v2

# --- agreement 3 vong ---
labs = {n: csv2("labels-%s.csv" % n)[0] for n in ("chi", "hieu", "tuananh")}
ids = sorted(labs["chi"])
three = sum(1 for k in ids if labs["chi"][k] == labs["hieu"][k] == labs["tuananh"][k])


def pair(a, b):
    return sum(1 for k in ids if labs[a][k] == labs[b][k])


lat1 = [c["lat"] for c in v1]
data = {
    "cases": cases,
    "stats": {
        "n1": len(v1), "n2": len(v2),
        "cost": round(sum(c["cost"] for c in v1), 4),
        "secs": round(sum(lat1), 1),
        "latMed": sorted(lat1)[len(lat1) // 2],
        "kb2": sum(1 for c in v1 if c["kb"] == 2),
        "gold": dict(Counter(c["hum"] for c in v1)),
        "judgeAgree": sum(1 for c in v1 if c["judge"] == c["hum"]),
        "agree3": three,
        "pairs": {"chi-ta": pair("chi", "tuananh"), "hieu-ta": pair("hieu", "tuananh"),
                  "chi-hieu": pair("chi", "hieu")},
        "spread": {n: dict(Counter(labs[n].values())) for n in labs},
    },
}

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
# Chuoi "</script>" trong noi dung tutor se dong som the <script> -> phai cat ra.
payload = payload.replace("</", "<\\/")

tpl = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = tpl.replace("__DATA__", payload)
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(out)

st = data["stats"]
print("da ghi slides/index.html  (%d case: %d v1 + %d v2, %.1f KB)"
      % (len(cases), st["n1"], st["n2"], len(out) / 1024))
print("  nhan vang v1:", st["gold"], "| judge khop: %d/20" % st["judgeAgree"])
print("  agreement 3 vong: %d/20 | pairs: %s" % (st["agree3"], st["pairs"]))
