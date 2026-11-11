# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

"""Stage A2: planetary health diet (PHD).

Implements the PHD roadmap: the diet Y data (from the FABIO dataset) drives the
N-balance adjustment of manure and synthetic fertilizer, the re-allocation of
AP-AMMO emissions, FABIO production-side emissions, and consumption-based
attribution.

Scenario: EAT.
"""
import time

from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path
from APSP_proc import Z_Proj_paths as Air_path

from AMMO_footprint import B1_Calc_LandenNflow_Chang_Prod as B1
from AMMO_footprint import B2_Basemap_Target_NenLand_Chek as B2
from AMMO_footprint import B3_Map_Prod_LandenNflow_Highreso as B3
from AMMO_footprint import B10_Calc_EURO_Diet_Ammo_Prod as B10
from AMMO_footprint import B11_Aggr_Diet_Chang_Emi_en_Fac as B11
from AMMO_footprint import B12_Map_Prodemi_Highreso as B12
from AMMO_footprint import B4_Allflow_en_SyntfertN_bala_ori as B4
from AMMO_footprint import B5_Adj_ManrinputN as B5
from AMMO_footprint import B6_Allo_AdjSyntfert_ManrN as B6
from AMMO_footprint import B7_Relink_CropLivstk_Scen as B7
from AMMO_footprint import B8_Adj_syntfert_emi_Scen as B8
from AMMO_footprint import B9_Collect_Revised_Emi_maps as B9
from AMMO_footprint import C1_Allo_adj_emi_consp as C1
from AMMO_footprint import C2_Calc_EURO_Diet_Ammo_Chang_Consp as C2

def merge_pkl(path):
    try:
        return Imp_func.open_plk(path), True
    except FileNotFoundError:
        return {}, False

def save_merge(path, updates):
    obj, _ = merge_pkl(path)
    obj.update(updates)
    Imp_func.save_plk(path, obj)

def save_merge_nested(path, scenario, values):
    try:
        obj = Imp_func.open_plk(path)
    except FileNotFoundError:
        obj = {"Tot_emi": {}, "Bystage_emi": {}, "Detailed_emi": {}}
    for section, val in values.items():
        obj.setdefault(section, {})[scenario] = val
    Imp_func.save_plk(path, obj)

SCEN = "EAT"
t0 = time.time()


def log(msg):
    print(f"[{time.time() - t0:8.1f}s] {msg}")


# --- N balance: synthetic fertilizer and manure ---------------------------------
log("B4: synthetic fertilizer N balance")
summa = {SCEN: B4.Syntfert_bala(SCEN)}
save_merge(FABIO_path.Prj_Pkl_output_wd + "Natu_Nflows_s.pkl", summa)

log("B5: adjust manure and synthetic fertilizer N")
B5.Adj_ManrSyntfert(SCEN)
adj = {SCEN: Imp_func.dict_name_path(
    ["Target_syntfertN", "Target_manrN"],
    Imp_func.glob.glob(FABIO_path.Prj_Rster_output_wd + f"{SCEN}_Adj_Nflows/*.tif"))}
adj[SCEN] = Imp_func.replace_keys(adj[SCEN], ["Adj_SyntfertN", "Adj_ManrinputN"])
save_merge(FABIO_path.Prj_Pkl_output_wd + "Adj_Syntfert_ManrInput_Nflows_s.pkl", adj)

log("B6: allocate adjusted N to crops and livestock")
B6.Allo_AdjSyntfert_ManrN(SCEN)
byprod = {SCEN: B6.Collect_adj_outputs_by_scenario(
    SCEN, MainCpNam=Air_path.MainCpNam, Ani_name=Air_path.Ani_name)}
save_merge(FABIO_path.Prj_Pkl_output_wd + "Byprod_Adj_Syntfert_ManrInput_s.pkl", byprod)

log("B7: relink crop-livestock N emissions (~50 min)")
B7.Relink_CropLivstk_N_Emi(SCEN)

log("B8: synthetic fertilizer emission collection")
B8.Syntfert_emi_collect(SCEN)
syntfert = {SCEN: Imp_func.dict_name_path(
    Air_path.MainCpNam,
    Imp_func.glob.glob(FABIO_path.Prj_Rster_output_wd + f"Syntfert_emi_{SCEN}/*.tif"))}
save_merge(FABIO_path.Prj_Pkl_output_wd + "Emi_syntfert_coupl_Scen.pkl", syntfert)

# --- land and N-flow reallocation ----------------------------------------------
log("B1: land and N-flow reallocation")
B1.N_flow_en_Land_Prod_Allfp(SCEN, ["Land"])

log("B2/B3: base maps, FABIO targets, calibration")
B2.Build_Nflow_BaseMaps(SCEN)
B2.Summa_FABIO_Land_en_Nflow_Targets(SCEN)
B3.Calibrate_LandenNflow_Diet(SCEN)
B3.Summa_Nflow_Highreso(SCEN)

# --- production-side emission allocation ---------------------------------------

log("B10/B11/B12: FABIO production emissions and high-resolution maps")
B10.Calc_EURO_Y_Prodfp(SCEN)
B11.AggrEmi_HighresoFac(SCEN)
B12.Cali_Highreso_emi(SCEN)
B12.Summa_Emi_Highreso(SCEN)

# --- collect revised emissions --------------------------------------------------
log("B9: collect revised emissions")
tot, stage, det = B9.Emi_Collect(SCEN)
save_merge_nested(FABIO_path.Prj_Pkl_output_wd + "ScenEmi_s.pkl", SCEN,
                  {"Tot_emi": tot, "Bystage_emi": stage, "Detailed_emi": det})

# --- consumption-based attribution ---------------------------------------------
log("C1/C2: consumption-based attribution")
C1.Allo_Emi(SCEN)
C2.Calc_Consp_fp(SCEN, "Total")
C2.Summary_Comsp_Emi(SCEN, "Total")

log("A2: done")
