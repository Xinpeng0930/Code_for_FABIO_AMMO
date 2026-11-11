# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

"""Stage A3: MTFR and PHD + MTFR.

The GAINS MTFR factors are applied to the PHD emissions (D1), giving the
EAT_MTFR scenario. The base-year and scenario emission pathways are provided as
intermediates (AP-AMMO method; Jin et al. 2025). Summaries and delta changes follow.

Scenarios: CURR (provided), CURR_MTFR (provided), EAT (from A2), EAT_MTFR (computed),
MTFR_EAT (provided).
"""
import time

from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path

from AMMO_footprint import D1_Newdetail_Diet_Techplus_Emi as D1
from AMMO_footprint import D2_Emi_Sort_Shar as D2
from AMMO_footprint import D3_Delta_Chang_Tot_Reved as D3

t0 = time.time()


def log(msg):
    print(f"[{time.time() - t0:8.1f}s] {msg}")


log("D1: apply MTFR factors to the PHD emissions (EAT_plus)")
D1.Emiplus_calc("EAT_plus", "MTFR")
comb = D1.Summar_Diet_Tech_plus("EAT_plus", "MTFR")
Imp_func.save_plk(FABIO_path.Prj_Pkl_output_wd + "Comb_diet_tech_emi.pkl",
                  {"EAT_MTFR": comb})

log("D2: shares and sorting (five scenarios)")
scenarios = ["CURR", "CURR_MTFR", "EAT", "EAT_MTFR", "MTFR_EAT"]
for s in scenarios:
    D2.Sort_Share(s)
shares = {s: D2.Shar_Newpath_pkl(s) for s in scenarios}
Imp_func.save_plk(FABIO_path.Prj_Pkl_output_wd + "Scen_SharSort_Emi.pkl", shares)

log("D3: delta emission changes")
for s in ["EAT", "CURR_MTFR", "EAT_MTFR"]:
    D3.Delta_Chang_Rev(s)

log("A3: done")
