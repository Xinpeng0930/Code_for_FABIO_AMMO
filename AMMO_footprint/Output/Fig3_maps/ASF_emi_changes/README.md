# Fig. 3d — emission changes for animal-sourced foods (bivariate maps)

Rasters and QGIS project behind the animal-source-food panels of Fig. 3d
(Beef, Pork, Dairy, Animal fats).

The maps are bivariate:
- **Manure driven** (x): emission change from manure management and manure left on pasture
- **Feed driven** (y): emission change from feed production

Values are emission changes (t N per grid cell). Classes per axis:

| Class | Value range |
|---|---|
| 1 | >= -500 (smallest reduction) |
| 2 | -2000 to -500 |
| 3 | -6000 to -2000 |
| 4 | < -6000 (largest reduction) |

Combined class = (Manure class - 1) * 4 + Feed class  (values 1-16).

| | F1 | F2 | F3 | F4 |
|---|---|---|---|---|
| **M1** | `#d3d3d3` | `#93B7A0` | `#4C9A6A` | `#007A30` |
| **M2** | `#B19BB9` | `#7A888B` | `#41705C` | `#005A28` |
| **M3** | `#90649F` | `#655878` | `#344951` | `#003921` |
| **M4** | `#6E2D84` | `#4D2764` | `#2B1F44` | `#00181D` |

## Contents

| File | Description |
|---|---|
| `<food>_ManureDriven_DeltaEmi.tif` | manure-driven emission change |
| `<food>_FeedDriven_DeltaEmi.tif` | feed-driven emission change |
| `<food>_biclass.tif` | combined 1-16 bivariate classes |
| `ASF_emi_changes.qgz` | QGIS project (EPSG:3035, relative paths, 16-colour styling) |

## Plotting in QGIS

Open `ASF_emi_changes.qgz` in QGIS 3.x; the four bivariate layers are styled with the
palette above and the project uses relative paths.

## Reproducing the maps in R

```
Rscript AMMO_footprint/F4_Product_driven_miti.R
```

The script reads the direct/indirect rasters from
`Output/EAT_Delemi_ProdSide_Aggr4Map_Methodone/` and writes
`Realfeed_<food>.png` for all seven animal-source foods
(Beef, Pork, Milk, Eggs, Animal fats, Mutton, Poultry meat).
