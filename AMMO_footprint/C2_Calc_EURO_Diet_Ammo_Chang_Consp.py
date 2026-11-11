# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# C2_Calc_EURO_Diet_Ammo_Chang_Consp — consumption-based emission accounting
'''
Here we are gonna get the consumption-based emissions in the base year.
But we test two scenario, one is the food scenario, the other is the total product scenario
'''


#%%
# Necessary packages
from APSP_proc import Z_fabio_rds_import as FABIO_Impt
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path


#%%
def Calc_Consp_fp(Scenario_Name, Footprint_driver):
    #----------------------------------------------------input_module----------------------------------------------------
    Imp_func.os.makedirs(FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byProd/',\
        exist_ok=True)
    # --------------Gerneral input data
    # OUTPUT_DATA
    fabio_items = FABIO_Impt.reader.items
    fabio_regions = FABIO_Impt.fabio_regions

    fabio_L = FABIO_Impt.reader.L_2021_mass()
    fabio_y_codes = FABIO_Impt.Y_codes

    fabio_nrreg = len(fabio_regions)
    fabio_nrcom = len(fabio_items)

    country_list = list(FABIO_Impt.fabio_regions['iso3c'])
    extension_list = FABIO_pj_path.extension_list[:-1] # we delete the "Manr_grazcrop_emi" because it is useless in following analysis

    ### Initialize Y data for the two scenarios
    Y_newly_adj_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + r'Y_newly_adj.pkl')
    Y_newly_adj_all_wddt = Imp_func.conv_df2dict(Y_newly_adj_df,\
        'Scenario','All')
    Y_newly_adj_food_wddt = Imp_func.conv_df2dict(Y_newly_adj_df,\
        'Scenario','Food')
    
    # --------------Scenario-based output data
    if Scenario_Name in ['CURR','CURR_MTFR']:

        
        fabio_X = FABIO_Impt.reader.X()
        
        if Scenario_Name == 'CURR_MTFR':
            E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
                    sheet_name='E_MTFR')
        else:
            E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
                    sheet_name='E_new_Imprv')
        
        if Footprint_driver == "Total":
            Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byProd/' # Most detailed data: detailed country-commodity -> country
            
            Y_new = Imp_func.pd.read_excel(Y_newly_adj_all_wddt['Curr'],\
                sheet_name='Sheet1',index_col=0).iloc[:,2:]
            
            fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
            fabio_y_codes_new['fd'] = 'All'
            
        elif Footprint_driver == "food":
            Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byFood/'

            Y_new = Imp_func.pd.read_excel(Y_newly_adj_food_wddt['Curr'],\
                sheet_name='Sheet1',index_col=0).iloc[:,2:]
            
            fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
            fabio_y_codes_new['fd'] = 'food'
            
    elif Scenario_Name in ['EAT','EAT_MTFR','MTFR_EAT']:

        fabio_X = Imp_func.pd.read_excel(FABIO_pj_path.Prj_Gene_output_wd + \
            f'EAT_X.xlsx',\
            sheet_name='Sheet1')[['All_countries']] # we need to change X which is from C1_B
        
        if Scenario_Name == 'EAT':
            E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
                sheet_name='E_Imprv_EAT_for_Cons')
        elif Scenario_Name == 'EAT_MTFR':
            E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
                    sheet_name='E_Imprv_EAT_MTFR_for_Cons')
        elif Scenario_Name == 'MTFR_EAT':
            E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
                    sheet_name='E_MTFR_EAT_for_Cons')
        else:
            print(f'We don not have such scenario yet')
        
        
        if Footprint_driver == "Total":
            Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byProd/' # Most detailed data: detailed country-commodity -> country
            
            Y_new = Imp_func.pd.read_excel(Y_newly_adj_all_wddt['EAT'],\
                sheet_name='Sheet1',index_col=0)
            
            fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
            fabio_y_codes_new['fd'] = 'All'
            
        elif Footprint_driver == "food":
            Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byFood/'

            Y_new = Imp_func.pd.read_excel(Y_newly_adj_food_wddt['EAT'],\
                sheet_name='Sheet1',index_col=0)
            
            fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
            fabio_y_codes_new['fd'] = 'food'
            
    else:
        print(f'We don not have such scenario yet')



    #----------------------------------------------------processing_module----------------------------------------------------
    ### Get the level-1 emissions (most detailed)
    #OUTPUT_FILE
    for extension in extension_list:
        FABIO_func.Output_ConspFP_byProd_byExten(
            regions=fabio_regions,\
            items=fabio_items,\
            nrcom=fabio_nrcom,\
            nrreg=fabio_nrreg,\
            COUNTY_LIST=country_list,\
            EXTENSION=extension,\
            CONSUMPTION=Footprint_driver,\
            E = E_new, \
            X = fabio_X,\
            L = fabio_L,\
            Y= Y_new,\
            Y_CODE = fabio_y_codes_new,\
            parallel_cores=4,\
            output_path= Level_one_output_path + \
                f"fp_{extension}_{Footprint_driver}.xlsx")
    
    return




