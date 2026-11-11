# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B7_Relink_CropLivstk_Scen — re-linking of crop and livestock N emissions by scenario

#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path


#%%
def Relink_CropLivstk_N_Emi(Scenario):
    #----------------------------------------------------input_module----------------------------------------------------
    # General inputs ---------------------------------------------------------------------
    ## Get the adjusted chemical fertilizer and manure input N flows
    All_Scen_SyntfertManr_Input_byprod = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd\
        +'Byprod_Adj_Syntfert_ManrInput_s.pkl') #from B6
    
    Livstk_manr_name = Air_pj_path.manrN_name2
    
    
    if Scenario in ['MTFR_EAT']:
        ## get the ratios between applied manure N and applied TAN
        Manr_manachain_dict = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                f'Manr_manachain_CURR_MTFR.pkl')
        App_manr_RatioTAN = Imp_func.conv_df2dict(Manr_manachain_dict['Manr_app_df'],\
            'Ani_manr_type','Orig_appmanr_Ratio_TAN')

        ## collect the emission factors by animal-manure
        ### In-house liquid emission factors
        Hous_Emi_LiqEFs_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name='Liq_manr_MTFREFs')
        ### In-house sld emission factors
        Hous_Emi_SldEFs_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name='Sld_manr_MTFREFs')
        ### Application emission factors
        App_Liqemifac = Hous_Emi_LiqEFs_df.iloc[:,31:37]
        App_Sldemifac = Hous_Emi_SldEFs_df.iloc[:,31:37]
        
        App_Liqemifac.columns = ['pig_liq','dair_liq','othcatl_liq',\
            'shep_liq','goat_liq','potr_liq']
        App_Sldemifac.columns = ['pig_sld','dair_sld','othcatl_sld',\
            'shep_sld','goat_sld','potr_sld']
        App_Emifac = Imp_func.pd.concat([Hous_Emi_LiqEFs_df['Name_abbre'],\
            App_Liqemifac,App_Sldemifac],axis=1)
        App_Emifac_new = App_Emifac[['Name_abbre']+Livstk_manr_name]
        
        ### Grazing emission factors
        Graz_EF_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name='graz_depo_MTFREFs')

    
    elif Scenario in ['EAT', 'EAT_Vegan', 'EAT_Meat']:
        ## get the ratios between applied manure N and applied TAN
        Manr_manachain_dict = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
            f'Manr_manachain_CURR.pkl')
        App_manr_RatioTAN = Imp_func.conv_df2dict(Manr_manachain_dict['Manr_app_df'],\
            'Ani_manr_type','Orig_appmanr_Ratio_TAN')
        
        ## collect the emission factors by animal-manure
        ### In-house liquid emission factors
        Hous_Emi_LiqEFs_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name= 'Liq_manr_ImprvEFs')
        ### In-house sld emission factors
        Hous_Emi_SldEFs_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name='Sld_manr_ImprvEFs')
        ### Application emission factors
        App_Liqemifac = Hous_Emi_LiqEFs_df.iloc[:,31:37]
        App_Sldemifac = Hous_Emi_SldEFs_df.iloc[:,31:37]
        
        App_Liqemifac.columns = ['pig_liq','dair_liq','othcatl_liq',\
            'shep_liq','goat_liq','potr_liq']
        App_Sldemifac.columns = ['pig_sld','dair_sld','othcatl_sld',\
            'shep_sld','goat_sld','potr_sld']
        App_Emifac = Imp_func.pd.concat([Hous_Emi_LiqEFs_df['Name_abbre'],\
            App_Liqemifac,App_Sldemifac],axis=1)
        App_Emifac_new = App_Emifac[['Name_abbre']+Livstk_manr_name]
        
        ### Grazing emission factors
        Graz_EF_df = Imp_func.pd.read_excel(Air_pj_path.Fac_tab_wd,\
            sheet_name= 'graz_depo_ImprvEFs')
        

    # Inputs based on specific scenarios---------------------------------------------------------------------

    ### Manure on agricultural by animal type
    ManrappN_Liq_byLiv_wddt = All_Scen_SyntfertManr_Input_byprod[Scenario]['Manrapp_liq_Liv_byprod']
    # Add prefix to all keys
    suffix1 = "_liq"
    ManrappN_Liq_byLiv_wddt = {key+suffix1 : value for key, value in ManrappN_Liq_byLiv_wddt.items()}
            
    ManrappN_Sld_byLiv_wddt = All_Scen_SyntfertManr_Input_byprod[Scenario]['Manrapp_sld_Liv_byprod']
    suffix2 = "_sld"
    ManrappN_Sld_byLiv_wddt = {key+suffix2 : value for key, value in ManrappN_Sld_byLiv_wddt.items()}
    

    ### Manure deposited on grassland by animal type 
    Animanr_grasdepo_wddt = All_Scen_SyntfertManr_Input_byprod[Scenario]['Depomanr_byprod']
    

    ## provides manure application by specific crops with no consideration of application limits

    ## get manure application by specific crops
    ManrappN_Liq_byProd_wddt =  All_Scen_SyntfertManr_Input_byprod[Scenario]['Manrapp_liq_Crop_byprod']
    ManrappN_Sld_byProd_wddt = All_Scen_SyntfertManr_Input_byprod[Scenario]['Manrapp_sld_Crop_byprod']

    ##provides manure deposition by specific grasses
    Manr_depo_onagri_wddt = All_Scen_SyntfertManr_Input_byprod[Scenario]['Depomanr_Crop_byprod']


    # Outputs based on scenarios---------------------------------------------------------------------
    Fold_path_spc_Liqlivstk_agri_manr = f'Connect_Liqmanr_Nagri_app_realDI_{Scenario}/'
    Fold_path_spc_Sldlivstk_agri_manr = f'Connect_Sldmanr_Nagri_app_realDI_{Scenario}/'
    Fold_path_spc_livstkcropgras_manrdepo = f'Connect_manr_Ngras_depo_realDI_{Scenario}/'
    Fold_path_spc_livstkcrop_manrTAN = f'Connect_manr_CropGras_appTAN_realDI_{Scenario}/' # this folder is under the air_pj_path
    Fold_path_spc_livstkcrop_manrEMI = f'Connect_manr_CropGras_appemi_realDI_{Scenario}/'#includes both applications on cropland and grassland
    Fold_path_spc_livstkcrop_manrdepoEMI = f'Connect_manr_Gras_depoemi_realDI_{Scenario}/'
    Excel_name_spc_livstkcrop_manr = f'Connect_CropAniManrappN_readDI_{Scenario}.xlsx'
    Excel_name_spc_livstkgras_manrdepo =  f'Connect_GrasAniManrdepoN_readDI_{Scenario}.xlsx'
    Excel_name_spc_livstkcrop_manrEMI = f'Emi_Connect_CropGrasAniManrapp_readDI_{Scenario}.xlsx'#includes both applications on cropland and grassland
    Excel_name_spc_livstkcrop_manrdepoEMI = f'Emi_Connect_AniManrdepo_readDI_{Scenario}.xlsx'

 
    #----------------------------------------------------Processing_module----------------------------------------------------
    '''
    All_Liqanimanr_agriapp_value = Imp_func.aggregate(list(ManrappN_Liq_byLiv_wddt.values()))
    All_Sldanimanr_agriapp_value = Imp_func.aggregate(list(ManrappN_Sld_byLiv_wddt.values()))'''
    
    ### Here we get all applied manure based on crop needs, because we want to get the share of each type of 
    ### crop in consumming manure. Then we use these shares to time manure by livestock, so as to connect crops
    ### and livestock. In this way, total manure actuallt depends on manure produced by livestock. This feature is 
    ### embodied in later sections.
    All_Liqanimanr_agriapp_value = Imp_func.aggregate(list(ManrappN_Liq_byProd_wddt.values()))
    All_Sldanimanr_agriapp_value = Imp_func.aggregate(list(ManrappN_Sld_byProd_wddt.values()))
    
    All_animanr_grasdepo_value = Imp_func.aggregate(list(Manr_depo_onagri_wddt.values()))

    ## Connecting animal_manure_type with agricultural land
    ## (use the proportions of individual animal manure to total manure to time total manure on individual crops)
    #OUTPUT_FILE
    '''
    for Ani_manr in ManrappN_Liq_byLiv_wddt:
        for Agri_prod in ManrappN_Liq_byProd_wddt:
            Anim_manr_sys_shar = Imp_func.tidy_zero(ManrappN_Liq_byLiv_wddt[Ani_manr])/All_Liqanimanr_agriapp_value 
            Anim_manr_sys_shar[Imp_func.np.isnan(Anim_manr_sys_shar)]=0
            
            Animanr_con_crop = Imp_func.tidy_zero(ManrappN_Liq_byProd_wddt[Agri_prod]) * Anim_manr_sys_shar
            Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd + \
                Fold_path_spc_Liqlivstk_agri_manr + Agri_prod +'_'+ Ani_manr + '_manrNapp.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_crop)'''

    for Agri_prod in ManrappN_Liq_byProd_wddt:
        for Ani_manr in ManrappN_Liq_byLiv_wddt:
            Agri_prod_manr_shar = Imp_func.tidy_zero(
                ManrappN_Liq_byProd_wddt[Agri_prod])/ All_Liqanimanr_agriapp_value 
            Agri_prod_manr_shar[Imp_func.np.isnan(Agri_prod_manr_shar)]=0
            
            Animanr_con_crop = Imp_func.tidy_zero(ManrappN_Liq_byLiv_wddt[Ani_manr]) * Agri_prod_manr_shar
            Imp_func.output_ras_filtered(Air_pj_path.output_wd + \
                Fold_path_spc_Liqlivstk_agri_manr + Agri_prod +'_'+ Ani_manr + '_manrNapp.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_crop)
        
        
        
    # OUTPUT_DATA
    AgriLiqAniManrapp_N_wdlt = Imp_func.glob.glob(
        Air_pj_path.output_wd + Fold_path_spc_Liqlivstk_agri_manr +'*.tif',recursive=False)

    AgriAniManrappN_name = []
    for path in AgriLiqAniManrapp_N_wdlt:
        filename = path.split('\\')[-1]
        result='_'.join(filename.split('_')[:3])
        AgriAniManrappN_name.append(result)

    Agri_AniLiqManrapp_N_wddt = Imp_func.dict_name_path(AgriAniManrappN_name,AgriLiqAniManrapp_N_wdlt)

    ## connect Sld manure applied on agricultural land
    
    # OUTPUT_FILE
    '''
    for Ani_manr in ManrappN_Sld_byLiv_wddt:
        for Agri_prod in ManrappN_Sld_byProd_wddt:
            Anim_manr_sys_shar = Imp_func.tidy_zero(ManrappN_Sld_byLiv_wddt[Ani_manr])/ All_Sldanimanr_agriapp_value 
            Anim_manr_sys_shar[Imp_func.np.isnan(Anim_manr_sys_shar)]=0
            
            Anisldmanr_con_agri = Imp_func.tidy_zero( ManrappN_Sld_byProd_wddt[Agri_prod]) * Anim_manr_sys_shar
            Imp_func.output_ras_filtered(
                FABIO_pj_path.Prj_Rster_output_wd  + \
                Fold_path_spc_Sldlivstk_agri_manr + Agri_prod +'_'+ Ani_manr +'_manrNapp.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Anisldmanr_con_agri)'''

    for Agri_prod in ManrappN_Sld_byProd_wddt:
        for Ani_manr in ManrappN_Sld_byLiv_wddt:
            Agri_prod_manr_shar = Imp_func.tidy_zero(ManrappN_Sld_byProd_wddt[Agri_prod])/ All_Sldanimanr_agriapp_value 
            Agri_prod_manr_shar[Imp_func.np.isnan(Agri_prod_manr_shar)]=0
            
            Anisldmanr_con_agri = Imp_func.tidy_zero(ManrappN_Sld_byLiv_wddt[Ani_manr]) * Agri_prod_manr_shar
            
            Imp_func.output_ras_filtered(
                Air_pj_path.output_wd + \
                Fold_path_spc_Sldlivstk_agri_manr + Agri_prod +'_'+ Ani_manr +'_manrNapp.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Anisldmanr_con_agri)

    #OUTPUT_DATA
    AgriSldAniManrapp_N_wdlt = Imp_func.glob.glob(Air_pj_path.output_wd + \
        Fold_path_spc_Sldlivstk_agri_manr +'*_manrNapp.tif',\
        recursive=False)

    Agri_AniSldManrappN_name = []
    for path in AgriSldAniManrapp_N_wdlt:
        filename = path.split('\\')[-1]
        result='_'.join(filename.split('_')[:3])
        Agri_AniSldManrappN_name.append(result)

    Agri_AniSldManrapp_N_wddt =Imp_func.dict_name_path(Agri_AniSldManrappN_name,\
        AgriSldAniManrapp_N_wdlt)



    ### connect manure deposited on agricultural land
    # OUTPUT_FILE
    '''
    for Liv in Animanr_grasdepo_wddt:
        for Gras in Manr_depo_onagri_wddt:
            Anim_manr_deposys_shar = Imp_func.tidy_zero(
                Animanr_grasdepo_wddt[Liv])/All_animanr_grasdepo_value 
            Anim_manr_deposys_shar[Imp_func.np.isnan(Anim_manr_deposys_shar)] = 0
            
            Animanr_con_depo = Imp_func.tidy_zero(Manr_depo_onagri_wddt[Gras]) * Anim_manr_deposys_shar
            
            Imp_func.output_ras_filtered(
                FABIO_pj_path.Prj_Rster_output_wd +Fold_path_spc_livstkcropgras_manrdepo + Gras +'_'+Liv+'_manrNdepo.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_depo)'''

    for Gras in Manr_depo_onagri_wddt:
        for Liv in Animanr_grasdepo_wddt:        
            Anim_manr_gras_shar = Imp_func.tidy_zero(
                Manr_depo_onagri_wddt[Gras])/All_animanr_grasdepo_value 
            Anim_manr_gras_shar[Imp_func.np.isnan(Anim_manr_gras_shar)] = 0
            
            Animanr_con_depo = Imp_func.tidy_zero(Animanr_grasdepo_wddt[Liv]) * Anim_manr_gras_shar
            
            Imp_func.output_ras_filtered(
                Air_pj_path.output_wd +Fold_path_spc_livstkcropgras_manrdepo + Gras +'_'+Liv+'_manrNdepo.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_depo)
    
    AniManrdepo_N_wdlt = Imp_func.glob.glob(Air_pj_path.output_wd + \
        Fold_path_spc_livstkcropgras_manrdepo+'*.tif',recursive=False) 

    AniManrdepoN_name = []
    for path in AniManrdepo_N_wdlt:
        filename = path.split('\\')[-1]
        result='_'.join(filename.split('_')[:2])
        AniManrdepoN_name.append(result)

    # OUTPUT_DATA
    AniManrdepo_N_wddt = Imp_func.dict_name_path(AniManrdepoN_name,AniManrdepo_N_wdlt) 


    # OUTPUT_DATA
    ## generate multi-layer lists for manure applied on crops. Outlayer is livestock-manure type.
    Connect_listkcrop_manr_app = {}

    for Ani_manr in Livstk_manr_name:
        Connect_listkcrop_manr_app[Ani_manr]= {}
        Connect_listkcrop_manr_app[Ani_manr] = Imp_func.dict_name_path(
                list(ManrappN_Liq_byProd_wddt.keys()),\
                Imp_func.glob.glob(Air_pj_path.output_wd + \
                    Fold_path_spc_Liqlivstk_agri_manr+'*_'+ Ani_manr + r'_*.tif',\
                    recursive = False)+\
                Imp_func.glob.glob(Air_pj_path.output_wd + \
                    Fold_path_spc_Sldlivstk_agri_manr +'*_'+ Ani_manr + r'_*.tif',\
                    recursive = False))
        
    Connect_listkcrop_manr_app = {k: v for k, v in Connect_listkcrop_manr_app.items() if v != {}}

    ## generate multi-layer lists for manure applied on crops. Outlayer is crop types
    ### don't have to do. Because we already had them from Manr_appli_onagri_wddt 


    ## generate multi-layer lists for manure deposited on agricultural land. Outlayer is livestock-manure type.
    Connect_listkagri_manr_depo = {}
    Graz_livstk_name = ['dair','othcatl','shep','goat']
    for Ani in Graz_livstk_name:
        Connect_listkagri_manr_depo[Ani] = {}
        Connect_listkagri_manr_depo[Ani] = Imp_func.dict_name_path(
            list(Manr_depo_onagri_wddt.keys()),\
            Imp_func.glob.glob(Air_pj_path.output_wd+Fold_path_spc_livstkcropgras_manrdepo +\
                '*_'+ Ani +r'_*.tif',\
                recursive=False))



    ## Export Connected CropAniManr emission maps by livestock emission factors
    ### TAN from manure applied on cropland
    # OUTPUT_FILE
    for Ani_manr in Connect_listkcrop_manr_app:
        for Agri_prod in list(ManrappN_Liq_byProd_wddt.keys()):
            TAN_connectted_Crop_Animanr = Imp_func.tidy_zero(App_manr_RatioTAN[Ani_manr])*\
                Imp_func.tidy_zero(Connect_listkcrop_manr_app[Ani_manr][Agri_prod])
            Imp_func.output_ras_filtered(Air_pj_path.output_wd + Fold_path_spc_livstkcrop_manrTAN +\
                Agri_prod +'_'+ Ani_manr + '_TAN.tif',\
                Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',TAN_connectted_Crop_Animanr)

    ## generate multi-layer lists for manure applied on crops. Outlayer is livestock-manure type.
    Connect_listkcrop_manrTAN_app = {}

    for Ani_manr in Livstk_manr_name:
        Connect_listkcrop_manrTAN_app[Ani_manr]= {}
        
        
        Connect_listkcrop_manrTAN_app[Ani_manr] = Imp_func.dict_name_path(
                list(ManrappN_Liq_byProd_wddt.keys()),\
                Imp_func.glob.glob(Air_pj_path.output_wd + \
                    Fold_path_spc_livstkcrop_manrTAN+r'*_'+ Ani_manr +r'_*.tif',\
                    recursive = False))
        
    Connect_listkcrop_manrTAN_app = {k: v for k, v in Connect_listkcrop_manrTAN_app.items() if v != {}}
    ## generate multi-layer lists for manure TAN applied on crops. 

    for Ani_manr in Connect_listkcrop_manrTAN_app:
        for Agri_prod in list(ManrappN_Liq_byProd_wddt.keys()):
            #OUTPUT_FILE
            Imp_func.cali_fig_filter(
                Connect_listkcrop_manrTAN_app[Ani_manr][Agri_prod],\
                Air_pj_path.Exam_crop_reson_wd,\
                Air_pj_path.EFTA_UK_wd,\
                App_Emifac_new,\
                'FID_1','Name_abbre',\
                App_Emifac_new.columns.tolist()[list(Connect_listkcrop_manrTAN_app.keys()).index(Ani_manr)+1],\
                0.0833333333333333,\
                Air_pj_path.output_wd+\
                    Fold_path_spc_livstkcrop_manrEMI +  Agri_prod +'_'+ Ani_manr + '_Emi.tif')
        
    

    ### emissions from manure deposited on agricultural land
    #OUTPUT_FILE
    for Ani_manr in Connect_listkagri_manr_depo:
        for Agri_prod in Manr_depo_onagri_wddt:
            Imp_func.cali_fig_filter(
                Connect_listkagri_manr_depo[Ani_manr][Agri_prod],\
                Air_pj_path.Exam_crop_reson_wd,Air_pj_path.EFTA_UK_wd, Graz_EF_df, 'FID_1','Name_abbre',\
                Graz_EF_df.columns.tolist()[list(Connect_listkagri_manr_depo.keys()).index(Ani_manr)+11],\
                0.0833333333333333,\
                Air_pj_path.output_wd + Fold_path_spc_livstkcrop_manrdepoEMI +\
                Agri_prod +'_'+ Ani_manr + '_Emi.tif')



    #----------------------------------------------------output_module----------------------------------------------------
    # SUMMARY
    ## manure applied N on crops
    Imp_func.zonal_summary(list(Agri_AniLiqManrapp_N_wddt.keys())+\
        list(Agri_AniSldManrapp_N_wddt.keys()),\
        list(Agri_AniLiqManrapp_N_wddt.values())+\
        list(Agri_AniSldManrapp_N_wddt.values()),\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+ Excel_name_spc_livstkcrop_manr) 



    ## manure deposited N on grassland
    #SUMMARY
    Imp_func.zonal_summary(AniManrdepoN_name,\
        AniManrdepo_N_wdlt,Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+ Excel_name_spc_livstkgras_manrdepo)


    ## Summarize emissions connected CropAniManr
    #SUMMARY
    ### manure application emissions calculated by animal parameters, including both applications on cropland and grassland
    AniManrapp_Emi_wdlt = Imp_func.glob.glob(
        Air_pj_path.output_wd+Fold_path_spc_livstkcrop_manrEMI+'*.tif',\
        recursive=False)

    AniManrapp_Emi_name = []
    for path in AniManrapp_Emi_wdlt:
        filename = path.split('\\')[-1]
        result='_'.join(filename.split('_')[:3])
        AniManrapp_Emi_name.append(result)

    AniManrapp_Emi_wddt = Imp_func.dict_name_path(AniManrapp_Emi_name,AniManrapp_Emi_wdlt) 

    Imp_func.zonal_summary(AniManrapp_Emi_name,AniManrapp_Emi_wdlt,\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+ Excel_name_spc_livstkcrop_manrEMI)


    #SUMMARY
    ### manure deposition emissions calculated by animal parameters
    AniManrdepo_Emi_wdlt = Imp_func.glob.glob(
        Air_pj_path.output_wd + Fold_path_spc_livstkcrop_manrdepoEMI+'*_Emi.tif',\
        recursive=False)

    AniManrdepo_Emi_name = []
    for path in AniManrdepo_Emi_wdlt:
        filename = path.split('\\')[-1]
        result='_'.join(filename.split('_')[:2])
        AniManrdepo_Emi_name.append(result)

    AniManrdepo_Emi_wddt=Imp_func.dict_name_path(AniManrdepo_Emi_name,AniManrdepo_Emi_wdlt)

    Imp_func.zonal_summary(AniManrdepo_Emi_name,AniManrdepo_Emi_wdlt,\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+ Excel_name_spc_livstkcrop_manrdepoEMI)


    ## Summarize important pathways
    Relink_Croplivstk_N_Emi_dict={
        'ManrLiq_agriapp_N_wddt':Agri_AniLiqManrapp_N_wddt,\
        'ManrSld_agriapp_N_wddt':Agri_AniSldManrapp_N_wddt,\
        'Manr_depo_N_wddt':AniManrdepo_N_wddt,\
        'Manr_app_emi_wddt':AniManrapp_Emi_wddt,\
        'Manr_depo_emi_wddt':AniManrdepo_Emi_wddt}


    Imp_func.save_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
                    f'Relink_Croplivstk_N_Emi_{Scenario}.pkl',\
                    Relink_Croplivstk_N_Emi_dict) #equals to I14.pkl
    
    return

