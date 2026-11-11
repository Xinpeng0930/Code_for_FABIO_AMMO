# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# E2 — spatial uncertainty of the PHD emission change (Fig. 4, SI S10)
# Functions:
#   spatial_uncertainty_maps() — per-pixel uncertainty maps from the MC draws
#   country_ua()               — country-level uncertainty accounting (DK/IE/NL)
#   package3_maps()            — high-resolution country-accounted maps
#   si10_panels()              — supplementary panel figure
import os
import sys
import json
import pickle
import gc
from collections import defaultdict

import numpy as np
import rasterio
from rasterio.features import rasterize
import fiona
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_path

if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

np.set_printoptions(precision=4, suppress=True)

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
UNC_DIR = os.environ.get("AMMO_UNC_DIR", os.path.join(FILE_DIR, "Figures", "uncertainty"))
os.makedirs(UNC_DIR, exist_ok=True)
SHP_PATH = os.environ.get("AMMO_SHP", os.path.join(FILE_DIR, "Data_shp", "Global_map_geo.shp"))
E1_PATH = os.path.join(FILE_DIR, "E1_UA_FullAdoption_Deep.py")
NODATA = -999.0
SHAPE = None


def spatial_uncertainty_maps():
    # 0. Load the MC data
    # ================================================================
    NPZ = os.path.join(UNC_DIR, "MC_Waterfall_Data.npz")
    d = np.load(NPZ, allow_pickle=True)
    eaf_tf = d["eaf_tf"]        # EAT animal +Trade+EF (1000, 8)
    epf_tf = d["epf_tf"]        # EAT plant +Trade+EF (1000, 14)
    cur_af1 = d["cur_af1"]      # Current animal EF (1000, 8)
    cur_pf1 = d["cur_pf1"]      # Current plant EF (1000, 14)
    eaf0 = d["eaf0"]            # EAT animal baseline (1000, 8)
    epf0 = d["epf0"]            # EAT plant baseline (1000, 14)
    cur_af0 = d["cur_af0"]      # Current animal baseline (1000, 8)
    cur_pf0 = d["cur_pf0"]      # Current plant baseline (1000, 14)
    animal_foods = list(d["animal_foods"])
    plant_foods = list(d["plant_foods"])

    # Paired delta: EAT (+Trade+EF) - Current (EF), same EF draws
    delta_af = eaf_tf - cur_af1          # (1000, 8)
    delta_pf = epf_tf - cur_pf1          # (1000, 14)
    base_delta_af = eaf0[0] - cur_af0[0]   # (8,)
    base_delta_pf = epf0[0] - cur_pf0[0]   # (14,)

    # ================================================================
    # 1. Inputs / outputs
    # ================================================================
    Delta_emi_paths = Imp_func.open_plk(FABIO_path.Prj_Pkl_output_wd +
        'EAT_Consupdriven_Emicut_Approach1.pkl')

    UA_map_dir = UNC_DIR + os.sep
    os.makedirs(UA_map_dir, exist_ok=True)

    EXAMPLE_RAS = Pj_path.Exam_500area_wd
    NODATA = -999.0
    EPS = 1e-6
    SIGN_COHERENCE_MIN = 0.2
    CHUNK = 50_000

    # ================================================================
    # 2. Food-name bridge
    # ================================================================
    mc_names = list(animal_foods) + list(plant_foods)

    ANIMAL_KEY2MC = {
        'Beef': 'Beef', 'Milk': 'Milk', 'Eggs': 'Egg',
        'Animal fats': 'Animal_fats',
        'Other ASFs': 'Other_ASFs',
        'Mutton': 'Mutton', 'Pork': 'Pork',
        'Pultry meat': 'Poultry_meat',
    }

    PLANT_KEY2MC = {
        'Fruits': 'Fruits', 'Barley': 'Barley', 'Pulses': 'Pulses',
        'Drinks_alcohol': 'Drink', 'Drinks_nonalcohol': 'Drink',
        'Potatoes': 'Potatoes', 'Other_cereals': 'Wheat',
        'Vegetables': 'Vegetables', 'Vegetable oils': 'Vegetable_oils',
        'Nuts': 'Nuts', 'Sugar': 'Sugar', 'Maize': 'Maize', 'Oats': 'Oats',
        'Oil crops': 'Oil_crops', 'Rye': 'Rye', 'Wheat': 'Wheat',
    }

    PLANT_AGG_EXCLUDE = {'Cereals', 'Pulses_Nuts', 'Fruits_Vege'}

    sample_for = {nm: delta_af[:, j] for j, nm in enumerate(animal_foods)}
    sample_for.update({nm: delta_pf[:, j] for j, nm in enumerate(plant_foods)})
    n_sim = delta_af.shape[0]

    R_animal_total = delta_af.sum(1) / base_delta_af.sum()
    R_plant_total = delta_pf.sum(1) / base_delta_pf.sum()

    # ================================================================
    # 3. Read base maps
    # ================================================================
    def read_delta(path):
        global SHAPE
        a = rasterio.open(path).read(1).astype(np.float32)
        if SHAPE is None:
            SHAPE = a.shape
        a[np.isnan(a)] = 0.0
        a[a == NODATA] = 0.0
        return a.ravel()

    def make_weight(foot):
        net = float(foot.sum())
        gross = float(np.abs(foot).sum())
        if gross < EPS:
            return foot * 0.0, 0.0, 'empty'
        if abs(net) / gross >= SIGN_COHERENCE_MIN:
            return foot / net, net, 'signed'
        return np.abs(foot) / gross, gross, 'abs'

    def build_entries(map_items, key2mc, group_proxy):
        combined = {}
        proxies = []
        for key, arr in map_items:
            mc = key2mc.get(key)
            if mc is None:
                print(f"  [warn] '{key}' unmatched -> group-total multiplier")
                proxies.append((key, arr))
            else:
                combined[mc] = combined.get(mc, 0.0) + arr

        entries = []
        for mc, foot in combined.items():
            w, _, mode = make_weight(foot)
            if mode != 'signed':
                print(f"  [note] '{mc}' footprint is '{mode}' -> distributed by "
                      f"|base| (sign-cancelling)" if mode == 'abs'
                      else f"  [warn] '{mc}' has no activity -> contributes 0")
            entries.append((mc, w, sample_for[mc], mode))
        for key, foot in proxies:
            w, norm, mode = make_weight(foot)
            entries.append((key, w, group_proxy * norm, mode))
        return entries

    print("Reading animal base maps (direct + indirect feed)...")
    animal_items = []
    for key, dpath in Delta_emi_paths['Animal_direct'].items():
        arr = read_delta(dpath.replace('\\', '/'))
        ipath = Delta_emi_paths['Animal_indirect'].get(key)
        if ipath:
            arr = arr + read_delta(ipath.replace('\\', '/'))
        animal_items.append((key, arr))

    print("Reading plant base maps...")
    plant_items = []
    for key, ppath in Delta_emi_paths['Plant'].items():
        if key in PLANT_AGG_EXCLUDE:
            continue
        plant_items.append((key, read_delta(ppath.replace('\\', '/'))))

    animal_entries = build_entries(animal_items, ANIMAL_KEY2MC, R_animal_total)
    plant_entries = build_entries(plant_items, PLANT_KEY2MC, R_plant_total)

    print("\nPer-food national delta (mean kt, CV) and spatial weighting mode:")
    for grp, entries in [("animal", animal_entries), ("plant", plant_entries)]:
        for nm, _w, samp, mode in entries:
            mu = float(np.mean(samp))
            cv = float(np.std(samp) / abs(mu)) if abs(mu) > EPS else float('nan')
            print(f"  [{grp}] {nm:<16s} {mode:<6s} mean={mu:9.2f}  cv={cv:5.3f}")

    print(f"\n  animal foods: {len(animal_entries)} | plant foods: {len(plant_entries)} "
          f"| grid: {SHAPE}")

    # ================================================================
    # 4. Per-pixel MC propagation
    # ================================================================
    def process_group(entries, name):
        arrs = [w for _, w, _, _ in entries]
        Msub = np.ascontiguousarray(
            np.array([samp for _, _, samp, _ in entries], dtype=np.float32))
        n_pix = arrs[0].shape[0]

        mean = np.empty(n_pix, np.float32)
        std = np.empty(n_pix, np.float32)
        lo = np.empty(n_pix, np.float32)
        hi = np.empty(n_pix, np.float32)

        for s in range(0, n_pix, CHUNK):
            e = min(s + CHUNK, n_pix)
            Bc = np.empty((e - s, len(arrs)), np.float32)
            for j, a in enumerate(arrs):
                Bc[:, j] = a[s:e]
            sims = Bc @ Msub
            mean[s:e] = sims.mean(axis=1)
            std[s:e] = sims.std(axis=1)
            lo[s:e] = np.percentile(sims, 2.5, axis=1)
            hi[s:e] = np.percentile(sims, 97.5, axis=1)

        cv = np.where(np.abs(mean) < EPS, NODATA,
                      std / np.maximum(np.abs(mean), EPS)).astype(np.float32)

        dtot = delta_af.sum(1) + delta_pf.sum(1)
        print(f"  [{name}] national mean sum = {mean.sum():,.1f} kt "
              f"(MC total = {dtot.mean():,.1f} kt ± {dtot.std():,.1f}) "
              f"-> saved mean/lower95/upper95/cv")

        out = {}
        for tag, vec in [('mean', mean), ('lower95', lo),
                         ('upper95', hi), ('cv', cv)]:
            p = UA_map_dir + f'{name}_Delta_{tag}.tif'
            Imp_func.output_reso_ras_filtered(p, EXAMPLE_RAS, 'EPSG:4326',
                                              vec.reshape(SHAPE))
            out[tag] = p

        del mean, std, lo, hi, cv
        gc.collect()
        return out

    print("\nComputing uncertainty maps...")
    UA_map_paths = {
        'Animal': process_group(animal_entries, 'Animal'),
        'Plant':  process_group(plant_entries, 'Plant'),
        'Total':  process_group(animal_entries + plant_entries, 'Total'),
    }

    Imp_func.save_plk(UA_map_dir + 'EAT_Consupdriven_Emicut_UA_maps.pkl', UA_map_paths)
    print("\nSaved path index -> EAT_Consupdriven_Emicut_UA_maps.pkl")
    print("Done.")


