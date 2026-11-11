# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)
#
# F1 — demand-driven emission maps with export/domestic ratios (Fig. 2 b-d)
# Bivariate maps: emission magnitude (Euro layer) and the export-to-domestic
# ratio (NonEuro layer), classified into a 4 x 4 colour matrix.
# Run from the package root:  Rscript AMMO_footprint/F1_Product_driven_emi.R

#---- Load necessary packages
library(biscale) # 双变量地图制图
library(cowplot) # 结合ggplot2对象
library(sf) # 处理矢量数据
library(faux) # 生成模拟数据
library(ggplot2) # 创建地图
library(raster) # 处理栅格数据
library(dplyr) # for using the mutate function


#---- Working directory: package root (folder above AMMO_footprint)
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
root <- if (length(file_arg) > 0) {
  dirname(dirname(normalizePath(sub("^--file=", "", file_arg[1]))))
} else {
  getwd()  # when sourced interactively, run from the package root
}
setwd(root)

#---- Input rasters (Fig. 2 b-d)
map_dir <- file.path("AMMO_footprint", "Output", "Fig2_maps", "Fig_2b-e")


#----- Import example maps

EU_EFTA <- st_read(dsn = file.path("AMMO_footprint", "Input", "Sptial_file", "EFTA_UK2_WGS.shp"), quiet = TRUE)

Exam_map_wd <- file.path("AMMO_footprint", "Input", "Sptial_file", "Agr_large500.tif")

# Crop window matching the Europe lon/lat filter below; cropping before
# as.data.frame avoids holding global-extent dataframes in memory
Euro_extent <- extent(-26.5, 36.0, 32.0, 72.0)

#----

Item_list <- c("Ani_dire", "Ani_feed", "Plant_food")

Item_path_dict <-  list(
  Ani_dire = list(
    Euro    = file.path(map_dir, "Curr_EuroAni_drivn.tif"),
    NonEuro = file.path(map_dir, "Curr_NonEuroAni_drivn.tif")
  ),
  Ani_feed = list(
    Euro    = file.path(map_dir, "Curr_EuroAni_feed.tif"),
    NonEuro = file.path(map_dir, "Curr_NonEuroAni_feed.tif")
  ),
  Plant_food = list(
    Euro    = file.path(map_dir, "Curr_EuroPlant_drivn.tif"),
    NonEuro = file.path(map_dir, "Curr_NonEuroPlant_drivn.tif")
  )
)


Item_break_dict <- list(
  Ani_dire = list(
    Euro    = list(breaks = c(-Inf, 15000, 35000, 65000, Inf),
                   labels = c("1", "2", "3", "4")),
    NonEuro = list(breaks = c(-Inf, 3000, 7000, 13000, Inf),
                   labels = c("1", "2", "3", "4"))
  ),
  Ani_feed = list(
    Euro    = list(breaks = c(-Inf, 15000, 35000, 65000, Inf),
                   labels = c("1", "2", "3", "4")),
    NonEuro = list(breaks = c(-Inf, 3000, 7000, 13000, Inf),
                   labels = c("1", "2", "3", "4"))
  ),
  Plant_food = list(
    Euro    = list(breaks = c(-Inf,15000, 35000, 65000,  Inf),
                   labels = c("1", "2", "3", "4")),
    NonEuro = list(breaks = c(-Inf, 3000, 7000, 13000,  Inf),
                   labels = c("1", "2", "3", "4"))
  )
)


# Loop through each key

