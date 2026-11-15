"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")




def run():
    from tda_ml.analysis import analyze
    points = [[0,0],[1,0],[1,1],[0,1]]
    def report(limit):
        return analyze({"schema_version":1,"points":points,"max_edge_length":limit})
    check("before edges: four components", report(.9)["betti_at_maximum"], [4,0])
    check("square edges: one component and one loop", report(1)["betti_at_maximum"], [1,1])
    loop = next(x for x in report(1)["intervals"] if x["dimension"] == 1)
    check("loop born at unit edge", loop["birth"], 1.0)
    check("unpaired interval is censored", loop["right_censored"], True)
    check("diagonals and triangles fill square", report(1.5)["betti_at_maximum"], [1,0])
    closed = next(x for x in report(1.5)["intervals"] if x["dimension"] == 1)
    check("death at square-root two", round(closed["death"]**2, 12), 2.0)
    rejects("nonfinite geometry rejected", lambda: analyze({"schema_version":1,"points":[[float("nan")]],"max_edge_length":1}))
    check("no execution authority", report(1)["execution_authorized"], False)

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
