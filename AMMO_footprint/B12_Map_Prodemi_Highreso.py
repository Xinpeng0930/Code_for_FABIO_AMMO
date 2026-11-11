# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B12_Map_Prodemi_Highreso — high-resolution production-emission maps
'''
This script aims to map new emissions under the eat-lancet scenario to
high-resolution maps based on AP-AMMO dataset

This script can run automatically

'''

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path
from pathlib import Path


#%%
def Cali_Highreso_emi(Scenarios_Name):
    #----------------------------------------------------input_module----------------------------------------------------   
    # Scenario-based inputs and outputs-----------------------------------------------------------------------
    if Scenarios_Name == 'EAT':
        Emi_fac_wd = FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_Highreso_califac_check.xlsx' #from B11
        Use_Emifac_shetname =Imp_func.pd.ExcelFile(Emi_fac_wd).sheet_names
        Higreso_path = r'./AMMO_footprint/Output_raster/Emi_EAT_'
        
        # Map inputs----------------------------
        ##Livestock-side emissions
        Manr_manachain_dict =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd+r'Manr_manachain_CURR.pkl') # manure management emissions by livestock

        Manr_mana_df = Manr_manachain_dict['Manr_mana_df']
        
        ## Crop-side emissions
        Crop_side_emi_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +\
                r'Emi_syntfert_coupl_CURR.pkl')
        
        ## Both involved emissions
        Manrcroplink_dict=Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                            f'Relink_Croplivstk_N_Emi_CURR.pkl') # pathways providing emissions from specific livestock to specific crops, including both deposition and application

        for key in Manrcroplink_dict:
            for key2 in Manrcroplink_dict[key]:
                Manrcroplink_dict[key][key2] = Manrcroplink_dict[key][key2].replace('\\', '/')

        # Base map summary pickle file
        Base_map_pkl_wd = FABIO_pj_path.Prj_Pkl_output_wd+'AP-AMMO_Map_CaliBase.pkl'
        

    elif Scenarios_Name == 'MTFR_EAT':
        Emi_fac_wd = FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_Highreso_califac_check.xlsx' #from B11
        Use_Emifac_shetname =Imp_func.pd.ExcelFile(Emi_fac_wd).sheet_names
        Higreso_path = r'./AMMO_footprint/Output_raster/Emi_MTFR_EAT_'
        
        # Map inputs----------------------------
        ##Livestock-side emissions
        Manr_manachain_dict =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd+r'Manr_manachain_CURR_MTFR.pkl') # manure management emissions by livestock

        Manr_mana_df = Manr_manachain_dict['Manr_mana_df']
        
        ## Crop-side emissions
        Crop_side_emi_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +\
                r'Emi_syntfert_coupl_CURR_MTFR.pkl')
        
        ## Both involved emissions
        Manrcroplink_dict=Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                            f'Relink_Croplivstk_N_Emi_CURR_MTFR.pkl') # pathways providing emissions from specific livestock to specific crops, including both deposition and application

        for key in Manrcroplink_dict:
            for key2 in Manrcroplink_dict[key]:
                Manrcroplink_dict[key][key2] = Manrcroplink_dict[key][key2].replace('\\', '/')

        # Base map summary pickle file
        Base_map_pkl_wd = FABIO_pj_path.Prj_Pkl_output_wd+\
            'AP-AMMO_Map_MTFR_CaliBase.pkl'
        
    elif Scenarios_Name == 'EAT_Meat':
        Emi_fac_wd = FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_Highreso_califac_check.xlsx' #from B11
        Use_Emifac_shetname =Imp_func.pd.ExcelFile(Emi_fac_wd).sheet_names
        Higreso_path = f'./AMMO_footprint/Output_raster/Emi_{Scenarios_Name}_'
        
        # Map inputs----------------------------
        ##Livestock-side emissions
        Manr_manachain_dict =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd+r'Manr_manachain_CURR.pkl') # manure management emissions by livestock

        Manr_mana_df = Manr_manachain_dict['Manr_mana_df']
        
        ## Crop-side emissions
        Crop_side_emi_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +\
                r'Emi_syntfert_coupl_CURR.pkl')
        
        ## Both involved emissions
        Manrcroplink_dict=Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                            f'Relink_Croplivstk_N_Emi_CURR.pkl') # pathways providing emissions from specific livestock to specific crops, including both deposition and application

        for key in Manrcroplink_dict:
            for key2 in Manrcroplink_dict[key]:
                Manrcroplink_dict[key][key2] = Manrcroplink_dict[key][key2].replace('\\', '/')
        
        # Base map summary pickle file
        Base_map_pkl_wd = FABIO_pj_path.Prj_Pkl_output_wd+\
            'AP-AMMO_Map_CaliBase.pkl'
        
    elif Scenarios_Name in ['EAT','EAT_Vegan','EAT_Meat']:
        Emi_fac_wd = FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_Highreso_califac_check.xlsx' #from B11
        Use_Emifac_shetname =Imp_func.pd.ExcelFile(Emi_fac_wd).sheet_names
        Higreso_path = f'./AMMO_footprint/Output_raster/Emi_{Scenarios_Name}_'
        
        # Map inputs----------------------------
        ##Livestock-side emissions
        Manr_manachain_dict =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd+r'Manr_manachain_CURR.pkl') 


        Manr_mana_df = Manr_manachain_dict['Manr_mana_df']
        
        ## Crop-side emissions
        Crop_side_emi_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +\
                r'Emi_syntfert_coupl_CURR.pkl') # The synthetic fertilizer N flows are constant for all scenarios
        
        ## Both involved emissions
        Manrcroplink_dict=Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                            f'Relink_Croplivstk_N_Emi_CURR.pkl') 
        # pathways providing emissions from specific livestock to specific crops, including both deposition and application
        for key in Manrcroplink_dict:
            for key2 in Manrcroplink_dict[key]:
                Manrcroplink_dict[key][key2] = Manrcroplink_dict[key][key2].replace('\\', '/')

        # Base map summary pickle file
        Base_map_pkl_wd = FABIO_pj_path.Prj_Pkl_output_wd+\
            'AP-AMMO_Map_Imprv_CaliBase.pkl'

    #----------------------------------------------------processing_module----------------------------------------------------

    ## Calibrate maps
    # OUTPUT_DATA
    ### Organize map pathways for processing

    ####Emissions from the livestock or crop side only
    Hous_emi_wddt = Imp_func.conv_df2dict(Manr_mana_df,'Ani_manr_type','Hous_emi_wddt')
    for key in Hous_emi_wddt:
        Hous_emi_wddt[key] = Hous_emi_wddt[key].replace('\\', '/')

    Stor_emi_wddt = Imp_func.conv_df2dict(Manr_mana_df,'Ani_manr_type','Stor_emi_wddt')
    for key in Stor_emi_wddt:
        Stor_emi_wddt[key] = Stor_emi_wddt[key].replace('\\', '/')
    
    
    Synt_fertemi_wddt = Imp_func.conv_df2dict(Crop_side_emi_df,'OSDCropname',\
        'Emi_chemfer_map')

    for key in Synt_fertemi_wddt :
        Synt_fertemi_wddt [key] = Synt_fertemi_wddt[key].replace('\\', '/')
    
    
    Hous_Liq_emi_wddt = {key: value for key, value in Hous_emi_wddt.items() if '_liq' in key}
    Hous_Sld_emi_wddt = {key: value for key, value in Hous_emi_wddt.items() if '_sld' in key}
    Stor_Liq_emi_wddt = {key: value for key, value in Stor_emi_wddt.items() if '_liq' in key}
    Stor_Sld_emi_wddt = {key: value for key, value in Stor_emi_wddt.items() if '_sld' in key}


    Hous_Liq_eminew_wddt = Imp_func.replace_keys(Hous_Liq_emi_wddt, Air_pj_path.Ani_name)
    Hous_Sld_eminew_wddt = Imp_func.replace_keys(Hous_Sld_emi_wddt, Air_pj_path.Ani_name)
    Stor_Liq_eminew_wddt = Imp_func.replace_keys(Stor_Liq_emi_wddt, Air_pj_path.Ani_name)
    Stor_Sld_eminew_wddt =  Imp_func.replace_keys(Stor_Sld_emi_wddt, Air_pj_path.Ani_name)

    #### Emissions involve both sides, including emissions from manure application and from manure deposition
    Manr_applink_dict = Manrcroplink_dict['Manr_app_emi_wddt'] # pathways providing manure applied on specific crops
    Manr_depolink_dict = Manrcroplink_dict['Manr_depo_emi_wddt'] # pathways providing manure deposited on specific crops
    
    App_Liq_linkemi_wddt = {key: value for key, value in Manr_applink_dict.items() if '_liq' in key}
    App_Sld_linkemi_wddt = {key: value for key, value in Manr_applink_dict.items() if '_sld' in key}


    ##### Emissions from liquid manure application
    App_Liq_emi_multi_wddt = {}
    for Prod in Air_pj_path.MainCpNam:
        App_Liq_emi_multi_wddt[Prod]=[value for key, value in App_Liq_linkemi_wddt.items() if Prod in key] 
    App_Liq_emi_multi_wddt=Imp_func.del_keys_dict(App_Liq_emi_multi_wddt,\
        ['Legumfod','Soya','Rice','Peabean'])

    ##### Emissions from solid manure application
    App_Sld_emi_multi_wddt = {}
    for Prod in Air_pj_path.MainCpNam:
        App_Sld_emi_multi_wddt[Prod]=[value for key, value in App_Sld_linkemi_wddt.items() if Prod in key] 
    App_Sld_emi_multi_wddt=Imp_func.del_keys_dict(App_Sld_emi_multi_wddt,\
        ['Legumfod','Soya','Rice','Peabean'])

    ##### Emissions from manure deposition
    Depo_emi_multi_wddt={}
    for Prod in Air_pj_path.Ani_name:
        Depo_emi_multi_wddt[Prod]=[value for key, value in Manr_depolink_dict.items() if Prod in key]
    Depo_emi_multi_wddt=Imp_func.del_keys_dict(Depo_emi_multi_wddt,['pig','potr'])



    # Get maps for individual products at the application and deposition stages
    #OUTPUT_FILE
    for Prod in App_Liq_emi_multi_wddt:
        App_Liq_emi = Imp_func.aggregate(App_Liq_emi_multi_wddt[Prod])
        Imp_func.output_ras_filtered(
            r'./AMMO_footprint/Output_raster/Manr_Liq_app_bycrop/'+ Prod +'_BU_emi.tif',\
            Air_pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',App_Liq_emi)


    #OUTPUT_FILE
    for Prod in App_Sld_emi_multi_wddt:
        App_Sld_emi = Imp_func.aggregate(App_Sld_emi_multi_wddt[Prod])
        Imp_func.output_ras_filtered(
            r'./AMMO_footprint/Output_raster/Manr_Sld_app_bycrop/'+Prod+'_BU_emi.tif',\
            Air_pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',App_Sld_emi)



    # OUTPUT_FILE
    for Prod in Depo_emi_multi_wddt:
        Depo_emi = Imp_func.aggregate(Depo_emi_multi_wddt[Prod])
        Imp_func.output_ras_filtered(
            r'./AMMO_footprint/Output_raster/Manr_depo_byanim/'+Prod+'_BU_depoemi.tif',\
            Air_pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',Depo_emi)
    #this is based on the pathway in my PC



    #OUTPUT_DATA
    App_Liq_emi_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(r'./AMMO_footprint/Output_raster/Manr_Liq_app_bycrop/*.tif',\
        recursive=False))

    App_Sld_emi_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(r'./AMMO_footprint/Output_raster/Manr_Sld_app_bycrop/*.tif',\
        recursive=False))

    Depo_emi_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(r'./AMMO_footprint/Output_raster/Manr_depo_byanim/*.tif',\
            recursive=False))


    ##### Organize all maps to be calibrated
    #OUTPUT_DATA
    Emi_byprod_wddt = {'NH3_Syntfert':Synt_fertemi_wddt,\
                    'NH3_ManrInhous_Liqexcr_Liv':Hous_Liq_eminew_wddt,\
                    'NH3_ManrInhous_Sldexcr_Liv':Hous_Sld_eminew_wddt,\
                    'NH3_Liqstor_Liv':Stor_Liq_eminew_wddt,\
                    'NH3_Sldstor_Liv':Stor_Sld_eminew_wddt,\
                    'NH3_LiqMA_Crop':App_Liq_emi_wddt,\
                    'NH3_SldMA_Crop':App_Sld_emi_wddt,\
                    'NH3_ManrGraz_excr_Liv':Depo_emi_wddt}



    ### Execuate the calibrations
    # OUTPUT_FILE

    for Stage in Use_Emifac_shetname:
        EAT_emifac_data = Imp_func.pd.read_excel(Emi_fac_wd,sheet_name = Stage)
        EAT_emifac_data = EAT_emifac_data.fillna(0)

        if Stage == 'NH3_Syntfert':
            for Prod in Air_pj_path.MainCpNam:
                Imp_func.cali_fig_filter(Emi_byprod_wddt[Stage][Prod],\
                    Air_pj_path.Exam_crop_reson_wd,\
                    Air_pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                    EAT_emifac_data.columns.tolist()[list(Emi_byprod_wddt[Stage].keys()).index(Prod)+1],\
                    #must ensure the same order in the two lists
                    0.0833333333333333,Higreso_path+\
                        Stage.split("_")[1]+'_byprod/'+Prod+f'_{Scenarios_Name}_fertemi.tif')
                
        elif Stage in ['NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
                    'NH3_Liqstor_Liv','NH3_Sldstor_Liv']:
            for Prod in Air_pj_path.Ani_name:
                Imp_func.cali_fig_filter(Emi_byprod_wddt[Stage][Prod],\
                    Air_pj_path.Exam_crop_reson_wd,\
                    Air_pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                    EAT_emifac_data.columns.tolist()[list(Emi_byprod_wddt[Stage].keys()).index(Prod)+1],\
                    0.0833333333333333,Higreso_path+\
                        Stage.split("_")[1]+'_'+Stage.split("_")[2]+\
                        '_byprod/'+Prod+f'_{Scenarios_Name}_'+Stage.split("_")[1]+'_emi.tif')
        
        elif Stage in ['NH3_LiqMA_Crop', 'NH3_SldMA_Crop']:
            for Prod in Imp_func.del_elemt_list(Air_pj_path.MainCpNam,[5,8,10,14]):
                Imp_func.cali_fig_filter(Emi_byprod_wddt[Stage][Prod],\
                    Air_pj_path.Exam_crop_reson_wd,\
                    Air_pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                    EAT_emifac_data.columns.tolist()[list(Emi_byprod_wddt[Stage].keys()).index(Prod)+1],\
                    0.0833333333333333,Higreso_path+\
                    Stage.split("_")[1]+'_byprod/'+Prod+f'_{Scenarios_Name}_'+ Stage.split("_")[1]+'_emi.tif')
        
        elif Stage in ['NH3_ManrGraz_excr_Liv']:
            for Prod in ['dair','othcatl','shep','goat']:
                Imp_func.cali_fig_filter(Emi_byprod_wddt[Stage][Prod],\
                Air_pj_path.Exam_crop_reson_wd,\
                Air_pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                    EAT_emifac_data.columns.tolist()[list(Emi_byprod_wddt[Stage].keys()).index(Prod)+1],\
                    0.0833333333333333,Higreso_path+\
                    Stage.split("_")[1]+'_'+Stage.split("_")[2]+'_byprod/'+ Prod + f'_{Scenarios_Name}_'+Stage.split("_")[1]+'_emi.tif')

    Imp_func.save_plk(Base_map_pkl_wd,\
        Emi_byprod_wddt)
    
    return



