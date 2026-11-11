# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# B11_Aggr_Diet_Chang_Emi_en_Fac — aggregation of diet-driven emission changes by factor
'''
This script aims to get aggregated emission data and scaling factors to map emissions under different scenarios

This script can run automatically. RUNNING TIME IS 9 mins.
'''

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path
from APSP_proc import Z_Proj_paths as Air_pj_path


#%%

def AggrEmi_HighresoFac(Scenarios_Name):
    #----------------------------------------------------input_module----------------------------------------------------
    # OUTPUT_DATA
    # Non-map inputs---------------------------------------------------------------------------------------------------------
    Para_wd = FABIO_pj_path.Prj_input_wd + 'Processing_plot_new.xlsx'

    ## Production side emissions
    Prod_Emi_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
        'ProdEmi.pkl') #from B10

    Prod_DetEmi_df = Prod_Emi_dt['Emi_Prod_Level1_Stage_spec']

    ## Standard head for EU and EFTA countries
    Standard_EUEFTA_head = Imp_func.pd.read_excel(Para_wd,\
        sheet_name='Country_name')

    ## Standard head for commodity classification (123 types)
    Items_head = Imp_func.pd.read_excel(Para_wd,\
        sheet_name='Food_group')
        
    ## FABIO useful product categories
    FABIO_CropName_list = ['Whea', 'Barl', 'Maiz&Grenmaiz', \
            'Legufod','Rapesd', 'Sunflrsd','Soya', \
            'Oats', 'Rice', 'Rye','Pota','Sugbt','Peabean','Nuts',\
            'Fruit','Vege', 'Tempgra&Permgra']

    FABIO_LivestkName_list = ['Pig', 'Dair','Othcatl','Shep','Goat','Potr']

    FABIO_CropManr_list = ['Whea', 'Barl', 'Maiz&Grenmaiz', \
            'Rapesd', 'Sunflrsd', \
            'Oats', 'Rye','Pota','Sugbt','Nuts',\
            'Fruit','Vege', 'Tempgra&Permgra']

    # Scenario-based inputs and outputs-----------------------------------------------------------------------
    if Scenarios_Name == 'EAT':
        AggEmi_wd = FABIO_pj_path.Prj_Gene_output_wd+'/fp_EATLANCET_ProdSide_Aggr4Map/'
        Ori_APAMMO_Emi_wd = FABIO_pj_path.Prj_input_wd+'N_flows_en_NH3_byStage.xlsx'
        
    elif Scenarios_Name == 'MTFR_EAT':
        AggEmi_wd = FABIO_pj_path.Prj_Gene_output_wd+'/fp_MTFR_EAT_ProdSide_Aggr4Map/'
        Ori_APAMMO_Emi_wd = FABIO_pj_path.Prj_input_wd+'N_flows_en_NH3_byStage_MTFR.xlsx'
      
    elif Scenarios_Name == 'EAT_Meat':
        AggEmi_wd = FABIO_pj_path.Prj_Gene_output_wd+f'/fp_{Scenarios_Name}_ProdSide_Aggr4Map/'
        Ori_APAMMO_Emi_wd = FABIO_pj_path.Prj_input_wd+'N_flows_en_NH3_byStage.xlsx'
        
    elif Scenarios_Name in ['EAT','EAT_Vegan','EAT_Meat']:
        AggEmi_wd = FABIO_pj_path.Prj_Gene_output_wd+f'/fp_{Scenarios_Name}_ProdSide_Aggr4Map/'
        Ori_APAMMO_Emi_wd = FABIO_pj_path.Prj_input_wd+'N_flows_en_NH3_byStage_Imprv.xlsx'
    
    ## Preprocess original emissions from AP-AMMO 
    AMMO_shetname =Imp_func.pd.ExcelFile(Ori_APAMMO_Emi_wd).sheet_names
    AMMO_emi_shetname = [item for item in AMMO_shetname  if "NH3_" in item]

    AMMO_useful_shetname = \
        ['NH3_Syntfert','NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
        'NH3_Liqstor_Liv','NH3_Sldstor_Liv','NH3_LiqMA_Crop','NH3_SldMA_Crop',\
            'NH3_ManrGraz_excr_Liv']
    
    
    #----------------------------------------------------processing_module----------------------------------------------------

    ## Align FABIO emissions from the production side to the classification of AP-AMMO under various scenario
    #OUTPUT_DATA
    Emi_excel_wddt = Imp_func.conv_df2dict(Prod_DetEmi_df,'Stage',\
        Scenarios_Name)
    Emi_excel_wddt = Imp_func.dict_del_nan(Emi_excel_wddt)
    
    Emi_FABIO_ProdEmi_dt = {}

    for Stage in list(Emi_excel_wddt.keys()):
        Emi_Prod_df = Imp_func.pd.read_excel(Emi_excel_wddt[Stage],sheet_name='Sheet1')
        Emi_Prod_df.fillna(0,inplace=True) # replaces nan values in the original dataframe
        Emi_Prod_df.replace([Imp_func.np.inf, -Imp_func.np.inf], 0,inplace=True)
        
        Emi_Prod_col = list(Emi_Prod_df.columns[6:])
        
        Emi_Prod_column_sum = Imp_func.pd.DataFrame({'iso3c':Emi_Prod_df['iso3c'],\
            'items':Emi_Prod_df['item'],\
            Stage:Emi_Prod_df[Emi_Prod_col].sum(axis=1)}) #add each columns horrizontally

        Emi_Prod_pivot = Imp_func.pd.pivot_table(Emi_Prod_column_sum,\
            index=[u'iso3c'], columns=[u'items'],\
            values=[Stage], aggfunc=[Imp_func.np.sum],fill_value=0)

        Emi_Prod_pivot.columns=list(Emi_Prod_pivot.columns.get_level_values('items'))

        ### Transpose the dataframe and aggregate items
        Emi_Prod_pivot_trans = Emi_Prod_pivot.T
        Emi_Prod_pivot_trans.insert(0,'item_names',Emi_Prod_pivot_trans.index)
        Emi_Prod_pivot_trans = Emi_Prod_pivot_trans.reset_index(drop=True)


        ### Get DataFrames
        Emi_Prod_pivot_trans_new = Imp_func.pd.merge(Items_head,Emi_Prod_pivot_trans,\
            how='left',left_on='Item_FABIO',right_on='item_names')

        Emi_Prod_pivot_trans_sum = Emi_Prod_pivot_trans_new.groupby('AP-AMMO_prod')[list(Emi_Prod_pivot_trans_new.columns)[13:]].sum().reset_index()

        ### Transpose back the dataframe
        Emi_Prod_pivot_sum =  Emi_Prod_pivot_trans_sum.T
        Emi_Prod_pivot_sum.columns = Emi_Prod_pivot_sum.iloc[0]
        Emi_Prod_pivot_sum_new = Emi_Prod_pivot_sum.drop('AP-AMMO_prod',axis=0)
        Emi_Prod_pivot_sum_new = Emi_Prod_pivot_sum_new.drop('item_names',axis=0) 
        Emi_Prod_pivot_sum_new = Emi_Prod_pivot_sum_new.clip(lower=0) #set negative values to zero
        
        Emi_Prod_pivot_sum_new2 = Imp_func.pd.merge(Standard_EUEFTA_head,\
            Emi_Prod_pivot_sum_new,how='left',left_on='Name_ISO',right_index=True)

        ###Output emission data
        #OUTPUT_DATA
        Emi_FABIO_ProdEmi_dt[Stage]=Emi_Prod_pivot_sum_new2
        
        #OUTPUT_FILE
        Emi_Prod_pivot_sum_new2.to_excel(AggEmi_wd+'Aggr_ProdEmi_APAMMO'+'_'+Stage+'.xlsx',\
            sheet_name='Sheet1',index=False)




    ### Inherit emissions from FABIO
    Useful_Emi_FABIO_ProdEmi_dt = Imp_func.deepcopy(Emi_FABIO_ProdEmi_dt)


    Imp_func.del_keys_dict(Useful_Emi_FABIO_ProdEmi_dt,\
        ['ManrLiq_appani_emi','ManrSld_appani_emi','Manr_grazcrop_emi'])


    Useful_Emi_FABIO_ProdEmi_dt = Imp_func.replace_keys(
        Useful_Emi_FABIO_ProdEmi_dt,\
        AMMO_useful_shetname)


    ### get targeting emissions from FABIO
    Emi_FABIO_Emi_extr_dt = {}


    for Stage in list(Useful_Emi_FABIO_ProdEmi_dt.keys()):
        #### reindex the dataframe to align with the AP-AMMO dataframe
        New_col_order = ['OBJECTID', 'Name_abbre' , 'Name', 'country_group',\
            'Name_ISO', 'Whea', 'Barl', 'Maiz&Grenmaiz', \
            'Legufod','Rapesd', 'Sunflrsd','Soya', \
            'Oats', 'Rice', 'Rye','Pota','Sugbt','Peabean','Nuts',\
            'Fruit', 'Vege', 'Tempgra&Permgra', 'Pig', 'Dair','Othcatl','Shep',\
            'Goat','Potr']
        
        Useful_Emi_FABIO_ProdEmi = Useful_Emi_FABIO_ProdEmi_dt[Stage]
        
        Useful_Emi_FABIO_ProdEmi = Useful_Emi_FABIO_ProdEmi.reindex(
            columns=New_col_order)
        Useful_Emi_FABIO_ProdEmi.reset_index(drop=True,inplace=True)

        #### only get useful columns in each stage
        if Stage  in ['NH3_Syntfert']:
            Useful_Emi_FABIO_ProdEmi_new = Useful_Emi_FABIO_ProdEmi[FABIO_CropName_list]
        elif Stage in ['NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
        'NH3_Liqstor_Liv','NH3_Sldstor_Liv']:
            Useful_Emi_FABIO_ProdEmi_new = Useful_Emi_FABIO_ProdEmi[FABIO_LivestkName_list]
        elif Stage in ['NH3_LiqMA_Crop','NH3_SldMA_Crop']:
            Useful_Emi_FABIO_ProdEmi_new = Useful_Emi_FABIO_ProdEmi[FABIO_CropManr_list]
        elif Stage in ['NH3_ManrGraz_excr_Liv']:
            Useful_Emi_FABIO_ProdEmi_new = Useful_Emi_FABIO_ProdEmi[['Dair','Othcatl','Shep','Goat']]
            
        Emi_FABIO_Emi_extr_dt[Stage] = Useful_Emi_FABIO_ProdEmi_new
        print(list(Useful_Emi_FABIO_ProdEmi_new.columns))
        
        # Create an ExcelWriter object
        #OUTPUT_FILE
        with Imp_func.pd.ExcelWriter(FABIO_pj_path.Prj_Gene_output_wd+\
            f'{Scenarios_Name}_FABIO_Emi_check.xlsx',\
            engine='xlsxwriter') as writer:
            # Iterate over the dictionary and write each DataFrame to a sheet
            for sheet_name, df in Emi_FABIO_Emi_extr_dt.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)



    ### Get original emissions from AP-AMMO
    Emi_APAMMO_dt ={}


    for Stage in AMMO_useful_shetname:
        ### get orignal emissions and aggregate several items aggregated in FABIO
        Emi_AMMO_df = Imp_func.pd.read_excel(Ori_APAMMO_Emi_wd,sheet_name= Stage)
        if Stage == 'NH3_Syntfert':
            Emi_AMMO_df['Maiz&Grenmaiz'] = Emi_AMMO_df['Maiz']+Emi_AMMO_df['Grenmaiz']
            Emi_AMMO_df['Tempgra&Permgra'] =  Emi_AMMO_df['Tempgra']+Emi_AMMO_df['Permgra']
            #(delete extra columns)
            Emi_AMMO_df = Emi_AMMO_df.drop(columns=['Maiz','Grenmaiz','Tempgra','Permgra'])
            
            Emi_AMMO_Num_df = Emi_AMMO_df[list(Emi_AMMO_df.columns)[2:]]
            Emi_AMMO_Num_new_df = Emi_AMMO_Num_df[FABIO_CropName_list]
            
        elif Stage in ['NH3_LiqMA_Crop','NH3_SldMA_Crop']:
            Emi_AMMO_df['Maiz&Grenmaiz'] = Emi_AMMO_df['Maiz']+Emi_AMMO_df['Grenmaiz']
            Emi_AMMO_df['Tempgra&Permgra'] =  Emi_AMMO_df['Tempgra']+Emi_AMMO_df['Permgra']
            #(delete extra columns)
            
            Emi_AMMO_Num_df = Emi_AMMO_df[list(Emi_AMMO_df.columns)[2:]]
            Emi_AMMO_Num_new_df = Emi_AMMO_Num_df[FABIO_CropManr_list]
        
        elif Stage in ['NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
                    'NH3_Liqstor_Liv','NH3_Sldstor_Liv']:
            Emi_AMMO_df =Emi_AMMO_df
            Emi_AMMO_Num_df = Emi_AMMO_df[list(Emi_AMMO_df.columns)[2:]]
            Emi_AMMO_Num_new_df = Emi_AMMO_Num_df[FABIO_LivestkName_list]
            
        elif Stage == 'NH3_ManrGraz_excr_Liv':
            Emi_AMMO_df =Emi_AMMO_df
            Emi_AMMO_Num_df = Emi_AMMO_df[list(Emi_AMMO_df.columns)[2:]]
            Emi_AMMO_Num_new_df = Emi_AMMO_Num_df[['Dair','Othcatl','Shep','Goat']]

        Emi_APAMMO_dt[Stage] = Emi_AMMO_Num_new_df
        print(list(Emi_AMMO_Num_new_df.columns)) # CHECK THE ORDER OF PRODUCTS



    ### Execute the divisions and get the calibration factors
    # OUTPUT_DATA
    Fac_cali_dt = {} 

    for Stage in Emi_FABIO_Emi_extr_dt:
        Emi_AMMO_matrix = Imp_func.np.array(Emi_APAMMO_dt[Stage])
        Emi_targ_matrix = Imp_func.np.array(Emi_FABIO_Emi_extr_dt[Stage])
        #### process the data
        Fac_cali = Imp_func.np.zeros_like(Emi_AMMO_matrix, dtype=float)
        APAMMO_Nonzero_mask = Emi_AMMO_matrix != 0
        Fac_cali[APAMMO_Nonzero_mask] = Emi_targ_matrix[APAMMO_Nonzero_mask]/Emi_AMMO_matrix[APAMMO_Nonzero_mask]
        
        ####  convert to dataframe
        Fac_cali_df = Imp_func.pd.DataFrame(Fac_cali)

        Fac_cali_df.columns=list(Emi_FABIO_Emi_extr_dt[Stage].columns)
        
        #### align products with that in AP-AMMO
        if Stage in [
            'NH3_Syntfert','NH3_LiqMA_Crop','NH3_SldMA_Crop']:
            New_columns =Imp_func.pd.DataFrame({
                'Grenmaiz':Fac_cali_df['Maiz&Grenmaiz'],\
                'Tempgras':Fac_cali_df['Tempgra&Permgra']})
            part_left = Fac_cali_df.iloc[:,:3]
            part_right = Fac_cali_df.iloc[:,3:]
            
            Fac_cali_new_df=Imp_func.pd.concat(
                [part_left,New_columns,part_right],axis=1)
        else:
            Fac_cali_new_df = Fac_cali_df
        
        #### add area information to the dataframe
        Fac_cali_new_df.insert(0,'Country', \
            Air_pj_path.Country_name_abbr)
        Fac_cali_dt[Stage]=Fac_cali_new_df
        
        # Create an ExcelWriter object
        #OUTPUT_FILE
        with Imp_func.pd.ExcelWriter(FABIO_pj_path.Prj_Gene_output_wd+f'{Scenarios_Name}_Highreso_califac_check.xlsx',\
            engine='xlsxwriter') as writer:
            # Iterate over the dictionary and write each DataFrame to a sheet
            for sheet_name, df in Fac_cali_dt.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return
        


