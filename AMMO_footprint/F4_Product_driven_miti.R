# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)
#
# F4 — bivariate emission-change maps for animal-sourced foods (Fig. 3d)
# Feed-driven (y) versus manure-driven (x) emission changes, classified into a
# 4 x 4 colour matrix. Plant-based panels of Fig. 3d use the Plant_food rasters.
# Run from the package root:  Rscript AMMO_footprint/F4_Product_driven_miti.R

#----
library(biscale) # bivariate map design
library(cowplot) # combining ggplot2 objects
library(sf) # vector data
library(faux) # simulated data helpers
library(ggplot2) # maps
library(raster) # raster data
library(dplyr) # data manipulation


#---- Working directory: package root (folder above AMMO_footprint)
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
root <- if (length(file_arg) > 0) {
  dirname(dirname(normalizePath(sub("^--file=", "", file_arg[1]))))
} else {
  getwd()  # when sourced interactively, run from the package root
}
setwd(root)

EU_EFTA <- st_read(dsn = file.path("AMMO_footprint", "Input", "Sptial_file", "EFTA_UK2_WGS.shp"), quiet = TRUE)

Exam_map_wd <- file.path("AMMO_footprint", "Input", "Sptial_file", "Agr_large500.tif")

#---- Emission-change rasters (Fig. 3d)
map_base <- file.path("AMMO_footprint", "Output", "EAT_Delemi_ProdSide_Aggr4Map_Methodone")
Anifood_list <- c("Beef", "Pork", "Milk", "Eggs", "Animal fats", "Mutton", "Pultry meat")

EAT_Listk_Real_wddt <- setNames(
  file.path(map_base, "Animal_food_direct", paste0(Anifood_list, "_DeltaEmi.tif")),
  Anifood_list)
EAT_Listk_Feed_wddt <- setNames(
  file.path(map_base, "Animal_food_indirect", paste0(Anifood_list, "_DeltaEmi.tif")),
  Anifood_list)
  
