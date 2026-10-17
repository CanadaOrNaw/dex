"""Offline documentation examples: AST-selected pure functions and synthetic answers only."""
import argparse
import ast
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def source_functions(relative, names):
    tree = ast.parse((ROOT / relative).read_text(), filename=relative)
    selected = [node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in selected} == set(names), "source function moved or renamed"
    namespace = {}
    exec(compile(ast.Module(body=selected, type_ignores=[]), relative, "exec"), namespace)
    return namespace


def shape_example():
    shape = source_functions("server/dex_server.py", {"jev_shape"})["jev_shape"]
    answers = {
        "intent": {"type": "choice", "choice": "refund", "confidence": 0.8,
                   "probabilities": {"refund": 0.8, "information": 0.2}, "action": "ignore"},
        "severity": {"type": "score", "score": 2, "confidence": 0.7,
                     "legend": ["low", "medium", "high"],
                     "probabilities": {"0": 0.1, "1": 0.2, "2": 0.7}, "action": "ignore"},
        "refund": {"type": "noul", "noul": 0.9, "confidence": 0.9, "action": "ignore"},
    }
    before = copy.deepcopy(answers)
    result = shape(answers)
    return {"types": sorted(answer["type"] for answer in result.values()),
            "runtime_only_removed": all("action" not in a for a in result.values())
                                    and "confidence" not in result["refund"],
            "input_unchanged": answers == before}


def scoring_example():
    pred = source_functions("benchmarks/report.py", {"pred"})["pred"]
    rows = [("choice", {"choice": "refund"}, "refund"),
            ("score", {"probabilities": {"0": 0.1, "1": 0.2, "2": 0.7}}, 2),
            ("noul", {"noul": 0.5}, True), ("choice", None, None)]
    predictions = [pred({"type": kind}, answer) for kind, answer, _ in rows]
    accepted = [(p, gold) for p, (_, _, gold) in zip(predictions, rows) if p is not None]
    return {"predictions": predictions, "correct": sum(p == gold for p, gold in accepted),
            "scored": len(accepted)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example", choices=["shape", "scoring"])
    args = parser.parse_args()
    print(json.dumps(shape_example() if args.example == "shape" else scoring_example(), sort_keys=True))
