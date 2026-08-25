#!/usr/bin/env python3
"""SVORAH taint-engine corpus benchmark runner.

Two modes:

  # 1) Integrity check — no engine needed. Confirms every file:line the answer key
  #    points at actually exists. Run this any time you edit the corpus.
  python -m tests.recall_benchmark --validate

  # 2) Scoring — diff a real scan against expected.yaml.
  python -m tests.recall_benchmark --findings scan.json

`scan.json` is a JSON list of findings, each: {"file": "<repo-relative>", "line": N,
"severity": "CRITICAL|HIGH|MEDIUM", "control": "DPDP-..."}. Adapt SVORAH's output to
this shape (or extend load_findings()).

Exit code is non-zero on any failure, so this is CI-friendly.
"""
import argparse
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED = os.path.join(ROOT, "expected.yaml")

GREEN, RED, DIM, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[0m"


def load_expected(path=EXPECTED):
    with open(path) as f:
        return yaml.safe_load(f)


# --------------------------------------------------------------------------- #
# Normalise the heterogeneous manifest into two flat views:
#   fires  = [(id, file, line, severity)]   -> a finding MUST exist here
#   silent = set(file)                        -> these files/paths must yield NOTHING
# --------------------------------------------------------------------------- #
def normalise(exp):
    """Flatten the manifest into three views:
      fires   -> a finding MUST exist here (scored)
      silent  -> these files must yield NOTHING (scored)
      targets -> aspirational / unbuilt cases (status: target): validated for
                 file:line integrity, but EXCLUDED from pass/fail scoring so a
                 run never counts an unbuilt feature as a bug.
    """
    fires, silent, targets = [], set(), []

    def add(bucket, cid, file, line, sev=None):
        if file and isinstance(line, int):
            bucket.append((cid, file, line, sev))

    for p in exp.get("positives", []):
        if p.get("line"):
            add(fires, p["id"], p["file"], p["line"], p.get("severity"))

    for n in exp.get("negatives", []):
        if n.get("file"):
            silent.add(n["file"])

    for c in exp.get("crosschecks", []):
        bucket = targets if c.get("status") == "target" else fires
        file = c.get("file")
        for e in c.get("expect", []):
            if isinstance(e, dict) and e.get("line") and e.get("fires") is not False:
                add(bucket, c["id"], file, e["line"], e.get("severity"))

    for r in exp.get("fn_resistance", []):
        if r.get("covered_by"):
            continue
        if r.get("sink"):  # interprocedural: finding at the sink
            s = r["sink"]
            add(fires, r["id"], s["file"], s["line"], r.get("severity"))
        for e in r.get("expect", []):
            add(fires, r["id"], r["file"], e["line"], e.get("severity"))

    for fp in exp.get("fp_resistance", []):
        if fp.get("file"):
            silent.add(fp["file"])

    for o in exp.get("ordering", []):
        for e in o.get("expect", []):
            if e.get("fires") is not False and e.get("line"):
                add(fires, o["id"], o["file"], e["line"], e.get("severity"))

    # Cross-border region hints: an unbuilt (target) capability by default.
    xb = exp.get("cross_border_region_hints") or exp.get("cross_border_vendors")
    if xb:
        bucket = targets if xb.get("status") == "target" else fires
        for e in xb.get("expect", []):
            add(bucket, "XB-REGION", xb["file"], e["line"], e.get("severity"))

    return fires, silent, targets


def load_excluded_paths():
    cfg = os.path.join(ROOT, ".svorah.yml")
    if not os.path.exists(cfg):
        return []
    data = yaml.safe_load(open(cfg)) or {}
    return data.get("excluded_paths", []) or []


def under_excluded(path, patterns):
    import fnmatch
    for pat in patterns:
        base = pat.rstrip("*").rstrip("/")
        if base and (path or "").startswith(base + "/"):
            return True
        if fnmatch.fnmatch(path or "", pat) or fnmatch.fnmatch(path or "", pat.replace("**", "*")):
            return True
    return False


# --------------------------------------------------------------------------- #
def line_count(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def read_line(path, line):
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, txt in enumerate(f, 1):
            if i == line:
                return txt.rstrip("\n")
    return None


def validate(exp):
    fires, silent, targets = normalise(exp)
    errors = []
    checked = 0

    all_refs = fires + targets
    all_files = {f for _, f, _, _ in all_refs} | silent
    for f in sorted(all_files):
        if not os.path.exists(os.path.join(ROOT, f)):
            errors.append(f"missing file referenced by manifest: {f}")

    for cid, f, line, _ in all_refs:
        full = os.path.join(ROOT, f)
        if not os.path.exists(full):
            continue
        n = line_count(full)
        checked += 1
        if not (1 <= line <= n):
            errors.append(f"{f}:{line} out of range (1..{n})  [{cid}]")

    print(f"{DIM}validated {checked} line refs across {len(all_files)} files "
          f"({len(fires)} scored, {len(targets)} target/xfail){RESET}")
    if errors:
        for e in errors:
            print(f"{RED}  ✗ {e}{RESET}")
        print(f"\n{RED}INTEGRITY FAIL: {len(errors)} problem(s){RESET}")
        return False
    print(f"{GREEN}INTEGRITY OK — every answer-key file:line resolves.{RESET}")
    return True


def load_findings(path):
    with open(path) as f:
        return json.load(f)


def score(exp, findings_path):
    fires, silent, targets = normalise(exp)
    findings = load_findings(findings_path)
    fire_index = {(f, ln): (cid, sev) for cid, f, ln, sev in fires}
    target_keys = {(f, ln) for _, f, ln, _ in targets}
    excluded = load_excluded_paths()

    tp, fp, sev_mismatch = 0, 0, []
    hit = set()
    for fnd in findings:
        key = (fnd.get("file"), fnd.get("line"))
        if key in target_keys:
            continue  # target/unbuilt: neither credit nor penalty
        if excluded and under_excluded(key[0], excluded):
            print(f"{RED}  CONFIG? finding under excluded path {key[0]}:{key[1]} "
                  f"— was .svorah.yml applied before scoring?{RESET}")
        if key in fire_index:
            tp += 1
            hit.add(key)
            _, want = fire_index[key]
            got = fnd.get("severity")
            if want and got and want != got:
                sev_mismatch.append((key, want, got))
        else:
            fp += 1
            print(f"{RED}  FP  {key[0]}:{key[1]}{RESET}")

    total_fires = len(fire_index)
    missed = [k for k in fire_index if k not in hit]
    for k in missed:
        print(f"{RED}  MISS {k[0]}:{k[1]}  [{fire_index[k][0]}]{RESET}")
    for key, want, got in sev_mismatch:
        print(f"{RED}  SEV  {key[0]}:{key[1]} expected {want}, got {got}{RESET}")

    recall = 100.0 * len(hit) / total_fires if total_fires else 0.0
    precision = 100.0 * tp / (tp + fp) if (tp + fp) else 0.0
    print(f"\nrecall    {recall:6.1f}%  ({len(hit)}/{total_fires})   target >= 95%")
    print(f"precision {precision:6.1f}%  ({tp}/{tp + fp})    target 100%")
    print(f"false positives: {fp}   severity mismatches: {len(sev_mismatch)}")
    if targets:
        print(f"{DIM}{len(targets)} target/xfail case(s) excluded from scoring "
              f"(unbuilt features){RESET}")
    ok = recall >= 95.0 and fp == 0 and not sev_mismatch
    print((GREEN + "PASS" + RESET) if ok else (RED + "FAIL" + RESET))
    return ok


def main():
    ap = argparse.ArgumentParser(description="SVORAH corpus benchmark runner")
    ap.add_argument("--repo", default=ROOT, help="repo root (default: this repo)")
    ap.add_argument("--expected", default=EXPECTED)
    ap.add_argument("--validate", action="store_true",
                    help="check every answer-key file:line exists (no engine needed)")
    ap.add_argument("--findings", help="scanner output JSON to score against expected.yaml")
    args = ap.parse_args()

    exp = load_expected(args.expected)
    if args.findings:
        ok = score(exp, args.findings)
    else:
        ok = validate(exp)  # default action
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
