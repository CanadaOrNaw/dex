#!/usr/bin/env python3
"""Latency and memory: Dex and stock Laya in-process on the GPU, Dex through its HTTP endpoint.

    python benchmarks/speed.py --stock PATH_TO_STOCK_LAYA [--out benchmarks/results/speed-rerun.json]

Workload: one state, k yes/no questions (1, 3, 5, 10, 15) answered in a single call, a short state (~120 tokens) and a long state (~900 tokens);
3 warm-up calls, then 15 timed calls per cell; median and p95 in milliseconds. Memory is what the model holds on the GPU after loading.
"""
import argparse
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "server"))

SHORT = "Customer message: Hi, I was charged twice for my last invoice and the card statement shows both. Can you refund the duplicate and confirm by email? Thanks, this is a bit urgent."
LONG = (SHORT + " ") * 1 + " ".join(
    f"Earlier note {i}: the customer asked about delivery times, the plan tier, a change of billing address and whether the refund policy covers annual plans. The agent explained the policy and promised a follow-up within two days."
    for i in range(1, 17))
QS = [
    "Is the customer asking for a refund?", "Does the message sound urgent?", "Is the customer angry?", "Does the message mention a duplicate charge?", "Is a reply by email requested?",
    "Is this a billing problem?", "Does the customer mention a deadline?", "Is the customer threatening to cancel?", "Is a manager's approval likely needed?", "Is this message spam?",
    "Does it mention a card statement?", "Is the tone polite?", "Is the issue technical?", "Does it ask about delivery?", "Is this a first contact?"]


def questions(k):
    return {f"q{i}": {"type": "noul", "instructions": QS[i]} for i in range(k)}


def timed(fn, reps=15, warm=3):
    for _ in range(warm):
        fn()
    t = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        t.append((time.perf_counter() - t0) * 1000)
    t.sort()
    return round(statistics.median(t), 1), round(t[int(len(t) * 0.95) - 1], 1)


def local(name, agent, out):
    out[name] = {"gpu_gb": round(torch.cuda.memory_allocated() / 1e9, 2), "cells": {}}
    for label, state in (("short", SHORT), ("long", LONG)):
        for k in (1, 3, 5, 10, 15):
            q = questions(k)
            out[name]["cells"][f"{label}/{k}"] = timed(lambda: agent.system_one(state, q))
            print(name, label, k, out[name]["cells"][f"{label}/{k}"], flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stock", required=True)
    ap.add_argument("--dex", default=str(ROOT / "model"))
    ap.add_argument("--out", default=str(ROOT / "benchmarks/results/speed-rerun.json"))
    a = ap.parse_args()
    from laya.agent import Agent
    import dex_server
    out = {"gpu": torch.cuda.get_device_name(0), "weights_mb": {"dex": round((Path(a.dex) / "model.safetensors").stat().st_size / 1e6), "stock_laya": round((Path(a.stock) / "model.safetensors").stat().st_size / 1e6)}}
    base = torch.cuda.memory_allocated()
    dex_server.MODEL_DIR = Path(a.dex)
    agent = dex_server.load()
    local("dex", agent, out)
    del agent
    torch.cuda.empty_cache()
    agent = Agent(a.stock, device="cuda")
    local("stock_laya", agent, out)
    Path(a.out).write_text(json.dumps(out, indent=1))
    print("saved", a.out)


if __name__ == "__main__":
    main()