for (Anifood in Anifood_list) {
  EAT_real_wd = EAT_Listk_Real_wddt[[Anifood]]
  EAT_feed_wd = EAT_Listk_Feed_wddt[[Anifood]]
  
  #----
  ## RasterLayer,real manure layser, feed layer and the example layer 
  EAT_real <- raster(EAT_real_wd)
  EAT_feed <- raster(EAT_feed_wd)
  Example_map <- raster(Exam_map_wd)
  
  ## Convert above layers to dataframes
  EAT_real_df <- as.data.frame(EAT_real, xy = TRUE)
  EAT_feed_df <- as.data.frame(EAT_feed, xy = TRUE)
  Example_map_df <- as.data.frame(Example_map, xy = TRUE)
  
  
  #----
  #%%
  ## Merge data
  names(EAT_real_df) <- c("x","y","Real_val")
  names(EAT_feed_df) <- c("x","y","Feed_val")
  
  EAT_Comprehensive_df <- merge(EAT_real_df,
                                EAT_feed_df,
                                by=c("x","y"))
  
  EAT_Comprehensive_df <-  merge(EAT_Comprehensive_df,
                                 Example_map_df,
                                 by = c("x", "y"))
  
  
  #classify values to different categories
  
  EAT_Comprehensive_df <- EAT_Comprehensive_df %>%
    mutate(
      feed_class = cut(Feed_val,
                       breaks = c(-Inf, -6000, -2000, -500, Inf),
                       labels = c( "4", "3", "2", "1"),
                       include.lowest = TRUE,
                       right = FALSE  # Intervals are left-closed: [lower, upper)
      )
    )
  
  
  EAT_Comprehensive_df <- EAT_Comprehensive_df %>%
    mutate(
      real_class = cut(Real_val,
                       breaks = c(-Inf, -6000, -2000, -500, Inf),
                       labels = c( "4", "3", "2", "1"),
                       include.lowest = TRUE,
                       right = FALSE  # Intervals are left-closed: [lower, upper)
      )
    )
  
  
  # Ensure they are factors
  EAT_Comprehensive_df$real_class <- as.factor(EAT_Comprehensive_df$real_class)
  EAT_Comprehensive_df$feed_class <- as.factor(EAT_Comprehensive_df$feed_class)
  
  
  # Create interaction: combines every pair of levels
  EAT_Comprehensive_df$combined_class <- interaction(
    EAT_Comprehensive_df$real_class,
    EAT_Comprehensive_df$feed_class,
    sep = "_"
  )
  
  # When the example layer is nan, then the plotting layer is nan
  EAT_Comprehensive_df$combined_class[is.na(EAT_Comprehensive_df$Agr_large500)] <- NA
  
  
  # Need to convert the data to coordinate EPSG3035
  ## Convert your raster-like df to points (for reprojection)
  
  ### First, filter original data to Europe in lat/lon (EPSG:4326)
  EAT_Europe <- EAT_Comprehensive_df %>%
    filter(
      x >= -26.5 & x <= 36.0,   # longitude: 26.5W to 36E
      y >= 32.0 & y <= 72.0     # latitude: 32N to 72N
    )
  
  
  
  ### Now reproject only the filtered data
  pts <- st_as_sf(EAT_Europe, 
                  coords = c("x", "y"),          # your lon/lat columns
                  crs = 4326) %>%
    st_transform(3035)
  
  
  coords_3035 <- st_coordinates(pts)
  
  
  ### Add back to dataframe
  EAT_3035 <- EAT_Europe %>%
    select(-x, -y) %>%
    bind_cols(data.frame(x = coords_3035[,1], 
                         y = coords_3035[,2]))%>%
    mutate(
      x = round(x, -2),  # Round to nearest 100m to reduce jitter
      y = round(y, -2)
    ) %>%
    arrange(y, x)  # Sort by y then x for proper tile layout
  
  
  
  # Hardcoded color map (same approach as Y14s): fixed color per category combination
  # real_class (direct) on x-axis, feed_class (indirect) on y-axis
  # "1" = smallest reduction (closest to 0), "4" = largest reduction (most negative)
  color_map <- c(
    "1_1" = "#d3d3d3",
    "1_2" = "#93B7A0",
    "1_3" = "#4C9A6A",
    "1_4" = "#007A30",
    "2_1" = "#B19BB9",
    "2_2" = "#7A888B",
    "2_3" = "#41705C",
    "2_4" = "#005A28",
    "3_1" = "#90649F",
    "3_2" = "#655878",
    "3_3" = "#344951",
    "3_4" = "#003921",
    "4_1" = "#6E2D84",
    "4_2" = "#4D2764",
    "4_3" = "#2B1F44",
    "4_4" = "#00181D"
  )
  
  
  map_3035 <- ggplot(EAT_3035, aes(x = x, y = y, fill = combined_class)) +
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
             xlim = range(EAT_3035$x) + c(-9200, 9200),  # Add padding
             ylim = range(EAT_3035$y) + c(-9200, 9200)
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
  
  
  print(map_3035)
  fig_dir <- file.path("AMMO_footprint", "Figures")
  dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)
  output_file <- file.path(fig_dir, paste0("Realfeed_", Anifood, ".png"))
  
  ggsave(
    output_file,
    plot = map_3035,
    width = 12, 
    height = 10, 
    dpi = 300,
    units = "in"
  )
  
  
}


  





