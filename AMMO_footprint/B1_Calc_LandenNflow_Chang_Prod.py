# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B1_Calc_LandenNflow_Chang_Prod — land and N-flow changes for the PHD production side


#%%
# Necessary packages
from APSP_proc import Z_fabio_rds_import as FABIO_Impt
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path


#%%
def N_flow_en_Land_Prod_Allfp(Scenarios_Name,N_extension_list):
    ## General inputs-----------------------------------------------------------------------
    ### read important FABIO files
    # OUTPUT_DATA
    fabio_regions = FABIO_Impt.fabio_regions
    fabio_items = FABIO_Impt.reader.items
    fabio_X = FABIO_Impt.reader.X() # X was already set as the swapped matrix 
    fabio_Y = FABIO_Impt.reader.Y()
    fabio_L = FABIO_Impt.reader.L_2021_mass()
    fabio_y_codes = FABIO_Impt.Y_codes

    fabio_nrreg = len(fabio_regions)
    fabio_nrcom = len(fabio_items)

    country_list = list(FABIO_Impt.fabio_regions['iso3c'])
    
    ### Initialize Y early
    Y_newly_adj_df = Imp_func.open_plk(FABIO_path.Prj_Pkl_output_wd + r'Y_newly_adj.pkl')
    Y_newly_adj_all_wddt = Imp_func.conv_df2dict(Y_newly_adj_df,\
        'Scenario','All')
    
    ## Scenario-based inputs and outputs-----------------------------------------------------------------------
    ### Maps scenario name to the Y_newly_adj key; None means no diet adjustment
    _diet_key_map = {
        'CURR_MTFR': None, 'CURR': None,
        'MTFR_EAT': 'EAT','MTFR_EAT_Vegan': 'EAT_Vegan',
        'EAT': 'EAT', 'EAT_Vegan': 'EAT_Vegan',
        'EAT_Meat': 'EAT_Meat'
    }
    diet_key = _diet_key_map[Scenarios_Name]
    Y_alldemand_wd = Y_newly_adj_all_wddt[diet_key] if diet_key else None

    ### Get the N flow data
    _nflow_sheet = 'N_MTFR' if 'MTFR' in Scenarios_Name else 'N_Imprv'
    N_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/N_AMMO.xlsx',\
        sheet_name=_nflow_sheet)
    
    ### The output path for the production-based N flow footprints
    Y_EmiProd_wd = f'./AMMO_footprint/Output/{Scenarios_Name}_Prodside_flow/{Scenarios_Name}_'



    ## Scenario-based pre-processing_module-----------------------------------------------------------------------
    # OUTPUT_DATA
    if Scenarios_Name in ['CURR_MTFR','CURR']:
        for extension in N_extension_list:
            FABIO_func.Output_ProdFP_byExten(
                regions=fabio_regions,\
                items=fabio_items,\
                nrcom=fabio_nrcom,\
                nrreg=fabio_nrreg,\
                COUNTY_LIST=country_list,\
                EXTENSION=extension,\
                CONSUMPTION="Total",\
                E = N_new, X=fabio_X,\
                L=fabio_L,Y=fabio_Y,Y_CODE=fabio_y_codes,\
                output_path= Y_EmiProd_wd+extension+'.xlsx',\
                parallel_cores = 4)
                # just keep Y as fabioY 
        

    else:
        # Get the adjusted Y_all

        ## get all new Y_demand
        Y_alldemand_df = Imp_func.pd.read_excel(Y_alldemand_wd,index_col=0)
        Y_alldemand_num_df = Y_alldemand_df.iloc[:,2:]

        # calculate Production based N flows
        Y_new = Y_alldemand_num_df
        
        # Switch the y_codes to the new y_codes, so that we can match the correct Y_country and execute the calculation
        fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
        fabio_y_codes_new['continent'] = fabio_y_codes_new['iso3c'].map(dict(zip(fabio_regions['iso3c'], \
            fabio_regions['continent'])))
        fabio_y_codes_new['fd'] = 'Total'
        
        for extension in N_extension_list:
            FABIO_func.Output_ProdFP_byExten(
                regions=fabio_regions,\
                items=fabio_items,\
                nrcom=fabio_nrcom,\
                nrreg=fabio_nrreg,\
                COUNTY_LIST=country_list,\
                EXTENSION=extension,\
                CONSUMPTION="Total",\
                E = N_new, X=fabio_X, \
                L=fabio_L,Y=Y_new,\
                Y_CODE=fabio_y_codes_new,\
                output_path= Y_EmiProd_wd+extension+'.xlsx',\
                parallel_cores = 4)

    return

