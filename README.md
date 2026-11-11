# FABIO_AMMO — analysis code

Code for the manuscript *Adopting a planetary health diet is critical for reducing
ammonia emissions in Europe* (Nature Food).

## Reference

The methods and results are described in:

> Jin, X., Behrens, P., Erisman, J.W., Navarre, N., & Mogollón, J.M. (2026).
> Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
> *Nature Food*. https://doi.org/<PAPER_DOI>

If you use this code or the data, please cite the paper above and the archived code
release: https://doi.org/10.5281/zenodo.24146167 (Zenodo).

## Contact

Xinpeng Jin — x.jin@cml.leidenuniv.nl / jinxinpeng16@gmail.com

This package contains the analysis pipeline: the FABIO–AP-AMMO coupling, the N-balance
accounting, dietary scenario construction, emission allocation, and the figure and
uncertainty scripts.

## Layout

```
run_pipeline.py        stage driver (base -> phd -> mtfr)
A1_base.py             base year: allocation to consumption (AP-AMMO emissions)
A2_phd.py              planetary health diet: N balance, re-allocation, consumption
A3_mtfr.py             MTFR alone and PHD+MTFR (production side)
AMMO_footprint/        pipeline modules B1-B13 (production/prep), C1-C7 (consumption), D1-D3 (MTFR)
AMMO_footprint/        E1-E3 uncertainty analysis, F1-F5 figures (F1 and F4 are R)
AMMO_footprint/Input/        model inputs
AMMO_footprint/Output/       parameter tables and figure rasters
AMMO_footprint/Output_pkl/   intermediate pickles
AMMO_footprint/Figures/      figure outputs (created on first run)
Air_pollution/B_Output/      AP-AMMO pathways
migrate_pkl_keys.py    utility: rename scenario keys in intermediate pickles
fix_paths.py           utility: normalise legacy path prefixes in intermediate pickles
```

Helper functions used by the modules are provided by the separate `APSP_proc` package.

## Module index

| Module                               | Purpose                                                              |
| ------------------------------------ | -------------------------------------------------------------------- |
| `B1_Calc_LandenNflow_Chang_Prod`     | land and N-flow changes for the PHD production side                  |
| `B2_Basemap_Target_NenLand_Chek`     | baseline maps of target N and land, with checks                      |
| `B3_Map_Prod_LandenNflow_Highreso`   | high-resolution production, land and N-flow maps                     |
| `B4_Allflow_en_SyntfertN_bala_ori`   | synthetic-fertilizer and manure N balance                            |
| `B5_Adj_ManrinputN`                  | adjustment of manure input N                                         |
| `B6_Allo_AdjSyntfert_ManrN`          | allocation of adjusted synthetic-fertilizer and manure N             |
| `B7_Relink_CropLivstk_Scen`          | re-linking of crop and livestock N emissions by scenario             |
| `B8_Adj_syntfert_emi_Scen`           | adjustment of synthetic-fertilizer emissions by scenario             |
| `B9_Collect_Revised_Emi_maps`        | collection of the revised emission maps                              |
| `B10_Calc_EURO_Diet_Ammo_Prod`       | FABIO production-side emissions for the diets                        |
| `B11_Aggr_Diet_Chang_Emi_en_Fac`     | aggregation of diet-driven emission changes by factor                |
| `B12_Map_Prodemi_Highreso`           | high-resolution production-emission maps                             |
| `B13_GAINS_Dataextr_Prod_MitiEFs`    | GAINS technical factors and emission tables (optional prep)          |
| `C1_Allo_adj_emi_consp`              | allocation of adjusted emissions to consumption                      |
| `C2_Calc_EURO_Diet_Ammo_Chang_Consp` | consumption-based emission accounting                                |
| `C3_Emi_perUnit_ConspProd`           | emission intensities per unit of consumption and production          |
| `C4_Calc_EURO_NonEURO_Specdrivn_Emi` | EU and non-EU specific demand-driven emissions                       |
| `C5_Summr_SpecProdemi`               | summary of specific production emissions                             |
| `C6_Map_SpecProdemi_Highreso`        | high-resolution maps of specific production emissions                |
| `C7_Delta_Emissions_approach1`       | emission changes between scenarios                                   |
| `D1_Newdetail_Diet_Techplus_Emi`     | MTFR factors applied to the PHD emissions                            |
| `D2_Emi_Sort_Shar`                   | emission shares and sorting across scenarios                         |
| `D3_Delta_Chang_Tot_Reved`           | change in total emissions (revised)                                  |
| `E1_UA_FullAdoption_Deep`            | Monte-Carlo uncertainty and the corner bound                         |
| `E2_UA_Spatial_Maps`                 | spatial uncertainty maps, country accounting, SI panels              |
| `E3_Country_Figure`                  | country comparison against the policy ceilings                       |
| `F1_Product_driven_emi.R`            | demand-driven emission maps with export/domestic ratios (Fig. 2 b-d) |
| `F2_Calories_Stack`                  | calorie intake charts                                                |
| `F3_Waterfall_Miti`                  | mitigation waterfall, stack bars, adoption-order figure              |
| `F4_Product_driven_miti.R`           | bivariate emission-change maps for animal-sourced foods (Fig. 3d)    |
| `F5_NUE_by_crops`                    | nitrogen-use efficiency by crop                                      |

