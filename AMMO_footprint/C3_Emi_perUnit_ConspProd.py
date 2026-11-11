# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# C3_Emi_perUnit_ConspProd — emission intensities per unit of consumption and production

#%%
# Necessary packages
from APSP_proc import Z_fabio_rds_import as FABIO_Impt
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path



#%%

def Emi_perUnit(Footprint_driver):
    # General inputs---------------------------------------------------------------------------------------------------------
    ## Get European countries
    fabio_regions = FABIO_Impt.fabio_regions
    EURO_region = FABIO_Impt.fabio_regions[FABIO_Impt.fabio_regions['EUEFTA']==True]['iso3c']
    EURO_country_ISO_list =  EURO_region.tolist()


    # Scenario-based inputs---------------------------------------------------------------------------------------------------------

    if Footprint_driver == "Total":
        ## Inputs for emissions from the consumption perspective
        ConspEmi_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+'ConspEmi.pkl') # this is from C2
        Curr_ConspEmi_wddt = Imp_func.conv_df2dict(ConspEmi_dt['Stage_spec_DetailenSummary'],\
            'Stage','Curr_detail')

        Useful_stage_names = Imp_func.del_elemt_list(list(Curr_ConspEmi_wddt.keys()),\
            [5,6])
        
        ## Get Euro and Non_Euro Y data (the unit of Y data is ton)
        Euro_NonEuro_Y_wd = FABIO_pj_path.Prj_Gene_output_wd + r'Y_regional_demand_2021ver.xlsx'

        
        ## the pathway for emission per unit
        Unit_Emi_wd = FABIO_pj_path.Prj_Gene_output_wd+r'Emi_perUnit_21Ver.xlsx'
        
    elif Footprint_driver == "Food":
        ## Inputs for emissions from the food consumption perspective
        ConspEmi_dt = Imp_func.open_plk(
            FABIO_pj_path.Prj_Pkl_output_wd+'FoodConspEmi.pkl')
        Curr_ConspEmi_wddt=Imp_func.conv_df2dict(ConspEmi_dt['Stage_spec_DetailenSummary'],\
            'Stage','Curr_detail')
        
        Useful_stage_names = Imp_func.del_elemt_list(list(Curr_ConspEmi_wddt.keys()),\
            [5,6,10])

        Euro_NonEuro_Y_wd = FABIO_pj_path.Prj_Gene_output_wd + f'Y_regional_Food_demand_2021ver.xlsx'

        
        ## the pathway for emission per unit
        Unit_Emi_wd = FABIO_pj_path.Prj_Gene_output_wd+'Emi_perUnit_food_21Ver.xlsx'


    #----------------------------------------------------processing_module------------------------------------------------
    ### Get emission data
    # OUTPUT_DATA
    Emi_EURO_byProd_dt = {}

    for i in Useful_stage_names:
        # Read the consumption-based emissions at the level one
        Curr_ConspEmi_df = Imp_func.pd.read_excel(Curr_ConspEmi_wddt[i].replace('\\', '/'),'Sheet1')
        Curr_ConspEmi_df['Countryitem']=Curr_ConspEmi_df['iso3c']+\
            Curr_ConspEmi_df['item']
        
        Inf_mask =  Curr_ConspEmi_df.index[Imp_func.np.where(
            Curr_ConspEmi_df['Countryitem'] == 'FRACitrus, Other')]
        Curr_ConspEmi_CL_df=Curr_ConspEmi_df.drop(Inf_mask)
        
        # Slice those produced by European countries
        Curr_ConspEmi_Domstic_df = Curr_ConspEmi_CL_df[
            Curr_ConspEmi_CL_df['iso3c'].isin(EURO_country_ISO_list)]
        
        # Add these emissions produced in Europe up by item and also only
        # preserve those consummed by European countries
        Curr_ConspEmi_Domstic_df = FABIO_func.Comb_row_vert(
            Curr_ConspEmi_Domstic_df,'item',EURO_country_ISO_list)
        
        # Slice those produced by European countries
        Curr_ConspEmi_EUROaggre_df = FABIO_func.Comb_col_hori(
            Curr_ConspEmi_Domstic_df,'item','EURO_emi_aggr',EURO_country_ISO_list
        )
        Emi_EURO_byProd_dt[i]=Curr_ConspEmi_EUROaggre_df


    ### get the dataframe aggregated by stages
    Emi_EUROaggre_byProd_df =  FABIO_func.aggregate_df_ori(
        df_list=list(Emi_EURO_byProd_dt.values()),\
        presv_col_name='item',\
        value_col_name_list =['EURO_emi_aggr'])
    # Unit is kg


    ### Get the Y data
    Euro_toEuro_Y_df = Imp_func.pd.read_excel(Euro_NonEuro_Y_wd,\
        sheet_name='EURO_EURO',index_col=0)

    EURO_fabio_Y_aggr = FABIO_func.Comb_col_hori(Euro_toEuro_Y_df,\
        'Prod','EURO_Y',\
        list(Euro_toEuro_Y_df.columns)[1:])


    ## Get the results of ammonia emission by a unit of products
    # OUTPUT_DATA
    Unit_emission_byProd_df = Imp_func.pd.merge(
        Emi_EUROaggre_byProd_df,EURO_fabio_Y_aggr,\
        left_on='item',right_on='Prod',how='left')

    Unit_emission_byProd_df['Emi_perUnit']= \
        Unit_emission_byProd_df['EURO_emi_aggr']/1000/Unit_emission_byProd_df['EURO_Y']


    # OUTPUT_FILE
    Unit_emission_byProd_df.to_excel(Unit_Emi_wd,\
        index=False)
    
    return