def country_ua():
    BASE = os.path.dirname(os.path.abspath(__file__))
    OUT_DIR = UNC_DIR
    os.makedirs(OUT_DIR, exist_ok=True)

    NPZ = os.path.join(OUT_DIR, "MC_Waterfall_Data.npz")
    PKL = os.path.join(FABIO_path.Prj_Pkl_output_wd, "EAT_Consupdriven_Emicut_Approach1.pkl")
    MAPS_PKL = os.path.join(FABIO_path.Prj_Pkl_output_wd, "ScenEmi_Maps_Foodspec.pkl")
    SHP = SHP_PATH
    E1_SRC = E1_PATH

    NODATA = -999.0

    # ----------------------------------------------------------------------
    # 1. Food bridges
    # ----------------------------------------------------------------------
    ANIMAL_KEY2MC = {
        'Beef': 'Beef', 'Milk': 'Milk', 'Eggs': 'Egg',
        'Animal fats': 'Animal_fats', 'Other ASFs': 'Other_ASFs',
        'Mutton': 'Mutton', 'Pork': 'Pork', 'Pultry meat': 'Poultry_meat',
    }
    PLANT_KEY2MC = {
        'Fruits': 'Fruits', 'Barley': 'Barley', 'Pulses': 'Pulses',
        'Drinks_alcohol': 'Drink', 'Drinks_nonalcohol': 'Drink',
        'Potatoes': 'Potatoes', 'Other_cereals': 'Wheat',
        'Vegetables': 'Vegetables', 'Vegetable oils': 'Vegetable_oils',
        'Nuts': 'Nuts', 'Sugar': 'Sugar', 'Maize': 'Maize', 'Oats': 'Oats',
        'Oil crops': 'Oil_crops', 'Rye': 'Rye', 'Wheat': 'Wheat',
    }
    PLANT_AGG_EXCLUDE = {'Cereals', 'Pulses_Nuts', 'Fruits_Vege'}

    # ----------------------------------------------------------------------
    # 2. Country masks
    # ----------------------------------------------------------------------
    COUNTRIES = {"DNK": "Denmark", "IRL": "Ireland", "NLD": "Netherlands"}
    TARGETS = ["DNK", "IRL", "NLD"]


    def load_masks(shape, transform):
        masks = {}
        with fiona.open(SHP) as src:
            for f in src:
                iso = f["properties"]["ISO_FABIO"]
                if iso in COUNTRIES:
                    masks[iso] = rasterize(
                        [(f["geometry"], 1)], out_shape=shape, transform=transform,
                        fill=0, dtype="uint8", all_touched=False)
        return masks


    # ----------------------------------------------------------------------
    # 3. Per-food country shares from the deterministic delta maps
    #    (same weighting rule as the map step)
    # ----------------------------------------------------------------------
    def make_weight(foot):
        net = float(foot.sum())
        gross = float(np.abs(foot).sum())
        if gross < 1e-6:
            return foot * 0.0
        if abs(net) / gross >= 0.2:
            return foot / net
        return np.abs(foot) / gross


    def country_shares():
        P = pickle.load(open(PKL, "rb"))
        food_map = defaultdict(lambda: None)
        for key, path in P["Animal_direct"].items():
            mc = ANIMAL_KEY2MC.get(key)
            if mc is None:
                continue
            arr = read_raster(path)
            ipath = P["Animal_indirect"].get(key)
            if ipath:
                arr = arr + read_raster(ipath)
            food_map[mc] = arr if food_map[mc] is None else food_map[mc] + arr
        for key, path in P["Plant"].items():
            if key in PLANT_AGG_EXCLUDE:
                continue
            mc = PLANT_KEY2MC.get(key)
            if mc is None:
                continue
            arr = read_raster(path)
            food_map[mc] = arr if food_map[mc] is None else food_map[mc] + arr
        return food_map


    _GRID = {}


    def read_raster(path):
        with rasterio.open(path.replace("\\", "/")) as src:
            a = src.read(1).astype("float64")
            _GRID["shape"] = a.shape
            _GRID["transform"] = src.transform
        a[a == NODATA] = 0.0
        return a


    # ----------------------------------------------------------------------
    # 4. Recover the central-MC draws (t_j(s), paired EF draws)
    # ----------------------------------------------------------------------
    def load_e1_head():
        src = open(E1_SRC, encoding="utf-8").read()
        head = src.split("def full_adoption_analysis():")[0]
        ns = {"__name__": "e1_head", "__file__": E1_SRC}
        exec(compile(head, E1_SRC, "exec"), ns)
        return ns


    # ----------------------------------------------------------------------
    # Main
    # ----------------------------------------------------------------------
    def main():
        print("=" * 78)
        print("E2 -- country-level spatial UA (DK / IE / NL)")
        print("=" * 78)

        # ---- country masks
        food_map = country_shares()
        shape, transform = _GRID["shape"], _GRID["transform"]
        masks = load_masks(shape, transform)
        print(f"grid {shape} | masks: " +
              ", ".join(f"{COUNTRIES[k]}={int(v.sum())} cells" for k, v in masks.items()))

        # ---- national per-food deterministic delta (model) and country shares
        h = load_e1_head()
        eaf0 = h["compute_eat_per_food"](h["ones_a"], h["ones_a"], h["ones_p"], h["ones_p"], False)[0]
        epf0 = h["compute_eat_per_food"](h["ones_a"], h["ones_a"], h["ones_p"], h["ones_p"], False)[1]
        det_af = eaf0[0] - h["cur_af0"][0]
        det_pf = epf0[0] - h["cur_pf0"][0]
        animal_foods = list(h["animal_foods"])
        plant_foods = list(h["plant_foods"])
        all_foods = animal_foods + plant_foods
        det = dict(zip(animal_foods, det_af))
        det.update(dict(zip(plant_foods, det_pf)))

        shares = {}
        for mc, arr in food_map.items():
            w = make_weight(arr)
            tot = w.sum()
            shares[mc] = {iso: float((w * masks[iso]).sum() / tot) if abs(tot) > 1e-9 else 0.0
                          for iso in TARGETS}

        # ---- central MC per-food delta (national) and EU t draws
        d = np.load(NPZ, allow_pickle=True)
        delta_af = d["eaf_tf"] - d["cur_af1"]
        delta_pf = d["epf_tf"] - d["cur_pf1"]
        n_sim = delta_af.shape[0]
        tm_af = h["tm_af"].copy()   # (n_sim, 8) EU market draws, same seed
        tm_pf = h["tm_pf"].copy()

        idx = {f: i for i, f in enumerate(animal_foods)}
        w_fat = h["_w_fat"].copy()

        MARKET = ["Beef", "Milk", "Pork", "Animal_fats"]
        RATIO = {  # Geibel country / Geibel EU, Lancet_full
            "DNK": {"Beef": 0.33 / 0.27, "Milk": 0.46 / 0.42, "Pork": 0.66 / 0.36},
            "IRL": {"Beef": 0.53 / 0.27, "Milk": 0.94 / 0.42, "Pork": 0.68 / 0.36},
        }
        RATIO["NLD"] = dict(RATIO["DNK"])          # DK-type proxy

        # central EU market t per food (same arrays as the MC data)
        t_eu = {f: tm_af[:, idx[f]] for f in ["Beef", "Milk", "Pork"]}
        t_eu["Animal_fats"] = tm_af[:, idx["Animal_fats"]]

        # country t: whole-range multiplication; fats = convex combo of scaled parents
        t_c = {}
        for iso in TARGETS:
            r = RATIO[iso]
            tc = {"Beef": r["Beef"] * t_eu["Beef"],
                  "Milk": r["Milk"] * t_eu["Milk"],
                  "Pork": r["Pork"] * t_eu["Pork"]}
            tc["Animal_fats"] = (w_fat * tc["Beef"] + (1.0 - w_fat) * tc["Pork"])
            t_c[iso] = tc

        # ---- per-country MC
        def country_delta(iso):
            out = np.zeros(n_sim)
            for j, f in enumerate(animal_foods):
                w = shares[f][iso] if f in shares else 0.0
                kappa = np.ones(n_sim)
                if f in MARKET:
                    kappa = (1.0 - t_c[iso][f]) / (1.0 - t_eu[f])
                out += w * delta_af[:, j] * kappa
            for j, f in enumerate(plant_foods):
                w = shares[f][iso] if f in shares else 0.0
                out += w * delta_pf[:, j]
            return out

        # ---- rest-of-EU compensation (per food, per iteration for fats)
        def rest_kappa(f):
            wsum = sum(shares[f][iso] for iso in TARGETS)
            if f == "Animal_fats":
                num = 1.0 - sum(shares[f][iso] * t_c[iso][f] / t_eu[f] for iso in TARGETS)
            else:
                num = 1.0 - sum(shares[f][iso] * RATIO[iso][f] for iso in TARGETS)
            den = 1.0 - wsum
            return num / den

        kappa_rest = {f: rest_kappa(f) for f in MARKET}

        # ---- 2017 base emissions from the current (base-year) broad maps
        base = {iso: 0.0 for iso in TARGETS}
        mp = pickle.load(open(MAPS_PKL, "rb"))
        for p in mp["Curr"]["Broad_drivn_type"].values():
            with rasterio.open(p.replace("\\", "/")) as s:
                a = s.read(1).astype("float64")
            a[a == NODATA] = 0.0
            for iso in TARGETS:
                base[iso] += float((a * masks[iso]).sum()) / 1e6  # kt

        # ---- results
        print("\n--- country shares of the national per-food delta ---")
        hdr = f"{'food':<15}" + "".join(f"{COUNTRIES[k]:>13}" for k in TARGETS)
        print(hdr)
        for f in MARKET + ["Egg", "Mutton", "Poultry_meat"]:
            print(f"{f:<15}" + "".join(f"{shares[f][k]*100:12.2f}%" for k in TARGETS))

        rows = []
        for iso in TARGETS:
            cut = sum(shares[f][iso] * det[f] for f in all_foods if f in shares)
            dl = country_delta(iso)
            net = float(dl.mean())
            erosion = net - cut          # positive = mitigation removed
            rows.append(dict(iso=iso, country=COUNTRIES[iso], base=base[iso],
                             cut=cut, erosion=erosion, net=net,
                             share=100.0 * net / base[iso]))

        print("\n--- Set B: country-revised central estimates (kt N) ---")
        print(f"{'country':<13}{'2017':>9}{'det cut':>10}{'erosion':>10}"
              f"{'net cut':>10}{'share':>8}{'eroded':>8}")
        for r in rows:
            print(f"{r['country']:<13}{r['base']:9.1f}{r['cut']:10.1f}"
                  f"{r['erosion']:10.1f}{r['net']:10.1f}{r['share']:7.1f}%"
                  f"{100*r['erosion']/abs(r['cut']):7.1f}%")

        # ---- EU-invariance check
        rest = np.zeros(n_sim)
        def wsum_of(f):
            return sum(shares[f][iso] for iso in TARGETS) if f in shares else 0.0
        for j, f in enumerate(animal_foods):
            if f in MARKET:
                rest += (1.0 - wsum_of(f)) * delta_af[:, j] * (1.0 - kappa_rest[f] * t_eu[f]) / (1.0 - t_eu[f])
            else:
                rest += (1.0 - wsum_of(f)) * delta_af[:, j]
        for j, f in enumerate(plant_foods):
            rest += (1.0 - wsum_of(f)) * delta_pf[:, j]
        ctry_sum = np.sum([country_delta(iso) for iso in TARGETS], axis=0)
        eu_central = float((delta_af.sum(1) + delta_pf.sum(1)).mean())
        print(f"\nEU central MC total          : {eu_central:9.1f} kt N")
        print(f"Sum(3 countries) + rest      : {float((ctry_sum + rest).mean()):9.1f} kt N"
              f"  (diff {float((ctry_sum + rest).mean()) - eu_central:+.3f})")
        print("rest-of-EU kappa (market t scale): " +
              ", ".join(f"{f}={float(np.mean(kappa_rest[f])):.3f}" for f in MARKET))
        rest_cut = sum((1.0 - (sum(shares[f][iso] for iso in TARGETS) if f in shares else 0.0)) * det[f]
                       for f in all_foods if f in det)
        rest_base = base["DNK"] + base["IRL"] + base["NLD"]
        rest_base = 0.0
        # EU total base from the same broad maps
        for p in mp["Curr"]["Broad_drivn_type"].values():
            with rasterio.open(p.replace("\\", "/")) as s:
                a = s.read(1).astype("float64")
            a[a == NODATA] = 0.0
            rest_base += float(a.sum()) / 1e6
        rest_base -= sum(r["base"] for r in rows)
        rest_net = float(rest.mean())
        print(f"Rest of EU: cut={rest_cut:.1f} net={rest_net:.1f} "
              f"share={100*rest_net/rest_base:.1f}% (base {rest_base:.1f})")

        # ---- t table
        EU_RANGE = {"Beef": (0.074, 0.266), "Milk": (0.098, 0.415),
                    "Pork": (0.129, 0.365)}
        print("\n--- t table (whole-range multiplication) ---")
        print(f"{'food':<13}{'EU range':>16}{'DK range':>18}{'IE range':>18}{'NL range':>18}")
        for f in ["Milk", "Beef", "Pork"]:
            lo, hi = EU_RANGE[f]
            cells = []
            for iso in TARGETS:
                r = RATIO[iso][f]
                cells.append(f"{r*lo:.3f}-{r*hi:.3f}")
            print(f"{f:<13}{f'{lo:.3f}-{hi:.3f}':>16}" + "".join(f"{c:>18}" for c in cells))
        print(f"{'Animal_fats':<13}{'0.074-0.365':>16}"
              f"{'combo beef/pork':>18}{'combo beef/pork':>18}{'combo beef/pork':>18}")

        # ---- write CSV
        csv = os.path.join(OUT_DIR, "country_spatial_bound.csv")
        with open(csv, "w", encoding="utf-8") as fh:
            fh.write("country,base2017_kt,det_cut_kt,erosion_kt,erosion_pct_of_cut,"
                     "net_cut_kt,share_pct\n")
            for r in rows:
                fh.write(f"{r['country']},{r['base']:.2f},{r['cut']:.2f},"
                         f"{r['erosion']:.2f},{100*r['erosion']/abs(r['cut']):.2f},"
                         f"{r['net']:.2f},{r['share']:.2f}\n")
            r_ero = rest_net - rest_cut
            fh.write(f"Rest of EU,{rest_base:.2f},{rest_cut:.2f},"
                     f"{r_ero:.2f},{100*r_ero/abs(rest_cut):.2f},"
                     f"{rest_net:.2f},{100*rest_net/rest_base:.2f}\n")
            fh.write(f"EU central MC,,,,,,"
                     f"{100*eu_central/2680.4:.2f}\n")
        print(f"\nSaved: {csv}")

        # ---- save json for the figure / md text
        js = os.path.join(OUT_DIR, "country_spatial_bound.json")
        with open(js, "w", encoding="utf-8") as fh:
            json.dump(dict(rows=rows,
                           ratios=RATIO,
                           shares=shares,
                           kappa_rest={k: float(np.mean(v)) for k, v in kappa_rest.items()},
                           eu_central=eu_central), fh, indent=2)
        print(f"Saved: {js}")



    main()


