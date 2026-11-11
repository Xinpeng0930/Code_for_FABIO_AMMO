# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B5_Adj_ManrinputN — adjustment of manure input N

'''
Running time is 50s
'''

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
import gc


#%%
def Adj_ManrSyntfert(Scenario_Name):
    # ----------------------------------------------------input_module----------------------------------------------------
    # General inputs-------------------------------------------
    Para_wd = FABIO_pj_path.Prj_input_wd + 'Processing_plot_new.xlsx'
    ## Standard head for EU and EFTA countries
    Standard_EUEFTA_head = Imp_func.pd.read_excel(Para_wd, \
                                                sheet_name='Country_name')

    # Scenario-based inputs-------------------------------------------
    ## SyntfertN balance data
    NatuN_flow_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+'Natu_Nflows_s.pkl')
    NatuN_flow_Scen_dt = NatuN_flow_dt[Scenario_Name]

    Syntfert_Orig_bala_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['Orig_SF_bala']
    Syntfert_Orig_bala2_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['Orig_SF_bala2']

    with Imp_func.rasterio.open(Syntfert_Orig_bala_wd) as _ds:
        Syntfert_bala_array = _ds.read(1) #for getting manure
    with Imp_func.rasterio.open(Syntfert_Orig_bala2_wd) as _ds:
        Syntfert_bala2_array = _ds.read(1) #for getting syntfert


    ## Maximun manure data
    RequirN_ConsidManr_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['TotN_requr_consider_manr']
    RequirN_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['TotN_requr']

    with Imp_func.rasterio.open(RequirN_ConsidManr_wd) as _ds:
        RequirN_ConsidManr_array = _ds.read(1) #for maximum manure data
    with Imp_func.rasterio.open(RequirN_wd) as _ds:
        RequirN_array = _ds.read(1)

    ## Original Manure input data(under scenario)
    Manr_input_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['Manr_input']
    with Imp_func.rasterio.open(Manr_input_wd) as _ds:
        Manr_input_ori_array = _ds.read(1)

    ## Origigal BNF inputs
    BNF_input_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['BNF']
    with Imp_func.rasterio.open(BNF_input_wd) as _ds:
        BNF_array = _ds.read(1)

    ## Original depostion inputs
    Depo_input_wd = NatuN_flow_Scen_dt['Aggregated_NatuNflow']['Depo']
    with Imp_func.rasterio.open(Depo_input_wd) as _ds:
        Depo_array = _ds.read(1)


    ## Synthetic fertilizer use data
    if Scenario_Name == 'EAT':
        Nflow_byProdStage_dt = Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + 'EAT_Nflow_byProdStage.pkl' ) #from C11_D
        
    elif Scenario_Name == 'EAT_Meat':
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenario_Name}_Nflow_byProdStage.pkl')
        
    elif Scenario_Name == 'MTFR_EAT':
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + 'MTFR_EAT_Nflow_byProdStage.pkl')

    elif Scenario_Name in ['EAT', 'EAT_Vegan', 'EAT_Meat']:
        Nflow_byProdStage_dt =  Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenario_Name}_Nflow_byProdStage.pkl')
    

    Syntfert_N_flow_Scen_wd = Nflow_byProdStage_dt['Aggregated']['Syntfert']
    with Imp_func.rasterio.open(Syntfert_N_flow_Scen_wd) as _ds:
        Syntfert_N_flow_Scen_array = _ds.read(1)

    # ----------------------------------------------------processing_module----------------------------------------------------
    ## Masks for synthetic fertilizer balance
    Mask_nega_array = Imp_func.np.where(
        ((Syntfert_bala_array != -999) & (Syntfert_bala_array < 0)),
        1,0)

    Mask_posi_array = Imp_func.np.where(
        ((Syntfert_bala_array >= 0)),1,0)


    ### Get the change ratios at the balance-positive areas 
    Delta_negative = Mask_nega_array * Syntfert_bala_array #extra manure
    
    Posi_syntfert_input = Mask_posi_array * Syntfert_bala_array # Case2: allowed N inputs considering at least 10% of synthetic fertilizer
    # Posi_syntfert_input = Mask_posi_array * Syntfert_bala2_array # Case1: all allowed synthetic fertilizer
    


    #OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Delta_nega_manr.tif",\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326', Delta_negative) 
    # the manure to be reduced at the exceeding area

    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Ori_PosiSFneed.tif",\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Posi_syntfert_input) 
    # the synthetic fertilizer to be changed at the positive-balance cells

    gc.collect()  # release write handles before reading the same files
    #OUTPUT_FILE
    Imp_func.zonal_summary(['Delta_redu_manr','Ori_Syntfert_input'],\
        [FABIO_pj_path.Prj_Rster_output_wd+f"{Scenario_Name}_Adj_Nflows/Delta_nega_manr.tif",\
        FABIO_pj_path.Prj_Rster_output_wd+f"{Scenario_Name}_Adj_Nflows/Ori_PosiSFneed.tif"],\
        Air_pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+f'{Scenario_Name}_manradj.xlsx')
    # Check the if delta_redu_manr can be absored by areas with N requirements.We found every country can make this in every scenario. 

    #OUTPUT_DATA
    Ratio_df = Imp_func.pd.read_excel(FABIO_pj_path.Prj_Gene_output_wd+\
        f'{Scenario_Name}_manradj.xlsx',\
        sheet_name='Sheet1')

    Ratio_new_df = Imp_func.pd.concat([Standard_EUEFTA_head['Name_abbre'],Ratio_df],\
        axis=1)

    Ratio_new_df['Scale_ratio_for_Syntfert'] = 1 + (Ratio_new_df['Delta_redu_manr'] / Ratio_new_df['Ori_Syntfert_input'])
    # the synthetic fertilizer to be reduced to absorb the extra manure
    
    Ratio_new_df['Scale_ratio_for_Manr'] = -(Ratio_new_df['Delta_redu_manr'] / Ratio_new_df['Ori_Syntfert_input'])
    # the manure to be transferred to the N required places.
    
    Ratio_new_df = Ratio_new_df.fillna(0)

    for col in ['Scale_ratio_for_Syntfert','Scale_ratio_for_Manr']:
        Ratio_new_df[col] = Imp_func.np.where(Ratio_new_df[col] < 0, 0,\
            Imp_func.np.where(Ratio_new_df[col] > 1, 1, Ratio_new_df[col]))
    ### make sure there is no overcapacity manure N added to N required areas

    ### Get the delta manure application
    # OUTPUT_FILE
    Imp_func.cali_fig_filter(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Ori_PosiSFneed.tif",\
        Air_pj_path.Exam_crop_reson_wd, \
        Air_pj_path.EFTA_UK_wd, Ratio_new_df, 'FID_1', 'Name_abbre', \
        'Scale_ratio_for_Manr', \
        # must ensure the same order in the two lists
        0.0833333333333333, FABIO_pj_path.Prj_Rster_output_wd +\
        f'N_require_{Scenario_Name}_byprod/Delta_Manr_trans_Orig.tif')


    ## Target manure input
    Targ_Manr_input_nega = Mask_nega_array * (RequirN_ConsidManr_array - BNF_array - Depo_array)

    gc.collect()  # release write handle from cali_fig_filter before reading
    with Imp_func.rasterio.open(FABIO_pj_path.Prj_Rster_output_wd \
            + f'N_require_{Scenario_Name}_byprod/Delta_Manr_trans_Orig.tif') as _ds:
        Targ_Manr_input_nega_trans_delta = _ds.read(1) * Mask_posi_array

    Targ_Manr_posi_ori = Manr_input_ori_array *  Mask_posi_array 

    Targ_Manr_input = Targ_Manr_input_nega + Targ_Manr_input_nega_trans_delta + Targ_Manr_posi_ori 

    # OUTPUT_Targ_Manr_input_nega_trans_delta FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Target_manrN.tif",\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Targ_Manr_input)
    
    ### For negative grids, we have manure input considering at least 10% of synthetic fertilizer; for
    ### positive grids, we have the original positive manure input plus the extra manure transferred from
    ### the negative grids.


    ## Target syntfert input
    Targ_Syntfert_input_nega = (RequirN_array - RequirN_ConsidManr_array) * Mask_nega_array

    gc.collect()  # release write handle from output_ras_filtered before reading Ori_PosiSFneed.tif
    # OUTPUT_FILE
    Imp_func.cali_fig_filter(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Ori_PosiSFneed.tif",\
        Air_pj_path.Exam_crop_reson_wd, \
        Air_pj_path.EFTA_UK_wd, Ratio_new_df, 'FID_1', 'Name_abbre', \
        'Scale_ratio_for_Syntfert', \
        # must ensure the same order in the two lists
        0.0833333333333333, FABIO_pj_path.Prj_Rster_output_wd +\
        f'N_require_{Scenario_Name}_byprod/Syntfert_adj_corr_deltamanrapp.tif')

    gc.collect()  # release write handle from cali_fig_filter before reading
    with Imp_func.rasterio.open(FABIO_pj_path.Prj_Rster_output_wd +\
        f'N_require_{Scenario_Name}_byprod/Syntfert_adj_corr_deltamanrapp.tif') as ds:
        Targ_Syntfert_input_posi = ds.read(1) * Mask_posi_array

    # Targ_Syntfert = Targ_Syntfert_input_nega + Targ_Syntfert_input_posi 
    Targ_Syntfert = Targ_Syntfert_input_nega + Targ_Syntfert_input_posi + (RequirN_array - RequirN_ConsidManr_array) * Mask_posi_array
    
    ### For negative grids, we get the least fertilizer input, namely 10% of the required N. For positive grids,
    ### we need to reduce those extra manure inputs.

    # OUTPUT_FILE
    Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Target_syntfertN.tif",\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Targ_Syntfert) #Targeted synthetic fertilizer


    ## Check manure and synthetic fertilizer inputs before and after the adjustment
    gc.collect()  # release write handles before reading Target_syntfertN.tif
    # OUTPUT_FILE
    Imp_func.zonal_summary(['Syntfert_before','Manrinput_before',\
        'Syntfert_after','Manrinput_after','N_require','BNF','Depo'],\
        [Syntfert_N_flow_Scen_wd,Manr_input_wd,FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Target_syntfertN.tif",FABIO_pj_path.Prj_Rster_output_wd+\
        f"{Scenario_Name}_Adj_Nflows/Target_manrN.tif",RequirN_wd,\
        BNF_input_wd,Depo_input_wd],Air_pj_path.EFTA_UK_wd,\
            32,'sum',-999,FABIO_pj_path.Prj_Gene_output_wd + f'{Scenario_Name}_Syntfert_Manrinput.xlsx')

    return


# %%
