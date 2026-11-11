# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

"""AP-AMMO footprint pipeline driver.

Runs the pipeline in the documented order, using the canonical scenario names
(CURR, EAT, CURR_MTFR, EAT_MTFR, MTFR_EAT) and the AP-AMMO production data for
the base year.

Stages
------
base    A1: base-year allocation to consumption (AP-AMMO emissions)
phd     A2: diet + N-balance chain + allocation (EAT)
mtfr    A3: MTFR alone and PHD+MTFR, production side

Usage
-----
    python run_pipeline.py
    python run_pipeline.py --only base
    python run_pipeline.py --from phd
    python run_pipeline.py --list
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGS = HERE / "logs"

STAGES = [
    ("base", ["A1_base.py"]),
    ("phd", ["A2_phd.py"]),
    ("mtfr", ["A3_mtfr.py"]),
]


def run_stage(name: str, scripts: list[str]) -> bool:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / f"{name}.log"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(HERE) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONUNBUFFERED", "1")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"\n===== stage {name} | {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
        for script in scripts:
            path = HERE / script
            log.write(f"--- {script} ---\n")
            log.flush()
            t0 = time.time()
            proc = subprocess.run([sys.executable, str(path)], cwd=HERE,
                                  env=env, stdout=log, stderr=subprocess.STDOUT)
            log.write(f"--- {script}: exit {proc.returncode} ({time.time() - t0:.1f} s) ---\n")
            log.flush()
            if proc.returncode != 0:
                print(f"[{name}] FAILED at {script}; see {log_path}")
                return False
    print(f"[{name}] OK ({log_path})")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--from", dest="start_from")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    names = [s[0] for s in STAGES]
    if args.list:
        for i, n in enumerate(names):
            print(f"{i + 1}. {n}")
        return 0
    selected = STAGES
    if args.only:
        if args.only not in names:
            print(f"unknown stage: {args.only}; choose from {names}")
            return 2
        selected = [s for s in STAGES if s[0] == args.only]
    elif args.start_from:
        if args.start_from not in names:
            print(f"unknown stage: {args.start_from}; choose from {names}")
            return 2
        selected = STAGES[names.index(args.start_from):]
    for name, scripts in selected:
        if not run_stage(name, scripts):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