def package3_maps():
    BASE = os.path.dirname(os.path.abspath(__file__))
    OUT = UNC_DIR

    NPZ = os.path.join(OUT, "MC_Waterfall_Data.npz")
    PKL = os.path.join(FABIO_path.Prj_Pkl_output_wd, "EAT_Consupdriven_Emicut_Approach1.pkl")
    SHP = SHP_PATH
    E1_SRC = E1_PATH
    TEMPLATE = os.path.join(OUT, "Total_Delta_mean.tif")
    NODATA = -999.0
    CHUNK = 25000

    ANIMAL_KEY2MC = {
        'Beef': 'Beef', 'Milk': 'Milk', 'Eggs': 'Egg',
        'Animal fats': 'Animal_fats', 'Other ASFs': 'Other_ASFs',
        'Mutton': 'Mutton', 'Pork': 'Pork', 'Pultry meat': 'Poultry_meat',
    }
    PLANT_KEY2MC = {
        'Fruits': 'Fruits', 'Barley': 'Barley', 'Pulses': 'Pulses',
        'Drinks_alcohol': 'Drink', 'Drinks_nonalcohol': 'Drink',
        'Potatoes': 'Potatoes', 'Other_cereals': 'Wheat',
        'Vegetables': 'Vegetables', 'Vegetable oils': 'Vegetable_oils',
        'Nuts': 'Nuts', 'Sugar': 'Sugar', 'Maize': 'Maize', 'Oats': 'Oats',
        'Oil crops': 'Oil_crops', 'Rye': 'Rye', 'Wheat': 'Wheat',
    }
    PLANT_AGG_EXCLUDE = {'Cereals', 'Pulses_Nuts', 'Fruits_Vege'}
    COUNTRIES = {"DNK": "Denmark", "IRL": "Ireland", "NLD": "Netherlands"}
    TARGETS = ["DNK", "IRL", "NLD"]
    MARKET = ["Beef", "Milk", "Pork", "Animal_fats"]
    RATIO = {
        "DNK": {"Beef": 0.33 / 0.27, "Milk": 0.46 / 0.42, "Pork": 0.66 / 0.36},
        "IRL": {"Beef": 0.53 / 0.27, "Milk": 0.94 / 0.42, "Pork": 0.68 / 0.36},
    }
    RATIO["NLD"] = dict(RATIO["DNK"])


    def read_raster(path):
        with rasterio.open(path.replace("\\", "/")) as src:
            a = src.read(1).astype("float32")
        a[a == NODATA] = 0.0
        return a


    def make_weight(foot):
        net = float(foot.sum())
        gross = float(np.abs(foot).sum())
        if gross < 1e-6:
            return foot * 0.0
        if abs(net) / gross >= 0.2:
            return foot / net
        return np.abs(foot) / gross


    def main():
        print("=" * 78)
        print("E2 Package 3 -- country-accounted high-resolution maps")
        print("=" * 78)

        # ---- central-MC draws (same as the MC data)
        src = open(E1_SRC, encoding="utf-8").read()
        head = src.split("def full_adoption_analysis():")[0]
        ns = {"__name__": "e1_head", "__file__": E1_SRC}
        exec(compile(head, E1_SRC, "exec"), ns)
        animal_foods = list(ns["animal_foods"])
        plant_foods = list(ns["plant_foods"])
        tm_af = ns["tm_af"].copy()
        idx = {f: i for i, f in enumerate(animal_foods)}
        w_fat = ns["_w_fat"].copy()

        d = np.load(NPZ, allow_pickle=True)
        delta_af = (d["eaf_tf"] - d["cur_af1"]).astype("float64")
        delta_pf = (d["epf_tf"] - d["cur_pf1"]).astype("float64")
        n_sim = delta_af.shape[0]

        # ---- food footprints -> weights and country shares
        P = pickle.load(open(PKL, "rb"))
        food_map = defaultdict(lambda: None)
        for key, path in P["Animal_direct"].items():
            mc = ANIMAL_KEY2MC.get(key)
            if mc is None:
                continue
            arr = read_raster(path)
            ipath = P["Animal_indirect"].get(key)
            if ipath:
                arr = arr + read_raster(ipath)
            food_map[mc] = arr if food_map[mc] is None else food_map[mc] + arr
        for key, path in P["Plant"].items():
            if key in PLANT_AGG_EXCLUDE:
                continue
            mc = PLANT_KEY2MC.get(key)
            if mc is None:
                continue
            arr = read_raster(path)
            food_map[mc] = arr if food_map[mc] is None else food_map[mc] + arr

        with rasterio.open(TEMPLATE) as tpl:
            profile = tpl.profile.copy()
            shp = (tpl.height, tpl.width)
            transform = tpl.transform

        masks = {}
        with fiona.open(SHP) as src_shp:
            for f in src_shp:
                iso = f["properties"]["ISO_FABIO"]
                if iso in COUNTRIES:
                    masks[iso] = rasterize([(f["geometry"], 1)], out_shape=shp,
                                           transform=transform, fill=0,
                                           dtype="uint8", all_touched=False)

        # pixel groups: 0 = rest-of-EU, 1..3 = DK/IE/NL
        ctry_id = np.zeros(shp, dtype="uint8")
        for k, iso in enumerate(TARGETS, start=1):
            ctry_id[masks[iso] == 1] = k

        # food list used by the maps (only foods with a footprint)
        map_foods = [f for f in animal_foods + plant_foods if f in food_map]
        print("mapped foods:", len(map_foods), "| unmapped:",
              [f for f in animal_foods + plant_foods if f not in food_map])

        W = np.zeros((shp[0] * shp[1], len(map_foods)), dtype="float32")
        shares = {}
        for j, f in enumerate(map_foods):
            w = make_weight(food_map[f]).ravel()
            W[:, j] = w
            tot = float(w.sum())
            shares[f] = {iso: float((w.reshape(shp) * masks[iso]).sum() / tot)
                         for iso in TARGETS}

        active = np.abs(W).sum(axis=1) > 0
        print("active pixels:", int(active.sum()))

        # ---- national delta matrix (n_food x n_sim)
        M = np.zeros((len(map_foods), n_sim), dtype="float32")
        for j, f in enumerate(map_foods):
            if f in animal_foods:
                M[j] = delta_af[:, animal_foods.index(f)]
            else:
                M[j] = delta_pf[:, plant_foods.index(f)]

        # ---- per-iteration t and factor matrices
        def t_of(food):
            if food in ("Beef", "Milk", "Pork"):
                return tm_af[:, idx[food]]
            return tm_af[:, idx["Animal_fats"]]

        def factor_country(iso):
            F = np.ones((len(map_foods), n_sim), dtype="float64")
            tc = {}
            tc["Beef"] = RATIO[iso]["Beef"] * tm_af[:, idx["Beef"]]
            tc["Milk"] = RATIO[iso]["Milk"] * tm_af[:, idx["Milk"]]
            tc["Pork"] = RATIO[iso]["Pork"] * tm_af[:, idx["Pork"]]
            tc["Animal_fats"] = w_fat * tc["Beef"] + (1 - w_fat) * tc["Pork"]
            for f in MARKET:
                te = t_of(f)
                F[map_foods.index(f)] = (1.0 - tc[f]) / (1.0 - te)
            return F

        def kappa_rest(f):
            wsum = sum(shares[f][iso] for iso in TARGETS)
            if f == "Animal_fats":
                # fats: per-iteration effective ratio
                tc = {iso: (w_fat * RATIO[iso]["Beef"] * tm_af[:, idx["Beef"]]
                            + (1 - w_fat) * RATIO[iso]["Pork"] * tm_af[:, idx["Pork"]])
                      for iso in TARGETS}
                te = tm_af[:, idx["Animal_fats"]]
                num = 1.0 - sum(shares[f][iso] * tc[iso] / te for iso in TARGETS)
            else:
                num = 1.0 - sum(shares[f][iso] * RATIO[iso][f] for iso in TARGETS)
            return num / (1.0 - wsum)

        F_rest = np.ones((len(map_foods), n_sim), dtype="float64")
        kap_mean = {}
        for f in MARKET:
            k = kappa_rest(f)
            te = t_of(f)
            F_rest[map_foods.index(f)] = (1.0 - k * te) / (1.0 - te)
            kap_mean[f] = float(np.mean(k))

        F_c = {iso: factor_country(iso) for iso in TARGETS}
        print("kappa (rest of EU):", {f: round(v, 4) for f, v in kap_mean.items()})

        # ---- per-group per-pixel statistics
        groups = {0: F_rest}
        for k, iso in enumerate(TARGETS, start=1):
            groups[k] = F_c[iso]

        stats = {name: np.full(shp[0] * shp[1], np.nan, dtype="float32")
                 for name in ("mean", "lo", "hi", "cv")}

        for g, F in groups.items():
            sel = (active & (ctry_id.ravel() == g))
            pix = np.where(sel)[0]
            if pix.size == 0:
                continue
            # factor per food, clipped (t<1 by construction)
            Fg = np.clip(F.T, 0.0, None)          # (n_sim, n_food)
            for s in range(0, pix.size, CHUNK):
                ii = pix[s:s + CHUNK]
                B = W[ii]                          # (n_c, n_food) float32
                sims = np.empty((ii.size, n_sim), dtype="float32")
                # loop over iterations in blocks to bound memory
                for a in range(0, n_sim, 200):
                    b = min(a + 200, n_sim)
                    sims[:, a:b] = B @ (M[:, a:b] * Fg[a:b].T).astype("float32")
                stats["mean"][ii] = sims.mean(axis=1)
                stats["lo"][ii] = np.percentile(sims, 2.5, axis=1)
                stats["hi"][ii] = np.percentile(sims, 97.5, axis=1)
                stats["cv"][ii] = sims.std(axis=1) / np.maximum(np.abs(sims.mean(axis=1)), 1e-9)
                del sims, B

        # template nodata mask (outside the European study area)
        with rasterio.open(TEMPLATE) as tpl:
            tmpl_nodata = (tpl.read(1) == NODATA).ravel()
        for name in ("mean", "lo", "hi", "cv"):
            stats[name] = np.where(active, stats[name], 0.0)      # empty land -> 0
            stats[name][tmpl_nodata] = NODATA                     # outside study area

        # ---- validation: country sums vs the country CSV
        def zonal(vec, iso):
            v = np.where(vec == NODATA, 0.0, vec)
            return float((v.reshape(shp) * masks[iso]).sum())

        js = json.load(open(os.path.join(OUT, "country_spatial_bound.json"), encoding="utf-8"))
        expected = {r["iso"]: r["net"] for r in js["rows"]}
        print("\n--- validation (Total mean raster sums, kt N) ---")
        for iso in TARGETS:
            got = zonal(stats["mean"], iso)
            print(f"{iso}: raster {got:9.2f} | reference {expected[iso]:9.2f} | "
                  f"diff {got - expected[iso]:+.3f}")
        print(f"EU mapped total: {float(stats['mean'][~tmpl_nodata].sum()):9.2f} kt "
              f"(EU total -1040.0; unmapped Other_ASFs excluded)")

        # ---- write rasters
        outs = {
            "Animal_mean_country": None,   # filled below (animal-only mean)
            "Total_mean_country": stats["mean"],
            "Total_cv_country": stats["cv"],
            "Total_lower95_country": stats["lo"],
            "Total_upper95_country": stats["hi"],
        }

        # animal-only mean (panel b)
        animal_idx = [j for j, f in enumerate(map_foods) if f in animal_foods]
        anim = np.full(shp[0] * shp[1], np.nan, dtype="float32")
        M_anim = M[animal_idx]
        for g, F in groups.items():
            sel = (active & (ctry_id.ravel() == g))
            pix = np.where(sel)[0]
            if pix.size == 0:
                continue
            for s in range(0, pix.size, CHUNK):
                ii = pix[s:s + CHUNK]
                B = W[np.ix_(ii, animal_idx)]
                sims = np.empty((ii.size, n_sim), dtype="float32")
                for a in range(0, n_sim, 200):
                    b = min(a + 200, n_sim)
                    Fa = F[animal_idx][:, a:b]
                    sims[:, a:b] = B @ (M_anim[:, a:b] * Fa).astype("float32")
                anim[ii] = sims.mean(axis=1)
                del sims, B
        anim = np.where(active, anim, 0.0)
        anim[tmpl_nodata] = NODATA
        outs["Animal_mean_country"] = anim

        for name, arr in outs.items():
            p = os.path.join(OUT, name + ".tif")
            prof = profile.copy()
            prof.update(dtype="float32", count=1, nodata=NODATA)
            with rasterio.open(p, "w", **prof) as dst:
                dst.write(arr.reshape(shp).astype("float32"), 1)
            print("saved", p)

        # quick zonal check for animal
        print("\nAnimal mean country sums:",
              {iso: round(zonal(anim, iso), 2) for iso in TARGETS})



    main()


