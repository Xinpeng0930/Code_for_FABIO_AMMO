# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# B9_Collect_Revised_Emi_maps — collection of the revised emission maps
'''
This script aims to get emission maps in each scenario with product resolution
Running time is 89s
'''

#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path


#%%
def Emi_Collect(Scenarios_Name):
    ## Scenario based inputs and outputs----------------------------------------------------------------------------------------------------
    if Scenarios_Name in ['CURR','CURR_MTFR']:
        ### Data from the Manure management emissions
        Livstk_Oriemi_dt =  Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
            f'Manr_manachain_{Scenarios_Name}.pkl')

        Livstk_Oriemi_df = Livstk_Oriemi_dt['Manr_mana_df']
        Hous_Manremi_wddt = Imp_func.conv_df2dict(Livstk_Oriemi_df,\
            'Ani_manr_type','Hous_emi_wddt')
        Stor_Manremi_wddt = Imp_func.conv_df2dict(Livstk_Oriemi_df,\
            'Ani_manr_type','Stor_emi_wddt')

        ### Data from synthetic fertilizer emissions
        if Scenarios_Name == 'CURR_MTFR':
            _sf_pkl = 'Emi_syntfert_coupl_CURR_MTFR.pkl'
        else:  # 'CURR' or 'CURR'
            _sf_pkl = 'Emi_syntfert_coupl_CURR.pkl'
        Crop_Oriemi_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + _sf_pkl)
        
        Ori_Cropsyntfert_wddt = Imp_func.conv_df2dict(Crop_Oriemi_df,\
            'OSDCropname', 'Emi_chemfer_map')
        
        ### Data from manure depostion emissions
        Ori_Cropmanr_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                    f'Relink_Croplivstk_N_Emi_{Scenarios_Name}.pkl')
               
        Ori_Cropmanrapp_wddt = Ori_Cropmanr_dt['Manr_app_emi_wddt']
        Ori_Cropmanrgra_wddt = Ori_Cropmanr_dt['Manr_depo_emi_wddt']
        
        ### Sort newkeys
        Hous_Manr_newkeys = [
            items + '_Hous' for items in list(Hous_Manremi_wddt.keys())]
        Stor_Manr_newkeys = [
            items + '_Stor' for items in list(Stor_Manremi_wddt.keys())]
        Manr_app_newkeys = [
            items + '_App' for items in list(Ori_Cropmanrapp_wddt.keys())]
        Manr_graz_newkeys = [
            items + '_Graz' for items in list(Ori_Cropmanrgra_wddt.keys())]
        
        Hous_Manremi_wddt = Imp_func.replace_keys(Hous_Manremi_wddt,Hous_Manr_newkeys)
        Stor_Manremi_wddt = Imp_func.replace_keys(Stor_Manremi_wddt,Stor_Manr_newkeys)
        App_Manremi_wddt = Imp_func.replace_keys(Ori_Cropmanrapp_wddt,Manr_app_newkeys)
        Graz_Manremi_wddt = Imp_func.replace_keys(Ori_Cropmanrgra_wddt,Manr_graz_newkeys)
        
        #OUTPUT_DATA
        Emi_bystage_detail_wddt = {'Syntfert_fert_emi':Ori_Cropsyntfert_wddt,\
            'Hous_Manr_emi':Hous_Manremi_wddt,'Stor_Manr_emi':Stor_Manremi_wddt,\
            'App_Manr_emi':App_Manremi_wddt,'Graz_Manr_emi':Graz_Manremi_wddt}
        
        Emi_bystage_middetail_wddt = {
            'Syntfert_fert_emi':list(Ori_Cropsyntfert_wddt.values()),\
            'Hous_Manr_emi':list(Hous_Manremi_wddt.values()),\
            'Stor_Manr_emi':list(Stor_Manremi_wddt.values()),\
            'App_Manr_emi':list(App_Manremi_wddt.values()),\
            'Graz_Manr_emi':list(Graz_Manremi_wddt.values())}
        
        Emi_bystage_aggr_wddt = {**Ori_Cropsyntfert_wddt,**Hous_Manremi_wddt,\
            **Stor_Manremi_wddt,**App_Manremi_wddt,**Graz_Manremi_wddt}
        
        #OUTPUT_DATA
        Stage_Emi_wd = FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Stage_Emi/'
        Total_Emi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}_totemi.tif'
        


    elif Scenarios_Name in ['EAT','EAT_Meat','MTFR_EAT',\
        'EAT',\
        'EAT_Vegan',\
        'EAT_Meat']:
        if Scenarios_Name == 'EAT':
            ## Emissions from manure housing and storage
            EMI_byProdStage_dict= Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                'EAT_EMI_byProdStage.pkl') #from E11C
        elif Scenarios_Name == 'EAT_Meat':
            EMI_byProdStage_dict= Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                'EAT_Meat_EMI_byProdStage.pkl')
        elif Scenarios_Name == 'MTFR_EAT':
            EMI_byProdStage_dict= Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                'MTFR_EAT_EMI_byProdStage.pkl')
        elif Scenarios_Name in ['EAT','EAT_Vegan','EAT_Meat']:
            EMI_byProdStage_dict= Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                f'{Scenarios_Name}_EMI_byProdStage.pkl')
    
        Emi_LiqManr_hous_wddt = EMI_byProdStage_dict['Detailed']['Liq_Manrhous']
        Emi_SldManr_hous_wddt = EMI_byProdStage_dict['Detailed']['Sld_Manrhous']
        Emi_LiqManr_stor_wddt = EMI_byProdStage_dict['Detailed']['Liq_Manrstor']
        Emi_SldManr_stor_wddt = EMI_byProdStage_dict['Detailed']['Sld_Manrstor']
    
        ### Sort newkeys
        Hous_LiqManr_newkeys = [
            items + '_liq_Hous' for items in list(Emi_LiqManr_hous_wddt.keys())]
        Hous_SldManr_newkeys = [
            items + '_sld_Hous' for items in list(Emi_SldManr_hous_wddt.keys())]
        Stor_LiqManr_newkeys = [
            items + '_liq_Stor' for items in list(Emi_LiqManr_stor_wddt.keys())]
        Stor_SldManr_newkeys = [
            items + '_sld_Stor' for items in list(Emi_SldManr_stor_wddt.keys())]
        
        Hous_Manremi_wddt = {**Imp_func.replace_keys(Emi_LiqManr_hous_wddt,Hous_LiqManr_newkeys),\
            **Imp_func.replace_keys(Emi_SldManr_hous_wddt, Hous_SldManr_newkeys)}
        Stor_Manremi_wddt = {**Imp_func.replace_keys(Emi_LiqManr_stor_wddt,Stor_LiqManr_newkeys),\
            **Imp_func.replace_keys(Emi_SldManr_stor_wddt, Stor_SldManr_newkeys)}

        ## Emissions from application and deposition
        Scen_emi_Croplivstk_link_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
            f'Relink_Croplivstk_N_Emi_{Scenarios_Name}.pkl') #  from B7
        
        Scen_emi_Livstk_depo_wddt =  Scen_emi_Croplivstk_link_dt['Manr_depo_emi_wddt']
        Scen_emi_Livstk_app_wddt = Scen_emi_Croplivstk_link_dt['Manr_app_emi_wddt']

        ## Emissions from synthetic fertilizer
        Scen_emi_Syntfert_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
            f'Emi_syntfert_coupl_Scen.pkl') #  from B8
        
        Scen_emi_Syntfert_wddt = Scen_emi_Syntfert_dt[f'{Scenarios_Name}']
        
        ## Sort emission data
        Emi_bystage_detail_wddt = {
            'Syntfert_fert_emi':Scen_emi_Syntfert_wddt,\
            'Hous_Manr_emi':Hous_Manremi_wddt,\
            'Stor_Manr_emi':Stor_Manremi_wddt,\
            'App_Manr_emi':Scen_emi_Livstk_app_wddt,\
            'Graz_Manr_emi':Scen_emi_Livstk_depo_wddt}
        
        Emi_bystage_middetail_wddt = {
            'Syntfert_fert_emi':list(Scen_emi_Syntfert_wddt.values()),\
            'Hous_Manr_emi':list(Hous_Manremi_wddt.values()),\
            'Stor_Manr_emi':list(Stor_Manremi_wddt.values()),\
            'App_Manr_emi':list(Scen_emi_Livstk_app_wddt.values()),\
            'Graz_Manr_emi':list(Scen_emi_Livstk_depo_wddt.values())}
        
        Emi_bystage_aggr_wddt = {**Scen_emi_Syntfert_wddt,**Hous_Manremi_wddt,\
            **Stor_Manremi_wddt,**Scen_emi_Livstk_app_wddt,**Scen_emi_Livstk_depo_wddt}
        
        
        #OUTPUT_DATA
        Stage_Emi_wd = FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Stage_Emi/'
        Total_Emi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}_totemi.tif'

    
    #----------------------------------------------------Processing_module----------------------------------------------------
    # Aggregate emissions in various scenarios
    Imp_func.os.makedirs(Stage_Emi_wd, exist_ok=True)
    # OUTPUT_DATA
    for stage in Emi_bystage_middetail_wddt:
        Stage_emi = Imp_func.aggregate(Emi_bystage_middetail_wddt[stage])
        # OUTPUT_FILE
        Imp_func.output_reso_ras_filtered(Stage_Emi_wd+f'{Scenarios_Name}_{stage}.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Stage_emi)
    
    By_stage_wddt = Imp_func.dict_name_path(['Syntfert_fert_emi','Hous_Manr_emi',\
        'Stor_Manr_emi','App_Manr_emi','Graz_Manr_emi'],\
        Imp_func.glob.glob(Stage_Emi_wd+r'*.tif',recursive=False))
    
    # SUMMARY
    Imp_func.zonal_summary(list(By_stage_wddt.keys()),\
        list(By_stage_wddt.values()),\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+\
        f'{Scenarios_Name}_revised_bystage.xlsx')
    
    Tot_emi = Imp_func.aggregate(list(Emi_bystage_aggr_wddt.values()))

    # OUTPUT_FILE
    Imp_func.output_reso_ras_filtered(Total_Emi_wd,\
        FABIO_pj_path.Prj_input_wd+r'Sptial_file/Agr_large500.tif',\
        'EPSG:4326',Tot_emi)

    return Total_Emi_wd, By_stage_wddt, Emi_bystage_detail_wddt 


