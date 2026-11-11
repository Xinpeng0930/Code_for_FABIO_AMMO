# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# C1_Allo_adj_emi_consp — allocation of adjusted emissions to consumption


#%%
# Import necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_important_functions as FABIO_func
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path


#%%

def Allo_Emi(Scenario):
    #----------------------------------------------------input_module----------------------------------------------------
    # General inputs ---------------------------------------------------------------------
    ## provides categories 
    Cate_wd = FABIO_pj_path.Prj_input_wd+r'Processing_plot_new.xlsx' 
    Item_APAMMO_FABIO_df = Imp_func.pd.read_excel(Cate_wd,sheet_name='Food_group')
    Country_APAMMO_FABIO_df = Imp_func.pd.read_excel(Cate_wd,sheet_name='Country_name')
    
    ## Dataframe of the NH3 allocating template
    NH3Nflow_temp_df = Imp_func.pd.read_excel(Cate_wd,sheet_name='Temp_NH3_Nflow_AMMO_FABIO')
    NH3Nflow_temp_df['ISO_country-itemcode']= NH3Nflow_temp_df['ISO_code']+ '_'+ NH3Nflow_temp_df['comm_code']

    ## Create output folder
    Imp_func.os.makedirs(FABIO_pj_path.Prj_Gene_output_wd+ \
        f'{Scenario}_NH3_Allo_ForConsum/', exist_ok=True) 
    
    # Scenario-based inputs ---------------------------------------------------------------------
    if Scenario == 'CURR':
        ## provides NH3 emissions from AP_AMMO
        NH3_AP_AMMO_wd = FABIO_pj_path.Prj_input_wd+ r'N_flows_en_NH3_byStage.xlsx'
        
        ### Dataframes of NH3 emissions
        NH3_dict ={}
        for i in ['NH3_Syntfert','NH3_ManrGraz_excr_Liv',\
                'NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
                'NH3_Liqstor_Liv' ,'NH3_Sldstor_Liv',\
                'NH3_LiqMA_Liv','NH3_SldMA_Liv',\
                'NH3_LiqMA_Crop','NH3_SldMA_Crop']:
            N_flow_df_ori = Imp_func.pd.read_excel(NH3_AP_AMMO_wd,sheet_name=i)
            del N_flow_df_ori['name']
            NH3_dict[i]=N_flow_df_ori 
            
    
    else:
        ## provides emissions under dietary scenarios  
       
        NH3_AP_AMMO_wd = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
            r'Scen_SharSort_Emi.pkl')[Scenario]['E_adj_VecforConsp'] # from D2
        
        
        ### Dataframes of NH3 emissions
        NH3_dict ={}
        for i in ['NH3_Syntfert','NH3_ManrGraz_excr_Liv',\
                'NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
                'NH3_Liqstor_Liv' ,'NH3_Sldstor_Liv',\
                'NH3_LiqMA_Liv','NH3_SldMA_Liv','NH3_LiqMA_Crop','NH3_SldMA_Crop']:
            
            if i in ['NH3_Syntfert']:
                N_flow_df_ori = Imp_func.pd.read_excel(NH3_AP_AMMO_wd,sheet_name=i)
                # Rename the column 'Legume fodder'
                N_flow_df_ori = N_flow_df_ori.rename(columns={'Legumfod': 'Legufod'})

            elif i in ['NH3_ManrGraz_excr_Liv',\
                    'NH3_ManrInhous_Liqexcr_Liv','NH3_ManrInhous_Sldexcr_Liv',\
                    'NH3_Liqstor_Liv' ,'NH3_Sldstor_Liv',\
                    'NH3_LiqMA_Liv','NH3_SldMA_Liv']:
                N_flow_df_ori = Imp_func.pd.read_excel(NH3_AP_AMMO_wd,sheet_name=i)
                N_flow_df_ori.columns = [col.capitalize() for col in N_flow_df_ori.columns]
            
            elif i in ['NH3_LiqMA_Crop','NH3_SldMA_Crop']:
                N_flow_df_ori = Imp_func.pd.read_excel(NH3_AP_AMMO_wd,sheet_name=i)
            
            N_flow_df_ori.insert(0,'Name_abbre',Country_APAMMO_FABIO_df['Name_abbre'])

            NH3_dict[i]=N_flow_df_ori

    #----------------------------------------------------processing_module------------------------------------------------

    ## Dataframes of disaggegated proportions of several products
    NH3_fac_disaggre_dict = {}
    NH3_fac_disaggre_name_dict = {'Disagg_Fruit':'Fruit','Disagg_Vege':'Vege',\
        'Disagg_Peabean':'Peabean','Disagg_Milk':'Dair'}

    ### for disaggretion factor, we need to fix to r'N_flows_en_NH3_byStage.xlsx'. Because we only have the data in that excel file
    for j in ['Disagg_Fruit','Disagg_Vege','Disagg_Peabean','Disagg_Milk']:
        N_disaggre_fac=Imp_func.pd.read_excel(FABIO_pj_path.Prj_input_wd+ r'N_flows_en_NH3_byStage.xlsx',\
            sheet_name=j)
        NH3_fac_disaggre_dict[NH3_fac_disaggre_name_dict[j]] = FABIO_func.DF_insert_row(N_disaggre_fac,\
            30, Imp_func.pd.DataFrame([[Imp_func.np.nan]*len(N_disaggre_fac.columns)],\
            columns=N_disaggre_fac.columns))
    

    ## Identify different mapping groups between AP-AMMO and FABIO
    Extact_matchtab_df = Item_APAMMO_FABIO_df.loc[Item_APAMMO_FABIO_df['Match_APAMMO_FABIO_Emi_Nflow']=='One-one',\
        ['AP-AMMO_prod','Item_FABIO']]
    Aggre_matchtab_df = Item_APAMMO_FABIO_df.loc[Item_APAMMO_FABIO_df['Match_APAMMO_FABIO_Emi_Nflow']=='Aggre',\
        ['AP-AMMO_prod','Item_FABIO']]
    Disaggre_matchtab_df = Item_APAMMO_FABIO_df.loc[Item_APAMMO_FABIO_df['Match_APAMMO_FABIO_Emi_Nflow']=='Disaggre',\
        ['AP-AMMO_prod','Item_FABIO']]


    ## Get the exact matching emissions data
    NH3_melt_Exact_dict = {}

    for Stage in NH3_dict:
        ## melt the dataframe
        NH3_melt_ori = NH3_dict[Stage].melt(
            id_vars=["Name_abbre"],var_name="Prod", value_name="NH3_N")
        
        ## add name columns from FABIO
        NH3_melt_ori = NH3_melt_ori.merge(Country_APAMMO_FABIO_df,\
            left_on='Name_abbre',right_on='Name_abbre',how= 'left')
        NH3_melt_ori = NH3_melt_ori.merge(Item_APAMMO_FABIO_df,left_on='Prod',\
            right_on='AP-AMMO_prod',how= 'left')

        ## get the exact matching emissions data
        NH3_melt_Exact_dict[Stage] = NH3_melt_ori[
            NH3_melt_ori['Prod'].isin(Extact_matchtab_df['AP-AMMO_prod'])][['Name_ISO','Item_FABIO','FABIO_comm_code','Name_abbre','Prod','NH3_N']]
        

    ## Get the multiple products to one product matching data (only for stages connected to crops)
    ### calculate the items which are comprised of several crops in AP-AMMO
    
    for Stage in ['NH3_Syntfert',\
            'NH3_LiqMA_Crop','NH3_SldMA_Crop']:
        NH3_dict[Stage]['Maiz&Grenmaiz']= NH3_dict[Stage]['Maiz']+\
            NH3_dict[Stage]['Grenmaiz']
        NH3_dict[Stage]['Tempgra&Permgra']= NH3_dict[Stage]['Tempgra']+\
            NH3_dict[Stage]['Permgra']

    NH3_melt_Aggre_dict = {}
    for Stage in NH3_dict:
        ## melt the dataframe
        NH3_melt_ori = NH3_dict[Stage].melt(
            id_vars=["Name_abbre"], var_name="Prod", value_name="NH3_N")
        ## add name columns from FABIO
        NH3_melt_ori = NH3_melt_ori.merge(Country_APAMMO_FABIO_df,\
            left_on='Name_abbre',right_on='Name_abbre',how= 'left')
        NH3_melt_ori = NH3_melt_ori.merge(Item_APAMMO_FABIO_df,left_on='Prod',\
            right_on='AP-AMMO_prod',how= 'left')

        ## get the Multiple-to-one matching emissions data
        NH3_melt_Aggre_dict[Stage] = NH3_melt_ori
        print(NH3_melt_Aggre_dict[Stage])
        
        NH3_melt_Aggre_dict[Stage] = NH3_melt_ori[
            NH3_melt_ori['Prod'].isin(Aggre_matchtab_df['AP-AMMO_prod'])][['Name_ISO','Item_FABIO','FABIO_comm_code','Name_abbre','Prod','NH3_N']]
        

    ## Get the one product to multiple products matching data
    One_to_muti_prod = \
        Disaggre_matchtab_df['AP-AMMO_prod'].drop_duplicates().tolist() 

    NH3_disaggre_dict = {}

    ### filter the One-to-multiple products matching data
    for Stage in NH3_dict:
        df = NH3_dict[Stage]
        
        ## Filter columns that are in One_to_muti_prod
        cols_to_extract = [col for col in One_to_muti_prod if col in df.columns]
        
        ## Extract the subset DataFrame
        subset_df = df[cols_to_extract].copy()  # .copy() avoids reference issues
        
        ## Store in the result dictionary
        NH3_disaggre_dict[Stage] = subset_df


    ### convert the data from dataframes to lists, calculate and sort data as well
    NH3_disaggre_calc_dict={}
    NH3_disaggre_result_dict={}

    for Stage in NH3_disaggre_dict:
        # get the disaggregating factor lists
        NH3_disaggre_calc_dict[Stage] =\
            NH3_disaggre_dict[Stage].to_dict(orient ='list')
        # prepare the result dataframe
        NH3_disaggre_result_dict[Stage] ={}
        for Prod in NH3_disaggre_calc_dict[Stage]:
            # disaggregate NH3 according to disaggregating factors
            Disaggre_emi_array = Imp_func.np.array(
                NH3_disaggre_calc_dict[Stage][Prod])[:,Imp_func.np.newaxis] *\
                Imp_func.np.array(NH3_fac_disaggre_dict[Prod].iloc[:,2:])
            # re-assamble the dataframes
            Disaggre_emi_df = Imp_func.pd.DataFrame(Disaggre_emi_array)
            Disaggre_emi_df.columns=NH3_fac_disaggre_dict[Prod].columns[2:]
            Disaggre_emi_df.insert(0,'Name_ISO',Country_APAMMO_FABIO_df['Name_ISO'])
            # Melt the dataframe
            Disaggre_emi_melt_df =  Disaggre_emi_df.melt(
                id_vars=["Name_ISO"], var_name="Prod", value_name="NH3_N")
            # store the results in the result dictionary
            NH3_disaggre_result_dict[Stage][Prod] = Disaggre_emi_melt_df


    ### Sort the melted result to align with previous melted results
    NH3_melt_Disaggre_dict = {}

    for Stage in NH3_disaggre_result_dict:
        print(NH3_disaggre_result_dict[Stage].keys())
        # concat dataframes under the same stages
        NH3_melt_Disaggre_df = Imp_func.pd.concat(
            NH3_disaggre_result_dict[Stage].values(),ignore_index=True)
        # add additional informations to align with previous results
        NH3_melt_Disaggre_df = NH3_melt_Disaggre_df.merge(
            Item_APAMMO_FABIO_df[['Item_FABIO','FABIO_comm_code','AP-AMMO_prod']],\
            left_on='Prod',right_on='Item_FABIO',how='left')
        
        NH3_melt_Disaggre_df = NH3_melt_Disaggre_df.merge(
            Country_APAMMO_FABIO_df[['Name_ISO','Name_abbre']],\
            left_on='Name_ISO',right_on='Name_ISO',how='left')
        # extract the important columns
        NH3_melt_Disaggre_df = NH3_melt_Disaggre_df[['Name_ISO','Item_FABIO',\
            'FABIO_comm_code','Name_abbre','AP-AMMO_prod','NH3_N']]
        # change columns to fully align
        NH3_melt_Disaggre_df.columns = ['Name_ISO','Item_FABIO',\
            'FABIO_comm_code','Name_abbre','Prod','NH3_N']
        
        #save the results
        NH3_melt_Disaggre_dict[Stage] = NH3_melt_Disaggre_df


    ## Integrate products from different groups by stage
    NH3_standard_allo_dict = {}

    for Stage in list(NH3_melt_Exact_dict.keys()):
        NH3_melt_total = Imp_func.pd.concat(
            [NH3_melt_Exact_dict[Stage],NH3_melt_Aggre_dict[Stage],\
            NH3_melt_Disaggre_dict[Stage]],ignore_index= True)
        # set a common field as the standard allocation table
        NH3_melt_total['ISO_country-itemcode'] = NH3_melt_total['Name_ISO'] + '_' + \
            NH3_melt_total['FABIO_comm_code']
        # connect
        N_standard_allo_df = Imp_func.pd.merge(NH3Nflow_temp_df,NH3_melt_total,\
            how='left',on='ISO_country-itemcode')
        # save in a  dictionary
        NH3_standard_allo_dict[Stage] = N_standard_allo_df 


    #----------------------------------------------------output_module----------------------------------------------------
    # OUTPUT_FILE
    for Stage in NH3_standard_allo_dict:
        NH3_standard_allo_dict[Stage].to_excel(
            FABIO_pj_path.Prj_Gene_output_wd+\
            f'{Scenario}_NH3_Allo_ForConsum/'+Stage+'_NH3_allocation.xlsx',index=False)
        
    return
