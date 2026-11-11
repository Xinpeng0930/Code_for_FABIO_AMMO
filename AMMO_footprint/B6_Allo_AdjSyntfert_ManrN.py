# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B6_Allo_AdjSyntfert_ManrN — allocation of adjusted synthetic-fertilizer and manure N


'''

Running time is 9 mins

'''
#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from pathlib import Path
import gc

#%%


def Allo_AdjSyntfert_ManrN(Scenario_Name):
    # ----------------------------------------------------input_module----------------------------------------------------
    ## Scenario-based N flow data (per-product raster paths, from  B3)
    # INPUT
    if Scenario_Name == 'EAT':
        Nflow_byProdStage_dt = Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + 'EAT_Nflow_byProdStage.pkl' ) 

    elif Scenario_Name == 'EAT_Meat':
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenario_Name}_Nflow_byProdStage.pkl') 

    elif Scenario_Name == 'MTFR_EAT':
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + 'MTFR_EAT_Nflow_byProdStage.pkl')

    elif Scenario_Name in ['EAT','EAT_Vegan','EAT_Meat']:
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenario_Name}_Nflow_byProdStage.pkl')

    ## Adjusted N flow targets (aggregated raster paths, from B5)
    # INPUT
    Adj_Nflow_Scen_wddt = Imp_func.open_plk(
        FABIO_pj_path.Prj_Pkl_output_wd+\
        r'Adj_Syntfert_ManrInput_Nflows_s.pkl') # from B5

    ## Synthetic fertilizer: baseline per-product paths + adjusted aggregate path
    # INPUT_DATA
    Orig_Syntfert_N_byprod_wddt = Nflow_byProdStage_dt['Detailed']['Syntfert']
    Orig_Syntfert_N_aggre_wd = Nflow_byProdStage_dt['Aggregated']['Syntfert']
    Adj_Syntfert_N_aggre_wd = Adj_Nflow_Scen_wddt[Scenario_Name]['Adj_SyntfertN']

    ## Manure deposition + application: baseline per-livestock paths (livestock view)
    # INPUT_DATA
    Orig_ManrDepo_N_byprod_wddt = Nflow_byProdStage_dt['Detailed']['Manrdepo']
    Orig_ManrApp_LiqN_byprod_wddt = Nflow_byProdStage_dt['Detailed']['LiqApp']
    Orig_ManrApp_SldN_byprod_wddt = Nflow_byProdStage_dt['Detailed']['SldApp']

    ## Manure aggregate paths: baseline totals + adjusted total (livestock view)
    # INPUT_DATA
    Orig_ManrDepo_N_aggre_wd = Nflow_byProdStage_dt['Aggregated']['ManrDepo']
    Orig_ManrApp_N_aggre_wd =  Nflow_byProdStage_dt['Aggregated']['ManrApp']
    Adj_ManrInput_N_aggre_wd = Adj_Nflow_Scen_wddt[Scenario_Name]['Adj_ManrinputN']

    ## Manure application + deposition: baseline per-crop paths (crop view)
    # INPUT_DATA
    Orig_ManrApp_LiqN_bycrop_prod_wddt = Nflow_byProdStage_dt['Detailed']['LiqApp_crop']
    Orig_ManrApp_SldN_bycrop_prod_wddt = Nflow_byProdStage_dt['Detailed']['SldApp_crop']
    Orig_ManrDepo_N_bycrop_prod_wddt = Nflow_byProdStage_dt['Detailed']['Manrdepo_gras']

    ## Manure aggregate paths: baseline crop-side totals (crop view)
    # INPUT_DATA
    Orig_ManrApp_N_Cropside_aggre_wd =  Nflow_byProdStage_dt['Aggregated']['ManrApp_crop']
    Orig_ManrGras_N_Grasside_aggre_wd = Nflow_byProdStage_dt['Aggregated']['ManrDepo_gras']

    # ----------------------------------------------------processing_module----------------------------------------------------
    ## Get the change share of synthetic fertilizer
    # OUTPUT_DATA
    Shar_Syntfert_change = Imp_func.tidy_zero(Adj_Syntfert_N_aggre_wd) / Imp_func.tidy_zero(Orig_Syntfert_N_aggre_wd)

    Shar_Syntfert_change_clean =Shar_Syntfert_change.copy()  # Use copy() to avoid modifying original
    Shar_Syntfert_change_clean[Imp_func.np.isnan(Shar_Syntfert_change_clean)] = 0

    #OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Change_Shar/Syntfert_N.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Shar_Syntfert_change_clean)

    for prod in Orig_Syntfert_N_byprod_wddt:
        Adj_Syntfert_N = Shar_Syntfert_change_clean * Imp_func.tidy_zero(
            Orig_Syntfert_N_byprod_wddt[prod]
        )
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Adj_Syntfert_byprod/{prod}_adj_SyntfertN.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Adj_Syntfert_N)
    
    #OUTPUT_DATA
    Syntfert_Scen_byprod_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenario_Name}_Adj_Syntfert_byprod/*.tif'))


    ## Get the change share of manure input from the perspective of livestock
    # OUTPUT_DATA
    Shar_ManrInput_change = Imp_func.tidy_zero(Adj_ManrInput_N_aggre_wd)/(Imp_func.tidy_zero(Orig_ManrDepo_N_aggre_wd)+\
        Imp_func.tidy_zero(Orig_ManrApp_N_aggre_wd))


    Shar_ManrInput_change_clean =Shar_ManrInput_change.copy()  # Use copy() to avoid modifying original
    Shar_ManrInput_change_clean[Imp_func.np.isnan(Shar_ManrInput_change_clean)] = 0

    #OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Change_Shar/ManrInput_N.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Shar_ManrInput_change_clean)

    ### Get the change of manure deposition
    #OUTPUT_FILE
    for prod in Orig_ManrDepo_N_byprod_wddt:
        Adj_Depomanr_N = Shar_ManrInput_change_clean * Imp_func.tidy_zero(
        Orig_ManrDepo_N_byprod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Adj_Depomanr_byprod/{prod}_adj_DepomanrN.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Adj_Depomanr_N)

    # OUTPUT_DATA
    Depomanr_Scen_byprod_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Adj_Depomanr_byprod/*.tif'))
    
    ### Get the change of liquid manure application
    # OUTPUT_FILE
    for prod in Orig_ManrApp_LiqN_byprod_wddt:
        Adj_Appliqmanr_N = Shar_ManrInput_change_clean  * Imp_func.tidy_zero(
            Orig_ManrApp_LiqN_byprod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_LiqmanrApp_byprod/{prod}_adj_Liqmanrapp.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Adj_Appliqmanr_N)

    # OUTPUT_DATA
    AppLiqmanr_Scen_byprod_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_LiqmanrApp_byprod/*.tif',recursive=False))
    
    ### Get the change of solid manure application
    # OUTPUT_FILE
    for prod in Orig_ManrApp_SldN_byprod_wddt:
        Adj_Appsldmanr_N = Shar_ManrInput_change_clean  * Imp_func.tidy_zero(
            Orig_ManrApp_SldN_byprod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_SldmanrApp_byprod/{prod}_adj_Sldmanrapp.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', Adj_Appsldmanr_N)
    
    # OUTPUT_DATA
    AppSldmanr_Scen_byprod_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_SldmanrApp_byprod/*.tif',recursive=False))
    
    
    ## Get the change share of manure inputs from the perspective of crops
    # OUTPUT_DATA
    Shar_ManrInput_crop_change = Imp_func.tidy_zero(Adj_ManrInput_N_aggre_wd)/(Imp_func.tidy_zero(Orig_ManrGras_N_Grasside_aggre_wd)+\
        Imp_func.tidy_zero(Orig_ManrApp_N_Cropside_aggre_wd))

    Shar_ManrInput_crop_change_clean = Shar_ManrInput_crop_change.copy()  # Use copy() to avoid modifying original
    Shar_ManrInput_crop_change_clean[Imp_func.np.isnan(Shar_ManrInput_crop_change_clean)] = 0
    
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Change_Shar/ManrInput_crop_N.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Shar_ManrInput_crop_change_clean)

    ### Get the change of manure deposition
    #OUTPUT_FILE
    
    Orig_ManrApp_SldN_bycrop_prod_wddt = Nflow_byProdStage_dt['Detailed']['SldApp_crop']
    
    
    for prod in Orig_ManrDepo_N_bycrop_prod_wddt:
        Adj_Depomanr_N = Shar_ManrInput_crop_change_clean * Imp_func.tidy_zero(
        Orig_ManrDepo_N_bycrop_prod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Adj_Depomanr_crop_byprod/{prod}_adj_DepomanrN.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Adj_Depomanr_N)

    #OUTPUT_DATA
    Depomanr_Scen_bycrop_prod_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+f'{Scenario_Name}_Adj_Depomanr_crop_byprod/*.tif'))
    
    ### Get the change of liquid manure application
    # OUTPUT_FILE
    for prod in Orig_ManrApp_LiqN_bycrop_prod_wddt:
        Adj_Appliqmanr_N = Shar_ManrInput_crop_change_clean * Imp_func.tidy_zero(
            Orig_ManrApp_LiqN_bycrop_prod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_LiqmanrApp_crop_byprod/{prod}_adj_Liqmanrapp.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Adj_Appliqmanr_N)

    #OUTPUT_DATA
    AppLiqmanr_Scen_bycrop_prod_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_LiqmanrApp_crop_byprod/*.tif',recursive=False))
    
    ### Get the change of solid manure application
    # OUTPUT_FILE
    for prod in Orig_ManrApp_SldN_bycrop_prod_wddt:
        Adj_Appsldmanr_N = Shar_ManrInput_crop_change_clean  * Imp_func.tidy_zero(
            Orig_ManrApp_SldN_bycrop_prod_wddt[prod])
        
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_SldmanrApp_crop_byprod/{prod}_adj_Sldmanrapp.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', Adj_Appsldmanr_N)
    
    # OUTPUT_DATA
    AppSldmanr_Scen_bycrop_prod_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
            f'{Scenario_Name}_Adj_SldmanrApp_crop_byprod/*.tif',recursive=False))
    
    
    gc.collect()  # release write handles from all output loops before zonal_summary reads the same files

    ## SUMMARY
    # OUTPUT_FILE
    Imp_func.zonal_summary(
        ['Syntfert_N_' + \
        item for item in \
        list(Syntfert_Scen_byprod_wddt.keys())] + \
            
        ['Appliq_livN_' + \
        item for item in \
        list(AppLiqmanr_Scen_byprod_wddt.keys())] + \
            
        ['Appsld_livN_' + \
        item for item in \
        list(AppSldmanr_Scen_byprod_wddt.keys())] + \
        
        ['Appliq_cropN_' + \
        item for item in \
        list(AppLiqmanr_Scen_bycrop_prod_wddt.keys())] + \

        ['Appsld_cropN_' + \
        item for item in \
        list(AppSldmanr_Scen_bycrop_prod_wddt.keys())] +  \


        ['Grazdepo_N_Gras_byLiv_' + \
        item for item in \
        list(Depomanr_Scen_byprod_wddt.keys())] + \
            
        ['Grazdepo_N_Gras_byCrop_'+ \
        item for item in \
        list(Depomanr_Scen_bycrop_prod_wddt.keys())] , 
    \
        list(Syntfert_Scen_byprod_wddt.values()) + \
        list(AppLiqmanr_Scen_byprod_wddt.values()) + \
        list(AppSldmanr_Scen_byprod_wddt.values()) + \
        list(AppLiqmanr_Scen_bycrop_prod_wddt.values()) + \
        list(AppSldmanr_Scen_bycrop_prod_wddt.values()) + \
        list(Depomanr_Scen_byprod_wddt.values()) + \
        list(Depomanr_Scen_bycrop_prod_wddt.values()),

        Air_pj_path.EFTA_UK_wd, 32, 'sum', -999, FABIO_pj_path.Prj_Gene_output_wd+\
            f'{Scenario_Name}_Adj_Nflow_byprod.xlsx') # Adjusted fertilizer and manure application N on different products
    
    # OUTPUT_FILE
    Imp_func.zonal_summary(
        ['Grazdepo_N_Gras_byLiv_' + \
        item for item in \
        list(Orig_ManrDepo_N_byprod_wddt.keys())]+ \
        
        ['Appliq_livN_' + \
        item for item in \
        list(Orig_ManrApp_LiqN_byprod_wddt.keys())] + \

        ['Appsld_livN_' + \
        item for item in \
        list(Orig_ManrApp_SldN_byprod_wddt.keys())] + \
        
        ['ManrDepo_aggre','ManrApp_aggre'],\
        
        list(Orig_ManrDepo_N_byprod_wddt.values())+\
        list(Orig_ManrApp_LiqN_byprod_wddt.values())+\
        list(Orig_ManrApp_SldN_byprod_wddt.values())+\
        [Orig_ManrDepo_N_aggre_wd] + [Orig_ManrApp_N_aggre_wd],\
        
        Air_pj_path.EFTA_UK_wd, 32, 'sum', -999, FABIO_pj_path.Prj_Gene_output_wd+\
            f'{Scenario_Name}_Compar_Orig_Nflow_SepAggre.xlsx'
    ) #
    
    return 



def Collect_adj_outputs_by_scenario(Scenario_Name, MainCpNam, Ani_name):
    base_dir = Path(FABIO_pj_path.Prj_Rster_output_wd)

    def get_tif_dict(folder_name, key_list):
        folder = base_dir / folder_name

        if not folder.exists():

            print(f"Warning: {folder} does not exist.")

            return {}

        tif_files = list(folder.glob("*.tif"))

        return Imp_func.dict_name_path(key_list, [str(f) for f in tif_files])


    return {
        'Syntfert_byprod': get_tif_dict(f"{Scenario_Name}_Adj_Syntfert_byprod", MainCpNam),

        'Depomanr_byprod': get_tif_dict(f"{Scenario_Name}_Adj_Depomanr_byprod", Ani_name),

        'Manrapp_liq_Liv_byprod': get_tif_dict(f"{Scenario_Name}_Adj_LiqmanrApp_byprod", Ani_name),

        'Manrapp_sld_Liv_byprod': get_tif_dict(f"{Scenario_Name}_Adj_SldmanrApp_byprod", Ani_name),

        'Depomanr_Crop_byprod': get_tif_dict(f"{Scenario_Name}_Adj_Depomanr_crop_byprod", MainCpNam),

        'Manrapp_liq_Crop_byprod': get_tif_dict(f"{Scenario_Name}_Adj_LiqmanrApp_crop_byprod", MainCpNam),

        'Manrapp_sld_Crop_byprod': get_tif_dict(f"{Scenario_Name}_Adj_SldmanrApp_crop_byprod", MainCpNam)
    }




