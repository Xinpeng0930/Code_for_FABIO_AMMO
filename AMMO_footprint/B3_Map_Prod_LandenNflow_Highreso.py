# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# B3_Map_Prod_LandenNflow_Highreso — high-resolution production, land and N-flow maps

'''
Calibrate high-resolution N-flow rasters using production-side FABIO targets.
Preparation (base maps + FABIO targets) is performed by B2; this script
only handles the calibration step.
'''

#%%
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path


# %%

def Calibrate_LandenNflow_Diet(Scenarios_Name):
    '''
    Calibrate AP-AMMO N-flow rasters to FABIO production-side targets for the
    given dietary scenario.  Delegates all preparation to B2.Prep_Nflow_Diet.
    '''
    # ------------------------------------------------------ preparation
    Calibase_map_dt = Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
        'N_flow_AP-AMMO_Map_CaliBase.pkl')['Base_map'] # from B2
    
    Target_flow_dt =Imp_func.open_plk(FABIO_pj_path.Prj_Pkl_output_wd+\
        'N_flow_AP-AMMO_Map_CaliBase.pkl')['Target_flow'] # from B2
    
    AMMO_Nflow_Important_shetname = [
        'N_coupl_Syntfert',
        'N_coupl_ManrInhous_Liqexcr_Liv',
        'N_coupl_ManrInhous_Sldexcr_Liv',
        'N_coupl_ManrGraz_excr_Liv',
        'N_coupl_LiqMA_Crop',
        'N_coupl_SldMA_Crop',
        'N_coupl_LiqMA_Liv',
        'N_coupl_SldMA_Liv',
        'Land']

    FABIO_CropName_list   = [
        'Whea', 'Barl', 'Maiz&Grenmaiz', 'Legufod', 'Rapesd', 'Sunflrsd', 'Soya',
        'Oats', 'Rice', 'Rye', 'Pota', 'Sugbt', 'Peabean', 'Nuts', 'Fruit', 'Vege',
        'Tempgra&Permgra']
    FABIO_CropManr_list   = [
        'Whea', 'Barl', 'Maiz&Grenmaiz', 'Rapesd', 'Sunflrsd',
        'Oats', 'Rye', 'Pota', 'Sugbt', 'Nuts', 'Fruit', 'Vege',\
        'Tempgra&Permgra']
    
    FABIO_LivestkName_list =  ['Pig', 'Dair', 'Othcatl', 'Shep', 'Goat', 'Potr']
    
    
    if Scenarios_Name in ['EAT','EAT_Meat',\
                          'EAT_Vegan']:
        Basemap_Summar_wd     = Calibase_map_dt['CURR']['LandenNflow_map_summary']
        Basemap_for_Cali_wddt = Calibase_map_dt['CURR']['LandenNflow_maps']
        Target_Summar_wd      = Target_flow_dt[Scenarios_Name]

    elif Scenarios_Name == 'MTFR_EAT':
        Basemap_Summar_wd     = Calibase_map_dt['CURR_MTFR']['LandenNflow_map_summary']
        Basemap_for_Cali_wddt = Calibase_map_dt['CURR_MTFR']['LandenNflow_maps']
        Target_Summar_wd      = Target_flow_dt[Scenarios_Name]
        
    
    Higreso_path = FABIO_pj_path.Prj_Rster_output_wd + r'Nflow_' + Scenarios_Name + r'_'

    
    #--------------------------------------------------------target data

    ### get targeting emissions from FABIO
    Nflow_FABIO_extr_dt = {}
    for Stage in AMMO_Nflow_Important_shetname:
        Useful_FABIO_ProdN_flow = Imp_func.pd.read_excel(Target_Summar_wd,\
            sheet_name=Stage)
        
        #### reindex the dataframe to align with the AP-AMMO dataframe
        New_col_order = ['Whea', 'Barl', 'Maiz&Grenmaiz', \
            'Legufod','Rapesd', 'Sunflrsd','Soya', \
            'Oats', 'Rice', 'Rye','Pota','Sugbt','Peabean','Nuts',\
            'Fruit', 'Vege', 'Tempgra&Permgra', 'Pig', 'Dair','Othcatl','Shep',\
            'Goat','Potr']

        Useful_FABIO_ProdN_flow = Useful_FABIO_ProdN_flow.reindex(
            columns=New_col_order)
        Useful_FABIO_ProdN_flow.reset_index(drop=True,inplace=True)

        #### only get useful columns in each stage
        if Stage in ['N_coupl_Syntfert','Land']:
            Useful_FABIO_ProdN_new = Useful_FABIO_ProdN_flow[FABIO_CropName_list]
            
        elif Stage in ['N_coupl_LiqMA_Crop','N_coupl_SldMA_Crop']:
            Useful_FABIO_ProdN_new  = Useful_FABIO_ProdN_flow[FABIO_CropManr_list]
            
        elif Stage in ['N_coupl_ManrInhous_Liqexcr_Liv', \
            'N_coupl_ManrInhous_Sldexcr_Liv','N_coupl_LiqMA_Liv','N_coupl_SldMA_Liv']:
            Useful_FABIO_ProdN_new  = Useful_FABIO_ProdN_flow[FABIO_LivestkName_list]
        
        elif Stage in ['N_coupl_ManrGraz_excr_Liv']:
            Useful_FABIO_ProdN_new  = Useful_FABIO_ProdN_flow[['Dair','Othcatl','Shep','Goat']]

        Nflow_FABIO_extr_dt[Stage] = Useful_FABIO_ProdN_new 
        print(list(Useful_FABIO_ProdN_new.columns))


    # ------------------------------------------------------ AP-AMMO N flows
    Nflow_APAMMO_dt = {}
    
    for Stage in AMMO_Nflow_Important_shetname:
        Nflow_AMMO_df = Imp_func.pd.read_excel(Basemap_Summar_wd,\
            sheet_name=Stage)
        Nflow_AMMO_df.columns = [c.capitalize() for c in Nflow_AMMO_df.columns]

        if Stage in ['N_coupl_Syntfert','Land']:
            Nflow_AMMO_df['Maiz&Grenmaiz'] = Nflow_AMMO_df['Maiz']  +\
                Nflow_AMMO_df['Grenmaiz']
            Nflow_AMMO_df['Tempgra&Permgra'] = Nflow_AMMO_df['Tempgra'] +\
                Nflow_AMMO_df['Permgra']
            Nflow_AMMO_df = Nflow_AMMO_df.drop(columns=['Maiz', \
                'Grenmaiz', 'Tempgra', 'Permgra'])
            Nflow_AMMO_df =  Nflow_AMMO_df.rename(columns={'Legumfod': 'Legufod'})
            print(list(Nflow_AMMO_df.columns))

            print(list(Nflow_FABIO_extr_dt[Stage].columns))
            Nflow_AMMO_df = Nflow_AMMO_df.reindex(
                columns=  list(Nflow_FABIO_extr_dt[Stage].columns)) 
            
            
        elif Stage in ['N_coupl_LiqMA_Crop', 'N_coupl_SldMA_Crop']:
            Nflow_AMMO_df['Maiz&Grenmaiz']   = Nflow_AMMO_df['Maiz'] +\
                Nflow_AMMO_df['Grenmaiz']
            Nflow_AMMO_df['Tempgra&Permgra'] = Nflow_AMMO_df['Tempgra'] +\
                Nflow_AMMO_df['Permgra']
            Nflow_AMMO_df = Nflow_AMMO_df.drop(columns=['Maiz', \
                'Grenmaiz', 'Tempgra', 'Permgra'])
            print(list(Nflow_AMMO_df.columns))
            
            print(list(Nflow_FABIO_extr_dt[Stage].columns))
            Nflow_AMMO_df = Nflow_AMMO_df.reindex(
                columns=  list(Nflow_FABIO_extr_dt[Stage].columns))

        elif Stage in ['N_coupl_ManrInhous_Liqexcr_Liv',\
                        'N_coupl_ManrInhous_Sldexcr_Liv',\
                       'N_coupl_LiqMA_Liv', 'N_coupl_SldMA_Liv']:

            Nflow_AMMO_df = Nflow_AMMO_df[FABIO_LivestkName_list]
            print(list(Nflow_AMMO_df.columns))

        elif Stage == 'N_coupl_ManrGraz_excr_Liv':
            Nflow_AMMO_df = Nflow_AMMO_df[['Dair', 'Othcatl', 'Shep', 'Goat']]
            print(list(Nflow_AMMO_df.columns))

        Nflow_AMMO_Num_df = Nflow_AMMO_df[list(Nflow_AMMO_df.columns)]
        Nflow_APAMMO_dt[Stage] = Nflow_AMMO_Num_df
        print(list(Nflow_AMMO_Num_df.columns))

    
    
    # ------------------------------------------------------ calibration factors
    Fac_cali_dt = {}

    for Stage in Nflow_FABIO_extr_dt:
        Nflow_AMMO_matrix = Imp_func.np.array(Nflow_APAMMO_dt[Stage])
        Nflow_targ_matrix = Imp_func.np.array(Nflow_FABIO_extr_dt[Stage])

        Fac_cali = Imp_func.np.zeros_like(Nflow_AMMO_matrix, dtype=float)
        nonzero  = Nflow_AMMO_matrix != 0
        Fac_cali[nonzero] = Nflow_targ_matrix[nonzero] / Nflow_AMMO_matrix[nonzero]

        Fac_cali_df = Imp_func.pd.DataFrame(Fac_cali)
        Fac_cali_df.columns = list(Nflow_FABIO_extr_dt[Stage].columns)

        if Stage in ['N_coupl_Syntfert', 'N_coupl_LiqMA_Crop',\
            'N_coupl_SldMA_Crop', 'Land']:
            New_columns = Imp_func.pd.DataFrame({
                'Grenmaiz': Fac_cali_df['Maiz&Grenmaiz'],
                'Tempgras': Fac_cali_df['Tempgra&Permgra'],
            })
            Fac_cali_new_df = Imp_func.pd.concat(
                [Fac_cali_df.iloc[:, :3], New_columns, Fac_cali_df.iloc[:, 3:]], axis=1)
        else:
            Fac_cali_new_df = Fac_cali_df

        Fac_cali_new_df.insert(0, 'Country', Air_pj_path.Country_name_abbr)
        Fac_cali_dt[Stage] = Fac_cali_new_df

    # OUTPUT_FILE — write calibration factor check
    with Imp_func.pd.ExcelWriter(
        FABIO_pj_path.Prj_Gene_output_wd +\
        f'{Scenarios_Name}_Highreso_Nflow_califac_check.xlsx',
        engine='xlsxwriter',
    ) as writer:
        for sheet_name, df in Fac_cali_dt.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # ------------------------------------------------------ apply calibrations
    '''
    N_coupl_ManrGraz_excr_Gras = Fac_cali_dt['N_coupl_LiqMA_Crop'][['Country', 'Tempgras', 'Tempgra&Permgra']]
    Fac_cali_dt['N_coupl_ManrGraz_excr_Gras'] = N_coupl_ManrGraz_excr_Gras
    '''
    for Stage in list(Fac_cali_dt.keys()):
        Nflow_fac_data = Fac_cali_dt[Stage].fillna(0)

        if Stage in ['N_coupl_Syntfert']:
            for Prod in Air_pj_path.MainCpNam:
                Imp_func.cali_fig_filter(
                    Basemap_for_Cali_wddt[Stage][Prod],
                    Air_pj_path.Exam_crop_reson_wd,
                    Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                    Nflow_fac_data.columns.tolist()[
                        list(Basemap_for_Cali_wddt[Stage].keys()).index(Prod) + 1],
                    0.0833333333333333,
                    Higreso_path + Stage.split('_')[2] + '_byprod/' +
                    Prod + f'_{Scenarios_Name}_' + Stage.split('_')[2] + '_Nflow.tif',
                )
        
        elif Stage in ['Land']:
            Imp_func.os.makedirs(Higreso_path + Stage + '_byprod', exist_ok=True)
            for Prod in Air_pj_path.MainCpNam:
                Imp_func.cali_fig_filter(
                        Basemap_for_Cali_wddt[Stage][Prod],
                        Air_pj_path.Exam_crop_reson_wd,
                        Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                        Nflow_fac_data.columns.tolist()[
                            list(Basemap_for_Cali_wddt[Stage].keys()).index(Prod) + 1],
                        0.0833333333333333,
                        Higreso_path + Stage + '_byprod/' +
                        Prod + f'_{Scenarios_Name}_' + Stage + '_flow.tif',
                    )
            
        
        elif Stage in ['N_coupl_LiqMA_Crop', 'N_coupl_SldMA_Crop']:
            for Prod in Imp_func.del_elemt_list(Air_pj_path.MainCpNam, [5, 8, 10, 14]):
                Imp_func.cali_fig_filter(
                    Basemap_for_Cali_wddt[Stage][Prod],
                    Air_pj_path.Exam_crop_reson_wd,
                    Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                    Nflow_fac_data.columns.tolist()[
                        list(Basemap_for_Cali_wddt[Stage].keys()).index(Prod) + 1],
                    0.0833333333333333,
                    Higreso_path + Stage.split('_')[2] + '_' + Stage.split('_')[3] +
                    '_byprod/' + Prod + f'_{Scenarios_Name}_' + Stage.split('_')[2] + '_Nflow.tif',
                )

        elif Stage in ['N_coupl_ManrInhous_Liqexcr_Liv', 'N_coupl_ManrInhous_Sldexcr_Liv',
                       'N_coupl_LiqMA_Liv', 'N_coupl_SldMA_Liv']:
            for Prod in Air_pj_path.Ani_name:
                Imp_func.cali_fig_filter(
                    Basemap_for_Cali_wddt[Stage][Prod],
                    Air_pj_path.Exam_crop_reson_wd,
                    Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                    Nflow_fac_data.columns.tolist()[
                        list(Basemap_for_Cali_wddt[Stage].keys()).index(Prod) + 1],
                    0.0833333333333333,
                    Higreso_path + Stage.split('_')[2] + '_' + Stage.split('_')[3] +
                    '_byprod/' + Prod + f'_{Scenarios_Name}_' + Stage.split('_')[0] + '_Nflow.tif',
                )

        elif Stage == 'N_coupl_ManrGraz_excr_Liv':
            for Prod in ['dair', 'othcatl', 'shep', 'goat']:
                Imp_func.cali_fig_filter(
                   Basemap_for_Cali_wddt[Stage][Prod],
                    Air_pj_path.Exam_crop_reson_wd,
                    Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                    Nflow_fac_data.columns.tolist()[
                        list(Basemap_for_Cali_wddt[Stage].keys()).index(Prod) + 1],
                    0.0833333333333333,
                    Higreso_path + Stage.split('_')[2] + '_byprod/' +
                    Prod + f'_{Scenarios_Name}_' + Stage.split('_')[0] + '_Nflow.tif',
                )
        '''
        elif Stage == 'N_coupl_ManrGraz_excr_Gras':
            for Prod in ['Tempgra', 'Permgra']:
                Imp_func.cali_fig_filter(
                    Nflow_byprod_wddt[Stage][Prod],
                    Air_pj_path.Exam_crop_reson_wd,
                    Air_pj_path.EFTA_UK_wd, Nflow_fac_data, 'FID_1', 'Country',
                    Nflow_fac_data.columns.tolist()[
                        list(Nflow_byprod_wddt[Stage].keys()).index(Prod) + 1],
                    0.0833333333333333,
                    Higreso_path + Stage.split('_')[2] + '_' + Stage.split('_')[4] +
                    '_byprod/' + Prod + f'_{Scenarios_Name}_' + Stage.split('_')[0] + '_Nflow.tif',
                )'''

    return



