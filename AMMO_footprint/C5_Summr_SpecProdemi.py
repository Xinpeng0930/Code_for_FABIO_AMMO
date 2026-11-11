# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# C5_Summr_SpecProdemi — summary of specific production emissions

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_Pj_path


#%%
def Summr_Food_Diet(Scenarios_Name):
    #----------------------------------------------------Input/Output_module----------------------------------------------------
    # Specific food-driven emissions
    Prod_Emi_wddt =\
        Imp_func.open_plk(FABIO_Pj_path.Prj_Pkl_output_wd + 'ScenEmi_Levelone_Foodspec.pkl')[Scenarios_Name]
        ### from C4
    
    # Animal food list and plant food list
    Ani_food_list = ['Others_animals','Beef','Milk','Eggs','Animal fats','Other ASFs',\
        'Mutton','Pork','Pultry meat','Others_nonfoods']
    
    Plant_food_list = ['Fruits','Barley','Pulses','Drinks_alcohol','Potatoes','Other_cereals',\
        'Vegetables','Drinks_nonalcohol','Vegetable oils','Nuts','Sugar','Maize','Oats',\
        'Oil crops','Rye','Wheat']
    
    # Output pathways
    
    
    #----------------------------------------------------Processing_module----------------------------------------------------
    Anifood_Summr_lt = []
    Plantfood_Summr_lt = []
    
    for Food in Ani_food_list:
        
        ## Feed emissions driven by Animal foods
        Feed_syntfert_orig_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['Ammo_fertemi'],index_col=0)
        Feed_syntfert_df = Feed_syntfert_orig_df[['EURO_Aggr','NONEURO_Aggr']]
        Feed_manrliq_app_df =  Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrLiq_appcrop_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        Feed_manrsld_app_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrSld_appcrop_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]

        Feed_inputorig_df = Feed_syntfert_df.add(Feed_manrliq_app_df).add(Feed_manrsld_app_df)
        Feed_df = Imp_func.pd.concat([Feed_syntfert_orig_df.iloc[:,:5],Feed_inputorig_df], axis=1)
        
        ## Manure management emissions by Animal foods
        Manrliq_hous_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrLiq_hous_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        Manrsld_hous_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrSld_hous_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        Manrliq_stor_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrLiq_stor_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        Manrsld_stor_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrSld_stor_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        
        ManrMana_df = Manrliq_hous_df.add(Manrsld_hous_df).add(Manrliq_stor_df).add(Manrsld_stor_df)
        
        ## Manre input emissions by Animal foods
        Manr_graz_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['Manr_grazani_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        
        
        ## Sort the data based on regions
        Animal_food_EUROemi_df = Imp_func.pd.concat([Feed_df[list(Feed_df.columns[:5])+['EURO_Aggr']],\
            ManrMana_df['EURO_Aggr'],Manr_graz_df['EURO_Aggr']],axis=1)
        
        Animal_food_EUROemi_df.columns = list(Animal_food_EUROemi_df.columns[:5]) +  [str(item) + 'EURO' for item in ['Feed','Manr_mana','Manr_graz']]
        
        Animal_food_NONEUROemi_df = Imp_func.pd.concat([Feed_df[list(Feed_df.columns[:5])+['NONEURO_Aggr']],\
            ManrMana_df['NONEURO_Aggr'],Manr_graz_df['NONEURO_Aggr']],axis=1)
        
        Animal_food_NONEUROemi_df.columns = list(Animal_food_NONEUROemi_df.columns[:5]) +  [str(item) + 'NONEURO' for item in ['Feed','Manr_mana','Manr_graz']]
        
        ## Merge data together
        Animal_food_emi_df =  Imp_func.pd.concat([Animal_food_EUROemi_df,Animal_food_NONEUROemi_df.iloc[:,5:]],\
            axis=1)
        
        Animal_food_emi_Summ_df = Animal_food_emi_df[list(Animal_food_emi_df.columns[5:])].sum()
        Animal_food_emi_Summ_df.name = Food 
        
        Anifood_Summr_lt.append(Animal_food_emi_Summ_df)
        
    for Food in Plant_food_list:
        
        ## fertilizer emissions driven by plant food
        Syntfert_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['Ammo_fertemi'],index_col=0)
        
        ## Manure application emissions by plant food
        Manrliq_app_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrLiq_appcrop_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        Manrsld_app_df = Imp_func.pd.read_excel(Prod_Emi_wddt[Food]['ManrSld_appcrop_emi'],index_col=0)[['EURO_Aggr','NONEURO_Aggr']]
        
        ManrApp_df = Manrliq_app_df.add(Manrsld_app_df)
        Syntfert_df['EURO_Aggr'].sum()
        
        ## Sort the data based on regions
        Plant_food_EUROemi_df = Imp_func.pd.concat([Syntfert_df[list(Syntfert_df.columns[:5])+['EURO_Aggr']],\
            ManrApp_df['EURO_Aggr']],axis=1)
        
        Plant_food_EUROemi_df.columns = list(Plant_food_EUROemi_df.columns[:5]) +  [str(item) + 'EURO' for item in ['Syntfert','Manr_app']]
        
        Plant_food_NONEUROemi_df = Imp_func.pd.concat([Syntfert_df[list(Syntfert_df.columns[:5])+['NONEURO_Aggr']],\
            ManrApp_df['NONEURO_Aggr']],axis=1)
        
        Plant_food_NONEUROemi_df.columns = list(Plant_food_NONEUROemi_df.columns[:5]) +  [str(item) + 'NONEURO' for item in ['Syntfert','Manr_app']]
        
        ## Merge data together
        Plant_food_emi_df =  Imp_func.pd.concat([Plant_food_EUROemi_df,Plant_food_NONEUROemi_df.iloc[:,5:]],\
            axis=1)
        
        Plant_food_emi_Summ_df = Plant_food_emi_df[list(Plant_food_emi_df.columns[5:])].sum()
        Plant_food_emi_Summ_df.name = Food 
        
        Plantfood_Summr_lt.append(Plant_food_emi_Summ_df)
        
    Ani_summr_result_df = Imp_func.pd.concat(Anifood_Summr_lt, axis=1)
    Plant_summr_result_df = Imp_func.pd.concat(Plantfood_Summr_lt, axis=1)
    
    Food_summr_dt = {'Animfood':Ani_summr_result_df,\
        'Plantfood':Plant_summr_result_df}
    
    return Food_summr_dt