for (Item in Item_list) {
  EuroFood_drivn_wd = Item_path_dict[[Item]][['Euro']]
  NonEuroFood_drivn_wd = Item_path_dict[[Item]][['NonEuro']]
  
  #----
  ## RasterLayer,real manure layser, feed layer and the example layer 
  Food_Euro <- crop(raster(EuroFood_drivn_wd), Euro_extent)
  Food_NonEuro <- crop(raster(NonEuroFood_drivn_wd), Euro_extent)
  Example_map <- crop(raster(Exam_map_wd), Euro_extent)
  
  ## Convert above layers to dataframes
  Food_Euro_df <- as.data.frame(Food_Euro, xy = TRUE)
  Food_NonEuro_df <- as.data.frame(Food_NonEuro, xy = TRUE)
  Example_map_df <- as.data.frame(Example_map, xy = TRUE)
  
  
  #----
  #%%
  ## Merge data
  names(Food_Euro_df) <- c("x","y","Euro_val")
  names(Food_NonEuro_df) <- c("x","y","NonEuro_val")
  
  Food_Comprehensive_df <- merge(Food_Euro_df,
                                Food_NonEuro_df,
                                by=c("x","y"))
  
  Food_Comprehensive_df <-  merge(Food_Comprehensive_df,
                                 Example_map_df,
                                 by = c("x", "y"))
  
  
  #classify values to different categories
  
  Food_Comprehensive_df  <- Food_Comprehensive_df  %>%
    mutate(
      Euro_class = cut(Euro_val,
                       breaks = Item_break_dict[[Item]][['Euro']][['breaks']],
                       labels =  Item_break_dict[[Item]][['Euro']][['labels']],
                       include.lowest = TRUE,
                       right = FALSE  # Intervals are left-closed: [lower, upper)
      )
    )
  
  
  Food_Comprehensive_df <- Food_Comprehensive_df %>%
    mutate(
      NonEuro_class = cut(NonEuro_val,
                       breaks = Item_break_dict[[Item]][['NonEuro']][['breaks']],
                       labels = Item_break_dict[[Item]][['NonEuro']][['labels']],
                       include.lowest = TRUE,
                       right = FALSE  # Intervals are left-closed: [lower, upper)
      )
    )
  
  
  # Ensure they are factors
  Food_Comprehensive_df$Euro_class <- as.factor(Food_Comprehensive_df$Euro_class)
  Food_Comprehensive_df$NonEuro_class <- as.factor(Food_Comprehensive_df$NonEuro_class)
  
  
  # Create interaction: combines every pair of levels
  Food_Comprehensive_df$combined_class <- interaction(
    Food_Comprehensive_df$Euro_class,
    Food_Comprehensive_df$NonEuro_class,
    sep = "_"
  )
  
  # When the example layer is nan, then the plotting layer is nan
  Food_Comprehensive_df$combined_class[is.na(Food_Comprehensive_df$Agr_large500)] <- NA
  
  
  # Need to convert the data to coordinate EPSG3035
  ## Convert your raster-like df to points (for reprojection)
  
  ### First, filter original data to Europe in lat/lon (EPSG:4326)
  Food_Comprehensive <- Food_Comprehensive_df %>%
    filter(
      x >= -26.5 & x <= 36.0,   # longitude: 26.5W to 36E
      y >= 32.0 & y <= 72.0     # latitude: 32N to 72N
    )
  
  
  
  ### Now reproject only the filtered data
  pts <- st_as_sf(Food_Comprehensive, 
                  coords = c("x", "y"),          # your lon/lat columns
                  crs = 4326) %>%
    st_transform(3035)
  
  
  coords_3035 <- st_coordinates(pts)
  
  
  ### Add back to dataframe
  Food_Comprehensive_3035 <- Food_Comprehensive %>%
    select(-x, -y) %>%
    bind_cols(data.frame(x = coords_3035[,1], 
                         y = coords_3035[,2]))%>%
    mutate(
      x = round(x, -2),  # Round to nearest 100m to reduce jitter
      y = round(y, -2)
    ) %>%
    arrange(y, x)  # Sort by y then x for proper tile layout
  
  
  
  color_map <- c(
    "1_1" = "#F2F2F2",
    "1_2" = "#D2E7FA",
    "1_3" = "#9BD0F0",
    "1_4" = "#5FA0DA",
    "2_1" = "#F8F1BA",
    "2_2" = "#BCBEBD",
    "2_3" = "#98BCDE",
    "2_4" = "#3C6E8F",
    "3_1" = "#F5D570",
    "3_2" = "#DBC089",
    "3_3" = "#818286",
    "3_4" = "#1C445E",
    "4_1" = "#F89C1D",
    "4_2" = "#CA8F2B",
    "4_3" = "#88682F",
    "4_4" = "#000000"
  )
  
  
  map_3035 <- ggplot(Food_Comprehensive_3035, aes(x = x, y = y, fill = combined_class)) +
    geom_tile(width = 9200, height = 9200, alpha = 1) +  # Set tile size in meters
    
    # Add shapefile layer — ggplot will auto-reproject to 3035
    geom_sf(data = EU_EFTA, 
            fill = NA, 
            color = "black",
            size = 0.5,
            inherit.aes = FALSE) +
    
    
    scale_fill_manual(
      values = color_map,
      name = "Combined Class\n(Real_Feed)",
      na.value = "white"
    ) +
    coord_sf(crs = 3035, 
             xlim = range(Food_Comprehensive_3035$x) + c(-9200, 9200),  # Add padding
             ylim = range(Food_Comprehensive_3035$y) + c(-9200, 9200)
    ) +
    
    
    theme_minimal() +
    
    theme(
      legend.position = "none", #hide the legend 
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_blank(),
      axis.ticks = element_blank(),
      axis.text = element_blank(),  # Optional: removes axis text (tick labels)
      axis.title = element_blank()  # Optional: removes "x" and "y" axis titles
      #legend.text = element_text(size = 7),
      #legend.title = element_text(size = 9),
      #plot.title = element_text(size = 12)
    )
  
  
  #map_3035
  fig_dir <- file.path("AMMO_footprint", "Figures")
  dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)
  output_file <- file.path(fig_dir, paste0(Item, "_EuroNonEuro.png"))
  
  ggsave(
    output_file,
    plot = map_3035,
    width = 12,
    height = 10,
    dpi = 300,
    units = "in"
  )

  # Release this iteration's large objects before the next one
  rm(Food_Euro_df, Food_NonEuro_df, Example_map_df, Food_Comprehensive_df,
     Food_Comprehensive, Food_Comprehensive_3035, pts, coords_3035, map_3035)
  gc()

}
