# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# E1 — Monte-Carlo uncertainty of the PHD emission change (Fig. 5, SI S9)
# Functions:
#   full_adoption_analysis() — full-adoption series and deep analysis
#   corner_bound()           — adversarial corner bound of the market effect
import textwrap


import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

if os.name == "nt":  # Windows console defaults to GBK; keep UTF-8 output
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
UNC_DIR = os.environ.get("AMMO_UNC_DIR", os.path.join(FILE_DIR, "Figures", "uncertainty"))
os.makedirs(UNC_DIR, exist_ok=True)
out_dir = UNC_DIR

animal_foods = ["Beef","Milk","Egg","Animal_fats","Mutton","Pork","Poultry_meat","Other_ASFs"]
plant_foods = ["Fruits","Barley","Pulses","Potatoes","Vegetables","Nuts",
               "Maize","Oats","Rye","Wheat","Drink","Vegetable_oils","Sugar","Oil_crops"]
n_af = len(animal_foods); n_pf = len(plant_foods)

ALL_FOODS = animal_foods + plant_foods
AF_DISPLAY = ["Beef","Milk","Egg","Animal\nfats","Mutton","Pork","Poultry\nmeat","Other\nASFs"]
PF_DISPLAY = ["Fruits","Barley","Pulses","Potatoes","Vegetables","Nuts",
              "Maize","Oats","Rye","Wheat","Drink","Veg.\noils","Sugar","Oil\ncrops"]
ALL_DISPLAY = AF_DISPLAY + PF_DISPLAY

