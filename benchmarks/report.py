#!/usr/bin/env python3
"""Rebuild every benchmark table and chart from the saved prompts, labels and answers in benchmarks/data and benchmarks/results (no model is run, no credit spent).

    python benchmarks/report.py        # writes benchmarks/results/tables.md, tables.json and charts/*.svg
"""
import collections
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, R = HERE / "data", HERE / "results"
SYS = ["jev", "dex", "stock-laya"]
NAME = {"jev": "JEV", "dex": "Dex", "stock-laya": "Stock Laya", "ablation-modernbert-base": "ModernBERT body, 285 task wordings", "ablation-modernbert-wide-instructions": "ModernBERT body, 1,080 task wordings"}


def jl(p):
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def pred(q, a):
    if a is None or "error" in a:
        return None
    if q["type"] == "noul":
        return float(a["noul"]) >= 0.5
    probs = a.get("probabilities") or {}
    if q["type"] == "score":
        return int(max(probs, key=probs.get)) if probs else None
    return a.get("choice")


def conf(q, a):
    if q["type"] == "noul":
        p = float(a["noul"])
        return max(p, 1 - p)
    probs = a.get("probabilities") or {}
    return max(probs.values()) if probs else None


def cell(k, n):
    lo, hi = wilson(k, n)
    return f"{k / n:.1%} ({lo:.0%}-{hi:.0%})" if n else "n/a"


def load_results(suite, systems):
    return {s: json.loads((R / f"{suite}-{s}.json").read_text()) for s in systems if (R / f"{suite}-{s}.json").exists()}


def collect():
    """items: (pool, suite-label, id, question, gold, qid, {system: answer dict}); every system's answer to the same prompt."""
    items = []
    allsys = SYS[1:] + ["ablation-modernbert-base", "ablation-modernbert-wide-instructions"]
    A = load_results("A", allsys)
    for x in jl(D / "usecases_items.jsonl"):
        (qid, q), = x["questions"].items()
        ans = {s: A[s].get(x["id"]) for s in A}
        items.append(("A", x["suite"], x["id"], q, x["gold"][qid], qid, ans))
    B = load_results("B", allsys)
    for r in jl(D / "heldout_tasks.jsonl"):
        ans = {s: B[s].get(r["id"]) for s in B}
        items.append(("B", "held-out tasks", r["id"], r["questions"]["q"], r["gold"]["q"], "q", ans))
    C = load_results("C", allsys)
    gold = json.loads((D / "exam_gold.json").read_text())
    for r in jl(D / "exam_items.jsonl"):
        for qid, q in r["questions"].items():
            g = gold.get(f"{r['id']}|{qid}")
            if g is None:
                continue
            ans = {s: C[s].get(r["id"]) for s in C}
            items.append(("C", r["dataset"], r["id"] + ":" + qid, q, g, qid, ans))
    return items


def score_items(items, systems):
    out = collections.defaultdict(lambda: {s: [0, 0] for s in systems})
    for pool, label, i, q, gold, qid, ans in items:
        for s in systems:
            a = ans.get(s)
            if not a or qid not in a:
                continue
            p = pred(q, a[qid])
            if p is None:
                continue
            for key in (pool, (pool, label)):
                out[key][s][0] += 1
                out[key][s][1] += int(p == gold)
    return out


def ece(pairs, bins=15):
    tot = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        sel = [(c, o) for c, o in pairs if (c > lo or b == 0) and c <= hi]
        if sel:
            tot += len(sel) / len(pairs) * abs(sum(c for c, _ in sel) / len(sel) - sum(o for _, o in sel) / len(sel))
    return tot