## Environment

* Python 3.12 (conda environment `AP_AMMO6`)

* GDAL / rasterio / pyogrio, pandas, numpy, geopandas, scipy

* If raster operations warn about GDAL data, set `GDAL_DATA` to the environment's
  `share/gdal` directory.

Run all commands from the directory that contains `run_pipeline.py`:

```
python run_pipeline.py            # all stages
python run_pipeline.py --only base
python run_pipeline.py --from phd
python run_pipeline.py --list
```

## Canonical scenarios

The pipeline uses one set of scenario names throughout. They correspond to the
consumption-side labels of the manuscript.

| Name        | Meaning                                               |
| ----------- | ----------------------------------------------------- |
| `CURR`      | base year 2017                                        |
| `EAT`       | planetary health diet (PHD)                           |
| `CURR_MTFR` | base year with maximum technically feasible reduction |
| `EAT_MTFR`  | PHD + MTFR, PHD-first ordering                        |
| `MTFR_EAT`  | combined mitigation, MTFR-first ordering              |

Step-level "plus-tech" labels (`CURR_plus`, `EAT_plus`, `CURR_plus_MTFR`,
`EAT_plus_MTFR`) name intermediate diet+technology runs inside the MTFR module.

## Execution order

1. **base** — base-year emissions are the AP-AMMO values; they are allocated to FABIO
   items and attributed to consumption (`CURR`).

2. **phd** — PHD runs the N-balance adjustment of manure and synthetic fertilizer,
   re-allocates emissions, and attributes them to consumption (`EAT`).

3. **mtfr** — GAINS MTFR factors are applied to the PHD emissions (`EAT_MTFR`).
   The base-year and MTFR pathway intermediates are provided (AP-AMMO method, cited);
   summaries and delta changes follow. These scenarios are reported on the production
   side only.

Logs are written to `logs/<stage>.log`; the driver stops at the first failure and can be
resumed with `--from <stage>`.

## Uncertainty and figure modules

Run these from the directory that contains `run_pipeline.py`, after the stages that
provide their inputs:

```
python -m AMMO_footprint.E1_UA_FullAdoption_Deep   # MC series and corner bound
python -m AMMO_footprint.E2_UA_Spatial_Maps        # spatial maps and country accounting (after E1)
python -m AMMO_footprint.E3_Country_Figure         # country comparison figure (after E2)
Rscript AMMO_footprint/F1_Product_driven_emi.R      # Fig. 2 b-d bivariate maps (R)
python -m AMMO_footprint.F2_Calories_Stack         # calorie intake charts
python -m AMMO_footprint.F3_Waterfall_Miti         # mitigation charts and adoption order
Rscript AMMO_footprint/F4_Product_driven_miti.R     # Fig. 3d bivariate maps (R)
python -m AMMO_footprint.F5_NUE_by_crops           # nitrogen-use efficiency by crop
```

Each module exposes its individual steps as functions, for example
`E1_UA_FullAdoption_Deep.corner_bound()` or `F3_Waterfall_Miti.fig4d_manual_orders(...)`.

