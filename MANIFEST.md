# Data manifest — FABIO_AMMO

## Key data inputs (public)

| Source                                   | Identifier                                      | Used for                                                                                                         |
| :--------------------------------------- | :---------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| FABIO 2021                               | Zenodo 2577067                                  | input–output tables, X/Y/Z                                                                                       |
| AP-AMMO dataset                          | Figshare 10.6084/m9.figshare.27642675           | agricultural NH3 emissions                                                                                       |
| GAINS Europe v4.0.3                      | IIASA GAINS                                     | MTFR factors and adoption rates                                                                                  |
| Parameter and plotting table             | Supplementary Data (`Processing_plot_new.xlsx`) | pipeline parameters (B2/B5/B11/C1/C4/D1) and figure data (F1-F3); place in `AMMO_footprint/Input/`               |
| CROPGRIDS                                | Tang et al. 2024, Sci Data 11:413               | crop areas                                                                                                       |
| LUCAS                                    | Copernicus LUCAS                                | grassland and fodder areas                                                                                       |
| FAOSTAT                                  | FAO                                             | production, trade, fertilizer use                                                                                |
| EAT-Lancet 2.0                           | Rockström et al. 2025                           | reference diet targets                                                                                           |
| PHD demand tables                        | `FABIO_model/FABIO_dataset/Anniek_new_Y_data/`  | adjusted demand                                                                                                  |
| Coudard et al. 2024                      | food loss and waste fractions                   | diet conversion                                                                                                  |
| EuropeAgriDB                             | Einarsson et al.                                | fodder and grass N data                                                                                          |
| Rieger et al. 2023; Geibel & Freund 2023 | P2C ratios                                      | market-mediated uncertainty                                                                                      |
| Country boundary polygons                | Global Map geodata (`Global_map_geo.shp`)       | outline in the spatial uncertainty maps; place at `AMMO_footprint/Data_shp/Global_map_geo.shp` or set `AMMO_SHP` |



## Key parameter inputs (described and cited)

These parameters files are assembled from the sources below. Their derivation is described in the manuscript Methods and Supplementary Information.

| Parameter                         | File(s)                                                                                                 | Source                                                         |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Crop areas                        | `Crop_area_coupl.pkl`, `Crop_areas_adj.xlsx`                                                            | AP-AMMO (Jin et al. 2025); CROPGRIDS (Tang et al. 2024); LUCAS |
| N uptake                          | `All_CropN.xlsx`                                                                                        | FAOSTAT; AP-AMMO                                               |
| NUE, BNF, N deposition            | `NUE_FABIO_APAMMO.xlsx`, `BNF_N_*`, `N_depo_*`                                                          | FAOSTAT; AP-AMMO; EuropeAgriDB (Einarsson et al.)              |
| Natural N flows                   | `Curr_Nuptake_flows.pkl`                                                                                | derived from the above (Eq. 10; SI Fig. 7)                     |
| MTFR factors                      | `Output/GAINS_UNFCCC_Emi_*.xlsx`, `Output/MTSF_2050_GAINS_byStage_Emi.xlsx`                             | GAINS Europe v4.0.3 (IIASA)                                    |
| Scenario emission/N-flow pathways | `Output_pkl/Manr_manachain_*`, `Manrbala_*`, `Manrdepo_*`, `Relink_*`, `Emi_*_coupl_*`, `ScenEmi_s.pkl` | AP-AMMO method (Jin et al. 2025), scenario adaptation          |
| Base-year pathways                | `Air_pollution/B_Output/`                                                                               | AP-AMMO (Jin et al. 2025)                                      |

##

## Key intermediate or final outputs

All files below are under `AMMO_footprint/Output/`.

| Folder / file                                                   | Size    | Purpose                                                                                                                   |
| --------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------- |
| `Output/*.xlsx`, `Output/*.pkl` (top level)                     | 1.6 MB  | parameter tables used by the stages and figure modules                                                                    |
| `Output/EAT_Delemi_ProdSide_Aggr4Map_Methodone/`                | 532 MB  | food-specific emission-change rasters used by the spatial uncertainty modules (E2/E3)                                     |
| `Output/Fig2_maps/Fig_2b-e/`                                    | 72.5 MB | demand-driven Euro/NonEuro rasters for Fig. 2 b-d (inputs to the F1 R script; QGIS-ready)                                 |
| `Output/Fig2_maps/*.tif`                                        | 72.6 MB | total and by-stage emission rasters for Fig. 2a and 2e-h (QGIS-ready)                                                     |
| `Output/Fig2_maps/Fig_2b-e/*_biclass.tif`, `Fig2_bivariate.qgz` | < 1 MB  | combined 1-16 bivariate classes and the QGIS project with the matching 16-colour styling (relative paths)                 |
| `Output/Fig3_maps/ASF_emi_changes/`                             | 97 MB   | manure/feed emission-change rasters, combined 1-16 classes and the QGIS project for the Fig. 3d animal-source-food panels |



## Notes

* FABIO version used: `FABIO_2021ver`.

* AP-AMMO record: version v1.

* GAINS extracts are produced by `AMMO_footprint/B13_GAINS_Dataextr_Prod_MitiEFs.py` from the GAINS Europe v4.0.3 database.

* All scenario labels follow the canonical names in `README.md`.

