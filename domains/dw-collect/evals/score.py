#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""evals 评分器：遍历 cases/*/check.py，汇总通过情况。
用法：python score.py [--case example-table-sync]
退出码：0=全绿（或全部SKIPPED） 1=有FAIL（含 check.py 异常退出）
"""
import subprocess, sys, argparse
from pathlib import Path

HERE = Path(__file__).parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=None)
    args = ap.parse_args()

    cases = sorted(HERE.glob("cases/*"))
    if args.case:
        cases = [c for c in cases if c.name == args.case]
    if not cases:
        print("no cases found"); sys.exit(2)

    exit_code = 0
    for c in cases:
        checker = c / "check.py"
        if not checker.exists():
            print(f"[MISSING] {c.name}: no check.py"); exit_code = 1; continue
        r = subprocess.run([sys.executable, "-X", "utf8", str(checker)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = (r.stdout or r.stderr).strip().splitlines()
        verdict = tail[-1] if tail else "(no output)"
        tag = {0: "GREEN", 1: "FAIL", 2: "SKIPPED"}.get(r.returncode, f"rc={r.returncode}")
        print(f"[{tag}] {c.name} — {verdict}")
        if r.returncode not in (0, 2): exit_code = 1   # 非全绿/非SKIPPED 一律判失败（含异常退出）

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
