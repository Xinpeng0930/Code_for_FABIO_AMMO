# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

"""Migrate scenario keys in intermediate pickle files to the canonical names.

Handles dict keys, DataFrame column names, and Series names.
Canonical set: CURR, EAT, CURR_MTFR, EAT_MTFR, MTFR_EAT.

Usage: python migrate_pkl_keys.py <file.pkl> [<file2.pkl> ...]
"""
import pickle
import sys
from pathlib import Path

import pandas as pd

PAIRS = [
    ("Curr_Imprv_EAT_plus_MTFR", "EAT_MTFR"),
    ("Curr_Imprv_EAT_plus", "EAT_plus"),
    ("Curr_Imprv_EAT_Meat", "EAT_Meat"),
    ("Curr_Imprv_EAT_Vegan", "EAT_Vegan"),
    ("Curr_Imprv_EAT", "EAT"),
    ("Curr_Imprv", "CURR"),
    ("CURR_Imprv", "CURR"),
    ("Curr_MTFR", "CURR_MTFR"),
]


def map_key(k):
    if not isinstance(k, str):
        return k
    for old, new in PAIRS:
        if k == old:
            return new
    out = k
    for old, new in PAIRS:
        out = out.replace(old, new)
    return out


def _prio(k):
    return 2 if isinstance(k, str) and "Imprv" in k else 1


def rename(obj):
    if isinstance(obj, dict):
        out, prio = {}, {}
        for k, v in obj.items():
            nk, p = map_key(k), _prio(k)
            nv = rename(v)
            if nk in out and prio.get(nk, 0) > p:
                continue
            out[nk] = nv
            prio[nk] = p
        return out
    if isinstance(obj, pd.DataFrame):
        df = obj.rename(columns=lambda c: map_key(c) if isinstance(c, str) else c)
        return df
    if isinstance(obj, pd.Series):
        return obj.rename(map_key(obj.name) if isinstance(obj.name, str) else obj.name)
    if isinstance(obj, list):
        return [rename(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(rename(v) for v in obj)
    return obj


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    for name in sys.argv[1:]:
        p = Path(name)
        with open(p, "rb") as f:
            obj = pickle.load(f)
        obj = rename(obj)
        with open(p, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("migrated", p.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
