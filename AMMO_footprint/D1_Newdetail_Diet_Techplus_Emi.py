# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# D1_Newdetail_Diet_Techplus_Emi — MTFR factors applied to the PHD emissions


#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path


#%%

def Emiplus_calc(Scenarios_Name,Tech_measure):
    Emi_fac_wd = FABIO_pj_path.Prj_input_wd + r'Processing_plot_new.xlsx'
    
    if Scenarios_Name == 'CURR_plus':
        ### The mitigated emission pathways (Output directory for the mitigated emission maps)
        Miti_manrchain_wd = Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
        ### The stage-specific emission maps
        Hous_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Hous_totemi.tif'
        Stor_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Stor_totemi.tif'
        App_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/App_totemi.tif'
        Graz_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Grazdepo_totemi.tif'

        
    elif Scenarios_Name == 'EAT_Vegan_plus':
        ### The mitigated emission pathways
        Miti_manrchain_wd =  Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
        ### The stage-specific emission maps
        Hous_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Hous_totemi.tif'
        Stor_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Stor_totemi.tif'
        App_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/App_totemi.tif'
        Graz_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Grazdepo_totemi.tif'


    elif Scenarios_Name == 'EAT_Meat_plus': 
        ### The mitigated emission pathways
        Miti_manrchain_wd =  Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
        ### The stage-specific emission maps
        Hous_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Hous_totemi.tif'
        Stor_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Stor_totemi.tif'
        App_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/App_totemi.tif'
        Graz_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Grazdepo_totemi.tif'


 
    elif Scenarios_Name == 'EAT_plus': 
        ### The mitigated emission pathways
        Miti_manrchain_wd =  Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
        Miti_syntfert_wd = Air_pj_path.output_wd + f'{Scenarios_Name}_Syntfert_Emi/'
        Imp_func.os.makedirs(Miti_syntfert_wd, exist_ok=True)
        ### The stage-specific emission maps
        Hous_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Hous_totemi.tif'
        Stor_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Stor_totemi.tif'
        App_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/App_totemi.tif'
        Graz_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Grazdepo_totemi.tif'
        Syntfert_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Syntfert_fert_emi.tif'
        
        
    elif Scenarios_Name == 'EAT_Meat_plus': 
        ### The mitigated emission pathways
        Miti_manrchain_wd =  Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
        Miti_syntfert_wd = Air_pj_path.output_wd + f'{Scenarios_Name}_Syntfert_Emi/'
        Imp_func.os.makedirs(Miti_syntfert_wd, exist_ok=True)
        ### The stage-specific emission maps
        Hous_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Hous_totemi.tif'
        Stor_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Stor_totemi.tif'
        App_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/App_totemi.tif'
        Graz_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Grazdepo_totemi.tif'
        Syntfert_MitiEmi_wd = FABIO_pj_path.Prj_Rster_output_wd+f'{Scenarios_Name}/{Tech_measure}/Syntfert_fert_emi.tif'
        
    else:
        # This prevents the UnboundLocalError by providing a fallback
        print(f"Warning: Tech_measure '{Tech_measure}' not recognized. Using default factors.")
        Miti_housfac_data = None 
        Miti_storfac_data = None
        Miti_appfac_data = None
        Miti_grazfac_data = None
        Miti_syntfertfac_data = None
        
    
    ### middle is the napcp scenario
    if Tech_measure == 'NAPCP':
        #### housing emissions
        Miti_housfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='NAPCP_Hous_imprv')
        #### storage emissions
        Miti_storfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='NAPCP_Stor_imprv')
        #### Application emissions
        Miti_appfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='NAPCP_App_imprv')
        #### grazing deposition emissions
        Miti_grazfac_data =  Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='NAPCP_Graz_imprv')
        
    elif  Tech_measure == 'MTFR':
        #### housing emissions
        Miti_housfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='MTFR_Hous_imprv')
        #### storage emissions
        Miti_storfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='MTFR_Stor_imprv')
        #### Application emissions
        Miti_appfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='MTFR_App_imprv')
        #### grazing deposition emissions
        Miti_grazfac_data =  Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='MTFR_Graz_imprv')
        #### synthetic fertilizer emissions
        Miti_syntfertfac_data = Imp_func.pd.read_excel(Emi_fac_wd,\
            sheet_name ='MTFR_Syntfert_imprv')

    
    else:
        # If Tech_measure is wrong, STOP the function here with a clear error
        raise ValueError(f"CRITICAL ERROR: Tech_measure '{Tech_measure}' is not valid.")
    
    #----------------------------------------------------Processing_module----------------------------------------------------
    # Calculate total emissions
    # OUTPUT_DATA
    base_name = Scenarios_Name.removesuffix('_plus')
    
    ## Emissions are from B9 (this is the input for the mitigation calculation)
    Manr_housemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Hous_Manr_emi']
    Manr_storemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Stor_Manr_emi']
    Manr_appemi_wddt =  Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['App_Manr_emi']
    Manr_graemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Graz_Manr_emi']
    Syntfert_emi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Syntfert_fert_emi']
    
    ## Sort manure application emissions by livestock
    Pig_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'pig_liq' in k}
    Pig_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'pig_sld' in k}
    
    Dair_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'dair_liq' in k}
    Dair_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'dair_sld' in k}
    
    Othcatl_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'othcatl_liq' in k}
    Othcatl_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'othcatl_sld' in k}
    
    Shep_liq_appemi_wddt =  {k: v for k, v in Manr_appemi_wddt.items() if 'shep_liq' in k}
    Shep_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'shep_sld' in k}
    
    Goat_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'goat_liq' in k}
    Goat_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'goat_sld' in k}
    
    Potr_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'potr_liq' in k}
    Potr_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'potr_sld' in k}
    
    Manr_Liveapp_wddt = {
        'pig_liq_App':Pig_liq_appemi_wddt,'dair_liq_App':Dair_liq_appemi_wddt,\
        'othcatl_liq_App':Othcatl_liq_appemi_wddt, 'shep_liq_App':Shep_liq_appemi_wddt,\
        'goat_liq_App':Goat_liq_appemi_wddt,'potr_liq_App':Potr_liq_appemi_wddt,\
        'pig_sld_App':Pig_sld_appemi_wddt, 'dair_sld_App':Dair_sld_appemi_wddt,\
        'othcatl_sld_App':Othcatl_sld_appemi_wddt, 'shep_sld_App':Shep_sld_appemi_wddt,\
        'goat_sld_App':Goat_sld_appemi_wddt,'potr_sld_App':Potr_sld_appemi_wddt}
    
    
    ## Sort manure grazing emissions by livestock
    if Scenarios_Name in ['CURR_plus']:
        Dair_graz_emi_wddt = {'Tempgra_dair':Manr_graemi_wddt['Tempgra_dair_Graz'],\
            'Permgra_dair':Manr_graemi_wddt['Permgra_dair_Graz']}
        Othcatl_graz_emi_wddt = {'Tempgra_othcatl': Manr_graemi_wddt['Tempgra_othcatl_Graz'],\
            'Permgra_othcatl':Manr_graemi_wddt['Permgra_othcatl_Graz']}
        Goat_graz_emi_wddt = {'Tempgra_goat':Manr_graemi_wddt['Tempgra_goat_Graz'],\
            'Permgra_goat':Manr_graemi_wddt['Permgra_goat_Graz']}
        Shep_graz_emi_wddt = {'Tempgra_shep':Manr_graemi_wddt['Tempgra_shep_Graz'],\
            'Permgra_shep':Manr_graemi_wddt['Permgra_shep_Graz']}
        
    else:
        Dair_graz_emi_wddt = {'Tempgra_dair':Manr_graemi_wddt['Tempgra_dair'],\
            'Permgra_dair':Manr_graemi_wddt['Permgra_dair']}
        Othcatl_graz_emi_wddt = {'Tempgra_othcatl': Manr_graemi_wddt['Tempgra_othcatl'],\
            'Permgra_othcatl':Manr_graemi_wddt['Permgra_othcatl']}
        Goat_graz_emi_wddt = {'Tempgra_goat':Manr_graemi_wddt['Tempgra_goat'],\
            'Permgra_goat':Manr_graemi_wddt['Permgra_goat']}
        Shep_graz_emi_wddt = {'Tempgra_shep':Manr_graemi_wddt['Tempgra_shep'],\
            'Permgra_shep':Manr_graemi_wddt['Permgra_shep']}
    
    Manr_Livgraz_wddt = {
        'dair_graz': Dair_graz_emi_wddt,\
        'othcatl_graz': Othcatl_graz_emi_wddt,\
        'shep_graz':Shep_graz_emi_wddt,\
        'goat_graz':Goat_graz_emi_wddt
        }
    
    
    #OUTPUT_FILE
    ### Getting synthetic fertilizer emissions
    Imp_func.os.makedirs(Miti_syntfert_wd + f'{Tech_measure}/', exist_ok=True)
    for items in Syntfert_emi_wddt:
        Imp_func.cali_fig_filter(Syntfert_emi_wddt[items],\
            Air_pj_path.Exam_crop_reson_wd,\
            Air_pj_path.EFTA_UK_wd,\
            Miti_syntfertfac_data,'FID_1','Name_abbre',\
            'Syntfert_Miti_fac',\
            #must ensure the same order in the two lists
            0.0833333333333333, Miti_syntfert_wd +\
                f'{Tech_measure}/{items}_miti_emi.tif')
    
    
    Synt_emi_value = Imp_func.aggregate(Imp_func.glob.glob(Miti_syntfert_wd +\
        f'{Tech_measure}/*.tif',\
        recursive=False))
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(Syntfert_MitiEmi_wd,Air_pj_path.Exam_500area_wd,\
        'EPSG:4326', Synt_emi_value)
    
    
    
    
    #OUTPUT_FILE
    ### Getting housing emissions    
    for items in Manr_housemi_wddt:
        Imp_func.cali_fig_filter(Manr_housemi_wddt[items],\
            Air_pj_path.Exam_crop_reson_wd,\
            Air_pj_path.EFTA_UK_wd, Miti_housfac_data,'FID_1','Name_abbre',\
            Miti_housfac_data.columns.tolist()[list(Manr_housemi_wddt.keys()).index(items)+1],\
            #must ensure the same order in the two lists
            0.0833333333333333, Miti_manrchain_wd +\
                f'{Tech_measure}/Housing/{items}_miti_emi.tif')
    
    
    Hous_emi_value = Imp_func.aggregate(Imp_func.glob.glob(Miti_manrchain_wd +\
        f'{Tech_measure}/Housing/*.tif',\
        recursive=False))
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(Hous_MitiEmi_wd,Air_pj_path.Exam_500area_wd,\
        'EPSG:4326', Hous_emi_value)
        
        
    ### Getting storage emissions       
    for items in Manr_storemi_wddt:
        Imp_func.cali_fig_filter(Manr_storemi_wddt[items],\
            Air_pj_path.Exam_crop_reson_wd,\
            Air_pj_path.EFTA_UK_wd, Miti_storfac_data,'FID_1','Name_abbre',\
            Miti_storfac_data.columns.tolist()[list(Manr_storemi_wddt.keys()).index(items)+1],\
            #must ensure the same order in the two lists
            0.0833333333333333, Miti_manrchain_wd +\
                f'{Tech_measure}/Storage/{items}_miti_emi.tif')
    
    Stor_emi_value =  Imp_func.aggregate(Imp_func.glob.glob(Miti_manrchain_wd +\
                f'{Tech_measure}/Storage/*.tif',recursive=False))
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(Stor_MitiEmi_wd,Air_pj_path.Exam_500area_wd,\
        'EPSG:4326', Stor_emi_value)
        
        
    ### Getting application emissions       
    for items in Manr_Liveapp_wddt:
        for submap in Manr_Liveapp_wddt[items]:
            Imp_func.cali_fig_filter(Manr_Liveapp_wddt[items][submap],\
                Air_pj_path.Exam_crop_reson_wd,\
                Air_pj_path.EFTA_UK_wd, Miti_appfac_data,'FID_1','Name_abbre',\
                Miti_appfac_data.columns.tolist()[list(Manr_Liveapp_wddt.keys()).index(items)+1],\
                #must ensure the same order in the two lists
                0.0833333333333333, Miti_manrchain_wd +\
                    f'{Tech_measure}/Application/{submap}_miti_emi.tif')
    
    
    App_emi_value =  Imp_func.aggregate(Imp_func.glob.glob(Miti_manrchain_wd +\
                f'{Tech_measure}/Application/*.tif',recursive=False))
    
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(App_MitiEmi_wd,Air_pj_path.Exam_500area_wd,\
        'EPSG:4326', App_emi_value)
    
        
    ### Getting grazing emissions         
    for items in Manr_Livgraz_wddt:
        for submap in Manr_Livgraz_wddt[items]:
            Imp_func.cali_fig_filter(Manr_Livgraz_wddt[items][submap],\
                Air_pj_path.Exam_crop_reson_wd,\
                Air_pj_path.EFTA_UK_wd, Miti_grazfac_data,'FID_1','Name_abbre',\
                Miti_grazfac_data.columns.tolist()[list(Manr_Livgraz_wddt.keys()).index(items)+1],\
                #must ensure the same order in the two lists
                0.0833333333333333, Miti_manrchain_wd +\
                    f'{Tech_measure}/Grazdepo/{submap}_miti_emi.tif')
    
    Grazdepo_emi_value = Imp_func.aggregate(Imp_func.glob.glob(Miti_manrchain_wd +\
                    f'{Tech_measure}/Grazdepo/*.tif',recursive=False))
    
    
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(Graz_MitiEmi_wd,Air_pj_path.Exam_500area_wd,\
        'EPSG:4326', Grazdepo_emi_value)
    
    
    #SUMMARY
    Imp_func.zonal_summary(['Hous','Storage','Application','Grazing_depo','Syntfert'],\
        [Hous_MitiEmi_wd, Stor_MitiEmi_wd, App_MitiEmi_wd, \
        Graz_MitiEmi_wd, Syntfert_MitiEmi_wd],\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_{Tech_measure}_Emichek.xlsx')
    
    return


#%%

def Summar_Diet_Tech_plus(Scenarios_Name,Tech_measure):
    Miti_manrchain_wd = Air_pj_path.output_wd + f'{Scenarios_Name}_Manrchain_Emi/'
    Miti_syntfert_wd = Air_pj_path.output_wd + f'{Scenarios_Name}_Syntfert_Emi/'
    
    #----------------------------------------------------Processing_module----------------------------------------------------
    # Calculate total emissions
    # OUTPUT_DATA
    base_name = Scenarios_Name.removesuffix('_plus')
    
    ## Emissions are from B9
    Syntfertemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Syntfert_fert_emi']
    Manr_housemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Hous_Manr_emi']
    Manr_storemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Stor_Manr_emi']
    Manr_appemi_wddt =  Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['App_Manr_emi']
    Manr_graemi_wddt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd +'ScenEmi_s.pkl')['Detailed_emi'][base_name]['Graz_Manr_emi']
    
    
    ## Sort manure application emissions by livestock
    Pig_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'pig_liq' in k}
    Pig_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'pig_sld' in k}
    
    Dair_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'dair_liq' in k}
    Dair_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'dair_sld' in k}
    
    Othcatl_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'othcatl_liq' in k}
    Othcatl_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'othcatl_sld' in k}
    
    Shep_liq_appemi_wddt =  {k: v for k, v in Manr_appemi_wddt.items() if 'shep_liq' in k}
    Shep_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'shep_sld' in k}
    
    Goat_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'goat_liq' in k}
    Goat_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'goat_sld' in k}
    
    Potr_liq_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'potr_liq' in k}
    Potr_sld_appemi_wddt = {k: v for k, v in Manr_appemi_wddt.items() if 'potr_sld' in k}
    
    Manr_Liveapp_wddt = {
        'pig_liq_App':Pig_liq_appemi_wddt,'dair_liq_App':Dair_liq_appemi_wddt,\
        'othcatl_liq_App':Othcatl_liq_appemi_wddt, 'shep_liq_App':Shep_liq_appemi_wddt,\
        'goat_liq_App':Goat_liq_appemi_wddt,'potr_liq_App':Potr_liq_appemi_wddt,\
        'pig_sld_App':Pig_sld_appemi_wddt, 'dair_sld_App':Dair_sld_appemi_wddt,\
        'othcatl_sld_App':Othcatl_sld_appemi_wddt, 'shep_sld_App':Shep_sld_appemi_wddt,\
        'goat_sld_App':Goat_sld_appemi_wddt,'potr_sld_App':Potr_sld_appemi_wddt}
    
    ## Sort manure grazing emissions by livestock
    if Scenarios_Name in ['CURR_plus']:
        Dair_graz_emi_wddt = {'Tempgra_dair':Manr_graemi_wddt['Tempgra_dair_Graz'],\
            'Permgra_dair':Manr_graemi_wddt['Permgra_dair_Graz']}
        Othcatl_graz_emi_wddt = {'Tempgra_othcatl': Manr_graemi_wddt['Tempgra_othcatl_Graz'],\
            'Permgra_othcatl':Manr_graemi_wddt['Permgra_othcatl_Graz']}
        Goat_graz_emi_wddt = {'Tempgra_goat':Manr_graemi_wddt['Tempgra_goat_Graz'],\
            'Permgra_goat':Manr_graemi_wddt['Permgra_goat_Graz']}
        Shep_graz_emi_wddt = {'Tempgra_shep':Manr_graemi_wddt['Tempgra_shep_Graz'],\
            'Permgra_shep':Manr_graemi_wddt['Permgra_shep_Graz']}
        
    else:
        Dair_graz_emi_wddt = {'Tempgra_dair':Manr_graemi_wddt['Tempgra_dair'],\
            'Permgra_dair':Manr_graemi_wddt['Permgra_dair']}
        Othcatl_graz_emi_wddt = {'Tempgra_othcatl': Manr_graemi_wddt['Tempgra_othcatl'],\
            'Permgra_othcatl':Manr_graemi_wddt['Permgra_othcatl']}
        Goat_graz_emi_wddt = {'Tempgra_goat':Manr_graemi_wddt['Tempgra_goat'],\
            'Permgra_goat':Manr_graemi_wddt['Permgra_goat']}
        Shep_graz_emi_wddt = {'Tempgra_shep':Manr_graemi_wddt['Tempgra_shep'],\
            'Permgra_shep':Manr_graemi_wddt['Permgra_shep']}
    
    Manr_Livgraz_wddt = {
        'dair_graz': Dair_graz_emi_wddt,\
        'othcatl_graz': Othcatl_graz_emi_wddt,\
        'shep_graz':Shep_graz_emi_wddt,\
        'goat_graz':Goat_graz_emi_wddt
        }
    
    Syntfert_tech_wddt = Imp_func.dict_name_path(
        list(Syntfertemi_wddt.keys()),Imp_func.glob.glob(Miti_syntfert_wd  +\
            f'{Tech_measure}/*.tif', recursive=False))

    Manr_houstech_wddt =  Imp_func.dict_name_path(
        list(Manr_housemi_wddt.keys()),Imp_func.glob.glob(Miti_manrchain_wd +\
            f'{Tech_measure}/Housing/*_miti_emi.tif', recursive=False))

    Manr_stortech_wddt = Imp_func.dict_name_path(
        list(Manr_storemi_wddt.keys()),Imp_func.glob.glob(Miti_manrchain_wd +\
                f'{Tech_measure}/Storage/*.tif',recursive=False))

    Manr_apptech_wddt = {}
    for item in Manr_Liveapp_wddt:
        Manr_apptech_wddt[item]={}
        Manr_apptech_wddt[item] = Imp_func.dict_name_path(list(Manr_Liveapp_wddt[item].keys()),\
            Imp_func.glob.glob(Miti_manrchain_wd +\
                        f'{Tech_measure}/Application/*_miti_emi.tif',recursive=False))
    
    Manr_graztech_wddt = {}
    for items in Manr_Livgraz_wddt:
        Manr_graztech_wddt[items] = {}
        Manr_graztech_wddt[items] = Imp_func.dict_name_path(
            list(Manr_Livgraz_wddt[items].keys()),\
            Imp_func.glob.glob(Miti_manrchain_wd +\
                    f'{Tech_measure}/Grazdepo/*_miti_emi.tif',recursive=False))
    
    Tot_emi_dt = \
        Imp_func.aggregate(
            list(Syntfert_tech_wddt.values()) +\
            list(Manr_houstech_wddt.values()) +\
            list(Manr_stortech_wddt.values()) +\
            [path for subdict in Manr_apptech_wddt.values() for\
            path in subdict.values()] +\
            [path for subdict in Manr_graztech_wddt.values() for\
            path in subdict.values()])

    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_{Tech_measure}_totemi.tif',\
        FABIO_pj_path.Prj_input_wd+r'Sptial_file/Agr_large500.tif',\
        'EPSG:4326',Tot_emi_dt)
            
    
    Diet_tech_emi_wddt = {
        'Tot_emi':FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_{Tech_measure}_totemi.tif',\
        'Syntfert_fert_emi': Syntfert_tech_wddt,\
        'Hous_Manr_emi':Manr_houstech_wddt,\
        'Stor_Manr_emi':Manr_stortech_wddt,\
        'App_Manr_emi':Manr_apptech_wddt,\
        'Graz_Manr_emi':Manr_graztech_wddt}
    
    return Diet_tech_emi_wddt


