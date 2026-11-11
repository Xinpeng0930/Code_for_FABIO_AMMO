# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)


# GAINS data extraction (prep stage): technical mitigation factors, adoption
# rates and UNFCCC emission tables for the MTFR scenarios.
# Functions:
#   Obtain_GAINS_para(scenario)         technical factors and mitigation parameters
#   Obtain_GAINS_UNFCCC_Emi(scenario)   UNFCCC emission tables
#   Obtain_GAINS_ByStage_Emi(scenario)  by-stage animal emission tables
# The GAINS extracts are read from the AP-AMMO input database (IIASA GAINS);
# the scenario parameters are documented in the Methods and Supplementary Information.

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Fir_Pj_path
from APSP_proc import Z_fabio_prj_paths as Sec_Pj_path


#%%

def Obtain_GAINS_para(GAINS_Scen):
    ## Path to GAINS model data
    if GAINS_Scen == 'MTSF_2050':
        GAINS_OriAba_EFs_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_factors_MTFR/*.csv',\
                recursive=False)) # Useful table 3 in our note

        GAINS_Mitirate_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_measures_rates_MTFR/*.csv',\
                recursive=False)) # Useful table 5 in our note

        Para_list = ['Unabated emission factor [kt/unit]',\
            'Abated emission factor [kt/unit]', ' Capacities controlled [%]']
        
    elif GAINS_Scen == 'NAPCP_2050':
        GAINS_OriAba_EFs_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
        Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_factors_NAPCP2050/*.csv',\
            recursive=False))

        GAINS_Mitirate_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_measures_rates_NAPCP2050/*.csv',\
                recursive=False))
        
        Para_list = ['Unabated emission factor',\
            'Abated emission factor', ' Capacities controlled']


    elif GAINS_Scen == 'Base_2050':
        GAINS_OriAba_EFs_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_factors_base2050/*.csv',\
                recursive=False))
        
        GAINS_Mitirate_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_measures_rates_base2050/*.csv',\
                recursive=False))
        
        Para_list = ['Unabated emission factor [kt/unit]',\
            'Abated emission factor [kt/unit]', ' Capacities controlled [%]']

    elif GAINS_Scen == 'Base_2020':
        GAINS_OriAba_EFs_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_factors_base2020/*.csv',\
                recursive=False))
        
        GAINS_Mitirate_livstkstage_wddt = Imp_func.dict_name_path(Fir_Pj_path.Country_name_abbr,\
            Imp_func.glob.glob(Fir_Pj_path.Input_prj_wd+r'Air_pollution_database/Database_collection/GAINS/Technical_measures_rates_base2020/*.csv',\
                    recursive=False))
        
        Para_list = ['Unabated emission factor [kt/unit]',\
            'Abated emission factor [kt/unit]', ' Capacities controlled [%]']
                
                
    ## Export GAINS data
    ### Get targeted emission data
    #OUTPUT_DATA
    Keep_rows = ['Dairy cows - liquid systems','Dairy cows - solid systems',\
        'Other cattle - liquid systems','Other cattle - solid systems',\
        'Pigs - liquid systems','Pigs - solid systems',\
        'Laying hens','Other poultry',\
            'Sheep and goats']

    Keep_ferti_rows = ['Mineral N fertilizers use (excl. urea)',\
        'Urea application (incl. ABC)']

    ### Get the stage-specific emissions from table 3 (not techology adoption rate specific)
    Livestk_OriAba_EFbystage_dt = {}
    for Country in GAINS_OriAba_EFs_livstkstage_wddt:
        df =Imp_func.pd.read_csv(GAINS_OriAba_EFs_livstkstage_wddt[Country],skiprows=8,sep=',')
        Livestk_Emi_bystage_df = df[df['Fuel'].isin(Keep_rows)]
        Livestk_Emi_bystage_df['Ani_tech'] = Livestk_Emi_bystage_df['Fuel'] + '_' + \
            Livestk_Emi_bystage_df['Technology']
        Livestk_OriAba_EFbystage_dt[Country] = Livestk_Emi_bystage_df

    ### Get technology adoption rates and emissions by livestock type (not stage specific)
    Livestk_Mitirate_bystage_dt = {}
    for Country in GAINS_Mitirate_livstkstage_wddt:
        df2 = Imp_func.pd.read_csv(GAINS_Mitirate_livstkstage_wddt[Country],skiprows=8,sep=',')
        df2 = df2[df2['Sector'] != 'Milk yield over 3000 kg/animal treshold']
        Livestk_techrate_df = df2[df2['Fuel activity'].isin(Keep_rows)]
        Livestk_techrate_df['Ani_tech'] =  Livestk_techrate_df['Fuel activity'] + '_' + \
            Livestk_techrate_df['Measure']
        Livestk_Mitirate_bystage_dt[Country] = Livestk_techrate_df 
        
    Syntfert_Mitirate_bystage_dt = {}
    for Country in GAINS_Mitirate_livstkstage_wddt:
        df_synt = Imp_func.pd.read_csv(GAINS_Mitirate_livstkstage_wddt[Country],skiprows=8,sep=',')
        df_synt = df_synt[df_synt['Sector'].isin(Keep_ferti_rows)]
        df_synt['Country'] = Country
        
        Syntfert_Mitirate_bystage_dt[Country] = \
            df_synt

    Syntfert_combined_df = Imp_func.pd.concat(Syntfert_Mitirate_bystage_dt.values(),\
        ignore_index=False)

    Syntfert_combined_df.to_excel(Sec_Pj_path.Prj_Gene_output_wd+\
            f'Syntfert_Mititech_Capa_{GAINS_Scen}.xlsx',\
            sheet_name='Sheet1')


    
    # OUTPUT_DATA
    Livstk_Mititech_StageEF_rate_dt = {}
    for Country in GAINS_OriAba_EFs_livstkstage_wddt:
        df3 =  Imp_func.pd.merge(Livestk_OriAba_EFbystage_dt[Country],\
            Livestk_Mitirate_bystage_dt[Country],how='left',\
            on='Ani_tech')
        df3_new = df3[['Fuel','Sector_x','Technology','Ani_tech','HOUSING',\
            'STORAGE','APPLICATION','GRAZING']+ Para_list]
        df3_new2 =  df3_new[df3_new[Para_list[-1]] != 0.0]
        ### make sure the following fields are numeric
        for col in ['HOUSING',\
            'STORAGE','APPLICATION','GRAZING']+Para_list:
            df3_new2[col] = Imp_func.pd.to_numeric(df3_new2[col], errors='coerce')
        ### drop the technologies without implementations
        df3_new2 = df3_new2.dropna(subset=[Para_list[0]])
        ### Get the technology specific emission factors
        df3_new2['Tech_spec_abated_EFs'] = df3_new2[Para_list[1]] * \
            df3_new2[Para_list[-1]] / 100
        ### Get the technology and stage specific emission factors
        df3_new2['Tech_hous_abated_EFs'] = df3_new2['HOUSING'] * \
            df3_new2[Para_list[-1]] / 100 / 1000
        df3_new2['Tech_stor_abated_EFs'] = df3_new2['STORAGE'] * \
            df3_new2[Para_list[-1]] / 100 / 1000
        df3_new2['Tech_app_abated_EFs'] = df3_new2['APPLICATION'] * \
            df3_new2[Para_list[-1]] / 100 / 1000
        df3_new2['Tech_graz_abated_EFs'] = df3_new2['GRAZING'] * \
            df3_new2[Para_list[-1]] / 100 / 1000
        
        df3_new2 ['Country'] = Country
        ### add country names
        Livstk_Mititech_StageEF_rate_dt[Country] = df3_new2 


    ### Export the original sorted technology EFs
    # OUTPUT_FILE
    with Imp_func.pd.ExcelWriter(Sec_Pj_path.Prj_Gene_output_wd+\
            f'MitiEF_Techrate_byStage_{GAINS_Scen}.xlsx',\
            engine='xlsxwriter') as writer:
            # Iterate over the dictionary and write each DataFrame to a sheet
            for sheet_name, df in Livstk_Mititech_StageEF_rate_dt.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)


    ### Export the original sorted technology EFs with all sheets combined
    Pivot_combined_techcapa_df = Imp_func.pd.concat(
        Livstk_Mititech_StageEF_rate_dt.values(),\
        ignore_index=False)


    Pivot_combined_techcapa_new_df = Pivot_combined_techcapa_df[['Fuel',
    'Sector_x','Technology',
    'Ani_tech'] + Para_list + [
        'Tech_spec_abated_EFs',
        'Tech_hous_abated_EFs','Tech_stor_abated_EFs',\
        'Tech_app_abated_EFs','Tech_graz_abated_EFs','Country']]

    # OUTPUT_FILE
    Pivot_combined_techcapa_new_df.to_excel(Sec_Pj_path.Prj_Gene_output_wd+\
            f'Pivot_Mititech_Capa_{GAINS_Scen}.xlsx',sheet_name='Sheet1')


    #OUTPUT_DATA
    ### Pivot EFs with technologies by animal-manure
    Pivot_Mititech_dt = {}

    for Country in Livstk_Mititech_StageEF_rate_dt:
        Pivot_df = Imp_func.pd.pivot_table(Livstk_Mititech_StageEF_rate_dt[Country],\
            index=[u'Fuel'], values=[u'Tech_spec_abated_EFs','Tech_hous_abated_EFs','Tech_stor_abated_EFs',\
                                       'Tech_app_abated_EFs','Tech_graz_abated_EFs'],\
            aggfunc=[Imp_func.np.sum],fill_value=0)
        
        Pivot_df.columns = Pivot_df.columns.get_level_values(1).tolist()
        Pivot_df_new = Pivot_df[['Tech_spec_abated_EFs','Tech_hous_abated_EFs','Tech_stor_abated_EFs',\
                                'Tech_app_abated_EFs','Tech_graz_abated_EFs']]
        
        Pivot_df_new['Country'] = Country
        
        Pivot_Mititech_dt[Country] = Pivot_df_new

    ### put all tables together
    Pivot_combined_df = Imp_func.pd.concat(Pivot_Mititech_dt.values(),\
        ignore_index=False)


    # OUTPUT_FILE
    Pivot_combined_df.to_excel(Sec_Pj_path.Prj_Gene_output_wd+\
            f'Pivot_Mititech_{GAINS_Scen}.xlsx',sheet_name='Sheet1')


    ### Unabated EFs with technologies by animal-manure
    Unabated_Mititech_dt = {}

    for Country in Livstk_Mititech_StageEF_rate_dt:
        Pivot_Unabated_df = Imp_func.pd.pivot_table(Livstk_Mititech_StageEF_rate_dt[Country],\
            index=[u'Fuel'], values=[Para_list[0]],\
            aggfunc=[Imp_func.np.mean],fill_value=0)
        
        Pivot_Unabated_df.columns = ['Unabated_EFs']
        Pivot_Unabated_df['Country'] = Country
        
        Unabated_Mititech_dt[Country] = Pivot_Unabated_df


    Pivot_Unabated_combined_df = Imp_func.pd.concat(
        Unabated_Mititech_dt.values(),\
        ignore_index=False)


    # OUTPUT_FILE
    Pivot_Unabated_combined_df.to_excel(Sec_Pj_path.Prj_Gene_output_wd+\
            f'Pivot_Unabated_Mititech_{GAINS_Scen}.xlsx',sheet_name='Sheet1')
    
    return


# %%
def Obtain_GAINS_UNFCCC_Emi(GAINS_Scen):
    Keep_rows = ['Dairy cattle_Manure management',\
            'Non_dairy cattle_ Manure management',\
            'Swine_Manure management',\
            'Sheep_Manure management',\
            'Laying hens_Manure management',\
            'Other poultry_Manure management',\
            'N-fertilizer']
    
    ## Path to GAINS model data
    if GAINS_Scen == 'MTSF_2050':
        _folder = Fir_Pj_path.Input_prj_wd + \
            r'Air_pollution_database/Database_collection/GAINS/UNFCCC_SectEmi_MTFR/'
        GAINS_UNFCCC_Emi_wddt = {
            Country: _folder + f'{Country}_emiss_nfr_detailed.csv'
            for Country in Fir_Pj_path.Country_name_abbr
        }

        ### Get targeted emission data
        #OUTPUT_DATA
        ### Get the stage-specific emissions from table 3 (not techology adoption rate specific)
        GAINS_UNFCCC_Emi_dt = {}

        for Country in GAINS_UNFCCC_Emi_wddt:
            if Country == 'LI':
                continue
            df = Imp_func.pd.read_csv(GAINS_UNFCCC_Emi_wddt[Country],\
                skiprows=8, sep=',', on_bad_lines='skip')[['[kt/yr]','2050']]
            UNFCCC_Emi_df = df[df['[kt/yr]'].isin(Keep_rows)]
            UNFCCC_Emi_df['Country'] = Country
            GAINS_UNFCCC_Emi_dt[Country] = UNFCCC_Emi_df

        GAINS_UNFCCC_Emi_combined_df = Imp_func.pd.concat(
            GAINS_UNFCCC_Emi_dt.values(),\
            ignore_index=False)
    
    elif GAINS_Scen == 'Base':
        GAINS_UNFCCC_Emi_wd = Fir_Pj_path.Input_prj_wd+\
            r'Air_pollution_database/Database_collection/GAINS/UNFCCC_SectEmi_Base/Ammonia_by_sector.xlsx'

        GAINS_UNFCCC_Emi_dt = {}

        for Country in [name + \
            '2015' for name in Fir_Pj_path.Country_name_abbr]:
            if Country == 'LI2015':
                continue
            
            df = Imp_func.pd.read_excel(GAINS_UNFCCC_Emi_wd,\
                sheet_name=Country)[['[kt/yr]',2020,2050]]
            
            UNFCCC_Emi_df = df[df['[kt/yr]'].isin(Keep_rows)]
            
            UNFCCC_Emi_df['Country'] = Country
            
            GAINS_UNFCCC_Emi_dt[Country] = UNFCCC_Emi_df

        GAINS_UNFCCC_Emi_combined_df = Imp_func.pd.concat(
            GAINS_UNFCCC_Emi_dt.values(),\
            ignore_index=False)

    GAINS_UNFCCC_Emi_combined_df.to_excel(
        Sec_Pj_path.Prj_Gene_output_wd+\
        f'GAINS_UNFCCC_Emi_{GAINS_Scen}.xlsx',sheet_name='Sheet1')
    
    return


# %%

def Obtain_GAINS_ByStage_Emi(GAINS_Scen):
    #OUTPUT_DATA
    Keep_rows = ['Dairy cows - liquid systems','Dairy cows - solid systems',\
        'Other cattle - liquid systems','Other cattle - solid systems',\
        'Pigs - liquid systems','Pigs - solid systems',\
        'Laying hens','Other poultry',\
            'Sheep and goats']
    
    
    ### Get the stage-specific emissions from table 2
    path_name_map = {'Base_2050': 'base2050', 'MTSF_2050': 'MTFR2050'}
   
    if GAINS_Scen in path_name_map:
        _folder = Fir_Pj_path.Input_prj_wd + \
            f'Air_pollution_database/Database_collection/GAINS/Ani_Emi_byStage_{path_name_map[GAINS_Scen]}/'
        GAINS_StageSpec_Emi_wddt = {
            Country: _folder + f'{Country}_emi_sum_stages_NH3.csv'
            for Country in Fir_Pj_path.Country_name_abbr
        }

        Livestk_Emibystage_dt = {}
        for Country in GAINS_StageSpec_Emi_wddt:
            if Country == 'LI':
                continue
            df = Imp_func.pd.read_csv(GAINS_StageSpec_Emi_wddt[Country],\
                skiprows=8, sep=',', on_bad_lines='skip')
            Livestk_Emi_bystage_df = df[df['Animals'].isin(Keep_rows)]
            Livestk_Emi_bystage_new_df = Livestk_Emi_bystage_df[['Animals',\
                'HOUSING','STORAGE','APPLICATION','GRAZING']]
            Livestk_Emi_bystage_new_df['Country'] = Country
            Livestk_Emibystage_dt[Country] = Livestk_Emi_bystage_new_df

    elif GAINS_Scen == 'Base_2015':
        GAINS_StageSpec_Emi_wd = Fir_Pj_path.Input_prj_wd+\
            r'Air_pollution_database/Database_collection/GAINS/Ani_Emi_byStage_base2015/Animal_by_stage.xlsx'

        Livestk_Emibystage_dt = {}

        for Country in [name + \
            '2015' for name in Fir_Pj_path.Country_name_abbr]:
            if Country == 'LI2015':
                continue
            
            df = Imp_func.pd.read_excel(GAINS_StageSpec_Emi_wd,\
                sheet_name=Country)
            
            Livestk_Emi_bystage_df = df[df['Animals'].isin(Keep_rows)]

            Livestk_Emi_bystage_new_df = Livestk_Emi_bystage_df[['Animals',\
                'HOUSING','STORAGE','APPLICATION','GRAZING']]
            
            Livestk_Emi_bystage_new_df['Country'] = Country
            
            Livestk_Emibystage_dt[Country] = Livestk_Emi_bystage_new_df

    Livestk_Emibystage_combined_df = Imp_func.pd.concat(
                Livestk_Emibystage_dt.values(),\
                ignore_index=False)

    Livestk_Emibystage_combined_df.to_excel(
            Sec_Pj_path.Prj_Gene_output_wd+\
            f'{GAINS_Scen}_GAINS_byStage_Emi.xlsx',\
            sheet_name='Sheet1')
    
    return


if __name__ == "__main__":
    # sequence used for the release
    for _scen in ("MTSF_2050", "Base"):
        Obtain_GAINS_UNFCCC_Emi(_scen)
    for _scen in ("Base_2050", "MTSF_2050", "Base_2015"):
        Obtain_GAINS_ByStage_Emi(_scen)
