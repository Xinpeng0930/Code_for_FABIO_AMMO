# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# D3_Delta_Chang_Tot_Reved — change in total emissions (revised)

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_Pj_path

#%%

def Delta_Chang_Rev(Scenarios_Name):
    Tot_EmiScen_dt = Imp_func.open_plk(FABIO_Pj_path.Prj_Pkl_output_wd+\
        r'ScenEmi_s.pkl')
    Total_Emi_with_Mitimeasure_dt = Imp_func.open_plk(FABIO_Pj_path.Prj_Pkl_output_wd+\
        r'Comb_diet_tech_emi.pkl') # from D1
    
    Curr_Total_Emi_wd = Tot_EmiScen_dt['Tot_emi']['CURR']

    ## Scenario based inputs and outputs----------------------------------------------------------------------------------------------------
    if Scenarios_Name in ['EAT','CURR_MTFR']:
        Total_Emi_wd = Tot_EmiScen_dt['Tot_emi'][Scenarios_Name]
      
    elif Scenarios_Name in ['EAT_MTFR']:
        Total_Emi_wd = Total_Emi_with_Mitimeasure_dt[Scenarios_Name]['Tot_emi']
    
    #----------------------------------------------------Processing_module----------------------------------------------------
    Delta_emi_value =  Imp_func.tidy_zero(Total_Emi_wd) - Imp_func.tidy_zero(Curr_Total_Emi_wd)
    
    
    # OUTPUT_FILE
    Imp_func.output_reso_ras_filtered(FABIO_Pj_path.Prj_Rster_output_wd +\
        f'Delta_Chang_Rev/{Scenarios_Name}_Delta_Chang_Emi.tif',\
        Pj_path.Exam_500area_wd,'EPSG:4326',Delta_emi_value)
    
    return

