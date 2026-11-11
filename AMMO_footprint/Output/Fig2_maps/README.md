# Fig. 2 map data and QGIS project

Raster layers behind the main-text maps of Fig. 2 (European agricultural NH3
emissions, 2017). All rasters share the same grid.

## Contents

| File | Panel |
|---|---|
| `Curr_tot_emi.tif` | Fig. 2a — total emissions |
| `Fig_2b-e/Curr_Euro*_drivn.tif`, `Curr_NonEuro*_drivn.tif` | Fig. 2b-d — emissions driven by European demand (Euro) and by non-European export demand (NonEuro) for animal-source foods (direct), feed, and plant-based food |
| `Fig_2b-e/*_biclass.tif` | combined 1-16 bivariate classes (derived) |
| `Curr_manrhous_emi.tif`, `Curr_manrstor_emi.tif` | Fig. 2e — manure management |
| `Curr_grazdrop_emi.tif` | Fig. 2f — manure left on pasture |
| `Curr_manrapp_emi.tif` | Fig. 2g — manure application |
| `Curr_syntfert_emi.tif` | Fig. 2h — synthetic fertilizer use |
| `Fig2_bivariate.qgz` | QGIS project with the bivariate styling for Fig. 2b-d |

## Bivariate classification (Fig. 2b-d)

| Class | Euro-driven value | NonEuro-driven value |
|---|---|---|
| 1 | <= 15 000 | <= 3 000 |
| 2 | 15 000 - 35 000 | 3 000 - 7 000 |
| 3 | 35 000 - 65 000 | 7 000 - 13 000 |
| 4 | > 65 000 | > 13 000 |

Combined class = (Euro class - 1) * 4 + NonEuro class  (values 1-16).

| | N1 | N2 | N3 | N4 |
|---|---|---|---|---|
| **E1** | `#F2F2F2` | `#D2E7FA` | `#9BD0F0` | `#5FA0DA` |
| **E2** | `#F8F1BA` | `#BCBEBD` | `#98BCDE` | `#3C6E8F` |
| **E3** | `#F5D570` | `#DBC089` | `#818286` | `#1C445E` |
| **E4** | `#F89C1D` | `#CA8F2B` | `#88682F` | `#000000` |

## Plotting in QGIS

Open `Fig2_bivariate.qgz` in QGIS 3.x. The three bivariate layers are styled with the
16-colour palette above and use relative paths, so the project works after moving or
cloning the repository. The project CRS is EPSG:3035 (LAEA Europe).

## Reproducing the maps in R

```
Rscript AMMO_footprint/F1_Product_driven_emi.R
```

The script reads the six `Curr_*_drivn.tif` layers from `Fig_2b-e/` and writes
`Ani_dire_EuroNonEuro.png`, `Ani_feed_EuroNonEuro.png` and
`Plant_food_EuroNonEuro.png` to `AMMO_footprint/Figures/`.
