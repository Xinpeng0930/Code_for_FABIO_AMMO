# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# D2_Emi_Sort_Shar — emission shares and sorting across scenarios
#%%
'''
Creator/Editor: Xinpeng Jin, CML Leiden University 

This script is aiming to get emission data from crop side only (synthetic fertilizer),\
livestock side only (manure management), and both side related emissions(manure on land)
This script also exports data to be uploaded in figshare for the second paper

'''
#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path

#%%

def Sort_Share(Scenarios_Name):
    # Create all output directories if they don't exist
    for folder in [
        f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Synthetic_fertilizer_use(SF)',
        f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Manure_input(MI)',
        f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Manure_management(MM)',
        f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Manure_deposition(MD)',
        f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Manure_application(MA)',
        FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Manrgrz_Emi_bygrass',
        FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appliq_Emi_bycrop',
        FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appsld_Emi_bycrop',
        FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appliq_Emi_byliv',
        FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appsld_Emi_byliv',
        FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Adj_Emi_for_Consp_allo',
    ]:
        Imp_func.os.makedirs(folder, exist_ok=True)

    #OUTPUT_DATA
    if Scenarios_Name in ['CURR','CURR_MTFR',\
        'EAT','MTFR_EAT','EAT_Meat']:
        
        ## Emissions from each detailed category (from B9)
        Scen_DetailEmi_dt = Imp_func.open_plk(
            r'./AMMO_footprint/Output_pkl/ScenEmi_s.pkl')['Detailed_emi'][Scenarios_Name]
        
        ### Manure application
        Manr_applink_dict = Scen_DetailEmi_dt['App_Manr_emi'] # pathways providing manure applied on specific crops

        #### Need to make some adjustments for emissions from manure application
        Crop_manr_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Manr_applink_dict,\
            Air_pj_path.MainCpNam)
        
        #### Get the liquid and solid manure
        Liqkeys3 = [key for key in Manr_applink_dict.keys() if '_liq' in key]
        Sldkeys3 = [key for key in Manr_applink_dict.keys() if '_sld' in key]

        App_liqemi_wddt = Imp_func.filter_dict(Manr_applink_dict,Liqkeys3)
        App_sldemi_wddt = Imp_func.filter_dict(Manr_applink_dict,Sldkeys3)

        App_liqemi_crop_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_liqemi_wddt,\
            Air_pj_path.MainCpNam)
        App_sldemi_crop_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_sldemi_wddt,\
            Air_pj_path.MainCpNam)
        App_liqemi_livsk_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_liqemi_wddt,\
            Air_pj_path.Ani_name)
        App_sldemi_livsk_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_sldemi_wddt,\
            Air_pj_path.Ani_name)
        
        #### Manure application by animal
        Livstk_app_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Manr_applink_dict,\
            Air_pj_path.Ani_name)
        
        ### Manure deposition
        Manr_depolink_dict = Scen_DetailEmi_dt['Graz_Manr_emi'] # pathways providing manure deposited on specific crops

        #### Emissions from manure deposition by crop
        Gras_depo_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Manr_depolink_dict,\
            ['Tempgra','Permgra'])
        
        #### Emissions from manure deposition by animal
        Livstk_depo_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Manr_depolink_dict,\
            Air_pj_path.Ani_name)
        
        
    
    
    elif Scenarios_Name in [
        'EAT_plus_NAPCP','EAT_plus_MTFR',\
        'EAT_Vegan_plus_NAPCP','EAT_Vegan_plus_MTFR',\
        'CURR_plus_NAPCP','CURR_plus_MTFR',\
        'CURR_plus_NAPCP','CURR_plus_MTFR',\
        'EAT_plus_NAPCP','EAT_MTFR',\
        'EAT_Vegan_plus_NAPCP','EAT_Vegan_plus_MTFR',\
        'EAT_Meat_plus_NAPCP','EAT_Meat_plus_MTFR']:
        
        ## Emissions from each detailed category
        Scen_DetailEmi_dt = Imp_func.open_plk(
            r'./AMMO_footprint/Output_pkl/Comb_diet_tech_emi.pkl')[Scenarios_Name]
        
        ### Manure application
        Manr_applink_dict = Scen_DetailEmi_dt['App_Manr_emi'] # pathways providing manure applied on specific crops

        #### Need to make some adjustments for emissions from manure application
        Flat_manr_app_dict = Imp_func.Flat_hierk_dict(Manr_applink_dict)

        Crop_manr_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Flat_manr_app_dict,\
            Air_pj_path.MainCpNam)

        #### Get the liquid and solid manure
        Liqkeys3 = [key for key in Flat_manr_app_dict.keys() if '_liq' in key]
        Sldkeys3 = [key for key in Flat_manr_app_dict.keys() if '_sld' in key]

        App_liqemi_wddt = Imp_func.filter_dict(Flat_manr_app_dict, Liqkeys3)
        App_sldemi_wddt = Imp_func.filter_dict(Flat_manr_app_dict, Sldkeys3)

        App_liqemi_crop_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_liqemi_wddt,\
            Air_pj_path.MainCpNam)
        App_sldemi_crop_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_sldemi_wddt,\
            Air_pj_path.MainCpNam)
        App_liqemi_livsk_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_liqemi_wddt,\
            Air_pj_path.Ani_name)
        App_sldemi_livsk_wddt = Imp_func.Decompose_linkdict2hierk_dictlist(App_sldemi_wddt,\
            Air_pj_path.Ani_name)
        
        #### Manure application by animal
        Livstk_app_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Flat_manr_app_dict,\
            Air_pj_path.Ani_name)
        
        ### Manure deposition
        Manr_depolink_dict = Scen_DetailEmi_dt['Graz_Manr_emi'] # pathways providing manure deposited on specific crops

        #### Emissions from manure deposition by crop
        Flat_manr_depo_dict = Imp_func.Flat_hierk_dict(Manr_depolink_dict)
        
        Gras_depo_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Flat_manr_depo_dict,\
            ['Tempgra','Permgra'])
        
        #### Emissions from manure deposition by animal
        Livstk_depo_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Flat_manr_depo_dict,\
            Air_pj_path.Ani_name)
        
        
    ### Chemical fertilizer
    Chemfer_EMI_wddt = Scen_DetailEmi_dt['Syntfert_fert_emi'] #pathways of emissions from synthetic fertilizer 

    
    ### Manure managemnet
    Hous_emi_wddt = Scen_DetailEmi_dt['Hous_Manr_emi']
    Stor_emi_wddt = Scen_DetailEmi_dt['Stor_Manr_emi']

    
    # OUTPUT_DATA
    # Emissions from synthetic fertilizer
    for Crop in list(Chemfer_EMI_wddt.keys()):
        source_path = Chemfer_EMI_wddt[Crop]
        
        destination_folder_path = f'AMMO_footprint/Data_Shar/{Scenarios_Name}/Synthetic_fertilizer_use(SF)/'
        New_Emi_synfer_filename = f"SF_{Crop}_NH3-N.tif"  # Example: prefix "new_" to each file name
        destination_path = Imp_func.os.path.join(destination_folder_path, New_Emi_synfer_filename) 

        # Copy the file and rename it
        # OUTPUT_FILE
        Imp_func.shutil.copy2(source_path, destination_path)


    # Emissions from manure input    
    ## Emission from manure inputs by crop
    Crop_manr_hierk_copy_dict= Imp_func.deepcopy(Crop_manr_hierk_dict) 

    Manr_input_bycrop = Imp_func.Comb_dict_bykeys(Crop_manr_hierk_copy_dict,\
        Gras_depo_hierk_dict)

    
    # OUTPUT_FILE
    for k in Manr_input_bycrop:
        Crop_manr_inputN = Imp_func.aggregate(Manr_input_bycrop[k])
        Imp_func.output_ras_filtered(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'
            r'Manure_input(MI)/MI_'+k+'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',Crop_manr_inputN)


    ## Emissions from manure management
    # OUTPUT_DATA
    ### Emissions from manure management by livestock
    Livestk_Housmanr_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Hous_emi_wddt,\
        Air_pj_path.Ani_name)

    Livestk_Stormanr_hierk_dict = Imp_func.Decompose_linkdict2hierk_dictlist(Stor_emi_wddt,\
        Air_pj_path.Ani_name)

    Livestk_Housmanr_copy_hierk_dict = Imp_func.deepcopy(Livestk_Housmanr_hierk_dict)
    Livestk_manr_hierk_dict = Imp_func.Comb_dict_bykeys(Livestk_Housmanr_copy_hierk_dict,\
        Livestk_Stormanr_hierk_dict)


    #OUTPUT_FILE
    for k in Livestk_manr_hierk_dict:
        Livestk_manr_mana_N = Imp_func.aggregate(Livestk_manr_hierk_dict[k])
        Imp_func.output_ras_filtered(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
                r'Manure_management(MM)/MM_'+k+'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',Livestk_manr_mana_N)

    
    ## Emissions from Manure deposited on grassland by livestock
    #OUTPUT_FILE
    for k in Livstk_depo_hierk_dict:
        Livstk_manr_depo_N = Imp_func.aggregate(Livstk_depo_hierk_dict[k])
        Imp_func.output_ras_filtered(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_deposition(MD)/MD_'+k+'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',Livstk_manr_depo_N)


    ## Emissions from Manure app
    #OUTPUT_FILE
    for k in Livstk_app_hierk_dict:
        Livstk_manr_app_N = Imp_func.aggregate(Livstk_app_hierk_dict[k])
        Imp_func.output_ras_filtered(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_application(MA)/MA_'+k+'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',Livstk_manr_app_N)

    
    #----------------------------------------------------output_module----------------------------------------------------
    #### execute the summarization
    ##### Summary for livestock related emissions
    #OUTPUT_DATA
    Livstk_manrapp_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_application(MA)/MA_*_NH3-N.tif',recursive=False))

    Livstk_manrdepo_wddt = Imp_func.dict_name_path(['dair','othcatl','shep','goat'],\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_deposition(MD)/MD_*_NH3-N.tif',recursive=False))

    Livstk_manrmana_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
                r'Manure_management(MM)/MM_*_NH3-N.tif',recursive=False))

    #SUMMARY
    ##### emissions from manure management, application, and deposition
    Imp_func.zonal_summary([item + 'mana' for item in list(Livstk_manrmana_wddt.keys())] + \
        [item + 'app' for item in list(Livstk_manrapp_wddt.keys())] + [item + 'depo' for item in list(Livstk_manrdepo_wddt.keys())] ,\
        list(Livstk_manrmana_wddt.values()) + list(Livstk_manrapp_wddt.values()) + list(Livstk_manrdepo_wddt.values()),\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999, \
        FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Emi_Livstkonly.xlsx')


    ### execute the summarization
    #### Summary for emissions from the crop side
    #OUTPUT_DATA
    Manr_Inputemi_bycrop_wddt = Imp_func.dict_name_path(
        Air_pj_path.MainCpNam,Imp_func.glob.glob(
            f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_input(MI)/MI_*_NH3-N.tif',recursive=False))

    Syn_fertemi_bycrop_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(
            f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Synthetic_fertilizer_use(SF)/*.tif',recursive=False))


    #SUMMARY
    #### emissions from synthetic fertilizer and manure input
    Imp_func.zonal_summary([item + 'syntfert' for item in list(Syn_fertemi_bycrop_wddt.keys())] + \
        [item + 'manrinput' for item in list(Manr_Inputemi_bycrop_wddt.keys())], \
        list(Syn_fertemi_bycrop_wddt.values()) + list(Manr_Inputemi_bycrop_wddt.values()),\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
    FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Emi_Croponly.xlsx')


    
    #------------Summarize data for allocate consumption-based calculations----------------------------------------------------

    # SUMMARY
    #### Synthetic fertilizer by crop
    Imp_func.zonal_summary(list(Chemfer_EMI_wddt.keys()),\
            list(Chemfer_EMI_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_Syntfert.xlsx')

    #### Manure emissions during grazing by livestock
    Imp_func.zonal_summary(list(Livstk_manrdepo_wddt.keys()),\
            list(Livstk_manrdepo_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_ManrGraz_excr_Liv.xlsx')

    #### Manure emissions during grazing by crop(grass)
    # OUTPUT_FILE
    for k in Gras_depo_hierk_dict:
        Gras_manr_depo_N = Imp_func.aggregate(Gras_depo_hierk_dict[k])
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Manrgrz_Emi_bygrass/'+\
            r'MD_'+k+'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',Gras_manr_depo_N)

    # OUTPUT_DATA
    Gras_manrdepo_wddt = Imp_func.dict_name_path(['Tempgra','Permgra'],\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Manrgrz_Emi_bygrass/*.tif',recursive=False))

    # SUMMARY
    Imp_func.zonal_summary(list(Gras_manrdepo_wddt.keys()),\
            list(Gras_manrdepo_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_ManrGraz_excr_Crop.xlsx')


    ### Liquid and Solid Manure emissions during housing by livestock
    Liqkeys = [key for key in Hous_emi_wddt.keys() if '_liq' in key]
    Sldkeys = [key for key in Hous_emi_wddt.keys() if '_sld' in key]

    Hous_liqemi_wddt = Imp_func.filter_dict(Hous_emi_wddt,Liqkeys)
    Hous_liqemi_wddt = Imp_func.replace_keys(Hous_liqemi_wddt,Air_pj_path.Ani_name)

    Hous_sldemi_wddt = Imp_func.filter_dict(Hous_emi_wddt,Sldkeys)
    Hous_sldemi_wddt = Imp_func.replace_keys(Hous_sldemi_wddt,Air_pj_path.Ani_name)

    # SUMMARY
    Imp_func.zonal_summary(list(Hous_liqemi_wddt.keys()),\
            list(Hous_liqemi_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_ManrInhous_Liqexcr_Liv.xlsx')

    Imp_func.zonal_summary(list(Hous_sldemi_wddt.keys()),\
            list(Hous_sldemi_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_ManrInhous_Sldexcr_Liv.xlsx')

    
    ###  Liquid and Solid Manure emissions during manure storage by livestock
    Liqkeys2 = [key for key in Stor_emi_wddt.keys() if '_liq' in key]
    Sldkeys2 = [key for key in Stor_emi_wddt.keys() if '_sld' in key]

    Stor_liqemi_wddt = Imp_func.filter_dict(Stor_emi_wddt,Liqkeys2)
    Stor_liqemi_wddt = Imp_func.replace_keys(Stor_liqemi_wddt,Air_pj_path.Ani_name)

    Stor_sldemi_wddt = Imp_func.filter_dict(Stor_emi_wddt,Sldkeys2)
    Stor_sldemi_wddt = Imp_func.replace_keys(Stor_sldemi_wddt,Air_pj_path.Ani_name)


    # SUMMARY
    Imp_func.zonal_summary(list(Stor_liqemi_wddt.keys()),\
            list(Stor_liqemi_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_Liqstor_Liv.xlsx')

    Imp_func.zonal_summary(list(Stor_sldemi_wddt.keys()),\
            list(Stor_sldemi_wddt.values()), \
            Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
            FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/NH3_Sldstor_Liv.xlsx')


    
    ### Liquid and Solid Manure emissions during manure application by livestock and by crop
    #OUTPUT_FILE
    for crop in App_liqemi_crop_wddt:
        App_liqemi_crop_N = Imp_func.aggregate(App_liqemi_crop_wddt[crop])
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Appliq_Emi_bycrop/'+\
            r'MA_'+ crop + '_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326', App_liqemi_crop_N)


    # OUTPUT_DATA
    App_liqemi_cropaggre_wddt = Imp_func.dict_name_path(list(App_liqemi_crop_wddt.keys()),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appliq_Emi_bycrop/MA_*_NH3-N.tif',\
        recursive = False)) # We just inherit the keys from App_liqemi_crop_wddt because not all crops receive manure


    # OUTPUT_FILE
    for crop in App_sldemi_crop_wddt:
        App_sldemi_crop_N = Imp_func.aggregate(App_sldemi_crop_wddt[crop])
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Appsld_Emi_bycrop/'+\
            r'MA_'+ crop +'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',App_sldemi_crop_N)


    # OUTPUT_DATA
    App_sldemi_cropaggre_wddt = Imp_func.dict_name_path(list(App_sldemi_crop_wddt.keys()),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appsld_Emi_bycrop/MA_*_NH3-N.tif',\
            recursive=False))



    # OUTPUT_FILE
    for liv in App_liqemi_livsk_wddt:
        App_liqemi_liv_N = Imp_func.aggregate(App_liqemi_livsk_wddt[liv])
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Appliq_Emi_byliv/'+\
            r'MA_'+ liv + '_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326', App_liqemi_liv_N)


    # OUTPUT_DATA
    App_liqemi_livaggre_wddt = Imp_func.dict_name_path(list(App_liqemi_livsk_wddt.keys()),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appliq_Emi_byliv/MA_*_NH3-N.tif',\
            recursive=False))



    # OUTPUT_FILE
    for liv in App_sldemi_livsk_wddt:
        App_sldemi_liv_N = Imp_func.aggregate(App_sldemi_livsk_wddt[liv])
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{Scenarios_Name}_Appsld_Emi_byliv/'+\
            r'MA_'+ liv +'_NH3-N.tif',Air_pj_path.Exam_crop_reson_wd,\
                'EPSG:4326',App_sldemi_liv_N)


    # OUTPUT_DATA
    App_sldemi_livaggre_wddt = Imp_func.dict_name_path(list((App_sldemi_livsk_wddt.keys())),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_Appsld_Emi_byliv/MA_*_NH3-N.tif',\
            recursive=False))


    # SUMMARY
    App_manr_aggre_wddt = dict(zip(['NH3_LiqMA_Liv','NH3_SldMA_Liv',\
        'NH3_LiqMA_Crop','NH3_SldMA_Crop'],\
        [App_liqemi_livaggre_wddt,App_sldemi_livaggre_wddt,\
            App_liqemi_cropaggre_wddt,App_sldemi_cropaggre_wddt]))


    for manr_stage in App_manr_aggre_wddt:
        Imp_func.zonal_summary(list(App_manr_aggre_wddt[manr_stage].keys()),\
                list(App_manr_aggre_wddt[manr_stage].values()), \
                Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
                FABIO_pj_path.Prj_Gene_output_wd + \
                f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/{manr_stage}.xlsx')


    # SUMMARY
    ## Aggregate all these individual stage emissions to one excel file
    Summary_Single_emi_wddt = Imp_func.dict_name_path(['NH3_Syntfert',\
        'NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
        'NH3_Liqstor_Liv','NH3_Sldstor_Liv',
        'NH3_LiqMA_Liv','NH3_SldMA_Liv',\
        'NH3_LiqMA_Crop','NH3_SldMA_Crop',\
        'NH3_ManrGraz_excr_Liv','NH3_ManrGraz_excr_Crop'],\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Gene_output_wd + \
        f'{Scenarios_Name}_Adj_Emi_for_Consp_allo/*.xlsx',recursive=False))

    Adj_emi_dt = {}

    for f_name in Summary_Single_emi_wddt:
        Adj_emi_dt[f_name] = Imp_func.pd.read_excel(Summary_Single_emi_wddt[f_name],\
            sheet_name='Sheet1')


    with Imp_func.pd.ExcelWriter(FABIO_pj_path.Prj_Gene_output_wd+\
        f'{Scenarios_Name}_Adj_APAMMOFABIO_Emi_check.xlsx',\
        engine='xlsxwriter') as writer:
        # Iterate over the dictionary and write each DataFrame to a sheet
        for sheet_name, df in Adj_emi_dt.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return 


def Shar_Newpath_pkl(Scenarios_Name):
    # Livestock related maps
    # OUTPUT_DATA
    ## Collect manure management maps
    Livstk_manrmana_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
                r'Manure_management(MM)/MM_*_NH3-N.tif',recursive=False))
    
    ## Collect manure application maps
    Livstk_manrapp_wddt = Imp_func.dict_name_path(Air_pj_path.Ani_name,\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_application(MA)/MA_*_NH3-N.tif',recursive=False))
    
    ## Collect manure deposition maps
    Livstk_manrdepo_wddt = Imp_func.dict_name_path(['dair','othcatl','shep','goat'],\
        Imp_func.glob.glob(f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_deposition(MD)/MD_*_NH3-N.tif',recursive=False))
    
   
    Livstk_emi_df = Imp_func.conv_dict2df(Livstk_manrmana_wddt,\
        'Ani_name','Manr_manaEMI')
    Livstk_emi_df = Imp_func.join_dict2df(Livstk_emi_df,\
        Livstk_manrapp_wddt,'Ani_name','Manr_appEMI')
    Livstk_emi_df = Imp_func.join_dict2df(Livstk_emi_df,\
        Livstk_manrdepo_wddt,'Ani_name','Manr_depoEMI')

    ## Crop related maps
    Syn_fertemi_bycrop_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(
            f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Synthetic_fertilizer_use(SF)/*.tif',recursive=False))
    
    Manr_Inputemi_bycrop_wddt = Imp_func.dict_name_path(
        Air_pj_path.MainCpNam,Imp_func.glob.glob(
            f'AMMO_footprint/Data_Shar/{Scenarios_Name}/'+\
            r'Manure_input(MI)/MI_*_NH3-N.tif',recursive=False))
    
    Crop_emi_df = Imp_func.conv_dict2df(Syn_fertemi_bycrop_wddt,\
        'Crop_name','Synt_fertEMI')
    Crop_emi_df = Imp_func.join_dict2df(Crop_emi_df,\
        Manr_Inputemi_bycrop_wddt,'Crop_name','Manr_inputEMI')

    
    ## E vectors for adjusted consumption-side modelling
    Adj_Emi_dict={
        'Livstk_emi_df':Livstk_emi_df,\
        'Crop_emi_df':Crop_emi_df,\
        'E_adj_VecforConsp':FABIO_pj_path.Prj_Gene_output_wd+\
            f'{Scenarios_Name}_Adj_APAMMOFABIO_Emi_check.xlsx'}
    
    return Adj_Emi_dict
    
    
