# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B4_Allflow_en_SyntfertN_bala_ori — synthetic-fertilizer and manure N balance
'''
This script aims to get all N flows and required chemical fertilizer 

Total running time is 110s

'''
#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path
import gc


#%%
def Syntfert_bala(Scenarios_Name):
    # ----------------------------------------------------input_module----------------------------------------------------
    # General inputs-------------------------------------------
    ## N uptake data
    Nuptake_natuN_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
        'Curr_Nuptake_flows.pkl')
    Nuptake_wddt = Imp_func.conv_df2dict(Nuptake_natuN_df,\
        'Crops', 'N_uptake')

    ## BNF data
    BNF_wddt = Imp_func.conv_df2dict(Nuptake_natuN_df,\
        'Crops', 'BNF')
    BNF_wddt = Imp_func.dict_del_nan(BNF_wddt) 

    ## Deposition data
    Depo_wddt = Imp_func.conv_df2dict(Nuptake_natuN_df, 'Crops', 'Depo')

    ## NUE data
    NUE_df=Imp_func.pd.read_excel(FABIO_pj_path.Prj_Gene_output_wd+r'NUE_FABIO_APAMMO.xlsx',\
        sheet_name='Sheet1',index_col=0)

    NUE_reverse_df = 1 / NUE_df.iloc[:,2:]
    NUE_reverse_df_left = NUE_reverse_df.iloc[:,:3]
    NUE_reverse_df_left.columns = Air_pj_path.MainCpNam[:3]

    NUE_reverse_df_right = NUE_reverse_df.iloc[:,2:]
    NUE_reverse_df_right.columns = Air_pj_path.MainCpNam[3:]

    NUE_reverse_new_df = Imp_func.pd.concat([NUE_reverse_df_left,NUE_reverse_df_right],\
        axis=1)
    NUE_reverse_new_df = NUE_reverse_new_df.replace([Imp_func.np.inf, -Imp_func.np.inf], 0)
    NUE_reverse_new_df = NUE_reverse_new_df.fillna(0)

    NUE_reverse_new2_df = Imp_func.pd.concat([NUE_df.iloc[:,:2],NUE_reverse_new_df],\
        axis=1)

    ## Scenario-based inputs-------------------------------------
    Nflow_fac_wd = FABIO_pj_path.Prj_Gene_output_wd +\
        f'{Scenarios_Name}_Highreso_Nflow_califac_check.xlsx'#from B2
        
    Cropfac_df = Imp_func.pd.read_excel(Nflow_fac_wd,\
        sheet_name = 'N_coupl_Syntfert')


    ### the calibration factors for depostion data
    if Scenarios_Name == 'EAT':
        Depofac_df = Cropfac_df.iloc[:,1:] * 0.52
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + 'EAT_Nflow_byProdStage.pkl')

        
    elif Scenarios_Name == 'EAT_Meat':
        Depofac_df = Cropfac_df.iloc[:,1:] * 0.73
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl')
        
    elif Scenarios_Name == 'MTFR_EAT':
        Depofac_df = Cropfac_df.iloc[:,1:] * 0.5
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + 'MTFR_EAT_Nflow_byProdStage.pkl')

    elif Scenarios_Name == 'EAT':
        Depofac_df = Cropfac_df.iloc[:,1:] * 0.56 # need to base on the theory emissions calculated by the FABIO model
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl')
    
    elif Scenarios_Name == 'EAT_Vegan':
        Depofac_df = Cropfac_df.iloc[:, 1:] * 0.40 # need to base on the theory emissions calculated by the FABIO model
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl')
    
    elif Scenarios_Name == 'EAT_Meat':
        Depofac_df = Cropfac_df.iloc[:, 1:] * 0.68 # need to base on the theory emissions calculated by the FABIO model
        Depofac_new_df = Imp_func.pd.concat([Cropfac_df.iloc[:,:1],Depofac_df],axis=1)
        Nflow_input_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl')
    
    
    # ----------------------------------------------------processing_module----------------------------------------------------
    ## Calibrate the BNF maps
    # OUTPUT_FILE
    for Prod in list(BNF_wddt.keys()):
        Imp_func.cali_fig_filter(BNF_wddt[Prod],\
            Air_pj_path.Exam_crop_reson_wd, \
            Air_pj_path.EFTA_UK_wd, Cropfac_df, 'FID_1', 'Country', \
            Cropfac_df.columns.tolist()[list(BNF_wddt.keys()).index(Prod) + 1], \
            # must ensure the same order in the two lists
            0.0833333333333333,\
            FABIO_pj_path.Prj_Rster_output_wd +\
            f'BNF_{Scenarios_Name}_byprod/'+Prod+'_BNF.tif')

    BNF_Scenario_wddt =  Imp_func.dict_name_path(BNF_wddt.keys(),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'BNF_{Scenarios_Name}_byprod/*_BNF.tif',\
            recursive=False))

    ## Calibrate the depostion maps
    for Prod in list(Depo_wddt.keys()):
        Imp_func.cali_fig_filter(Depo_wddt[Prod],\
            Air_pj_path.Exam_crop_reson_wd, \
            Air_pj_path.EFTA_UK_wd, Depofac_new_df , 'FID_1', 'Country', \
            Depofac_new_df.columns.tolist()[list(Depo_wddt.keys()).index(Prod) + 1], \
            # must ensure the same order in the two lists
            0.0833333333333333, FABIO_pj_path.Prj_Rster_output_wd +\
            f'Depo_{Scenarios_Name}_byprod/'+Prod+'_depo.tif')

    Depo_Scenario_wddt = Imp_func.dict_name_path(list(Depo_wddt.keys()),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'Depo_{Scenarios_Name}_byprod/*_depo.tif',\
            recursive=False))

    ## Calibrate the N uptakes
    # OUTPUT_FILE
    for Prod in list(Nuptake_wddt.keys()):
        Imp_func.cali_fig_filter(Nuptake_wddt[Prod],\
            Air_pj_path.Exam_crop_reson_wd, \
            Air_pj_path.EFTA_UK_wd,\
            Cropfac_df , 'FID_1', 'Country', \
            Cropfac_df.columns.tolist()[list(Nuptake_wddt.keys()).index(Prod) + 1], \
            # must ensure the same order in the two lists
            0.0833333333333333, \
            FABIO_pj_path.Prj_Rster_output_wd + f'Nuptake_{Scenarios_Name}_byprod/'+Prod+'_Nuptake.tif')

    ## Get the N required for crops
    # OUTPUT_DATA
    N_uptake_Scenario_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + f'Nuptake_{Scenarios_Name}_byprod/*.tif',\
            recursive=False))

    # OUTPUT_INTE_FILE
    Imp_func.zonal_summary(list(N_uptake_Scenario_wddt.keys()),\
        list(N_uptake_Scenario_wddt.values()),Air_pj_path.EFTA_UK_wd,\
        32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+f'Crop_UptakeN_{Scenarios_Name}_Grid_Chek.xlsx')
    
    
    for Prod in list(N_uptake_Scenario_wddt.keys()):
        Imp_func.cali_fig_filter(N_uptake_Scenario_wddt[Prod],\
            Air_pj_path.Exam_crop_reson_wd, \
            Air_pj_path.EFTA_UK_wd,NUE_reverse_new2_df, 'FID_1', 'Country_abbre', \
            NUE_reverse_new2_df.columns.tolist()[list(N_uptake_Scenario_wddt.keys()).index(Prod) + 2], \
            # must ensure the same order in the two lists
            0.0833333333333333, FABIO_pj_path.Prj_Rster_output_wd +\
            f'N_require_{Scenarios_Name}_byprod/'+Prod+'_Nrequire.tif')

    ### Check crop N requirements
    # OUTPUT_INTE_FILE
    N_requirement_Scenario_wddt = Imp_func.dict_name_path(Air_pj_path.MainCpNam,\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'N_require_{Scenarios_Name}_byprod/*_Nrequire.tif'))

    Imp_func.zonal_summary(list(N_requirement_Scenario_wddt.keys()),\
        list(N_requirement_Scenario_wddt.values()),Air_pj_path.EFTA_UK_wd,\
        32,'sum',-999,FABIO_pj_path.Prj_Gene_output_wd+f'Crop_RequireN_{Scenarios_Name}_Grid_Chek.xlsx')
    # we past the test
    
    ### Dataframe
    N_Natuflows_Scenario_df = Imp_func.conv_dict2df(N_uptake_Scenario_wddt,'Crop_names','N_uptake')
    N_Natuflows_Scenario_df =  Imp_func.join_dict2df(N_Natuflows_Scenario_df,N_requirement_Scenario_wddt,\
        'Crop_names','N_requir')
    N_Natuflows_Scenario_df = Imp_func.join_dict2df(N_Natuflows_Scenario_df,BNF_Scenario_wddt,\
        'Crop_names','BNF')
    N_Natuflows_Scenario_df = Imp_func.join_dict2df(N_Natuflows_Scenario_df,Depo_Scenario_wddt,\
        'Crop_names', 'DepoN')

    ### Get the synthetic fertilizer balance
    #### Get the total N requirement
    TotN_require_array =  Imp_func.aggregate(list(N_requirement_Scenario_wddt.values())) 
    
    TotN_require_manr_array = TotN_require_array * 0.9
    
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/TotN_requr.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',TotN_require_array)
    
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/TotN_requr_consider_manr.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', TotN_require_manr_array)
    
    #### Get the manure inputs 
    Manr_input_array = Imp_func.tidy_zero(Nflow_input_dt ['Aggregated']['ManrApp'])\
        + Imp_func.tidy_zero(Nflow_input_dt ['Aggregated']['ManrDepo'])
    
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/Manr_input_aggr.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', Manr_input_array)

    #### Get the BNF inputs
    BNF_input_array = Imp_func.aggregate(list(BNF_Scenario_wddt.values()))
    
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/BNF_aggr.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', BNF_input_array)

    #### Get the deposition input
    Depo_input_array =  Imp_func.aggregate(list(Depo_Scenario_wddt.values()))
    
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/Depo_aggr.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', Depo_input_array)


    #### Get the original Syntfert balance considering synthetic fertilizer at least 10%
    Ori_Syntbala_array = \
        TotN_require_manr_array  - Manr_input_array - BNF_input_array - Depo_input_array
    
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/Orig_SF_bala.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Ori_Syntbala_array)
    
    #### Get the second Syntfert balance which is really for synthetic fertilizer
    Ori_Syntbala2_array = \
        TotN_require_array - Manr_input_array - BNF_input_array - Depo_input_array
    
    # OUTPUT_FILE
    Imp_func.output_reso_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/Orig_SF_bala2.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Ori_Syntbala2_array)
    
    
    # Release rasterio file handles from previous writes before reading
    gc.collect()

    # OUTPUT_FILE
    Imp_func.zonal_summary(['Fert_bala'],[FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/Orig_SF_bala.tif'],\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+f'Orig_SF_bala_{Scenarios_Name}.xlsx')
    
    
    # SUMMARY
    Aggregated_NatuNflow_wddt = Imp_func.dict_name_path(['TotN_requr','TotN_requr_consider_manr',\
        'Manr_input','BNF','Depo','Orig_SF_bala','Orig_SF_bala2'],\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd+\
        f'{Scenarios_Name}_Aggr_Natu_Nflow/*.tif'))
    
    NatuNflow_pkl_wddt = {'Detailed_NatuNflow':N_Natuflows_Scenario_df,\
        'Aggregated_NatuNflow':Aggregated_NatuNflow_wddt}
    
    return NatuNflow_pkl_wddt


# %%