def si10_panels():
    BASE = os.path.dirname(os.path.abspath(__file__))
    OUT = UNC_DIR
    SHP = SHP_PATH
    NODATA = -999.0
    TARGETS = {"DNK": "DK", "IRL": "IE", "NLD": "NL"}
    LABEL_XY = {"DNK": (9.6, 56.2), "IRL": (-11.5, 52.6), "NLD": (5.3, 52.6)}
    LABEL_DX = {"DNK": (5.0, -0.4), "IRL": (-4.2, -1.2), "NLD": (3.6, 0.4)}

    with open(os.path.join(OUT, "country_spatial_bound.json"), encoding="utf-8") as fh:
        share = {r["iso"]: r["share"] for r in json.load(fh)["rows"]}

    with fiona.open(SHP) as src:
        polys = [(f["properties"]["ISO_FABIO"], f["geometry"]) for f in src]

    GREEN_RED = ["#1a7a3c", "#66bd63", "#a6d96a", "#d9ef8b", "#fee08b", "#d73027"]
    REDS = ["#f7f7f7", "#fee0d2", "#fcbba1", "#fc9272", "#de2d26", "#a50f15"]


    def draw(ax, arr, bounds, colors, legend_labels, title, letter, labels=False,
             legend_title=None):
        a = arr.astype("float64").copy()
        a[a == NODATA] = np.nan
        with rasterio.open(os.path.join(OUT, "Total_Delta_mean.tif")) as s:
            b = s.bounds
        ext = (b.left, b.right, b.bottom, b.top)
        cmap = ListedColormap(colors)
        norm = BoundaryNorm(bounds, cmap.N)
        ax.imshow(a, extent=ext, origin="upper", cmap=cmap, norm=norm,
                  interpolation="nearest")
        for iso, g in polys:
            parts = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
            lw = 1.6 if iso in TARGETS else 0.35
            col = "black" if iso in TARGETS else "0.25"
            for part in parts:
                ring = part[0]
                ax.plot([p[0] for p in ring], [p[1] for p in ring],
                        color=col, lw=lw, zorder=4 if iso in TARGETS else 2)
        if labels:
            for iso, xy in LABEL_XY.items():
                dx, dy = LABEL_DX[iso]
                txt = f"{TARGETS[iso]}: {share[iso]:.0f}%"
                ax.annotate(txt, xy=xy, xytext=(xy[0] + dx, xy[1] + dy),
                            fontsize=8.5, fontweight="bold", zorder=6,
                            bbox=dict(boxstyle="round,pad=0.18", fc="white",
                                      ec="black", lw=0.6),
                            arrowprops=dict(arrowstyle="-", lw=0.8, color="black"))
        ax.set_xlim(-15, 32)
        ax.set_ylim(35, 62)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"{letter}  {title}", fontsize=10, loc="left")
        handles = [Patch(fc=c, ec="none", label=l)
                   for c, l in zip(colors, legend_labels)]
        if labels:
            handles.append(Line2D([0], [0], color="black", lw=1.6, label="DK / IE / NL"))
        ax.legend(handles=handles, loc="lower left", fontsize=7, frameon=False,
                  title=legend_title, title_fontsize=7)


    def load(name):
        with rasterio.open(os.path.join(OUT, name)) as s:
            return s.read(1)


    def main():
        mean_anim = load("Animal_mean_country.tif").astype("float64")
        mean_tot = load("Total_mean_country.tif").astype("float64")
        m_anim = mean_anim == NODATA
        m_tot = mean_tot == NODATA
        mean_anim *= 1000.0
        mean_tot *= 1000.0
        mean_anim[m_anim] = NODATA
        mean_tot[m_tot] = NODATA
        cv = load("Total_cv_country.tif")
        lo = load("Total_lower95_country.tif")
        hi = load("Total_upper95_country.tif")
        hi = hi.astype("float64"); lo = lo.astype("float64")
        hi[hi == NODATA] = 0.0; lo[lo == NODATA] = 0.0
        width = (hi - lo) * 1000.0
        with rasterio.open(os.path.join(OUT, "Total_Delta_mean.tif")) as s0:
            nod = (s0.read(1) == NODATA)
        width[nod] = NODATA

        bins_em = [-1e9, -30, -15, -10, -5, 0, 1e9]
        lab_em = ["< -30", "-30 - -15", "-15 - -10", "-10 - -5", "-5 - 0", "> 0"]
        bins_cv = [-1e9, 0.12, 0.14, 0.18, 0.25, 0.35, 1e9]
        lab_cv = ["< 12%", "12-14%", "14-18%", "18-25%", "25-35%", "> 35%"]
        bins_w = [-1e9, 3, 6, 12, 20, 1e9]
        lab_w = ["< 3", "3-6", "6-12", "12-20", "> 20"]

        specs = [
            ("b", "ASF-driven NH3 emission changes [kt N]", mean_anim, bins_em,
             GREEN_RED, lab_em, False, "ASF-driven\nemission changes"),
            ("c", "Total NH3 emission changes [kt N]", mean_tot, bins_em,
             GREEN_RED, lab_em, True, "Total emission\nchanges"),
            ("d", "Coefficient of variation", cv, bins_cv, REDS, lab_cv, False,
             "Coefficient\nof variation"),
            ("e", "95% confidential interval width [kt N]", width, bins_w,
             REDS[:5], lab_w, False, "95% confidential\ninterval width"),
        ]
        for letter, title, arr, bins, cols, labs, lab_flag, ltitle in specs:
            fig, ax = plt.subplots(figsize=(6.4, 6.0))
            draw(ax, arr, bins, cols, labs, title, letter, labels=lab_flag,
                 legend_title=ltitle)
            plt.tight_layout()
            for extn in ("png", "svg"):
                p = os.path.join(OUT, f"SI10_panel_{letter}.{extn}")
                plt.savefig(p, dpi=300 if extn == "png" else None, bbox_inches="tight")
                print("saved", p)
            plt.close(fig)



    main()


if __name__ == "__main__":
    spatial_uncertainty_maps()
    country_ua()
    package3_maps()
    si10_panels()