def bar_svg(title, rows, systems, path):
    """Grouped horizontal bars, accuracy 0-100, in a fixed palette that reads on light and dark."""
    colors = {"jev": "#7a8794", "dex": "#2f6fed", "stock-laya": "#d98a2b"}
    w, rh, left = 820, 22, 250
    h = 60 + len(rows) * (rh * len(systems) + 14)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica,Arial,sans-serif" font-size="12">',
         '<rect width="100%" height="100%" fill="#ffffff"/>', f'<text x="10" y="22" font-size="15" font-weight="bold" fill="#222">{title}</text>']
    lx = left
    for s in systems:
        o.append(f'<rect x="{lx}" y="32" width="12" height="12" fill="{colors[s]}"/><text x="{lx + 17}" y="42" fill="#333">{NAME[s]}</text>')
        lx += 120
    y = 60
    for label, vals in rows:
        o.append(f'<text x="10" y="{y + rh * len(systems) / 2 + 4}" fill="#333">{label}</text>')
        for s in systems:
            v = vals.get(s)
            if v is not None:
                bw = (w - left - 60) * v / 100
                o.append(f'<rect x="{left}" y="{y}" width="{bw:.1f}" height="{rh - 4}" fill="{colors[s]}"/><text x="{left + bw + 5:.1f}" y="{y + rh - 9}" fill="#333">{v:.1f}%</text>')
            y += rh
        y += 14
    o.append("</svg>")
    path.write_text("\n".join(o))


