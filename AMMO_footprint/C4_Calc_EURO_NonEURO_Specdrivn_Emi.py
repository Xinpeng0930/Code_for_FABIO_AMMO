# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# C4_Calc_EURO_NonEURO_Specdrivn_Emi — EU and non-EU specific demand-driven emissions

#%%
# Necessary packages
from APSP_proc import Z_fabio_rds_import as FABIO_Impt
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path



#%%
def fp_Food_Stage_Diet(Scenarios_Name, Food_type):
    ## General inputs-----------------------------------------------------------------------
    ### read important FABIO files
    # OUTPUT_DATA
    # Regions and items
    fabio_regions = FABIO_Impt.fabio_regions
    Fabio_regions_cut = fabio_regions[['area','iso3c']]
    EURO_country_list = list(fabio_regions['iso3c'][fabio_regions['EUEFTA']==True])
    NonEURO_country_list = list(fabio_regions['iso3c'][fabio_regions['EUEFTA']==False])
    Aggre_country_list = ['EURO_Aggr','NONEURO_Aggr']

    fabio_items = FABIO_Impt.reader.items
    fabio_L = FABIO_Impt.reader.L_2021_mass()
    fabio_nrreg = len(fabio_regions)
    fabio_nrcom = len(fabio_items)

    extension_list = FABIO_pj_path.extension_list[:-1]  # exclude Manr_grazcrop_emi (unused)
    
    ## get products from different classifications
    Para_wd = FABIO_pj_path.Prj_input_wd+r'Processing_plot_new.xlsx'
    Foodgroup_df = Imp_func.pd.read_excel(Para_wd,sheet_name='Food_group')
    Foodtype_list = Imp_func.pd.Series(list(Foodgroup_df['FigOne_EAT_items'])).drop_duplicates().tolist()

    ### Initialize early
    Y_newly_adj_df = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd + r'Y_newly_adj.pkl')
    Y_newly_adj_all_wddt = Imp_func.conv_df2dict(Y_newly_adj_df,\
        'Scenario','All')
  
    
    
    ## Scenario-based inputs-----------------------------------------------------------------------
    if Scenarios_Name == 'Curr':

        Yall_df = Imp_func.pd.read_excel(Y_newly_adj_all_wddt[Scenarios_Name],\
            sheet_name='Sheet1',index_col=0)
        
        fabio_X = FABIO_Impt.reader.X()
        E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
        sheet_name='E_new_Imprv') #from C1; CURR equals to CURR after B9
        
        Y_EmiProd_wd = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_ProdEmi_Specprod/{Food_type}/{Scenarios_Name}_'
        
    
    elif Scenarios_Name == 'EAT':

        Yall_df = Imp_func.pd.read_excel(
            Y_newly_adj_all_wddt[Scenarios_Name],\
            sheet_name='Sheet1',index_col=0) # from C1
        
        fabio_X = Imp_func.pd.read_excel(FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_X.xlsx',sheet_name='Sheet1')[['All_countries']] # from C1_B
        
        E_new = Imp_func.pd.read_excel('./AMMO_footprint/Input/E_AMMO.xlsx',\
            sheet_name='E_Imprv_EAT_for_Cons')  # CONSUMPTION convention (C2:79)
        
        Y_EmiProd_wd = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_ProdEmi_Specprod/{Food_type}/{Scenarios_Name}_'
        

    elif Scenarios_Name == 'EAT_Vegan':

        Yall_df = Imp_func.pd.read_excel(
            Y_newly_adj_all_wddt[Scenarios_Name],\
            sheet_name='Sheet1',index_col=0)
        
        fabio_X = Imp_func.pd.read_excel(FABIO_pj_path.Prj_Gene_output_wd + \
            f'{Scenarios_Name}_X.xlsx',sheet_name='Sheet1')[['All_countries']] # from C1_B
        
        E_new = Imp_func.pd.read_excel(\
        './AMMO_footprint/Input/E_AMMO.xlsx',\
        sheet_name='E_Imprv_EAT_Vegan_for_Cons')  # CONSUMPTION convention
        
        Y_EmiProd_wd = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_ProdEmi_Specprod/{Food_type}/{Scenarios_Name}_'

    else:
        raise ValueError(f"Unrecognised Scenarios_Name: '{Scenarios_Name}'. Expected one of: 'Curr', 'EAT', 'EAT_Vegan'.")


    #----------------------------------------------------processing_module----------------------------------------------------

    #OUTPUT_DATA
    ## Get Y_all based on regions    
    Yall_df_EURO = FABIO_func.Comb_col_hori(Yall_df,list(Yall_df.columns)[:2],\
        'EURO_Aggr',EURO_country_list)
    
    
    Yall_df_NONEURO =  FABIO_func.Comb_col_hori(Yall_df,list(Yall_df.columns)[:2],\
        'NONEURO_Aggr',NonEURO_country_list)
    
    
    Yall_df_Aggr_EUROenNonEURO = Imp_func.pd.concat([Yall_df_EURO,Yall_df_NONEURO.iloc[:,2]],\
        axis=1)
    
    '''
    ### Check if Y_all properly attributed to different regions
    Check_bala = Yall_df[list(Yall_df.columns)[2:]].sum().sum() - Yall_df_Aggr_EUROenNonEURO[list(Yall_df_Aggr_EUROenNonEURO.columns)[2:]].sum().sum() 
    print(Check_bala) # passed the balance check
    '''
    
    ## Get Y_all based on food types
    Yall_df_Aggre_foodtype = Imp_func.pd.merge(Yall_df_Aggr_EUROenNonEURO,\
        Foodgroup_df,how='left',left_on='item',\
        right_on='Item_FABIO')
    

    
    Yall_df_Aggre_foodtype_new = Imp_func.deepcopy(Yall_df_Aggre_foodtype)
    
    if Food_type == Foodtype_list[0]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[0],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
        
        
    elif Food_type == Foodtype_list[1]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[1],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[2]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[2],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[3]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[3],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[4]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[4],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]


    elif  Food_type == Foodtype_list[5]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[5],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[6]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[6],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[7]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[7],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[8]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[8],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[9]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[9],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[10]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[10],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[11]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[11],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[12]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[12],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[13]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[13],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[14]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[14],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[15]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[15],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]


    elif Food_type == Foodtype_list[16]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[16],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[17]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[17],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[18]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[18],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[19]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[19],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[20]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[20],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
        
    elif Food_type == Foodtype_list[21]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[21],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[22]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[22],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]

    elif Food_type == Foodtype_list[23]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[23],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item', 'EURO_Aggr','NONEURO_Aggr']]
        
    elif Food_type == Foodtype_list[24]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[24],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[25]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[25],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]
    
    elif Food_type == Foodtype_list[26]:
        Yall_df_Aggre_foodtype_new.loc[Yall_df_Aggre_foodtype_new['FigOne_EAT_items'] != Foodtype_list[26],\
        ['EURO_Aggr','NONEURO_Aggr']] = 0
        
        Yall_df_EURO_foodtype_essential = Yall_df_Aggre_foodtype_new[[
            'area', 'item','EURO_Aggr','NONEURO_Aggr']]
    
    ## Get parameters for calculating emissions
    Y_new = Yall_df_EURO_foodtype_essential.iloc[:,2:]

    ### Set new y codes
    fabio_y_codes_new = Imp_func.pd.DataFrame({'iso3c':Y_new.columns})
    fabio_y_codes_new['fd'] = 'All'


    for extension in extension_list:
            FABIO_func.Output_ProdFP_byExten(
                regions=fabio_regions,\
                items=fabio_items,\
                nrcom=fabio_nrcom,\
                nrreg=fabio_nrreg,\
                COUNTY_LIST=Aggre_country_list,\
                EXTENSION=extension,\
                CONSUMPTION='Total',\
                E = E_new, X=fabio_X, \
                L=fabio_L,Y=Y_new,\
                Y_CODE=fabio_y_codes_new,\
                output_path= Y_EmiProd_wd + extension+'.xlsx',\
                parallel_cores=4)
    
    return

