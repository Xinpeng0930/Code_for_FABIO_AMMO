# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

"""Stage A1: base year.

Production-side emissions are the AP-AMMO values (published dataset); no
re-generation is performed. The emissions are allocated to FABIO items and
attributed to final consumption.

Scenario: CURR (base year 2017).
"""
from AMMO_footprint import C1_Allo_adj_emi_consp as C1
from AMMO_footprint import C2_Calc_EURO_Diet_Ammo_Chang_Consp as C2

SCEN = "CURR"

print(f"A1: allocate {SCEN} emissions to FABIO items")
C1.Allo_Emi(SCEN)

print(f"A1: consumption-based accounting for {SCEN}")
C2.Calc_Consp_fp(SCEN, "Total")
C2.Summary_Comsp_Emi(SCEN, "Total")

print("A1: done")
