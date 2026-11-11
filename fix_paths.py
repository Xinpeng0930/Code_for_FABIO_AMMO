# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

"""Normalise legacy path prefixes embedded in intermediate pickle files.

Some intermediate outputs were produced when the project used a different root
directory. This utility rewrites those stored prefixes to the configured location.

Usage:
    python fix_paths.py --dir <folder-with-pkls> [--old PREFIX] [--new PREFIX]
"""
import argparse
import pickle
from pathlib import Path

import pandas as pd


def _rewrite_str(x, old, new, stats):
    if isinstance(x, str) and old in x:
        stats["strings"] += 1
        return x.replace(old, new)
    return x


def rewrite(obj, old, new, stats):
    if isinstance(obj, str):
        return _rewrite_str(obj, old, new, stats)
    if isinstance(obj, pd.DataFrame):
        return obj.map(lambda x: _rewrite_str(x, old, new, stats))
    if isinstance(obj, pd.Series):
        return obj.map(lambda x: _rewrite_str(x, old, new, stats))
    if isinstance(obj, dict):
        return {rewrite(k, old, new, stats): rewrite(v, old, new, stats) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rewrite(v, old, new, stats) for v in obj]
    if isinstance(obj, tuple):
        return tuple(rewrite(v, old, new, stats) for v in obj)
    if isinstance(obj, set):
        return {rewrite(v, old, new, stats) for v in obj}
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="folder containing .pkl files")
    ap.add_argument("--old", default="../../../Online_work/1.Air_pollution/")
    ap.add_argument("--new", default="F:/1.Air_pollution/")
    args = ap.parse_args()

    folder = Path(args.dir)
    if not folder.is_dir():
        print(f"not a directory: {folder}")
        return 2

    changed = 0
    for p in sorted(folder.glob("*.pkl")):
        stats = {"strings": 0}
        try:
            with open(p, "rb") as f:
                obj = pickle.load(f)
            new_obj = rewrite(obj, args.old, args.new, stats)
            if stats["strings"]:
                with open(p, "wb") as f:
                    pickle.dump(new_obj, f, protocol=pickle.HIGHEST_PROTOCOL)
                changed += 1
                print(f"updated {p.name}: {stats['strings']} path strings")
            else:
                print(f"unchanged {p.name}")
        except Exception as e:  # noqa: BLE001
            print(f"FAILED {p.name}: {e!r}")
    print(f"done: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