def Summary_Comsp_Emi(Scenario_Name, Footprint_driver):
    # --------------Gerneral input data
    # OUTPUT_DATA
    fabio_regions = FABIO_Impt.fabio_regions
    extension_list = FABIO_pj_path.extension_list[:-1] # we delete the "Manr_grazcrop_emi" because it is useless in following analysis

    # --------------Scenario-based output data
    if Scenario_Name not in ['CURR', 'EAT','EAT_MTFR',\
        'CURR_MTFR','MTFR_EAT']:
        raise ValueError(f'Unhandled scenario: {Scenario_Name!r}')

    if Footprint_driver == "Total":
        Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byProd/' # Most detailed data: detailed country-commodity -> country
        Level_two_output_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenario_Name}_ConspEmi_byProd/' # Second detailed data: food -> country
        Level_three_output_path =FABIO_pj_path.Prj_Gene_output_wd + f'Chek_{Scenario_Name}_ConspbyProd_Emi.xlsx' # Third detailed data : food->country, but all stages are aggregated together
        Level_four_output_path = FABIO_pj_path.Prj_Gene_output_wd + f'Chek_{Scenario_Name}_ConspbyProdbyRegion_Emi.xlsx'# Most rough data: just food->coutry, and all stages are aggregated
        Summary_pkl = f'{Scenario_Name}_ConspEmi.pkl'

    elif Footprint_driver == "food":
        Level_one_output_path = FABIO_pj_path.Prj_Gene_output_wd +f'{Scenario_Name}Consp_Emi_byFood/'
        Level_two_output_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenario_Name}_ConspEmi_byFood/' # Second detailed data: food -> country
        Level_three_output_path = FABIO_pj_path.Prj_Gene_output_wd + f'Chek_{Scenario_Name}_ConspbyFood_Emi.xlsx'
        Level_four_output_path = FABIO_pj_path.Prj_Gene_output_wd + f'Chek_{Scenario_Name}_ConspbyFoodbyRegion_Emi.xlsx'
        Summary_pkl = f'{Scenario_Name}_FoodConspEmi.pkl'

    else:
        raise ValueError(f'Unhandled Footprint_driver: {Footprint_driver!r}')

    Imp_func.os.makedirs(Level_one_output_path, exist_ok=True)
    Imp_func.os.makedirs(Level_two_output_path, exist_ok=True)


    ### Sum up values vertically and group them by product(level-2 emissions)
    # OUTPUT_DATA
    Curtcons_excel_wddt= Imp_func.dict_name_path(extension_list,\
        Imp_func.glob.glob(Level_one_output_path +r'fp_*.xlsx',\
        recursive=False))

    # OUTPUT_FILE
    for i in Curtcons_excel_wddt:
        Emi_Consp_byProd_df = Imp_func.pd.read_excel(Curtcons_excel_wddt[i],sheet_name='Sheet1')
        Emi_Consp_byProd_df_sum = Emi_Consp_byProd_df.groupby('item')[list(fabio_regions['iso3c'])].sum().reset_index()
        Emi_Consp_byProd_df_sum.to_excel(Level_two_output_path+i+'_SummarybyProd.xlsx',\
            sheet_name='Sheet1',index=False)

    # OUTPUT_DATA
    Curtcons_Summbyprod_excel_wddt = Imp_func.dict_name_path(extension_list,\
        Imp_func.glob.glob(Level_two_output_path +'*_SummarybyProd.xlsx',\
            recursive=False))


    ### Sum up all values horizontally and sort to an aggregated dataframe (level-3 emissions)
    # OUTPUT_DATA
    
    
    Emi_Consp_standard = Imp_func.pd.DataFrame(Imp_func.pd.read_excel(Curtcons_Summbyprod_excel_wddt['Ammo_fertemi'],\
        sheet_name='Sheet1')['item'])


    for i in Curtcons_Summbyprod_excel_wddt:
        Emi_Consp_df = Imp_func.pd.read_excel(Curtcons_Summbyprod_excel_wddt[i],\
            sheet_name='Sheet1')
        Emi_Consp_sum = FABIO_func.Comb_col_hori(Emi_Consp_df,'item',i,\
            list(Emi_Consp_df.columns[1:]))
        Emi_Consp_standard = Imp_func.pd.merge(Emi_Consp_standard,Emi_Consp_sum,\
            how='left', left_on='item',\
            right_on='item')

    # OUTPUT_FILE
    Emi_Consp_standard.to_excel(Level_three_output_path,\
        sheet_name='Sheet1',index=False)


    ### Sum up all values horizontally and distinguish whether the driving force is from Europe
    EURO_region = FABIO_Impt.fabio_regions[FABIO_Impt.fabio_regions['EUEFTA']==True]['iso3c']
    Non_EURO_region = FABIO_Impt.fabio_regions[FABIO_Impt.fabio_regions['EUEFTA']==False]['iso3c']

    for i in Curtcons_Summbyprod_excel_wddt:
        Emi_Consp_byarea_df = Imp_func.pd.read_excel(Curtcons_Summbyprod_excel_wddt[i],\
            sheet_name='Sheet1')
        Emi_Consp_byEURO_sum = FABIO_func.Comb_col_hori(Emi_Consp_byarea_df,'item',i+"EURO",\
            list(EURO_region))
        Emi_Consp_byNonEURO_sum = FABIO_func.Comb_col_hori(Emi_Consp_byarea_df,'item',i+"_NonEURO",\
            list(Non_EURO_region))
        Emi_Consp_standard =  Imp_func.pd.merge(Emi_Consp_standard,Emi_Consp_byEURO_sum,\
            how='left', left_on='item',\
            right_on='item')
        Emi_Consp_standard = Imp_func.pd.merge(Emi_Consp_standard,Emi_Consp_byNonEURO_sum,\
            how='left', left_on='item',\
            right_on='item')

    Emi_Consp_standard.to_excel(Level_four_output_path,\
        sheet_name='Sheet1',index=False)

    #----------------------------------------------------summary_module----------------------------------------------------
    # SUMMARY
    Emi_consp_df = Imp_func.conv_dict2df(Curtcons_excel_wddt,'Stage',\
        'Curr_detail')
    Emi_consp_df = Imp_func.join_dict2df(Emi_consp_df,Curtcons_Summbyprod_excel_wddt,'Stage',\
        'Curr_summary')

    ConspEmi_dt = {'Stage_spec_DetailenSummary':Emi_consp_df,\
        'Summary_aggre_stage':Level_three_output_path,\
        'Summary_aggre_stage_diff_region':Level_four_output_path}

    Imp_func.save_plk(FABIO_pj_path.Prj_Pkl_output_wd + Summary_pkl,ConspEmi_dt)
    
    return