EAT_sa = np.array([[0.58,3.24,2.10,0.44,0.02,4.78,6.53,0.41],[0.34,1.91,1.36,0.26,0.01,3.62,4.03,0.29],[0.65,5.52,3.31,0.65,0.04,5.19,10.75,0.59],[0.03,0.46,0,0.03,0,0.01,0.01,0.01],[0.16,3.81,0.38,0.14,0,1.37,1.22,0.13],[0.06,1.78,0.27,0.06,0,0.59,0.81,0.07],[0.02,0.68,0.09,0.03,0,0.20,0.28,0.03],[0.09,0.67,0.44,0.08,0,1.03,1.32,0.10],[0,0.01,0,0,0,0.01,0.01,0],[0.02,0.12,0.07,0.02,0,0.24,0.25,0.02],[0.01,0.07,0.04,0.01,0,0.06,0.12,0.01],[0,0.03,0.01,0,0,0.02,0.03,0],[0.02,0.21,0.11,0.02,0,0.16,0.36,0.02],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0.02,0.01,0,0,0.02,0.04,0],[2.66,8.54,0.08,2.20,0.49,0.25,0.29,0.34]])
EAT_sp = np.array([[0,0,0,0,0,0,0,0,0,114.27,2.12,0,1.14,0],[0,10.60,0,0,0,0,0,0,0,0,9.65,0,0,0],[0,0,0,0,0,0,8.68,0,0,0,2.69,0.51,2.05,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,18.15,0,18.07],[0,0,0,0,0,0,0,0,0,0,0,6.49,0,0.59],[0,0,1.13,0,0,0,0,0,0,0,0,0.60,0,0],[0,0,0,0,0,0,0,3.45,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0],[0,0,0,0,0,0,0,0,2.31,0,0.42,0,0,0],[0,0,0,6.00,0,0,0,0,0,0,0.03,0,0.07,0],[0,0,0,0,0,0,0,0,0,0,0.13,0,5.98,0],[0,0,29.15,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,76.45,0,0,0,0,0,0,0,0],[17.13,0,0,0,0,0,0,0,0,0,12.96,0,0,0],[0,0,0,0,30.22,0,0,0,0,0,0.10,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
EAT_hl = np.array([[0,0,0,0,0,28.52,0,1.24],[0.09,43.08,0.23,0.07,0,0.72,0.78,0.04],[8.48,0.06,0.03,5.23,0,0.13,0.09,0.30],[0,0,0,0,0.02,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1.84,0,0,0,6.24,0.04]])
EAT_hs = np.array([[0,0,0,0,0,4.60,0,0.18],[0.01,9.43,0.05,0.01,0,0.10,0.15,0.01],[4.59,0.07,0.03,3.28,0,0.11,0.09,0.20],[0,0.02,0.01,1.24,1.47,0.04,0.02,0.08],[0,0,0,0.26,0.26,0.01,0.01,0.01],[0,0,14.39,0,0,0,46.05,0.36]])
EAT_sl = np.array([[0,0,0,0,0,5.88,0,0.26],[0.04,21.16,0.10,0.03,0,0.29,0.32,0.02],[4.30,0.03,0.02,2.40,0,0.07,0.05,0.16],[0,0,0,0.01,0.02,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1.87,0,0,0,5.91,0.04]])
EAT_ss = np.array([[0,0,0,0,0,4.35,0,0.17],[0.05,34.72,0.18,0.05,0,0.35,0.55,0.03],[16.90,0.25,0.12,12.08,0,0.39,0.34,0.73],[0,0.02,0.01,1.32,1.56,0.04,0.03,0.08],[0,0,0,0.27,0.27,0.01,0.01,0.02],[0,0,11.09,0,0,0,35.27,0.28]])
EAT_al = np.array([[0.10,0.55,0.33,0.08,0,1.01,1.09,0.07],[0.11,0.64,0.41,0.09,0,1.23,1.31,0.08],[0.06,0.40,0.26,0.06,0,0.56,0.87,0.05],[0.02,0.58,0.05,0.02,0,0.26,0.16,0.02],[0,0.05,0.01,0,0,0.02,0.02,0],[0.01,0.08,0.05,0.01,0,0.12,0.17,0.01],[0.01,0.06,0.03,0.01,0,0.13,0.11,0.01],[0,0.02,0.01,0,0,0.02,0.03,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0.01,0],[2.80,8.52,0.10,1.72,0.68,0.29,0.33,0.26]])
EAT_as = np.array([[0.25,1.26,0.83,0.17,0.01,1.61,2.61,0.15],[0.22,1.18,0.81,0.15,0.01,1.58,2.55,0.14],[0.13,0.88,0.55,0.12,0,1.04,1.80,0.10],[0.05,1.23,0.13,0.04,0,0.42,0.40,0.04],[0.01,0.22,0.03,0.01,0,0.08,0.09,0.01],[0.03,0.21,0.13,0.03,0,0.23,0.44,0.02],[0.01,0.11,0.06,0.02,0,0.19,0.23,0.01],[0.01,0.03,0.02,0,0,0.03,0.06,0],[0,0.01,0,0,0,0.01,0.01,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0.01,0,0,0,0.01,0.01,0],[2.28,8.11,0.06,1.97,1.15,0.13,0.18,0.37]])
EAT_gr = np.array([[0.02,11.10,0.05,0.01,0,0.12,0.16,0.01],[6.92,0.08,0.04,0.86,0,0.13,0.11,0.27],[0,0.02,0.01,0.37,2.71,0.04,0.03,0.11],[0,0,0,0.06,0.38,0.01,0.01,0.02]])
EAT_pl = np.array([[0,0,0,0,0,0,0,0,0,17.83,0.27,0,0.19,0],[0,1.17,0,0,0,0,0,0,0,0,3.47,0,0,0],[0,0,0,0,0,0,1.42,0,0,0,0.18,0.05,0.20,0],[0,0,0,0,0,0,0,0,0,0,0,2.42,0,-0.23],[0,0,0,0,0,0,0,0,0,0,0,0.20,0,-0.01],[0,0,0,0,0,0,0,0.88,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,1.10,0,0.23,0,0,0],[0,0,0,1.57,0,0,0,0,0,0,0.02,0,0.06,0],[0,0,0,0,0,0,0,0,0,0,0.03,0,1.26,0],[0,0,0,0,0,5.11,0,0,0,0,0,0,0,0],[1.90,0,0,0,0,0,0,0,0,0,0.93,0,0,0],[0,0,0,0,6.70,0,0,0,0,0,0.03,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
EAT_ps = np.array([[0,0,0,0,0,0,0,0,0,42.92,0.86,0,0.44,0],[0,2.31,0,0,0,0,0,0,0,0,5.75,0,0,0],[0,0,0,0,0,0,2.95,0,0,0,0.46,0.11,0.41,0],[0,0,0,0,0,0,0,0,0,0,0,5.89,0,1.76],[0,0,0,0,0,0,0,0,0,0,0,0.80,0,0.01],[0,0,0,0,0,0,0,1.35,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2.54,0,0.44,0,0,0],[0,0,0,2.39,0,0,0,0,0,0,0.02,0,0.07,0],[0,0,0,0,0,0,0,0,0,0,0.04,0,2.22,0],[0,0,0,0,0,9.43,0,0,0,0,0,0,0,0],[3.84,0,0,0,0,0,0,0,0,0,2.24,0,0,0],[0,0,0,0,11.13,0,0,0,0,0,0.03,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
CUR_sa = np.array([[2.99,8.19,3.50,2.46,0.10,26.67,7.10,2.06],[1.82,4.56,2.36,1.44,0.07,20.41,4.77,1.32],[3.29,12.87,5.03,3.29,0.21,29.10,10.98,2.90],[0.18,0.97,0,0.18,0.01,0.08,0.01,0.04],[0.81,10.04,0.60,0.80,0.01,7.71,1.28,0.66],[0.31,4.14,0.41,0.35,0.01,3.60,0.90,0.37],[0.11,1.60,0.14,0.13,0,1.16,0.29,0.14],[0.48,1.50,0.72,0.44,0.02,5.65,1.48,0.42],[0.01,0.02,0.01,0.01,0,0.04,0.01,0],[0.08,0.30,0.12,0.10,0,1.28,0.24,0.08],[0.05,0.17,0.06,0.04,0,0.35,0.13,0.04],[0.01,0.06,0.01,0.01,0,0.10,0.03,0.01],[0.03,0.16,0.05,0.04,0,0.35,0.12,0.05],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0.01,0.04,0.02,0.01,0,0.13,0.04,0.01],[15.26,26.75,0.15,13.37,3.09,1.54,0.28,2.08]])
CUR_sp = np.array([[0,0,0,0,0,0,0,0,0,83.50,1.74,0,3.29,0],[0,4.44,0,0,0,0,0,0,0,0,8.27,0,0,0],[0,0,0,0,0,0,8.39,0,0,0,2.13,0.65,5.39,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,17.22,0,-1.39],[0,0,0,0,0,0,0,0,0,0,0,8.99,0,2.51],[0,0,0.13,0,0,0,0,0,0,0,0,0.62,0,0],[0,0,0,0,0,0,0,2.24,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0.04,0,0.09,0],[0,0,0,0,0,0,0,0,1.41,0,0.31,0,0,0],[0,0,0,8.52,0,0,0,0,0,0,0.02,0,0.18,0],[0,0,0,0,0,0,0,0,0,0,0.11,0,12.98,0],[0,0,1.75,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,12.72,0,0,0,0,0,0,0,0],[9.85,0,0,0,0,0,0,0,0,0,9.47,0,0,0],[0,0,0,0,15.17,0,0,0,0,0,0.06,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
CUR_hl = np.array([[0,0,0,0,0,200.69,0,8.76],[0.58,126.82,0.49,0.53,0.01,5.06,0.84,0.34],[53.95,0.19,0.07,37.63,0,0.88,0.13,2.17],[0,0,0,0.03,0.13,0,0,0.01],[0,0,0,0.02,0.03,0,0,0],[0,0,3.57,0,0,0,7.34,0.32]])
CUR_hs = np.array([[0,0,0,0,0,33.14,0,1.25],[0.08,25.57,0.08,0.09,0,0.66,0.18,0.06],[29.69,0.21,0.07,22.40,0,0.74,0.13,1.33],[0.02,0.04,0.02,7.65,10.46,0.24,0.04,0.45],[0.01,0.01,0,1.38,1.75,0.04,0.01,0.09],[0,0,28.86,0,0,0,58.95,2.46]])
CUR_sl = np.array([[0,0,0,0,0,41.45,0,1.84],[0.24,60.98,0.19,0.22,0.01,1.98,0.35,0.14],[27.31,0.10,0.04,16.35,0,0.49,0.07,1.12],[0,0,0,0.04,0.14,0,0,0.01],[0,0,0,0.02,0.03,0,0,0],[0,0,0.72,0,0,0,1.48,0.07]])
CUR_ss = np.array([[0,0,0,0,0,31.34,0,1.18],[0.31,94.11,0.31,0.33,0.02,2.44,0.66,0.23],[109.28,0.79,0.27,82.44,0.01,2.74,0.48,4.91],[0.02,0.05,0.02,8.13,11.13,0.25,0.04,0.48],[0.01,0.01,0,1.47,1.87,0.04,0.01,0.09],[0,0,22.15,0,0,0,45.50,1.91]])
CUR_al = np.array([[0.75,2.28,0.89,0.71,0.02,8.08,1.71,0.56],[0.86,2.49,1.04,0.77,0.02,9.62,2.04,0.62],[0.67,2.03,0.82,0.62,0.01,6.21,1.60,0.46],[0.17,2.56,0.13,0.21,0,2.27,0.25,0.17],[0.02,0.26,0.02,0.02,0,0.25,0.04,0.02],[0.12,0.35,0.14,0.10,0,1.12,0.29,0.08],[0.06,0.25,0.09,0.09,0,1.07,0.16,0.07],[0.02,0.06,0.02,0.01,0,0.16,0.04,0.01],[0,0.01,0,0,0,0.02,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0.01,0.01,0,0,0.04,0.01,0],[18.67,30.22,0.18,13.12,4.79,1.81,0.32,1.88]])
CUR_as = np.array([[2.10,5.52,2.26,1.71,0.06,16.10,4.63,1.33],[1.65,4.50,1.98,1.36,0.05,14.84,4.27,1.08],[1.37,4.19,1.67,1.26,0.04,11.36,3.44,0.97],[0.43,5.19,0.31,0.42,0.01,3.87,0.66,0.34],[0.10,1.02,0.09,0.09,0,0.92,0.19,0.08],[0.26,0.83,0.33,0.24,0.01,2.27,0.77,0.18],[0.11,0.40,0.15,0.13,0,1.49,0.33,0.10],[0.03,0.09,0.03,0.03,0,0.22,0.08,0.02],[0.01,0.03,0.01,0.01,0,0.05,0.01,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0.01,0.02,0.01,0.01,0,0.06,0.02,0.01],[15.06,28.54,0.14,14.32,7.40,1.15,0.29,2.41]])
CUR_gr = np.array([[0.13,33.91,0.10,0.11,0,0.84,0.18,0.08],[45.65,0.25,0.09,27.19,0,0.93,0.16,1.98],[0.02,0.05,0.02,9.33,17.10,0.27,0.04,0.67],[0,0.01,0,1.50,2.25,0.06,0.01,0.09]])
CUR_pl = np.array([[0,0,0,0,0,0,0,0,0,21.5957,0.3975,0,0.906,0],[0,1.2928,0,0,0,0,0,0,0,0,4.6817,0,0,0],[0,0,0,0,0,0,1.931,0,0,0,0.2949,0.1343,1.0537,0],[0,0,0,0,0,0,0,0,0,0,0,4.0507,0,-0.8331],[0,0,0,0,0,0,0,0,0,0,0,0.5222,0,0.0681],[0,0,0,0,0,0,0,1.0129,0,0,0.0004,0,0,0],[0,0,0,0,0,0,0,0,1.1016,0,0.3136,0,0,0],[0,0,0,3.4734,0,0,0,0,0,0,0.0125,0,0.1305,0],[0,0,0,0,0,0,0,0,0,0,0.0397,0,4.1521,0],[0,0,0,0,0,1.8053,0,0,0,0,0,0,0,0],[2.4062,0,0,0,0,0,0,0,0,0,1.5984,0,0,0],[0,0,0,0,5.4852,0,0,0,0,0,0.0426,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
CUR_ps = np.array([[0,0,0,0,0,0,0,0,0,55.7508,1.3965,0,2.5544,0],[0,3.0073,0,0,0,0,0,0,0,0,7.3626,0,0,0],[0,0,0,0,0,0,5.1837,0,0,0,0.7132,0.2586,2.2025,0],[0,0,0,0,0,0,0,0,0,0,0,9.0667,0,-0.5331],[0,0,0,0,0,0,0,0,0,0,0,2.0182,0,0.4847],[0,0,0,0,0,0,0,1.4107,0,0,0.0011,0,0,0],[0,0,0,0,0,0,0,0,2.5565,0,0.4525,0,0,0],[0,0,0,4.6855,0,0,0,0,0,0,0.012,0,0.1216,0],[0,0,0,0,0,0,0,0,0,0,0.0455,0,5.9236,0],[0,0,0,0,0,3.4915,0,0,0,0,0,0,0,0],[4.3645,0,0,0,0,0,0,0,0,0,3.8889,0,0,0],[0,0,0,0,9.4482,0,0,0,0,0,0.0321,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# Option B bounds: single relative formula t = (P2C_ours - P2C_lit)/P2C_ours
# Lower = Rieger et al. (2023), Upper = Geibel and Freund (2023), both on the
# rounded P2C values published in Supplementary Table 12.
# Market-mediated effects apply to the three major ASFs with compiled P2C
# ranges and, as pigs/cattle co-products, to animal fats (t_fat = a convex
# combination of the beef and pork draws, spanning their union range
# [0.074, 0.365]); all other foods get t = 0.
trade_animal = {"Beef":[0.074,0.266],"Milk":[0.098,0.415],"Egg":[0.0,0.0],"Animal_fats":[0.0,0.0],
                "Mutton":[0.0,0.0],"Pork":[0.129,0.365],"Poultry_meat":[0.0,0.0],"Other_ASFs":[0.0,0.0]}
trade_plant = {pf:[0.0,0.0] for pf in plant_foods}

ef_synth_cv = 0.30; ef_manure_app_cv = 0.402
EF_hous = {"liq":{"Pig":0.50,"Dair":0.67,"Othcatl":0.67,"Shep":0.67,"Goat":0.67,"Potr":0.65},"sld":{"Pig":0.50,"Dair":0.57,"Othcatl":0.57,"Shep":0.57,"Goat":0.57,"Potr":0.65}}
EF_stor = {"liq":{"Pig":0.63,"Dair":0.59,"Othcatl":0.59,"Shep":0.59,"Goat":0.59,"Potr":0.58},"sld":{"Pig":0.54,"Dair":0.49,"Othcatl":0.49,"Shep":0.49,"Goat":0.49,"Potr":0.58}}
EF_app_animal = {"liq":{"Beef":0.287,"Milk":0.287,"Egg":0.507,"Animal_fats":0.409,"Mutton":0.287,"Pork":0.531,"Poultry_meat":0.507,"Other_ASFs":0.403},"sld":{"Beef":0.287,"Milk":0.287,"Egg":0.507,"Animal_fats":0.409,"Mutton":0.287,"Pork":0.531,"Poultry_meat":0.507,"Other_ASFs":0.403}}
EF_graz_cv = 0.50
manure_livstk = ["Pig","Dair","Othcatl","Shep","Goat","Potr"]
graz_livstk = ["Dair","Othcatl","Shep","Goat"]

def sample_lognormal(mean_val, cv, size=1):
    sigma = np.sqrt(np.log(1 + cv**2))
    mu = np.log(mean_val) - 0.5 * sigma**2
    return np.random.lognormal(mean=mu, sigma=sigma, size=size)

np.random.seed(42)
n_sim = 1000; n_crops_synth=17; n_crops_app=13; n_livstk=6

ef_synth = sample_lognormal(1.0, ef_synth_cv, (n_sim, n_crops_synth))
ef_hl = np.zeros((n_sim,n_livstk)); ef_hs = np.zeros((n_sim,n_livstk))
ef_sl = np.zeros((n_sim,n_livstk)); ef_ss = np.zeros((n_sim,n_livstk))
for r,lv in enumerate(manure_livstk):
    ef_hl[:,r]=sample_lognormal(1.0,EF_hous["liq"][lv],n_sim)
    ef_hs[:,r]=sample_lognormal(1.0,EF_hous["sld"][lv],n_sim)
    ef_sl[:,r]=sample_lognormal(1.0,EF_stor["liq"][lv],n_sim)
    ef_ss[:,r]=sample_lognormal(1.0,EF_stor["sld"][lv],n_sim)
ef_al = np.zeros((n_sim,n_af)); ef_as_af = np.zeros((n_sim,n_af))
for j,food in enumerate(animal_foods):
    ef_al[:,j]=sample_lognormal(1.0,EF_app_animal["liq"][food],n_sim)
    ef_as_af[:,j]=sample_lognormal(1.0,EF_app_animal["sld"][food],n_sim)
ef_grz = sample_lognormal(1.0, EF_graz_cv, (n_sim,len(graz_livstk)))
ef_pl_app = sample_lognormal(1.0, ef_manure_app_cv, (n_sim,n_crops_app))

ones_a = np.ones((n_sim,n_af)); ones_p = np.ones((n_sim,n_pf))
# Market-mediated erosion fraction t_j (Choice B): sampled uniformly over the
# compiled bounds and applied multiplicatively to the emission change.
tm_af = np.zeros((n_sim,n_af)); tm_pf = np.zeros((n_sim,n_pf))
for j,food in enumerate(animal_foods):
    tv = trade_animal[food]
    if len(tv)==2: tm_af[:,j] = np.random.uniform(tv[0],tv[1],n_sim)
# Animal fats are co-products of pigs and cattle: t_fat is a convex combination
# of the simultaneously drawn beef and pork fractions with the unknown co-product
# weight drawn uniformly per iteration (2026-10-28); spans [0.074, 0.365]
# while preserving E[t_fat] = 0.2085.
_fj = {f: i for i, f in enumerate(animal_foods)}
for j,food in enumerate(plant_foods):
    tvp = trade_plant[food]
    if len(tvp)==2: tm_pf[:,j] = np.random.uniform(tvp[0],tvp[1],n_sim)
_w_fat = np.random.uniform(0.0, 1.0, n_sim)
tm_af[:, _fj["Animal_fats"]] = (_w_fat * tm_af[:, _fj["Beef"]]
                                + (1.0 - _w_fat) * tm_af[:, _fj["Pork"]])

def compute_eat_per_food(dm_a, tm_a, dm_p, tm_p, use_ef):
    T_af = np.zeros((n_sim,n_af)); T_pf = np.zeros((n_sim,n_pf))
    cm_a = dm_a*tm_a; cm_p = dm_p*tm_p
    one_crops = np.ones(n_crops_synth); one_app = np.ones(n_crops_app)
    for i in range(n_sim):
        rs = ef_synth[i] if use_ef else one_crops
        ra = ef_pl_app[i] if use_ef else one_app
        T_af[i] += (EAT_sa*rs[:,np.newaxis]*cm_a[i]).sum(axis=0)
        T_pf[i] += (EAT_sp*rs[:,np.newaxis]*cm_p[i]).sum(axis=0)
        if use_ef:
            for r in range(n_livstk):
                row = (EAT_hl[r]*ef_hl[i,r]+EAT_hs[r]*ef_hs[i,r]+EAT_sl[r]*ef_sl[i,r]+EAT_ss[r]*ef_ss[i,r])
                T_af[i] += row*cm_a[i]
            for j in range(n_af):
                T_af[i,j] += (EAT_al[:,j].sum()*ef_al[i,j]+EAT_as[:,j].sum()*ef_as_af[i,j])*cm_a[i,j]
            for r,lv in enumerate(graz_livstk):
                T_af[i] += EAT_gr[r]*ef_grz[i,r]*cm_a[i]
        else:
            for r in range(n_livstk):
                T_af[i] += (EAT_hl[r]+EAT_hs[r]+EAT_sl[r]+EAT_ss[r])*cm_a[i]
            for j in range(n_af):
                T_af[i,j] += (EAT_al[:,j].sum()+EAT_as[:,j].sum())*cm_a[i,j]
            for r,lv in enumerate(graz_livstk):
                T_af[i] += EAT_gr[r]*cm_a[i]
        T_pf[i] += ((EAT_pl+EAT_ps)*ra[:,np.newaxis]*cm_p[i]).sum(axis=0)
    return T_af, T_pf

def compute_cur_per_food(use_ef):
    T_af = np.zeros((n_sim,n_af)); T_pf = np.zeros((n_sim,n_pf))
    one_crops = np.ones(n_crops_synth); one_app = np.ones(n_crops_app)
    for i in range(n_sim):
        rs = ef_synth[i] if use_ef else one_crops
        ra = ef_pl_app[i] if use_ef else one_app
        T_af[i] += (CUR_sa*rs[:,np.newaxis]).sum(axis=0)
        T_pf[i] += (CUR_sp*rs[:,np.newaxis]).sum(axis=0)
        if use_ef:
            for r in range(n_livstk):
                T_af[i] += (CUR_hl[r]*ef_hl[i,r]+CUR_hs[r]*ef_hs[i,r]+CUR_sl[r]*ef_sl[i,r]+CUR_ss[r]*ef_ss[i,r])
            for j in range(n_af):
                T_af[i,j] += (CUR_al[:,j].sum()*ef_al[i,j]+CUR_as[:,j].sum()*ef_as_af[i,j])
            for r,lv in enumerate(graz_livstk):
                T_af[i] += CUR_gr[r]*ef_grz[i,r]
        else:
            for r in range(n_livstk):
                T_af[i] += (CUR_hl[r]+CUR_hs[r]+CUR_sl[r]+CUR_ss[r])
            for j in range(n_af):
                T_af[i,j] += (CUR_al[:,j].sum()+CUR_as[:,j].sum())
            for r,lv in enumerate(graz_livstk):
                T_af[i] += CUR_gr[r]
        T_pf[i] += ((CUR_pl+CUR_ps)*ra[:,np.newaxis]).sum(axis=0)
    return T_af, T_pf

cur_af0, cur_pf0 = compute_cur_per_food(False)
cur0 = cur_af0.sum(axis=1) + cur_pf0.sum(axis=1)
cur_af1, cur_pf1 = compute_cur_per_food(True)
cur1 = cur_af1.sum(axis=1) + cur_pf1.sum(axis=1)



def full_adoption_analysis():
    _rc = plt.rcParams.copy()
    print("=" * 80)
    print("  FULL ADOPTION SERIES — DEEP ANALYSIS")
    print("  1. Baseline  1a. +Market-mediated effect  1b. +EF  1c. +Market-mediated + EF  1d. Corner + EF")
    print("=" * 80)

    eat_af_steps = []; eat_pf_steps = []; eat_steps = []; del_steps = []
    labels = ["(a) Baseline (deterministic)", "(b) +Market-mediated effect",
              "(c) +EF (emission-factor uncertainty)", "(d) +Market-mediated effect + EF",
              "(e) Corner (3 major ASFs at upper bound) + EF"]

    # Step 1: Baseline
    eaf0, epf0 = compute_eat_per_food(ones_a, ones_a, ones_p, ones_p, False)
    eat0 = eaf0.sum(axis=1) + epf0.sum(axis=1)
    del0 = eat0 - cur0
    eat_af_steps.append(eaf0); eat_pf_steps.append(epf0); eat_steps.append(eat0); del_steps.append(del0)

    # Step 1a: +Market-mediated effect (P2C ratios) - Choice B delta formula
    # Delta_t = Delta_det * (1 - t_j); the base year keeps its observed trade.
    del_af_t = (eaf0 - cur_af0) * (1.0 - tm_af)
    del_pf_t = (epf0 - cur_pf0) * (1.0 - tm_pf)
    eaf_t = cur_af0 + del_af_t
    epf_t = cur_pf0 + del_pf_t
    eat_t = eaf_t.sum(axis=1) + epf_t.sum(axis=1)
    del_t = eat_t - cur0
    eat_af_steps.append(eaf_t); eat_pf_steps.append(epf_t); eat_steps.append(eat_t); del_steps.append(del_t)

    # Step 1b: +EF (paired)
    eaf_f, epf_f = compute_eat_per_food(ones_a, ones_a, ones_p, ones_p, True)
    eat_f = eaf_f.sum(axis=1) + epf_f.sum(axis=1)
    del_f = eat_f - cur1
    eat_af_steps.append(eaf_f); eat_pf_steps.append(epf_f); eat_steps.append(eat_f); del_steps.append(del_f)

    # Step 1c: +Market-mediated effect + EF (paired) - Choice B delta formula
    # Delta_tf = Delta_ef * (1 - t_j), with EF draws shared between scenarios.
    del_af_tf = (eaf_f - cur_af1) * (1.0 - tm_af)
    del_pf_tf = (epf_f - cur_pf1) * (1.0 - tm_pf)
    eaf_tf = cur_af1 + del_af_tf
    epf_tf = cur_pf1 + del_pf_tf
    eat_tf = eaf_tf.sum(axis=1) + epf_tf.sum(axis=1)
    del_tf = eat_tf - cur1
    eat_af_steps.append(eaf_tf); eat_pf_steps.append(epf_tf); eat_steps.append(eat_tf); del_steps.append(del_tf)

    # Step 1d: adversarial corner - 3 major ASFs pinned at their upper-bound erosion + EF (paired)
    T_MAX = {"Beef": 0.266, "Milk": 0.415, "Pork": 0.365}
    tm_af_corner = np.zeros((n_sim, n_af))
    for j, food in enumerate(animal_foods):
        if food in T_MAX:
            tm_af_corner[:, j] = T_MAX[food]
    # Animal fats follow the maximum parent bound in the corner (0.365, i.e. fats
    # behaving entirely like pork, the more persistent parent)
    tm_af_corner[:, animal_foods.index("Animal_fats")] = max(T_MAX["Beef"], T_MAX["Pork"])
    del_af_c = (eaf_f - cur_af1) * (1.0 - tm_af_corner)
    del_pf_c = (epf_f - cur_pf1) * (1.0 - tm_pf)   # plants: t = 0
    eaf_c = cur_af1 + del_af_c
    epf_c = cur_pf1 + del_pf_c
    eat_c = eaf_c.sum(axis=1) + epf_c.sum(axis=1)
    del_c = eat_c - cur1
    eat_af_steps.append(eaf_c); eat_pf_steps.append(epf_c); eat_steps.append(eat_c); del_steps.append(del_c)

    print(f"\n{'Step':<30s}  {'EAT mean':>9s} {'EAT CV':>7s} {'EAT var':>9s}  {'DEL mean':>9s} {'DEL CV':>7s} {'DEL var':>9s}  {'DEL 95% CI':>22s}")
    print("-" * 110)
    for idx in range(5):
        e = eat_steps[idx]; d = del_steps[idx]
        ci = f"[{np.percentile(d,2.5):.0f}, {np.percentile(d,97.5):.0f}]"
        print(f"  {labels[idx]:<30s}  {e.mean():9.1f} {e.std()/e.mean()*100 if e.mean()>0 else 0:7.2f}% {np.var(e):9.1f}  {d.mean():9.1f} {abs(d.std()/d.mean())*100 if d.mean()!=0 else 0:7.2f}% {np.var(d):9.1f}  {ci:>22s}")

    # ============================================================
    # Variance decomposition — 3 sources: Market, EF, M×F
    # ============================================================
    print(f"\n{'='*70}")
    print("  VARIANCE ATTRIBUTION — Full Adoption Series")
    print(f"{'='*70}")

    t_var = np.var(eat_steps[1]); f_var = np.var(eat_steps[2])
    tf_var = np.var(eat_steps[3])
    txi = tf_var - t_var - f_var
    print(f"  EAT:  Market = {t_var:8.0f} ({t_var/tf_var*100:5.1f}%)   EF = {f_var:8.0f} ({f_var/tf_var*100:5.1f}%)   M×F = {txi:8.0f} ({txi/tf_var*100:5.1f}%)   Total = {tf_var:8.0f}")

    dt_var = np.var(del_steps[1]); df_var = np.var(del_steps[2])
    dtf_var = np.var(del_steps[3])
    dtxi = dtf_var - dt_var - df_var
    print(f"  DELTA: Market = {dt_var:8.0f} ({dt_var/dtf_var*100 if dtf_var>0 else 0:5.1f}%)   EF = {df_var:8.0f} ({df_var/dtf_var*100 if dtf_var>0 else 0:5.1f}%)   M×F = {dtxi:8.0f} ({dtxi/dtf_var*100:5.1f}%)   Total = {dtf_var:8.0f}")

    r_ec = np.corrcoef(eat_steps[3], cur1)[0,1]
    var_eat_all = np.var(eat_steps[3]); var_cur_all = np.var(cur1)
    var_delta_all = np.var(del_steps[3])
    unpaired = var_eat_all + var_cur_all
    print(f"\n  Paired diagnostics: r(EAT,Cur) = {r_ec:.3f}, Cancellation = {(unpaired-var_delta_all)/unpaired*100:.0f}%")
    print(f"  Var(EAT)={var_eat_all:.0f}  Var(Cur)={var_cur_all:.0f}  Cov={np.cov(eat_steps[3],cur1)[0,1]:.0f}")
    print(f"  Var(Delta paired)={var_delta_all:.0f}  Unpaired={unpaired:.0f}")

    # ============================================================
    # PLOT SETUP
    # ============================================================
    plt.rcParams.update({"font.size":12,"axes.titlesize":14,"axes.labelsize":12,
                         "xtick.labelsize":9,"ytick.labelsize":10,"legend.fontsize":9,
                         "figure.dpi":200,"savefig.bbox":"tight",
                         "svg.fonttype":"none"})  # keep text editable in SVG

    def save_png_svg(fig, png_name):
        """Save a figure as both PNG and editable SVG in out_dir."""
        fig.savefig(os.path.join(out_dir, png_name))
        svg_name = png_name.rsplit(".", 1)[0] + ".svg"
        fig.savefig(os.path.join(out_dir, svg_name))
        print(f"Saved: {png_name} + {svg_name}")

    AF_COLORS = ["#D7191C","#2C7BB6","#FDAE61","#ABD9E9","#5E4FA2","#F46D43","#A6D96A","#1A9641"]
    PF_COLORS = ["#FBB4AE","#C2A5CF","#E78AC3","#A1887F","#8DD3C7","#B2DF8A","#FEE08B",
                 "#D4E157","#8D6E63","#FDB863","#4DB6AC","#FFB74D","#90CAF9","#CE93D8"]

    # Fig5 (Manuscriptv27) category order and colors, applied to the 22-food grids.
    # Foods ordered category-major (Fig5 sequence), members by ascending deterministic delta.
    FIG5_CAT_ORDER = [
        ("Pork",              "#FF6C64", [5]),
        ("Milk",              "#C4003A", [1]),
        ("Beef",              "#EA0041", [0]),
        ("Fats & oils",       "#FF8A27", [3, 19, 21]),
        ("Other animal",      "#FFE2D7", [4, 7]),
        ("Poultry & eggs",    "#FFAD99", [2, 6]),
        ("Whole grains",      "#296AB0", [14, 18, 16, 15, 9, 17]),
        ("Veg & fruits",      "#8CC6E2", [8, 12]),
        ("Legumes",           "#A3ECB2", [10]),
        ("Nuts",              "#00B96D", [13]),
        ("Other plant",       "#3F94C8", [20, 11]),
    ]
    FIG5_ORDER = [i for _, _, m in FIG5_CAT_ORDER for i in m]
    FIG5_COLORS = [c for _, c, m in FIG5_CAT_ORDER for _ in m]
    # 22-food indices: animal 0-7 = Beef,Milk,Egg,Animal_fats,Mutton,Pork,Poultry_meat,Other_ASFs
    #                 plant 8-21  = Fruits,Barley,Pulses,Potatoes,Vegetables,Nuts,Maize,Oats,Rye,
    #                               Wheat,Drink,Vegetable_oils,Sugar,Oil_crops

    def plot_22food_grid(title, suptitle, fname, is_delta=False):
        fig, axes = plt.subplots(2, 2, figsize=(24, 14))
        axes = axes.flatten()
        for idx in range(4):
            ax = axes[idx]
            if is_delta:
                eaf = eat_af_steps[idx]; epf = eat_pf_steps[idx]
                if idx <= 1:
                    caf, cpf = cur_af0, cur_pf0
                else:
                    caf, cpf = cur_af1, cur_pf1
                daf = eaf - caf; dpf = epf - cpf
                all_vals = np.concatenate([daf, dpf], axis=1)
            else:
                all_vals = np.concatenate([eat_af_steps[idx], eat_pf_steps[idx]], axis=1)

            order = FIG5_ORDER
            means = all_vals.mean(axis=0)
            sorted_means = means[order]
            sorted_display = [ALL_DISPLAY[i] for i in order]
            vals_sorted = all_vals[:, order]
            p25 = np.percentile(vals_sorted, 2.5, axis=0); p75 = np.percentile(vals_sorted, 97.5, axis=0)  # 95% CI (p2.5–p97.5), aligned with main-text reporting

            colors = FIG5_COLORS

            x = np.arange(22)
            ax.bar(x, sorted_means, color=colors, edgecolor="black", linewidth=0.5, alpha=0.9)
            ax.errorbar(x, sorted_means, yerr=[np.maximum(sorted_means-p25,0), np.maximum(p75-sorted_means,0)],
                        fmt="none", ecolor="#333", capsize=0, linewidth=2)
            if is_delta:
                ax.axhline(0, color="#999", linewidth=0.5, linestyle="--")
            ax.set_xticks(x)
            ax.set_xticklabels(sorted_display, rotation=45, ha="right", fontsize=8)
            ax.set_ylabel("kt NH₃-N")
            ax.set_title(labels[idx], fontweight="bold", fontsize=11)
            ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
            ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
            ax.ticklabel_format(axis="y", style="plain")

        fig.suptitle(suptitle, fontsize=15, fontweight="bold", y=1.01)
        fig.tight_layout()
        save_png_svg(fig, fname)
        plt.close(fig)

    # (22-food PerFood grids superseded by Fig5-category grids below; calls removed)

    # ============================================================
    # Fig5 category-level grids (11 categories, Fig5 labels/order/colors)
    # ============================================================
    FIG5_CAT_DISPLAY = ["Pork", "Milk or\nequivalent", "Beef", "Fats & oils", "Other animal\nproducts",
                        "Poultry meat\n& eggs", "Whole grains", "Vegetables\n& fruits", "Legumes",
                        "Nuts", "Other plant\nproducts"]

    def to_category_vals(idx, is_delta):
        if is_delta:
            eaf = eat_af_steps[idx]; epf = eat_pf_steps[idx]
            if idx <= 1:
                caf, cpf = cur_af0, cur_pf0
            else:
                caf, cpf = cur_af1, cur_pf1
            all_vals = np.concatenate([eaf - caf, epf - cpf], axis=1)
        else:
            all_vals = np.concatenate([eat_af_steps[idx], eat_pf_steps[idx]], axis=1)
        return np.column_stack([all_vals[:, members].sum(axis=1) for _, _, members in FIG5_CAT_ORDER])

    def draw_category_panel(ax, vals, is_delta, title):
        """Draw one category bar panel (Fig5 categories, 95% CI whiskers with caps)."""
        means = vals.mean(axis=0)
        lo = np.percentile(vals, 2.5, axis=0); hi = np.percentile(vals, 97.5, axis=0)
        cat_colors = [c for _, c, _ in FIG5_CAT_ORDER]
        x = np.arange(len(FIG5_CAT_ORDER))
        ax.bar(x, means, color=cat_colors, edgecolor="black", linewidth=0.5, alpha=0.9)
        if np.any(hi - lo > 0):
            ax.errorbar(x, means, yerr=[np.maximum(means-lo, 0), np.maximum(hi-means, 0)],
                        fmt="none", ecolor="#333", capsize=3, linewidth=2)
        if is_delta:
            ax.axhline(0, color="#999", linewidth=0.5, linestyle="--")
        ax.set_xticks(x)
        ax.set_xticklabels(FIG5_CAT_DISPLAY, rotation=30, ha="right", fontsize=9)
        ax.set_title(title, fontweight="bold", fontsize=11)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
        ax.ticklabel_format(axis="y", style="plain")


    def plot_category_grid(suptitle, fname, is_delta=False,
                           panel_idx=None, panel_titles=None):
        if panel_idx is None:
            panel_idx = list(range(4))
        if panel_titles is None:
            panel_titles = [labels[i] for i in panel_idx]
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        axes = axes.flatten()
        all_vals = [to_category_vals(i, is_delta) for i in panel_idx]
        shared_ylim = None
        if is_delta:
            # consistent y-scale across all four panels, set by the combined CI extents
            lo_all = np.concatenate([np.percentile(v, 2.5, axis=0) for v in all_vals])
            hi_all = np.concatenate([np.percentile(v, 97.5, axis=0) for v in all_vals])
            ylo = min(np.floor(np.min(lo_all) / 100) * 100, -100)
            yhi = max(np.ceil(np.max(hi_all) / 100) * 100, 100)
            shared_ylim = (ylo, yhi)
        for k, idx in enumerate(panel_idx):
            ax = axes[k]
            draw_category_panel(ax, all_vals[k], is_delta, panel_titles[k])
            ax.set_ylabel("kt NH₃-N")
            if shared_ylim is not None:
                ax.set_ylim(*shared_ylim)
                ax.set_yticks(np.arange(shared_ylim[0], shared_ylim[1] + 1, 100))
        fig.suptitle(suptitle, fontsize=15, fontweight="bold", y=1.01)
        fig.tight_layout()
        save_png_svg(fig, fname)
        plt.close(fig)


    # Supplementary Fig. 9 panels (Category_Delta_4scenarios):
    # (c) central case = market effect at mean erosion + EF uncertainty (step 3)
    # (d) adversarial corner = 3 major ASFs pinned at upper-bound erosion + EF (step 4)
    DELTA_PANEL_IDX = [0, 2, 3, 4]
    DELTA_PANEL_TITLES = ["(a) Baseline (deterministic)",
                          "(b) Emission-factor uncertainty",
                          "(c) Market effect (mean erosion) + emission-factor uncertainty",
                          "(d) Upper-bound corner (3 major ASFs) + emission-factor uncertainty"]


    plot_category_grid("EAT Emissions by Category — Full Adoption Series (Fig5 categories)",
                       "Category_EAT_4scenarios.png", is_delta=False)
    plot_category_grid("Uncertainty analysis of ammonia emission changes under the PHD transition",
                       "Category_Delta_4scenarios.png", is_delta=True,
                       panel_idx=DELTA_PANEL_IDX, panel_titles=DELTA_PANEL_TITLES)

    print("\n" + "=" * 120)
    print("  CATEGORY-LEVEL TABLES (Fig5 categories) — Mean ± SD [95% CI] kt")
    print("=" * 120)
    for tag, is_delta in (("EAT", False), ("DELTA", True)):
        print(f"\n  --- {tag} ---")
        hdr = f"{'Category':<22}" + "".join(f"  {l[:16]:>24}" for l in labels)
        print(hdr); print("-" * 120)
        for ci, (cname, _, _) in enumerate(FIG5_CAT_ORDER):
            row = f"{cname:<22}"
            for idx in range(5):
                v = to_category_vals(idx, is_delta)[:, ci]
                row += f"  {v.mean():7.1f}±{v.std():5.1f} [{np.percentile(v,2.5):6.0f},{np.percentile(v,97.5):6.0f}]"
            print(row)

    # ============================================================
    # Variance decomposition for full T+EF scenario (food level: console only; figures at Fig5-category level)
    # ============================================================
    def per_food_var_contrib(data_af, data_pf, total, title, fname=None):
        all_data = np.concatenate([data_af, data_pf], axis=1)
        cov_mat = np.cov(all_data.T)
        diag = np.diag(cov_mat)
        total_var = np.var(total)
        full_sum = cov_mat.sum()

        contrib = diag.copy()
        cov_sum_per_food = cov_mat.sum(axis=0) - diag
        adj = total_var / full_sum if full_sum > 1e-10 else 1.0
        contrib = diag * adj + cov_sum_per_food * adj / 2

        order = np.argsort(contrib)[::-1]
        sorted_contrib = contrib[order]
        sorted_labels = [ALL_DISPLAY[i] for i in order]
        colors = FIG5_COLORS  # unused when fname is None

        if fname is not None:
            fig, ax = plt.subplots(figsize=(12, 6))
            x = np.arange(22)
            ax.bar(x, sorted_contrib, color=colors, edgecolor="black", linewidth=0.5, alpha=0.9)
            ax.set_xticks(x); ax.set_xticklabels(sorted_labels, rotation=45, ha="right", fontsize=8)
            ax.set_ylabel("Variance contribution"); ax.set_title(f"Per-food variance contribution — {title}")
            ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

            pct = sorted_contrib / total_var * 100
            cumul_pct = np.cumsum(pct)
            for i in range(22):
                if pct[i] > 3 or (i < 5 and pct[i] > 1):
                    ax.text(i, sorted_contrib[i] + total_var*0.005, f"{pct[i]:.1f}%", ha="center", fontsize=7, color="#333")
            ax2 = ax.twinx()
            ax2.plot(x, cumul_pct, "o-", color="#333", linewidth=1.5, markersize=4)
            ax2.set_ylabel("Cumulative %", color="#333"); ax2.tick_params(axis="y", labelcolor="#333")
            ax2.set_ylim(0, 105)

            fig.tight_layout()
            save_png_svg(fig, fname)
            plt.close(fig)
        return contrib, order

    eat_contrib, eat_order = per_food_var_contrib(eat_af_steps[3], eat_pf_steps[3], eat_steps[3],
                                                   "EAT (+Market+EF)")

    daf_tf = eat_af_steps[3] - cur_af1; dpf_tf = eat_pf_steps[3] - cur_pf1
    del_contrib, del_order = per_food_var_contrib(daf_tf, dpf_tf, del_steps[3],
                                                   "Delta (+Market+EF)")

    def category_var_contrib(is_delta, title, fname):
        cat = to_category_vals(3, is_delta)
        cov_mat = np.cov(cat.T)
        diag = np.diag(cov_mat)
        total_var = np.var(cat.sum(axis=1))
        full_sum = cov_mat.sum()
        adj = total_var / full_sum if full_sum > 1e-10 else 1.0
        contrib = (diag + (cov_mat.sum(axis=0) - diag) / 2) * adj

        order = [i for i in range(len(FIG5_CAT_ORDER))]  # fixed Fig5 order
        colors = [c for _, c, _ in FIG5_CAT_ORDER]
        x = np.arange(len(order))
        pct = contrib / total_var * 100
        cumul_pct = np.cumsum(pct)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x, contrib[order], color=colors, edgecolor="black", linewidth=0.5, alpha=0.9)
        ax.set_xticks(x); ax.set_xticklabels(FIG5_CAT_DISPLAY, rotation=30, ha="right", fontsize=9)
        ax.set_ylabel("Variance contribution"); ax.set_title(f"Category variance contribution — {title}")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        for i in range(len(order)):
            if pct[i] > 2:
                ax.text(i, contrib[i] + total_var*0.005, f"{pct[i]:.1f}%", ha="center", fontsize=8, color="#333")
        ax2 = ax.twinx()
        ax2.plot(x, cumul_pct, "o-", color="#333", linewidth=1.5, markersize=4)
        ax2.set_ylabel("Cumulative %", color="#333"); ax2.tick_params(axis="y", labelcolor="#333")
        ax2.set_ylim(0, 105)

        fig.tight_layout()
        save_png_svg(fig, fname)
        plt.close(fig)
        print(f"  Category % of total variance ({title}): " +
              ", ".join(f"{n}={p:.1f}%" for (n,_,_),p in zip(FIG5_CAT_ORDER, pct)))
        return contrib

    eat_cat_contrib = category_var_contrib(False, "EAT (+Market+EF)", "Variance_Decomp_EAT_byCategory.png")
    del_cat_contrib = category_var_contrib(True, "Delta (+Market+EF)", "Variance_Decomp_Delta_byCategory.png")

    # ============================================================
    # Per-food tables across 4 scenarios
    # ============================================================
    print("\n" + "=" * 130)
    print("  PER-FOOD EAT EMISSIONS — Mean ± SD [95% CI] kt  |  All 5 scenarios")
    print("=" * 130)
    header = f"{'Food':<20s}"
    for s in labels:
        header += f"  {s[:12]:>16s}"
    print(header)
    print("-" * 130)
    for fi, food in enumerate(animal_foods+plant_foods):
        row = f"{food:<20s}"
        for idx in range(5):
            if fi < 8:
                v = eat_af_steps[idx][:,fi]
            else:
                v = eat_pf_steps[idx][:,fi-8]
            m = v.mean(); cv = v.std()/m*100 if m > 0.01 else 0
            lo = np.percentile(v, 2.5); hi = np.percentile(v, 97.5)
            row += f"  {m:6.1f}±{v.std():5.1f} [{lo:5.0f},{hi:5.0f}]"
        print(row)

    print("\n" + "=" * 130)
    print("  PER-FOOD DELTA (EAT − Current) — Mean ± SD [95% CI] kt  |  All 5 scenarios")
    print("=" * 130)
    print(header)
    print("-" * 130)
    for fi, food in enumerate(animal_foods+plant_foods):
        row = f"{food:<20s}"
        for idx in range(5):
            if fi < 8:
                cafeat = eat_af_steps[idx][:,fi]
                ccur = cur_af1[:,fi] if idx>=2 else cur_af0[:,fi]
            else:
                cafeat = eat_pf_steps[idx][:,fi-8]
                ccur = cur_pf1[:,fi-8] if idx>=2 else cur_pf0[:,fi-8]
            v = cafeat - ccur
            m = v.mean(); cv = abs(v.std()/m)*100 if abs(m)>0.01 else 0
            lo = np.percentile(v, 2.5); hi = np.percentile(v, 97.5)
            row += f"  {m:6.1f}±{v.std():5.1f} [{lo:5.0f},{hi:5.0f}]"
        print(row)

    # ============================================================
    # Variance contribution table — EAT + Delta
    # ============================================================
    print("\n" + "=" * 70)
    print("  TOP 10 PER-FOOD VARIANCE CONTRIBUTORS — EAT (+Market+EF)")
    print("=" * 70)
    top10_eat = np.argsort(eat_contrib)[::-1][:10]
    print(f"{'Food':<20s}  {'Contrib':>8s}  {'% of Total Var':>15s}")
    print("-" * 50)
    for i in top10_eat:
        print(f"  {ALL_FOODS[i]:<20s}  {eat_contrib[i]:8.0f}  {eat_contrib[i]/np.var(eat_steps[3])*100:14.1f}%")

    print(f"\n{'='*70}")
    print("  TOP 10 PER-FOOD VARIANCE CONTRIBUTORS — Delta (+Market+EF)")
    print(f"{'='*70}")
    top10_del = np.argsort(del_contrib)[::-1][:10]
    for i in top10_del:
        print(f"  {ALL_FOODS[i]:<20s}  {del_contrib[i]:8.0f}  {del_contrib[i]/np.var(del_steps[3])*100:14.1f}%")

    # Save per-food MC results for the waterfall overlay
    npz_save = os.path.join(out_dir, "MC_Waterfall_Data.npz")
    np.savez(npz_save,
             eaf_tf=eaf_tf, epf_tf=epf_tf,
             cur_af1=cur_af1, cur_pf1=cur_pf1,
             eaf0=eaf0, epf0=epf0,
             cur_af0=cur_af0, cur_pf0=cur_pf0,
             animal_foods=np.array(animal_foods), plant_foods=np.array(plant_foods))
    print(f"Saved MC waterfall data: {npz_save}")

    print(f"\nDone — Output: {out_dir}")
    plt.rcParams.update(_rc)

def corner_bound():
    src_path = os.path.join(FILE_DIR, "F3_Waterfall_Miti.py")
    src = open(src_path, encoding="utf-8").read()

    def slice_between(a_marker, b_marker):
        a = src.index(a_marker)
        a = src.rfind("\n", 0, a) + 1
        b = src.index(b_marker, a)
        b = src.rfind("\n", 0, b) + 1
        return src[a:b]


    code = textwrap.dedent(slice_between("# ---- MC Simulation", "# ======== Map 22 foods"))
    ns = {"np": np}
    exec(compile(code, "F3-data", "exec"), ns)

    eaf_ef, epf_ef = ns["eaf_ef"], ns["epf_ef"]
    cur_af1, cur_pf1 = ns["cur_af1"], ns["cur_pf1"]
    delta_af_ef = eaf_ef - cur_af1          # paired EF-only deltas (1000, 8)
    delta_pf_ef = epf_ef - cur_pf1          # (1000, 14)
    delta_af_base = ns["delta_af_base"]     # deterministic deltas (8,)
    delta_pf_base = ns["delta_pf_base"]     # (14,)
    tm_af, tm_pf = ns["tm_af"], ns["tm_pf"] # sampled erosion fractions
    af_names = ns["animal_foods"]
    pf_names = ns["plant_foods"]

    # Compiled bounds for the three major ASFs (Option B formula, Supp. Table 11)
    T_MAX = {"Beef": 0.266, "Milk": 0.415, "Pork": 0.365}
    T_MIN = {"Beef": 0.074, "Milk": 0.098, "Pork": 0.129}
    T_MID = {k: 0.5 * (T_MIN[k] + T_MAX[k]) for k in T_MAX}
    # Animal fats: co-product of pigs and cattle. The per-iteration fraction is a
    # convex combination of the beef and pork draws with an unknown (uniform) weight,
    # so it spans the union of the parent ranges [0.074, 0.365].
    T_FAT_MAX = max(T_MAX["Beef"], T_MAX["Pork"])   # 0.365 - maximum parent bound
    T_FAT_MIN = min(T_MIN["Beef"], T_MIN["Pork"])   # 0.074 - minimum parent bound
    T_FAT_MID = 0.5 * (T_FAT_MIN + T_FAT_MAX)       # 0.2195 - range midpoint

    # Literature-consistent responses of the foods without compiled ranges
    T_EGG_POULTRY = 1.0   # production constant in the CGE models -> P2C_lit = 0
    T_MUTTON = 0.76       # t = (0.974 - 0.23)/0.974; P2C_ours from Diet_Y_change_compr
    HORT = ["Fruits", "Pulses", "Vegetables", "Nuts", "Potatoes"]    # P2C 0.19-0.28; potato is a horticulture proxy (its PHD delta is negative, so this erodes a reduction)
    T_HORT_MEAN = 0.745   # mean of the compiled horticulture-type bounds: midpoint of 0.70-0.79 / 0.79
    GRAINS = ["Barley", "Maize", "Oats", "Rye", "Wheat"] # production marginal -> P2C 0

    det_total = delta_af_base.sum() + delta_pf_base.sum()

    def summarize(tot):
        lo, hi = np.percentile(tot, [2.5, 97.5])
        return tot.mean(), lo, hi

    rows = []

    # 1. Deterministic
    rows.append(("Deterministic baseline", det_total, det_total, det_total))

    # 2. Central MC (already sampled: majors uniform over compiled bounds,
    #    all other foods t = 0)
    tot_central = ns["delta_af_mc"].sum(1) + ns["delta_pf_mc"].sum(1)
    rows.append(("Central MC (independent draws)", *summarize(tot_central)))

    # 3. Corner: 3 major ASFs at upper bound, the rest as in the central setup
    tA = tm_af.copy()
    for j, f in enumerate(af_names):
        if f in T_MAX:
            tA[:, j] = T_MAX[f]
    tA[:, af_names.index("Animal_fats")] = T_FAT_MAX   # fats at the maximum parent bound
    tot_A = (delta_af_ef * (1 - tA)).sum(1) + (delta_pf_ef * (1 - tm_pf)).sum(1)
    rows.append(("Adversarial corner (all at upper bound)", *summarize(tot_A)))

    # [removed 2026-10-29] Lower-bound corner dropped from the reported table (author decision:
    # the reviewer asks for the extreme case, so only the upper-bound cases are reported). Formula kept for reference.
    # # 4. Lower-bound corner: 3 major ASFs at lower bound (Rieger ends)
    # tL = tm_af.copy()
    # for j, f in enumerate(af_names):
    #     if f in T_MIN:
    #         tL[:, j] = T_MIN[f]
    # tL[:, af_names.index("Animal_fats")] = T_FAT_MIN   # fats at the minimum parent bound
    # tot_L = (delta_af_ef * (1 - tL)).sum(1) + (delta_pf_ef * (1 - tm_pf)).sum(1)
    # rows.append(("Lower-bound corner (Rieger ends)", *summarize(tot_L)))

    # 5. All-evidence case (plant responses at mean): the corner treatment extended to
    #    every food with P2C evidence. 3 major ASFs pinned at their upper bounds and
    #    animal fats at 0.365 (maximum parent bound); mutton 0.76 (unchanged);
    #    horticulture-type PBFs (Fruits, Pulses, Vegetables, Nuts, Potatoes) at the mean
    #    of their compiled bounds (T_HORT_MEAN = 0.745); sugar 0.36. Poultry meat and
    #    eggs are NOT adjusted, nor are grains (t = 0); all other foods stay at t = 0.
    tU = tm_af.copy()
    for j, f in enumerate(af_names):
        if f in T_MAX:
            tU[:, j] = T_MAX[f]
        elif f == "Mutton":
            tU[:, j] = T_MUTTON
    tU[:, af_names.index("Animal_fats")] = T_FAT_MAX   # fats at the maximum parent bound
    tUp = np.zeros_like(tm_pf)
    for j, f in enumerate(pf_names):
        if f in HORT:
            tUp[:, j] = T_HORT_MEAN
        elif f == "Sugar":
            tUp[:, j] = 0.36
    tot_U = (delta_af_ef * (1 - tU)).sum(1) + (delta_pf_ef * (1 - tUp)).sum(1)
    rows.append(("All-evidence case", *summarize(tot_U)))

    print("=" * 88)
    print("  BOUNDING TABLE - market-mediated erosion of the PHD NH3 reduction (kt N)")
    print("  Choice B delta formula; Option B bounds; EUR+NE scope; n=1000")
    print("=" * 88)
    print(f"{'Case':<38} {'Mean':>9} {'95% CI low':>11} {'95% CI high':>12}")
    print("-" * 88)
    for name, m, lo, hi in rows:
        print(f"{name:<38} {m:9.1f} {lo:11.1f} {hi:12.1f}")

    # Output directory (shared with the other uncertainty modules)
    OUT_DIR = UNC_DIR
    out_csv = os.path.join(OUT_DIR, "corner_bounding_table.csv")
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("case,mean_kt,ci_low_kt,ci_high_kt\n")
        for name, m, lo, hi in rows:
            f.write(f"{name},{m:.2f},{lo:.2f},{hi:.2f}\n")
    print(f"\nSaved: {out_csv}")

    # Comparison figure (forest-plot style, SVG only)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        names = [r[0] for r in rows]
        means = [r[1] for r in rows]
        los = [r[2] for r in rows]
        his = [r[3] for r in rows]

        fig, ax = plt.subplots(figsize=(8.6, 3.8))
        y = np.arange(len(rows))[::-1]          # top-to-bottom: deterministic, central, corner, all-evidence
        colors = ["#777777", "#2C7BB6", "#D7191C", "#FDAE61"]

        for i, (yi, m, lo, hi, c) in enumerate(zip(y, means, los, his, colors)):
            if i == 0:
                # Deterministic row: degenerate CI -> marker only, no interval line
                ax.plot([m], [yi], "o", color=c, ms=9, zorder=3)
                ax.text(m + 15, yi, f"{m:,.0f} kt N", fontsize=8, color="#333333",
                        va="center", ha="left")
            else:
                ax.plot([lo, hi], [yi, yi], color="#333333", lw=1.5,
                        solid_capstyle="round", zorder=2)
                ax.plot([m], [yi], "o", color=c, ms=9, zorder=3)
                ax.text(hi + 15, yi, f"{m:,.0f} kt N", fontsize=8, color="#333333",
                        va="center", ha="left")

        # Deterministic reference
        ax.axvline(det_total, color="#888888", ls="--", lw=1, zorder=1)
        ax.text(det_total + 10, 3.5, "deterministic", fontsize=7.5, color="#666666",
                va="center", ha="left")

        # Policy ceilings
        import matplotlib.patheffects as pe
        for xv, cv, lab in ((-800, "#B2182B", "MTFR ceiling 0.80 Tg N"),
                            (-440, "#1A9850", "NECD target 0.44 Tg N")):
            ax.axvline(xv, color=cv, ls=":", lw=1, zorder=1)
            ax.text(xv - 6, 3.5, lab, fontsize=7.5, color=cv,
                    rotation=0, va="center", ha="right", zorder=5,
                    path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

        # Primary x-axis: kt N
        ax.set_xlabel("NH3 emission change relative to the base year (kt N)", fontsize=10)
        ax.set_xlim(min(los) - 60, max(his) + 320)

        # Secondary top x-axis: Tg N
        secax = ax.secondary_xaxis("top", functions=(lambda x: x / 1000.0, lambda x: x * 1000.0))
        secax.set_xlabel("Tg N", fontsize=10)
        secax.set_xticks(np.arange(-1.6, -0.3, 0.2))

        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=9)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.tick_params(axis="y", length=0)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        out_svg = os.path.join(OUT_DIR, "corner_bounding_figure.svg")
        fig.savefig(out_svg, bbox_inches="tight")
        print(f"Saved: {out_svg}")
    except Exception as e:
        print("Figure skipped:", e)


if __name__ == "__main__":
    full_adoption_analysis()
    corner_bound()
