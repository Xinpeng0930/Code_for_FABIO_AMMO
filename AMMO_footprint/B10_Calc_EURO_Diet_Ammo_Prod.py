# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B10_Calc_EURO_Diet_Ammo_Prod — FABIO production-side emissions for the diets
'''
This manuscript aims to get footprints in 
each scenarios

This script can run automatically and the running time is about 1 hours for one scenario.

'''

#%%
# Necessary packages
from APSP_proc import Z_fabio_rds_import as FABIO_Impt
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path


#%%

def Calc_EURO_Y_Prodfp(Scenarios_Name):
    #----------------------------------------------------input_module----------------------------------------------------
    ## General inputs-----------------------------------------------------------------------
    ### read important FABIO files
    # OUTPUT_DATA
    fabio_regions = FABIO_Impt.fabio_regions
    fabio_items = FABIO_Impt.reader.items

    fabio_X = FABIO_Impt.reader.X()
    fabio_Y = FABIO_Impt.reader.Y()
    fabio_L = FABIO_Impt.reader.L_2021_mass()

    fabio_y_codes = FABIO_Impt.Y_codes
    fabio_year = "2021"

    fabio_nrreg = len(fabio_regions)
    fabio_nrcom = len(fabio_items)

    country_list   = list(FABIO_Impt.fabio_regions['iso3c'])
    extension_list = FABIO_path.extension_list[:-1]  # exclude Manr_grazcrop_emi (unused)

    ## Scenario-based inputs-----------------------------------------------------------------------
    Y_newly_adj_df = Imp_func.open_plk(FABIO_path.Prj_Pkl_output_wd + r'Y_newly_adj.pkl')
    Y_newly_adj_all_wddt = Imp_func.conv_df2dict(Y_newly_adj_df,\
        'Scenario','All')
    
    emi_base  = './AMMO_footprint/Output/'
    e_file    = './AMMO_footprint/Input/E_AMMO.xlsx'

    
    # Keys per scenario:
    #   diet_file    – path to adjusted Y demand Excel (None = use current FABIO Y)
    #   emi_prod_pfx – output path prefix for production-side footprint files
    #   E_sheet      – sheet name in E_AMMO.xlsx to load
    scenario_config = {
        'CURR_MTFR': {
            'diet_file':    None,
            'emi_prod_pfx': emi_base + f'{Scenarios_Name}_Emi_Prodside/fp_CURR_MTFR_',
            'E_sheet':      'E_MTFR',
        },
        'MTFR_EAT': {
            'diet_file':    Y_newly_adj_all_wddt['EAT'],
            'emi_prod_pfx': emi_base + f'{Scenarios_Name}_Emi_Prodside/fp_MTFR_EAT_',
            'E_sheet':      'E_MTFR',
        },
        'EAT_Vegan': {
            'diet_file':    Y_newly_adj_all_wddt['EAT_Vegan'],
            'emi_prod_pfx': emi_base + f'{Scenarios_Name}_Emi_Prodside/fp_Vegan_',
            'E_sheet':      'E_MTFR',
        },
        'CURR': {
            'diet_file':    None,
            'emi_prod_pfx': emi_base + 'fp_CURR_Prodside/fp_CURR_',
            'E_sheet':      'E_new_Imprv',
        },
        'EAT': {
            'diet_file':    Y_newly_adj_all_wddt['EAT'],
            'emi_prod_pfx': emi_base + 'fp_EAT_Prodside/fp_EAT_',
            'E_sheet':      'E_new_Imprv',
        },
        'EAT_Meat': {
            'diet_file':    Y_newly_adj_all_wddt['EAT_Meat'],
            'emi_prod_pfx': emi_base + 'fp_EAT_Meat_Prodside/fp_EAT_Meat_',
            'E_sheet':      'E_new_Imprv',
        },
        'EAT_Vegan': {
            'diet_file':    Y_newly_adj_all_wddt['EAT_Vegan'],
            'emi_prod_pfx': emi_base + 'fp_EAT_Vegan_Prodside/fp_EAT_Vegan_',
            'E_sheet':      'E_new_Imprv',
        },

    }

    cfg            = scenario_config[Scenarios_Name]
    Y_alldemand_wd = cfg['diet_file']           # None for current-diet scenarios
    Y_EmiProd_wd   = cfg['emi_prod_pfx']
    E_new          = Imp_func.pd.read_excel(e_file, sheet_name=cfg['E_sheet'])
    


    #----------------------------------------------------processing_module----------------------------------------------------
    # OUTPUT_DATA
    if Scenarios_Name in ['CURR_MTFR','CURR']:
        
        ### (Get the footprint from the production perspective; because here is the 
        # calculation for the current scenario, we just keep Y as fabio_Y)
        #OUTPUT_FILE
        for extension in extension_list:
            FABIO_func.Output_ProdFP_byExten(
                regions=fabio_regions,\
                items=fabio_items,\
                nrcom=fabio_nrcom,\
                nrreg=fabio_nrreg,\
                COUNTY_LIST= country_list,\
                EXTENSION=extension,\
                CONSUMPTION="Total",\
                E = E_new, X=fabio_X,\
                L=fabio_L,Y=fabio_Y,\
                Y_CODE=fabio_y_codes,\
                output_path= Y_EmiProd_wd + f"{extension}.xlsx",\
                parallel_cores = 4)
        #just keep Y as fbioY 

    else:
        # Get the adjusted Y_all
        Y_alldemand_df = Imp_func.pd.read_excel(Y_alldemand_wd,index_col=0)
        Y_alldemand_num_df = Y_alldemand_df.iloc[:,2:]
        
        # calculate Production based emissions
        Y_new = Y_alldemand_num_df 
        
        # Switch the y_codes to the new y_codes, so that we can match the correct Y_country and execute the calculation
        fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
        fabio_y_codes_new['continent'] = fabio_y_codes_new['iso3c'].map(dict(zip(fabio_regions['iso3c'], \
            fabio_regions['continent'])))
        fabio_y_codes_new['fd'] = 'Total'
        
        for extension in extension_list:
            FABIO_func.Output_ProdFP_byExten(
                regions=fabio_regions,\
                items=fabio_items,\
                nrcom=fabio_nrcom,\
                nrreg=fabio_nrreg,\
                COUNTY_LIST=country_list,\
                EXTENSION=extension,\
                CONSUMPTION="Total",\
                E = E_new, X=fabio_X, L=fabio_L,Y=Y_new,Y_CODE=fabio_y_codes_new,\
                output_path= Y_EmiProd_wd+ fabio_year+ '_'+extension+'_total_mass.xlsx',\
                parallel_cores = 4)

    return

# %%