Environment variables:

| Variable | Default | Purpose |
|---|---|
| `AMMO_UNC_DIR` | `AMMO_footprint/Figures/uncertainty` | output directory for the uncertainty modules |
| `AMMO_SHP` | `AMMO_footprint/Data_shp/Global_map_geo.shp` | country boundary polygons for the spatial maps (see `MANIFEST.md`) |

## Prerequisites

The stages read a small set of intermediate files. The parameter inputs listed in `MANIFEST.md` (crop areas, N uptake/NUE, natural N flows, GAINS factors) are  described in the manuscript Methods and Supplementary
Information and the sources are cited.

| Item | Produced by | Notes |
|---|---|
| `Crop_area_coupl.pkl`, `Crop_areas_adj.xlsx` | prep (B10) | crop-area calibration |
| `All_CropN.xlsx`, `NUE_FABIO_APAMMO.xlsx`, `BNF_N_*`, `N_depo_*` | prep (D12/D13) | N uptake and NUE |
| `Curr_Nuptake_flows.pkl` | prep (D15) | natural N flows |
| `GAINS_UNFCCC_Emi_*`, `MitiEF_Techrate_byStage_*` | `AMMO_footprint/B13_GAINS_Dataextr_Prod_MitiEFs.py` | GAINS factors |
| `Y_newly_adj.pkl`, `Y_Curr*_check.xlsx` | diet step | base-year demand |
| `Manr_manachain_*`, `Manrbala_Orig_Adj_*`, `Manrdepo_app_allo_*`, `Relink_Croplivstk_N_Emi_*`, `Emi_*_coupl_*` | provided | emission and N-flow pathways (AP-AMMO method, cited) |
| `ScenEmi_s.pkl`, `Scen_SharSort_Emi.pkl` | emission collection | scenario emission and share tables |
| `N_flow_AP-AMMO_Map_CaliBase.pkl` | `B2` | land/N-flow calibration base |
| `EAT_*`, `MTFR_EAT_*`, `CURR_MTFR_*` rasters | N-balance and allocation modules | stage inputs/outputs |

## Inputs and sources

| Input                                     | Source                                                           |
| ----------------------------------------- | ---------------------------------------------------------------- |
| FABIO (2021 version)                      | Zenodo, record 2577067; Bruckner et al. (2019)                   |
| AP-AMMO emissions dataset                 | Figshare, doi:10.6084/m9.figshare.27642675; Jin et al. (2025)    |
| GAINS Europe v4.0.3 mitigation parameters | IIASA GAINS; extracted with `B13_GAINS_Dataextr_Prod_MitiEFs.py` |
| Crop areas                                | CROPGRIDS (Tang et al., 2024, Sci Data 11:413); LUCAS            |
| Livestock and feed data                   | FAOSTAT; FABIO feed balances                                     |
| Diet scenarios                            | EAT-Lancet 2.0 reference diet; PHD demand tables                 |
| Food loss and waste fractions             | Coudard et al. (2024)                                            |
| EuropeAgriDB (fodder/grass N)             | European nitrogen dataset                                        |
| Market-mediated ratios                    | Rieger et al. (2023); Geibel & Freund (2023)                     |
| Emission-factor uncertainty ranges        | literature compiled in Supplementary Table 13                    |

The manuscript's Methods and Supplementary Information describe how these inputs enter
the calculation. FABIO data are used under CC BY-NC-SA 4.0 and the AP-AMMO dataset
under CC BY 4.0; please cite the sources listed in `MANIFEST.md`.

## Outputs

Stage outputs are written under `AMMO_footprint/Output` and `Output_pkl`.&#x20;

## License

This code is licensed under the GNU General Public License v3.0 (GPL-3.0).
See `LICENSE`. In short: you may use, modify and redistribute it, including
commercially, provided that redistributed modifications remain under GPL-3.0 and
their source code is made available. Copyright notices must be preserved.

Data sources keep their own terms: FABIO (CC BY-NC-SA 4.0) and AP-AMMO (CC BY 4.0);
see `MANIFEST.md` for identifiers and citations.
