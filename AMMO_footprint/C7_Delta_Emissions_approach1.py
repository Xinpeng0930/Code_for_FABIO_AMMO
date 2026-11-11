# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# C7_Delta_Emissions_approach1 — emission changes between scenarios

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_path
import gc

#%%
# Import maps from C6
Scen_prod_spec_map_wddt = Imp_func.open_plk(FABIO_path.Prj_Pkl_output_wd + \
    r'ScenEmi_Maps_Foodspec.pkl')

Curr_prod_spec_map_wddt =Scen_prod_spec_map_wddt['Curr']['Detail_drivn_type']
EAT_prod_spec_map_wddt =Scen_prod_spec_map_wddt['EAT']['Detail_drivn_type']

# Data processing
## Add the Euro and Non-Euro driven maps together
Pland_food_list = list(Curr_prod_spec_map_wddt['EuroPlant_drivn'].keys())
Animal_food_list = list(Curr_prod_spec_map_wddt['EuroAni_drivn'].keys())


# Store output paths for animal food maps
Ani_direct_paths = {}
Ani_indirect_paths = {}

for food in Animal_food_list:
    Delta_direct_data = \
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['EuroAni_drivn'][food].replace('\\', '/'))  + \
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['NonEuroAni_drivn'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['EuroAni_drivn'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['NonEuroAni_drivn'][food].replace('\\', '/'))
    
    direct_path = FABIO_path.Prj_Gene_output_wd + \
        'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Animal_food_direct/' + \
        f'{food}_DeltaEmi.tif'
    Ani_direct_paths[food] = direct_path
    Imp_func.output_reso_ras_filtered(direct_path, Pj_path.Exam_500area_wd,
        'EPSG:4326', Delta_direct_data)

    Delta_feed_data =\
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['EuroAni_feed'][food].replace('\\', '/')) + \
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['NonEuroAni_feed'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['EuroAni_feed'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['NonEuroAni_feed'][food].replace('\\', '/'))
    
    indirect_path = FABIO_path.Prj_Gene_output_wd + \
        'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Animal_food_indirect/' + \
        f'{food}_DeltaEmi.tif'
    Ani_indirect_paths[food] = indirect_path
    Imp_func.output_reso_ras_filtered(indirect_path, Pj_path.Exam_500area_wd,
        'EPSG:4326', Delta_feed_data)



# Store output paths for plant food maps
Plant_paths = {}

for food in Pland_food_list:
    Delta_map_data = \
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['EuroPlant_drivn'][food].replace('\\', '/')) + \
        Imp_func.tidy_zero(EAT_prod_spec_map_wddt['NonEuroPlant_drivn'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['EuroPlant_drivn'][food].replace('\\', '/')) -\
        Imp_func.tidy_zero(Curr_prod_spec_map_wddt['NonEuroPlant_drivn'][food].replace('\\', '/'))
    
    plant_path = FABIO_path.Prj_Gene_output_wd + \
        'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/' + \
        f'{food}_DeltaEmi.tif'
    Plant_paths[food] = plant_path
    Imp_func.output_reso_ras_filtered(plant_path, Pj_path.Exam_500area_wd,
        'EPSG:4326', Delta_map_data)

## Aggregate cereals together
Aggre_cereals_list = ['Wheat','Rye','Barley','Maize','Oats','Other_cereals','Barley']
Cereals_delta_map_wddt = Imp_func.dict_name_path(Aggre_cereals_list,\
    Imp_func.glob.glob(FABIO_path.Prj_Gene_output_wd+\
            f'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/*_DeltaEmi.tif',\
            recursive=False))

Cereals_emi = Imp_func.aggregate_ori(list(Cereals_delta_map_wddt.values()))

cereals_path = FABIO_path.Prj_Gene_output_wd + \
    'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/Cereals_DeltaEmi.tif'
Plant_paths['Cereals'] = cereals_path
Imp_func.output_reso_ras_filtered(cereals_path, Pj_path.Exam_500area_wd,
    'EPSG:4326', Cereals_emi)

## Aggregate pulses and nuts together
Aggre_pulses_nuts_list = ['Pulses','Nuts']
Pulses_nuts_delta_map_wddt = Imp_func.dict_name_path(Aggre_pulses_nuts_list,\
    Imp_func.glob.glob(FABIO_path.Prj_Gene_output_wd+\
            f'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/*_DeltaEmi.tif',\
            recursive=False))

Pulses_nuts_emi = Imp_func.aggregate_ori(list(Pulses_nuts_delta_map_wddt.values()))

pulses_nuts_path = FABIO_path.Prj_Gene_output_wd + \
    'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/Pulses_Nuts_DeltaEmi.tif'
Plant_paths['Pulses_Nuts'] = pulses_nuts_path
Imp_func.output_reso_ras_filtered(pulses_nuts_path, Pj_path.Exam_500area_wd,
    'EPSG:4326', Pulses_nuts_emi)


## Aggregate fruits and vegetables together
Aggre_fruits_vege_list = ['Fruits','Vegetables']

Fruits_vege_delta_map_wddt = Imp_func.dict_name_path(Aggre_fruits_vege_list,\
    Imp_func.glob.glob(FABIO_path.Prj_Gene_output_wd+\
            f'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/*_DeltaEmi.tif',\
            recursive=False))

Fruits_vege_emi = Imp_func.aggregate_ori(list(Fruits_vege_delta_map_wddt.values()))

fruits_vege_path = FABIO_path.Prj_Gene_output_wd + \
    'EAT_Delemi_ProdSide_Aggr4Map_Methodone/Plant_food/Fruits_Vege_DeltaEmi.tif'
    
Plant_paths['Fruits_Vege'] = fruits_vege_path

Imp_func.output_reso_ras_filtered(fruits_vege_path, Pj_path.Exam_500area_wd,
    'EPSG:4326', Fruits_vege_emi)


# Store all output pathways in a dictionary for later use
Delta_emi_paths = {
    'Animal_direct': Ani_direct_paths,
    'Animal_indirect': Ani_indirect_paths,
    'Plant': Plant_paths,
}

Imp_func.save_plk( FABIO_path.Prj_Pkl_output_wd + \
    'EAT_Consupdriven_Emicut_Approach1.pkl',Delta_emi_paths)


# %%
