"""Smoke test against a running Dex server:  python tests/test_server.py [http://127.0.0.1:18766]
Checks the three question types answer, probabilities are valid, the field sets equal Jev's, bad input is rejected, and /health works."""
import json
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18766"
FIELDS = {"choice": {"type", "choice", "confidence", "probabilities"}, "score": {"type", "score", "confidence", "legend", "probabilities"}, "noul": {"type", "noul"}}


def post(body, path="/v1/systemone"):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        check.failed += 1


check.failed = 0
q = {"c": {"type": "choice", "instructions": "Which fruit is it?", "criteria": {"apple": "a red fruit", "banana": "a long yellow fruit", "cherry": "a small red fruit"}},
     "s": {"type": "score", "instructions": "How ripe?", "criteria": ["green", "ripe", "overripe"]},
     "n": {"type": "noul", "instructions": "Is it yellow?"}}
for path in ("/v1/systemone", "/api/v1/decide", "/v1/decide"):
    r = post({"state": "A long curved yellow fruit, slightly brown.", "questions": q}, path)
    check(f"{path} answers all three types", set(r["answers"]) == {"c", "s", "n"})
a = r["answers"]
check("choice picks an offered option", a["c"]["choice"] in q["c"]["criteria"])
check("choice probabilities sum to 1", abs(sum(a["c"]["probabilities"].values()) - 1) < 0.01)
check("score probabilities sum to 1", abs(sum(a["s"]["probabilities"].values()) - 1) < 0.01)
check("noul is a probability", 0 <= a["n"]["noul"] <= 1)
check("field sets equal Jev's", all(set(v) == FIELDS[v["type"]] for v in a.values()))
check("usage reports zero cost", r["usage"]["cost_usd"] == 0)
check("banana beats the other fruits on an obvious case", a["c"]["choice"] == "banana")
try:
    post({"state": "x"})
    check("missing questions is rejected", False)
except urllib.error.HTTPError as e:
    check("missing questions is rejected (422)", e.code == 422)
h = json.load(urllib.request.urlopen(BASE + "/health", timeout=10))
check("/health ok", h["ok"] is True)
sys.exit(1 if check.failed else 0)
