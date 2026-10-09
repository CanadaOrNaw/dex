#!/usr/bin/env python3
"""Answer-order check: does the model pick the same option when the options are listed in a different order?

    python benchmarks/order.py --stock PATH_TO_STOCK_LAYA [--n 400]

Takes multiple-choice questions (3 or more options) from the ten-use-case benchmark and from the held-out tasks, asks each one twice, once as written and once with
the option order reversed (same keys, same text), and counts how often the chosen option changes ("flip rate"). A model that reads the options should flip rarely;
one that leans on position flips often. Also reports accuracy against the human label in both orders.
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "benchmarks/data"


def load_server():
    path = next((ROOT / "server").glob("*_server.py"))
    spec = importlib.util.spec_from_file_location("srv", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reverse(q):
    return dict(q, criteria=dict(reversed(list(q["criteria"].items()))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stock", required=True)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--out", default=str(ROOT / "benchmarks/results/order-rerun.json"))
    a = ap.parse_args()
    pool = []
    for line in (DATA / "usecases_items.jsonl").read_text().splitlines():
        x = json.loads(line)
        (qid, q), = x["questions"].items()
        if q["type"] == "choice" and len(q["criteria"]) >= 3:
            pool.append({"id": "A" + x["id"], "state": x["state"], "qid": qid, "q": q, "gold": x["gold"][qid]})
    for line in (DATA / "heldout_tasks.jsonl").read_text().splitlines():
        r = json.loads(line)
        q = r["questions"]["q"]
        if q["type"] == "choice" and len(q["criteria"]) >= 3:
            pool.append({"id": "B" + r["id"], "state": r["state"], "qid": "q", "q": q, "gold": r["gold"]["q"]})
    random.Random(3).shuffle(pool)
    pool = pool[: a.n]
    print(len(pool), "choice questions with 3+ options", flush=True)
    res = {}

    def run(name, ask):
        flips = ok1 = ok2 = n = 0
        for it in pool:
            first = ask(it["state"], {it["qid"]: it["q"]})[it["qid"]]["choice"]
            second = ask(it["state"], {it["qid"]: reverse(it["q"])})[it["qid"]]["choice"]
            if first is None or second is None:
                continue
            n += 1
            flips += int(first != second)
            ok1 += int(first == it["gold"])
            ok2 += int(second == it["gold"])
        res[name] = {"questions": n, "flip_rate": round(flips / n, 4), "accuracy_as_written": round(ok1 / n, 4), "accuracy_reversed": round(ok2 / n, 4)}
        print(name, res[name], flush=True)

    from laya.agent import Agent
    srv = load_server()
    srv.MODEL_DIR = ROOT / "model"
    agent = srv.load()
    run("dex", lambda s, q: agent.system_one(s, q)["answers"])
    del agent
    torch.cuda.empty_cache()
    agent = Agent(a.stock, device="cuda")
    run("stock_laya", lambda s, q: agent.system_one(s, q)["answers"])
    Path(a.out).write_text(json.dumps(res, indent=1))
    print("saved", a.out)


if __name__ == "__main__":
    main()