# %%

# ---------------------------------------------------------------------------
# Summa_Nflow_Highreso  — zonal statistics and stage aggregation
# ---------------------------------------------------------------------------

def Summa_Nflow_Highreso(Scenarios_Name):
    # Scenario-based path setup
    if Scenarios_Name == 'EAT':
        Aggre_path      = FABIO_pj_path.Prj_Rster_output_wd + r'Nflow_' + Scenarios_Name + '_bystage/'
        Summar_path     = FABIO_pj_path.Prj_Gene_output_wd + 'EAT_Nflow_byProdStage.xlsx'
        Summar_aggre_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_AggreStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + 'EAT_Nflow_byProdStage.pkl'

    elif Scenarios_Name == 'EAT_Meat':
        Aggre_path      = FABIO_pj_path.Prj_Rster_output_wd + r'Nflow_' + Scenarios_Name + '_bystage/'
        Summar_path     = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.xlsx'
        Summar_aggre_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_AggreStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl'

    elif Scenarios_Name == 'MTFR_EAT':
        Aggre_path      = FABIO_pj_path.Prj_Rster_output_wd + r'Nflow_' + Scenarios_Name + '_bystage/'
        Summar_path     = FABIO_pj_path.Prj_Gene_output_wd + 'MTFR_EAT_Nflow_byProdStage.xlsx'
        Summar_aggre_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_AggreStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + 'MTFR_EAT_Nflow_byProdStage.pkl'

    elif Scenarios_Name in ['EAT', \
        'EAT_Vegan', 'EAT_Meat']:
        Aggre_path      = FABIO_pj_path.Prj_Rster_output_wd + r'Nflow_' + Scenarios_Name + '_bystage/'
        Summar_path     = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.xlsx'
        Summar_aggre_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_Nflow_AggreStage.xlsx'
        Summar_pkl_path = FABIO_pj_path.Prj_Pkl_output_wd + f'{Scenarios_Name}_Nflow_byProdStage.pkl'

    # Collect N flows for all scenarios
    def collect_emissions(prefix):
        base_path = './AMMO_footprint/Output_raster'
        get = lambda stage: Imp_func.glob.glob(
            f'{base_path}/Nflow_{prefix}_{stage}_byprod/*.tif', recursive=False)

        
        dict_list_rough = {
            'Syntfert':     get('Syntfert'),
            'ManrInhous':   get('ManrInhous_Liqexcr') + get('ManrInhous_Sldexcr'),
            'ManrApp':      get('LiqMA_Liv') + get('SldMA_Liv'),
            'ManrApp_crop': get('LiqMA_Crop') + get('SldMA_Crop'),
            'ManrDepo':     get('ManrGraz'),
            'ManrDepo_gras': get('ManrGraz_Gras'),
            'Land': get('Land')
        }
        dict_dict_fine = {
            'Syntfert':      Imp_func.dict_name_path(Air_pj_path.MainCpNam, get('Syntfert')),
            'Liqinhous':     Imp_func.dict_name_path(Air_pj_path.Ani_name, get('ManrInhous_Liqexcr')),
            'Sldinhous':     Imp_func.dict_name_path(Air_pj_path.Ani_name, get('ManrInhous_Sldexcr')),
            'LiqApp':        Imp_func.dict_name_path(Air_pj_path.Ani_name, get('LiqMA_Liv')),
            'SldApp':        Imp_func.dict_name_path(Air_pj_path.Ani_name, get('SldMA_Liv')),
            'LiqApp_crop':   Imp_func.dict_name_path(Air_pj_path.MainCpNam, get('LiqMA_Crop')),
            'SldApp_crop':   Imp_func.dict_name_path(Air_pj_path.MainCpNam, get('SldMA_Crop')),
            'Manrdepo':      Imp_func.dict_name_path(Air_pj_path.Ani_name, get('ManrGraz')),
            'Manrdepo_gras': Imp_func.dict_name_path(['Tempgra', 'Permgra'], get('ManrGraz_Gras')),
            'Land': Imp_func.dict_name_path(Air_pj_path.MainCpNam, get('Land'))
        }
        return dict_list_rough, dict_dict_fine

    EAT_N_bystage_Aggrwddt,          EAT_N_bystage_Sumarwddt           = collect_emissions('EAT')
    Meat_N_bystage_Aggrwddt,         Meat_N_bystage_Sumarwddt          = collect_emissions('EAT_Meat')
    MTFR_EAT_N_bystage_Aggrwddt,     MTFR_EAT_N_bystage_Sumarwddt      = collect_emissions('MTFR_EAT')
    EAT_N_bystage_Aggrwddt,        EAT_N_bystage_Sumarwddt        = collect_emissions('EAT')
    EAT_Vegan_bystage_Aggrwddt,    EAT_Vegan_N_bystage_Sumarwddt  = collect_emissions('EAT_Vegan')
    EAT_Meat_bystage_Aggrwddt,     EAT_Meat_N_bystage_Sumarwddt   = collect_emissions('EAT_Meat')

    Scenarios_Nflow_bystageAggr_wddt = {
        'EAT':                EAT_N_bystage_Aggrwddt,
        'EAT_Meat':           Meat_N_bystage_Aggrwddt,
        'MTFR_EAT':           MTFR_EAT_N_bystage_Aggrwddt,
        'EAT':     EAT_N_bystage_Aggrwddt,
        'EAT_Vegan': EAT_Vegan_bystage_Aggrwddt,
        'EAT_Meat':  EAT_Meat_bystage_Aggrwddt,
    }
    Scenarios_Nflow_bystageSummar_wddt = {
        'EAT':                EAT_N_bystage_Sumarwddt,
        'EAT_Meat':           Meat_N_bystage_Sumarwddt,
        'MTFR_EAT':           MTFR_EAT_N_bystage_Sumarwddt,
        'EAT':     EAT_N_bystage_Sumarwddt,
        'EAT_Vegan': EAT_Vegan_N_bystage_Sumarwddt,
        'EAT_Meat':  EAT_Meat_N_bystage_Sumarwddt,
    }

    # OUTPUT_FILE — aggregate to stage-level rasters
    for Stage in Scenarios_Nflow_bystageAggr_wddt[Scenarios_Name]:
        Aggr_emi = Imp_func.aggregate(Scenarios_Nflow_bystageAggr_wddt[Scenarios_Name][Stage])
        Imp_func.output_ras_filtered(
            Aggre_path + Stage + f'_{Scenarios_Name}_Nflow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326', Aggr_emi,
        )

    # SUMMARY — per-stage zonal statistics, one sheet per AP-AMMO stage name
    S = Scenarios_Nflow_bystageSummar_wddt[Scenarios_Name]
    _stage_key_map = [
        ('N_coupl_Syntfert',               'Syntfert'),
        ('N_coupl_ManrInhous_Liqexcr_Liv', 'Liqinhous'),
        ('N_coupl_ManrInhous_Sldexcr_Liv', 'Sldinhous'),
        ('N_coupl_LiqMA_Liv',              'LiqApp'),
        ('N_coupl_SldMA_Liv',              'SldApp'),
        ('N_coupl_LiqMA_Crop',             'LiqApp_crop'),
        ('N_coupl_SldMA_Crop',             'SldApp_crop'),
        ('N_coupl_ManrGraz_excr_Liv',      'Manrdepo'),
        ('N_coupl_ManrGraz_excr_Gras',     'Manrdepo_gras'),
        ('Land',     'Land')
    ]
    _tmp = Summar_path.replace('.xlsx', '_{}_tmp.xlsx')
    with Imp_func.pd.ExcelWriter(Summar_path, engine='xlsxwriter') as writer:
        for stage_name, s_key in _stage_key_map:
            stage_dict = S[s_key]
            tmp_path = _tmp.format(s_key)
            Imp_func.zonal_summary(
                list(stage_dict.keys()), list(stage_dict.values()),
                Air_pj_path.EFTA_UK_wd, 32, 'sum', -999, tmp_path,
            )
            Imp_func.pd.read_excel(tmp_path).to_excel(writer, sheet_name=stage_name, index=False)
            Imp_func.os.remove(tmp_path)

    # SUMMARY — zonal statistics by aggregated stage
    Aggr_Nflow_wddt = Imp_func.dict_name_path(
        list(Scenarios_Nflow_bystageAggr_wddt[Scenarios_Name].keys()),
        Imp_func.glob.glob(Aggre_path + '*.tif', recursive=False),
    )
    Aggr_Nflow_wdlt = Imp_func.glob.glob(Aggre_path + '*.tif', recursive=False)
    Aggr_Nflow_wddt.update({'ManrApp': Aggr_Nflow_wdlt[1]})

    Imp_func.zonal_summary(
        list(Aggr_Nflow_wddt.keys()), list(Aggr_Nflow_wddt.values()),
        Air_pj_path.EFTA_UK_wd, 32, 'sum', -999, Summar_aggre_path,
    )

    Imp_func.save_plk(Summar_pkl_path, {
        'Detailed':   S,
        'Aggregated': Aggr_Nflow_wddt,
    })

    return