# 
# #----
# # Create 4x4 legend grid
# legend_data <- expand.grid(
#   feed_class_leg = as.factor(1:4),
#   real_class_leg = as.factor(4:1)  # Reverse so high is on top
# ) %>%
#   mutate(
#     combined_class_leg = interaction(real_class_leg, feed_class_leg, sep = "_"),
#     #label = paste(real_class_leg, feed_class_leg, sep = "\n")  # For text labels
#   )
# 
# 
# # Define GrPink-like gradient (from green to pink via white/grey)
# 
# grpink_palette <- colorRampPalette(c(
#   "#d3d3d3", # low x, low y 1-1
#   "#B19BB9", # 2-1
#   "#90649F", # 3-1
#   "#6E2D84", # 4-1
#   "#93B7A0", # manure 1 - feed 2
#   "#7A888B", # 2-2
#   "#655878", # 3-2
#   "#4D2764", # 4-2
#   "#4C9A6A", # 1-3
#   "#41705C", # 2-3
#   "#344951", # 3-3
#   "#2B1F44", # 4-3
#   "#007A30", # 1-4
#   "#005A28", # 2-4
#   "#003921", # 3-4
#   "#00181D" # high x, high y
# ), space = "Lab")
# 
# 
# 
# # Get unique combinations in sorted order
# n_colors <- 16
# colors <- grpink_palette(n_colors)
# 
# # Create named vector for scale
# color_map_leg <- setNames(colors, sort(levels(factor(legend_data$combined_class_leg))))
# 
# legend_plot <- ggplot(legend_data, aes(x = feed_class_leg, y = real_class_leg)) +
#   geom_tile(aes(fill = combined_class_leg), color = "white", size = 0.5) +
#   
#   #geom_text(aes(label = label), size = 3.5, color = "black") +
#   scale_fill_manual(
#     values = color_map_leg,
#     guide = "none"  # No extra legend
#   ) +
#   
#   #scale_x_discrete(name = "Manure driven emissions", position = "top") +
#   #scale_y_discrete(name = "Feed driven emissions", labels = c("4", "3", "2", "1")) +  # Reverse back
#   
#   theme_minimal() +
#   theme(
#     panel.background = element_blank(),
#     panel.grid = element_blank(),
#     # axis.text = element_text(size = 9),
#     # axis.title = element_text(size = 10),
#     legend.position = "none",
#     plot.margin = margin(4, 4, 4, 4)
#   ) 
# 
# 
# legend_plot 
# 
# 
# 
# 
# ## construct final plot
# finalPlot <-  plot_grid(
#   map_3035, legend_plot,
#   rel_widths = c(1, .4),
#   nrow = 1
# )
# 
# ## print final plot
# finalPlot




# 
# 
# # Create 4x4 legend grid
# legend_data <- expand.grid(
#   feed_class_leg = as.factor(1:4),
#   real_class_leg = as.factor(4:1)  # Reverse so high is on top
# ) %>%
#   mutate(
#     combined_class_leg = interaction(real_class_leg, feed_class_leg, sep = "_"),
#     #label = paste(real_class_leg, feed_class_leg, sep = "\n")  # For text labels
#   )
# 
# 
# # Define GrPink-like gradient (from green to pink via white/grey)
# 
# grpink_palette <- colorRampPalette(c(
#   "#FDF2ED", # low x, low y 1-1
#   "#B19BB9", # 2-1
#   "#90649F", # 3-1
#   "#6E2D84", # 4-1
#   "#D8B5B5", # manure 1 - feed 2
#   "#7A888B", # 2-2
#   "#655878", # 3-2
#   "#4D2764", # 4-2
#   "#8D3C45", # 1-3
#   "#41705C", # 2-3
#   "#344951", # 3-3
#   "#2B1F44", # 4-3
#   "#67000D", # 1-4
#   "#005A28", # 2-4
#   "#003921", # 3-4
#   "#00181D" # high x, high y
# ), space = "Lab")
# 
# 
# 
# # Get unique combinations in sorted order
# n_colors <- 16
# colors <- grpink_palette(n_colors)
# 
# # Create named vector for scale
# color_map_leg <- setNames(colors, sort(levels(factor(legend_data$combined_class_leg))))
# 
# legend_plot <- ggplot(legend_data, aes(x = feed_class_leg, y = real_class_leg)) +
#   geom_tile(aes(fill = combined_class_leg), color = "white", size = 0.5) +
# 
#   #geom_text(aes(label = label), size = 3.5, color = "black") +
#   scale_fill_manual(
#     values = color_map_leg,
#     guide = "none"  # No extra legend
#   ) +
# 
#   #scale_x_discrete(name = "Manure driven emissions", position = "top") +
#   #scale_y_discrete(name = "Feed driven emissions", labels = c("4", "3", "2", "1")) +  # Reverse back
# 
#   theme_minimal() +
#   theme(
#     panel.background = element_blank(),
#     panel.grid = element_blank(),
#     # axis.text = element_text(size = 9),
#     # axis.title = element_text(size = 10),
#     legend.position = "none",
#     plot.margin = margin(4, 4, 4, 4)
#   )
# 
# 
# legend_plot