def Summa_Emi_Highreso(Scenarios_Name):
    # Scenario-based inputs and outputs-----------------------------------------------------------------------
    if Scenarios_Name == 'EAT':
        Aggre_path = r'./AMMO_footprint/Output_raster/Emi_EAT_bystage/'
        Summar_path = FABIO_pj_path.Prj_Gene_output_wd+'EAT_EMI_byProdStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd+'EAT_EMI_byProdStage.pkl'
        
    elif Scenarios_Name == 'MTFR_EAT':
        Aggre_path = r'./AMMO_footprint/Output_raster/Emi_MTFR_EAT_bystage/'
        Summar_path = FABIO_pj_path.Prj_Gene_output_wd+'MTFR_EAT_EMI_byProdStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd+'MTFR_EAT_EMI_byProdStage.pkl'
        
    elif Scenarios_Name == 'EAT_Meat':
        Aggre_path = f'./AMMO_footprint/Output_raster/Emi_{Scenarios_Name}_bystage/'
        Summar_path =  FABIO_pj_path.Prj_Gene_output_wd+ f'{Scenarios_Name}_EMI_byProdStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_EMI_byProdStage.pkl'
    
    elif Scenarios_Name in ['EAT','EAT_Vegan','EAT_Meat']:
        Aggre_path = f'./AMMO_footprint/Output_raster/Emi_{Scenarios_Name}_bystage/'
        Summar_path =  FABIO_pj_path.Prj_Gene_output_wd+ f'{Scenarios_Name}_EMI_byProdStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_EMI_byProdStage.pkl'
    
        
    ### Aggregate and compare with original emissions
    #OUTPUT
    def collect_emissions(prefix):
        base_path = './AMMO_footprint/Output_raster'
        get = lambda stage: Imp_func.glob.glob(f'{base_path}/Emi_{prefix}_{stage}_byprod/*.tif', recursive=False)
        
        dict_list_rough={
            'Syntfert': get('Syntfert'),
            'Manrhous': get('ManrInhous_Liqexcr') + get('ManrInhous_Sldexcr'),
            'Manrstor': get('Liqstor_Liv') + get('Sldstor_Liv'),
            'Manrapp' : get('LiqMA') + get('SldMA'),
            'Manrdepo': get('ManrGraz_excr')
        }
        
        dict_dict_fine={
            'Syntfert': Imp_func.dict_name_path(Air_pj_path.MainCpNam,get('Syntfert')),
            'Liq_Manrhous': Imp_func.dict_name_path(Air_pj_path.Ani_name,get('ManrInhous_Liqexcr')),
            'Sld_Manrhous':Imp_func.dict_name_path(Air_pj_path.Ani_name,get('ManrInhous_Sldexcr')),
            'Liq_Manrstor': Imp_func.dict_name_path(Air_pj_path.Ani_name, get('Liqstor_Liv')),
            'Sld_Manrstor':Imp_func.dict_name_path(Air_pj_path.Ani_name, get('Sldstor_Liv')),
            'Liq_Manrapp' : Imp_func.dict_name_path(Air_pj_path.MainCpNam,get('LiqMA')),
            'Sld_Manrapp': Imp_func.dict_name_path(Air_pj_path.MainCpNam, get('SldMA')),
            'Manrdepo': Imp_func.dict_name_path(Air_pj_path.Ani_name,get('ManrGraz_excr'))
        }

        return dict_list_rough, dict_dict_fine

    # Collect emissions for both EAT and VEG
    EAT_Emi_bystage_Aggrwddt,  EAT_Emi_bystage_Sumarwddt= collect_emissions('EAT')
    MTFR_EAT_Emi_bystage_Aggrwddt, MTFR_EAT_Emi_bystage_Sumarwddt = collect_emissions('MTFR_EAT')
    Meat_Emi_bystage_Aggrwddt, Meat_Emi_bystage_Sumarwddt = collect_emissions('EAT_Meat')
    EAT_Emi_bystage_Aggrwddt,EAT_Emi_bystage_Sumarwddt= collect_emissions('EAT')
    EAT_Vegan_Emi_bystage_Aggrwddt,EAT_Vegan_Emi_bystage_Sumarwddt= collect_emissions('EAT_Vegan')
    EAT_Meat_Emi_bystage_Aggrwddt,EAT_Meat_Emi_bystage_Sumarwddt= collect_emissions('EAT_Meat')
    
    Scenarios_Emi_bystageAggr_wddt={'EAT':EAT_Emi_bystage_Aggrwddt,\
        'EAT_Meat':Meat_Emi_bystage_Aggrwddt,\
        'MTFR_EAT':MTFR_EAT_Emi_bystage_Aggrwddt,\
        'EAT':EAT_Emi_bystage_Aggrwddt,\
        'EAT_Vegan': EAT_Vegan_Emi_bystage_Aggrwddt,\
        'EAT_Meat': EAT_Meat_Emi_bystage_Aggrwddt}

    Scenarios_Emi_bystageSummar_wddt={'EAT':EAT_Emi_bystage_Sumarwddt,\
        'EAT_Meat':Meat_Emi_bystage_Sumarwddt,\
        'MTFR_EAT':MTFR_EAT_Emi_bystage_Sumarwddt,\
        'EAT':EAT_Emi_bystage_Sumarwddt,\
        'EAT_Vegan':EAT_Vegan_Emi_bystage_Sumarwddt,\
        'EAT_Meat': EAT_Meat_Emi_bystage_Sumarwddt}



    # OUTPUT_FILE
    for i in Scenarios_Emi_bystageAggr_wddt[Scenarios_Name]:
        Aggr_emi = Imp_func.aggregate(Scenarios_Emi_bystageAggr_wddt[Scenarios_Name][i])
        Imp_func.output_ras_filtered(Aggre_path+i+f'_{Scenarios_Name}_emi.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Aggr_emi)


    #----------------------------------------------------Output_module---------------------------------------------------
    ## summarize dictionaries by product and stage
    #SUMMARY

    Imp_func.zonal_summary(
    ['Syntfert_emi_'+\
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Syntfert'].keys())]+\
    ['Housliq_emi_'+\
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrhous'].keys())]+\
    ['Houssld_emi_'+ \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrhous'].keys())]+\
    ['Storliq_emi_'+ \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrstor'].keys())]+\
    ['Storsld_emi_' + \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrstor'].keys())]+\
    ['Appliq_emi_' + \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrapp'].keys())]+\
    ['Appsld_emi_' + \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrapp'].keys())]+\
    ['Grazdepo_emi_'+ \
        item for item in \
        list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Manrdepo'].keys())],\

    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Syntfert'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrhous'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrhous'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrstor'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrstor'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Liq_Manrapp'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Sld_Manrapp'].values())+\
    list(Scenarios_Emi_bystageSummar_wddt[Scenarios_Name]['Manrdepo'].values()),
        
    Air_pj_path.EFTA_UK_wd,32,'sum',-999,Summar_path)


    Aggr_emi_wddt = Imp_func.dict_name_path(
        list(Scenarios_Emi_bystageAggr_wddt[Scenarios_Name].keys()),\
        Imp_func.glob.glob(Aggre_path+'*.tif',recursive=False))


    Imp_func.save_plk(Summar_pkl_path,\
        {'Detailed':Scenarios_Emi_bystageSummar_wddt[Scenarios_Name],\
        'Aggregated':Aggr_emi_wddt})
    
    return