def main():
    items = collect()
    ab = ["ablation-modernbert-base", "ablation-modernbert-wide-instructions"]
    sc = score_items(items, SYS[1:] + ab)
    JS = json.loads((R / "jev_summary.json").read_text())      # JEV's results as summary numbers: [questions, correct] per test and per use case / dataset
    for key, v in JS["cells"].items():
        sc[tuple(key.split("|", 1)) if "|" in key else key]["jev"] = v
    L, J = [], {}
    # headline
    L += ["## Accuracy against the human label", "", "| test | questions | JEV | Dex | Stock Laya |", "|---|---|---|---|---|"]
    names = {"A": "A. Ten use cases", "B": "B. Tasks never trained on", "C": "C. Exam: 8 datasets never used"}
    tot = {s: [0, 0] for s in SYS}
    for pool in "ABC":
        row = sc[pool]
        for s in SYS:
            tot[s][0] += row[s][0]; tot[s][1] += row[s][1]
        L.append(f"| {names[pool]} | {max(v[0] for v in row.values())} | " + " | ".join(cell(row[s][1], row[s][0]) for s in SYS) + " |")
    L.append("| **All three** | " + str(max(v[0] for v in tot.values())) + " | " + " | ".join(f"**{tot[s][1] / tot[s][0]:.1%}**" for s in SYS) + " |")
    J["headline"] = {s: tot[s][1] / tot[s][0] for s in SYS}
    # A by use case
    L += ["", "## A. Ten use cases", "", "| use case | questions | JEV | Dex | Stock Laya |", "|---|---|---|---|---|"]
    rows = []
    for (pool, label), row in sorted(((k, v) for k, v in sc.items() if isinstance(k, tuple) and k[0] == "A"), key=lambda kv: int(kv[0][1].split()[0])):
        L.append(f"| {label} | {row['jev'][0]} | " + " | ".join(cell(row[s][1], row[s][0]) for s in SYS) + " |")
        rows.append((label, {s: 100 * row[s][1] / row[s][0] for s in SYS if row[s][0]}))
    bar_svg("Ten JEV use cases: accuracy against the human label", rows, SYS, HERE / "charts/usecases.svg")
    # C by dataset
    L += ["", "## C. Exam datasets, one by one (accuracy against the human label)", "", "| dataset | questions | JEV | Dex | Stock Laya |", "|---|---|---|---|---|"]
    rows = []
    for (pool, label), row in sorted((k, v) for k, v in sc.items() if isinstance(k, tuple) and k[0] == "C"):
        L.append(f"| {label.replace('x_', '')} | {row['jev'][0]} | " + " | ".join(cell(row[s][1], row[s][0]) for s in SYS) + " |")
        rows.append((label.replace("x_", ""), {s: 100 * row[s][1] / row[s][0] for s in SYS if row[s][0]}))
    bar_svg("Exam datasets: accuracy against the human label", rows, SYS, HERE / "charts/exam.svg")
    # who is right when they disagree
    L += ["", "## When a model and JEV disagree, who is right?", "", "| model | both right | JEV only | model only | both wrong | of the disagreements, the model is right |", "|---|---|---|---|---|---|"]
    for s in ("dex", "stock-laya"):
        c = collections.Counter(JS["disagree"][s])
        dis = c["JEV only"] + c["model only"]
        L.append(f"| {NAME[s]} | {c['both right']} | {c['JEV only']} | {c['model only']} | {c['both wrong']} | {c['model only'] / dis:.0%} |")
    # calibration
    L += ["", "## Is the confidence honest? (all three tests together)", "", "| system | accuracy | calibration error (lower is better) | sure (90%+): share of questions | sure (90%+): accuracy there |", "|---|---|---|---|---|"]
    for s in SYS:
        if s == "jev":
            k = JS["calibration"]
            L.append(f"| {NAME[s]} | {k['accuracy']:.1%} | {k['ece']:.3f} | {k['sure_share']:.0%} | {k['sure_accuracy']:.1%} |")
            continue
        pairs = []
        for pool, label, i, q, gold, qid, ans in items:
            a = ans.get(s)
            if not a or qid not in a:
                continue
            p, c = pred(q, a[qid]), conf(q, a[qid])
            if p is not None and c is not None:
                pairs.append((c, int(p == gold)))
        sure = [x for x in pairs if x[0] >= 0.9]
        L.append(f"| {NAME[s]} | {sum(o for _, o in pairs) / len(pairs):.1%} | {ece(pairs):.3f} | {len(sure) / len(pairs):.0%} | {sum(o for _, o in sure) / len(sure):.1%} |")
    # ablation
    L += ["", "## What helped (accuracy against the human label)", "", "| model | A. Ten use cases | B. Tasks never trained on | C. Exam datasets |", "|---|---|---|---|"]
    for s in ["stock-laya"] + ab + ["dex"]:
        L.append(f"| {NAME[s]} | " + " | ".join(cell(sc[p][s][1], sc[p][s][0]) for p in "ABC") + " |")
    # speed and order
    sp = json.loads((R / "speed.json").read_text())
    L += ["", f"## Speed and memory ({sp['gpu']}, median / 95th percentile in ms per call)", "", "| call | Dex | Stock Laya | JEV API |", "|---|---|---|---|"]
    for label in ("short", "long"):
        for k in (1, 3, 5, 10, 15):
            key = f"{label}/{k}"
            jv = sp.get("jev_api", {}).get("cells", {}).get(key)
            L.append(f"| {label} text, {k} question{'s' if k > 1 else ''} | {sp['dex']['cells'][key][0]:.0f} / {sp['dex']['cells'][key][1]:.0f} | {sp['stock_laya']['cells'][key][0]:.0f} / {sp['stock_laya']['cells'][key][1]:.0f} | " + (f"{jv[0]:.0f} / {jv[1]:.0f}" if jv else "-") + " |")
    L += ["", f"GPU memory after loading: Dex {sp['dex']['gpu_gb']} GB, Stock Laya {sp['stock_laya']['gpu_gb']} GB. Weights on disk: Dex {sp['weights_mb']['dex']} MB, Stock Laya {sp['weights_mb']['stock_laya']} MB."]
    od = json.loads((R / "order.json").read_text())
    L += ["", "## Answer-order check (400 multiple-choice questions, asked twice: as written and with the options reversed)", "", "| system | picks a different option when the order is reversed | accuracy as written | accuracy reversed |", "|---|---|---|---|"]
    for key, nm in (("jev", "JEV"), ("dex", "Dex"), ("stock_laya", "Stock Laya")):
        v = od[key]
        L.append(f"| {nm} | {v['flip_rate']:.1%} | {v['accuracy_as_written']:.1%} | {v['accuracy_reversed']:.1%} |")
    (R / "tables.md").write_text("\n".join(L) + "\n")
    (R / "tables.json").write_text(json.dumps(J, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    (HERE / "charts").mkdir(exist_ok=True)
    main()
