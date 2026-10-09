"""Dex: an open-source, Jev-compatible, non-autoregressive System 1 decision model, served over HTTP.

Same request and response shape as TypeSafe Jev:

    POST /v1/systemone        (also /api/v1/decide and /v1/decide)
    {"state": "...", "questions": {"id": {"type": "choice|score|noul", "instructions": "...", "criteria": ...}}}
 -> {"model": "dex-1b", "answers": {...}, "usage": {"input_tokens": n, "output_tokens": 0, "cost_usd": 0}}

    GET  /health              -> {"ok": true, "model": "dex-1b", "device": "cuda", "dtype": "bfloat16"}

Standard library HTTP server plus the open `laya` runtime (pip install laya) for the typed-decision head and scoring; Dex supplies the Ettin-1B encoder weights.
Loopback by default, no key. One forward pass at a time (the runtime is not thread-safe).

    DEX_MODEL   model directory (default: ../model next to this file)
    DEX_DEVICE  cuda (default, falls back to cpu) or cpu
    DEX_HOST    bind address (default 127.0.0.1)
    DEX_TOKEN   if set, requests must send  Authorization: Bearer <token>
    DEX_EXTRAS  set to 1 to also return the runtime's extra fields (confidence on yes/no answers, action); off by default so answers match JEV's schema exactly
"""
from __future__ import annotations

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import torch
from laya.agent import Agent

NAME = "dex-1b"
MODEL_DIR = Path(os.environ.get("DEX_MODEL", Path(__file__).resolve().parent.parent / "model"))
TOKEN = os.environ.get("DEX_TOKEN", "")
MAX_BODY = 1_000_000
POST_PATHS = {"/v1/systemone", "/api/v1/decide", "/v1/decide"}
LOCK = threading.Lock()
AGENT: Agent | None = None
EXTRAS = os.environ.get("DEX_EXTRAS", "") == "1"


def jev_shape(answers: dict) -> dict:
    """JEV's answer fields only: choice {type, choice, confidence, probabilities}; score {type, score, confidence, legend, probabilities}; noul {type, noul}."""
    keep = {"choice": ("type", "choice", "confidence", "probabilities"), "score": ("type", "score", "confidence", "legend", "probabilities"), "noul": ("type", "noul")}
    return {qid: {k: a[k] for k in keep[a["type"]] if k in a} for qid, a in answers.items()}


def load() -> Agent:
    """Load on the CPU, keep the 1.1B encoder in bfloat16, then move to the GPU: a full-precision copy (4.4 GB) never touches an 8 GB card."""
    agent = Agent(str(MODEL_DIR), device="cpu")
    agent.model.encoder.to(torch.bfloat16)
    want = os.environ.get("DEX_DEVICE", "cuda")
    if want == "cuda" and torch.cuda.is_available():
        agent.model.to("cuda")
        agent.device = torch.device("cuda")
        agent.dtype = torch.bfloat16
    return agent


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _authorised(self) -> bool:
        return not TOKEN or self.headers.get("Authorization", "") == f"Bearer {TOKEN}"

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"ok": AGENT is not None, "model": NAME, "device": str(AGENT.device), "dtype": "bfloat16"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in POST_PATHS:
            self._send(404, {"error": "not found"})
            return
        if not self._authorised():
            self._send(401, {"error": "missing or wrong bearer token"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            self._send(413, {"error": "bad size"})
            return
        try:
            body = json.loads(self.rfile.read(length))
            with LOCK:
                result = AGENT.system_one(body.get("state"), body["questions"])
        except (ValueError, KeyError, TypeError) as exc:
            self._send(422, {"error": str(exc)[:200]})
            return
        usage = dict(result.get("usage") or {})
        usage["cost_usd"] = 0
        self._send(200, {"model": NAME, "answers": result["answers"] if EXTRAS else jev_shape(result["answers"]), "usage": usage})

    def log_message(self, *args) -> None:
        return


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18766
    AGENT = load()
    AGENT.system_one("warm up", {"w": {"type": "noul", "instructions": "Is this a warm-up?"}})
    ThreadingHTTPServer((os.environ.get("DEX_HOST", "127.0.0.1"), port), Handler).serve_forever()  # NOSONAR python:S5332
