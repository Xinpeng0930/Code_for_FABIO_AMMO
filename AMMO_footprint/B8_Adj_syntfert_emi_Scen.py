# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B8_Adj_syntfert_emi_Scen — adjustment of synthetic-fertilizer emissions by scenario
'''
This script aims to get emissions from adjusted synthetic fertilizer use

Running time is 43s
'''

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
import gc


#%%

def Syntfert_emi_collect(Scenarios_Name):
    # ----------------------------------------------------input_module----------------------------------------------------
    # General inputs ---------------------------------------------------------------------
    ## Adjusted N inputs pickles
    AdjN_scen_dt = Imp_func.open_plk(
        FABIO_pj_path.Prj_Pkl_output_wd+'Byprod_Adj_Syntfert_ManrInput_s.pkl') # from B6


    ## Pathways for crop-specific EFs
    if 'MTFR' in Scenarios_Name:
        _coupl_pkl = 'Emi_syntfert_coupl_CURR_MTFR.pkl'
    else:
        _coupl_pkl = 'Emi_syntfert_coupl_CURR.pkl'

        
    Chemfert_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + _coupl_pkl)
    Chemfert_EF_wddt = Imp_func.conv_df2dict(Chemfert_df,\
        'OSDCropname','Chemfer_EF_map')
    for key in Chemfert_EF_wddt:
        Chemfert_EF_wddt[key] = Chemfert_EF_wddt[key].replace('\\', '/')
        Chemfert_EF_wddt[key] =  Chemfert_EF_wddt[key].replace('../../../Online_work/','F:/')
    
    # Scenario-based inputs ---------------------------------------------------------------------
    SyntfertN_Scen_wddt = AdjN_scen_dt[f'{Scenarios_Name}']['Syntfert_byprod']


    #----------------------------------------------------processing_module----------------------------------------------------
    # OUTPUT_DATA
    ## Get total fertilizer use maps
    Scen_syntfertN_tot = Imp_func.aggregate(list(
        SyntfertN_Scen_wddt.values()))
    
    #OUTPUT_FILE
    Imp_func.output_reso_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+\
        f'Syntfert_Totemi_Scen/SyntFertN_{Scenarios_Name}_EFTA.tif',\
        Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Scen_syntfertN_tot)
    
    
    ## Get ammonia emissions from synthetic fertilizer by product
    for crop in SyntfertN_Scen_wddt:
        N_fert = Imp_func.tidy_zero(SyntfertN_Scen_wddt[crop])
        N_NEF = Imp_func.tidy_zero(Chemfert_EF_wddt[crop])

        Nfert_emi = N_fert * N_NEF
        
        #OUTPUT_FILE
        Imp_func.output_ras_filtered(FABIO_pj_path.Prj_Rster_output_wd+f'Syntfert_emi_{Scenarios_Name}/'+crop+'_fertemiEFTA.tif',\
            Air_pj_path.Exam_crop_reson_wd,'EPSG:4326',Nfert_emi)

    gc.collect()  # release write handles from the loop before reading the same files

    #OUTPUT_DATA
    Vital_feremiN_wddt = Imp_func.dict_name_path(list(SyntfertN_Scen_wddt.keys()),\
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'Syntfert_emi_{Scenarios_Name}/*.tif',recursive=False))


    #----------------------------------------------------output_module----------------------------------------------------
    ## Summarizing data
    # SUMMARY
    Imp_func.zonal_summary(list(Vital_feremiN_wddt.keys()),\
        list(Vital_feremiN_wddt.values()),Air_pj_path.EFTA_UK_wd,32,\
        'sum',-999,\
        FABIO_pj_path.Prj_Gene_output_wd+ \
            f'Fert_use_Emi_byprod_{Scenarios_Name}.xlsx')
    
    return


