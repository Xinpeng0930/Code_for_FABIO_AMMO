# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# B2_Basemap_Target_NenLand_Chek — baseline maps of target N and land, with checks

'''
This script builds base raster maps, computes zonal statistics, and extracts
summarised FABIO emission/N-flow/land targets for downstream calibration.
Functions here are called by B3 (N-flow calibration) and are self-contained
for land-use base-map calibration.
'''

#%%
import os
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Air_pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_pj_path

open_plk = Imp_func.open_plk
pd = Imp_func.pd
np = Imp_func.np

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------
FABIO_CROPNAME_LIST = [
    'Whea', 'Barl', 'Maiz&Grenmaiz', 'Legufod', 'Rapesd', 'Sunflrsd', 'Soya',
    'Oats', 'Rice', 'Rye', 'Pota', 'Sugbt', 'Peabean', 'Nuts', 'Fruit', 'Vege',
    'Tempgra&Permgra',
]

FABIO_CROPMANR_LIST = [
    'Whea', 'Barl', 'Maiz&Grenmaiz', 'Rapesd', 'Sunflrsd',
    'Oats', 'Rye', 'Pota', 'Sugbt', 'Nuts', 'Fruit', 'Vege', 'Tempgra&Permgra',
]

FABIO_LIVESTKNAME_LIST = ['Pig', 'Dair', 'Othcatl', 'Shep', 'Goat', 'Potr']

AMMO_NFLOW_IMPORTANT_SHETNAME = [
    'N_coupl_Syntfert',
    'N_coupl_ManrInhous_Liqexcr_Liv',
    'N_coupl_ManrInhous_Sldexcr_Liv',
    'N_coupl_ManrGraz_excr_Liv',
    'N_coupl_LiqMA_Crop',
    'N_coupl_SldMA_Crop',
    'N_coupl_LiqMA_Liv',
    'N_coupl_SldMA_Liv',
    'Land'
]

RASTER_RESOLUTION = 1.0 / 12.0

NEW_COL_ORDER = [
    'OBJECTID', 'Name_abbre', 'Name', 'country_group', 'Name_ISO',
    'Whea', 'Barl', 'Maiz&Grenmaiz', 'Legufod', 'Rapesd', 'Sunflrsd', 'Soya',
    'Oats', 'Rice', 'Rye', 'Pota', 'Sugbt', 'Peabean', 'Nuts',
    'Fruit', 'Vege', 'Tempgra&Permgra',
    'Pig', 'Dair', 'Othcatl', 'Shep', 'Goat', 'Potr',
]

EXCLUDED_MANR_CROPS = [5, 8, 10, 14]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _resolve_scenario_config(scenario_name):
    '''Return (nflow_excel_path, suffix, is_imprv) for a given scenario.'''
    is_imprv = scenario_name.startswith('CURR') or scenario_name.startswith('CURR')
    if is_imprv:
        suffix = 'CURR'
        nflow_excel = os.path.join(
            FABIO_pj_path.Prj_input_wd, 'N_flows_en_NH3_byStage_Imprv.xlsx')
    else:
        suffix = 'CURR_MTFR' or scenario_name.startswith('MTFR')
        nflow_excel = os.path.join(
            FABIO_pj_path.Prj_input_wd, 'N_flows_en_NH3_byStage_MTFR.xlsx')
    return nflow_excel, suffix, is_imprv


def _load_scenario_data(suffix):
    '''Load manure chain pickles for the given suffix (CURR or CURR).'''
    pkl_dir = FABIO_pj_path.Prj_Pkl_output_wd
    manr_manachain_dict = open_plk(os.path.join(pkl_dir, f'Manr_manachain_{suffix}.pkl'))
    manr_mana_df = manr_manachain_dict['Manr_mana_df']
    manr_graz_df = open_plk(os.path.join(pkl_dir, f'Emi_Grazdepo_{suffix}.pkl'))
    manrcroplink_dict = open_plk(os.path.join(pkl_dir, f'Relink_Croplivstk_N_Emi_{suffix}.pkl'))
    
    _syntfert_pkl = 'Emi_syntfert_coupl_CURR_MTFR.pkl' if 'MTFR' in suffix else 'Emi_syntfert_coupl_CURR.pkl'
    crop_side_emi_df = open_plk(os.path.join(pkl_dir, _syntfert_pkl))
    
    land_dict = {k: v.replace('../../../Online_work/', 'F:/') for k, v in
                 open_plk(FABIO_pj_path.Prj_Gene_output_wd + r'Crop_area_coupl.pkl').items()}
    return manr_mana_df, manr_graz_df, manrcroplink_dict, crop_side_emi_df, land_dict


# ---------------------------------------------------------------------------
# Build_Nflow_BaseMaps  — aggregate manure-chain rasters and collect paths
# ---------------------------------------------------------------------------

def Build_Nflow_BaseMaps(Scenarios_Name):
    '''
    Load manure chain data, aggregate linked rasters, and organise output paths
    by N-flow stage and product.

    Returns
    -------
    Nflow_byprod_wddt: dict  {stage: {product: raster_path}}
    '''
    _, suffix, _ = _resolve_scenario_config(Scenarios_Name)
    Manr_mana_df, Manr_graz_df, Manrcroplink_dict,\
        Crop_side_emi_df, land_dict = \
        _load_scenario_data(suffix)

    ### Livestock inhouse manure excretion
    Manr_InhousexcrN_wddt = Imp_func.conv_df2dict(Manr_mana_df, 'Ani_manr_type', 'Manr_excr')
    for key in Manr_InhousexcrN_wddt:
        Manr_InhousexcrN_wddt[key] = Manr_InhousexcrN_wddt[key].replace('\\', '/')

    ### Livestock grazing manure excretions
    Manr_GrazexcrN_wddt = Imp_func.conv_df2dict(Manr_graz_df, 'Anim_name', 'Graz_ExcrN')
    for key in Manr_GrazexcrN_wddt:
        Manr_GrazexcrN_wddt[key] = Manr_GrazexcrN_wddt[key].replace('\\', '/')

    ### Manure-crop link pathways
    for key in Manrcroplink_dict:
        for key2 in Manrcroplink_dict[key]:
            Manrcroplink_dict[key][key2] = Manrcroplink_dict[key][key2].replace('\\', '/')

    ManrN_Cropapplink_dict = Manrcroplink_dict['Manr_cropapp_N_wddt']
    ManrN_Grasapplink_dict = Manrcroplink_dict['Manr_grasapp_N_wddt']
    ManrN_Depolink_dict    = Manrcroplink_dict['Manr_depo_N_wddt']

    ### Synthetic fertiliser N flows
    Synt_fertN_wddt = Imp_func.conv_df2dict(Crop_side_emi_df, 'OSDCropname', 'Chemfer_use_map')
    for key in Synt_fertN_wddt:
        Synt_fertN_wddt[key] = Synt_fertN_wddt[key].replace('\\', '/')

    # Organise raster path groups by stage/product
    Hous_Liq_Nflow_wddt = {k: v for k, v in Manr_InhousexcrN_wddt.items() if '_liq' in k}
    Hous_Sld_Nflow_wddt = {k: v for k, v in Manr_InhousexcrN_wddt.items() if '_sld' in k}

    Hous_Liq_Nflownew_wddt = Imp_func.replace_keys(Hous_Liq_Nflow_wddt, Air_pj_path.Ani_name)
    Hous_Sld_Nflownew_wddt = Imp_func.replace_keys(Hous_Sld_Nflow_wddt, Air_pj_path.Ani_name)

    App_Liq_linkN_wddt = {
        **{k: v for k, v in ManrN_Cropapplink_dict.items() if '_liq' in k},
        **{k: v for k, v in ManrN_Grasapplink_dict.items() if '_liq' in k},
    }
    App_Sld_linkN_wddt = {
        **{k: v for k, v in ManrN_Cropapplink_dict.items() if '_sld' in k},
        **{k: v for k, v in ManrN_Grasapplink_dict.items() if '_sld' in k},
    }

    App_Liq_flows_multi_wddt = {
        Prod: [v for k, v in App_Liq_linkN_wddt.items() if Prod in k]
        for Prod in Air_pj_path.Ani_name
    }
    App_Sld_flows_multi_wddt = {
        Prod: [v for k, v in App_Sld_linkN_wddt.items() if Prod in k]
        for Prod in Air_pj_path.Ani_name
    }
    App_Liq_bycrop_flows_multi = {
        k: v for k, v in {
            Prod: [v for key, v in App_Liq_linkN_wddt.items() if Prod in key]
            for Prod in Air_pj_path.MainCpNam
        }.items() if v
    }
    App_Sld_bycrop_flows_multi = {
        k: v for k, v in {
            Prod: [v for key, v in App_Sld_linkN_wddt.items() if Prod in key]
            for Prod in Air_pj_path.MainCpNam
        }.items() if v
    }
    Depo_flows_multi_wddt = {
        Prod: [v for k, v in ManrN_Depolink_dict.items() if Prod in k]
        for Prod in Air_pj_path.Ani_name
    }
    Depo_flows_multi_wddt = Imp_func.del_keys_dict(Depo_flows_multi_wddt, ['pig', 'potr'])

    Depo_flows_bygras_multi_wddt = {
        Prod: [v for k, v in ManrN_Depolink_dict.items() if Prod in k]
        for Prod in ['Tempgra', 'Permgra']
    }

    # OUTPUT_FILE — aggregate and write base rasters
    for Prod in App_Liq_flows_multi_wddt:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_LiqN_app_byLiv/' + Prod + '_BU_Nflow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(App_Liq_flows_multi_wddt[Prod]),
        )

    for Prod in App_Sld_flows_multi_wddt:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_SldN_app_byLiv/' + Prod + '_BU_flow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(App_Sld_flows_multi_wddt[Prod]),
        )

    for Prod in App_Liq_bycrop_flows_multi:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_LiqN_app_bycrop/' + Prod + '_BU_flow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(App_Liq_bycrop_flows_multi[Prod]),
        )

    for Prod in App_Sld_bycrop_flows_multi:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_SldN_app_bycrop/' + Prod + '_BU_flow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(App_Sld_bycrop_flows_multi[Prod]),
        )

    for Prod in Depo_flows_multi_wddt:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_depoN_byLiv/' + Prod + '_BU_depo_BU_flow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(Depo_flows_multi_wddt[Prod]),
        )

    for Prod in Depo_flows_bygras_multi_wddt:
        Imp_func.output_ras_filtered(
            FABIO_pj_path.Prj_Rster_output_wd + f'{suffix}_App_Depo_Nflow/Manr_depoN_bygras/' + Prod + '_BU_depo_flow.tif',
            Air_pj_path.Exam_crop_reson_wd, 'EPSG:4326',
            Imp_func.aggregate(Depo_flows_bygras_multi_wddt[Prod]),
        )

    # Collect written raster paths
    App_LiqN_wddt = Imp_func.dict_name_path(
        Air_pj_path.Ani_name,
        Imp_func.glob.glob( FABIO_pj_path.Prj_Rster_output_wd +\
            f'{suffix}_App_Depo_Nflow/Manr_LiqN_app_byLiv/*.tif', recursive=False),
    )
    App_SldN_wddt = Imp_func.dict_name_path(
        Air_pj_path.Ani_name,
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'{suffix}_App_Depo_Nflow/Manr_SldN_app_byLiv/*.tif', recursive=False),
    )
    App_LiqN_crop_wddt = Imp_func.dict_name_path(
        Air_pj_path.MainCpNam,
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'{suffix}_App_Depo_Nflow/Manr_LiqN_app_bycrop/*.tif', recursive=False),
    )
    App_SldN_crop_wddt = Imp_func.dict_name_path(
        Air_pj_path.MainCpNam,
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'{suffix}_App_Depo_Nflow/Manr_SldN_app_bycrop/*.tif', recursive=False),
    )
    DepoN_wddt = Imp_func.dict_name_path(
        Air_pj_path.Ani_name,
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd +\
            f'{suffix}_App_Depo_Nflow/Manr_depoN_byLiv/*.tif', recursive=False),
    )
    DepoN_gras_wddt = Imp_func.dict_name_path(
        ['Tempgra', 'Permgra'],
        Imp_func.glob.glob(FABIO_pj_path.Prj_Rster_output_wd + \
            f'{suffix}_App_Depo_Nflow/Manr_depoN_bygras/*.tif', recursive=False),
    )
    
    
    
    Nflow_byprod_wddt = {
        'N_coupl_Syntfert':               Synt_fertN_wddt,
        'N_coupl_ManrInhous_Liqexcr_Liv': Hous_Liq_Nflownew_wddt,
        'N_coupl_ManrInhous_Sldexcr_Liv': Hous_Sld_Nflownew_wddt,
        'N_coupl_ManrGraz_excr_Liv':       DepoN_wddt,
        'N_coupl_LiqMA_Liv':               App_LiqN_wddt,
        'N_coupl_SldMA_Liv':               App_SldN_wddt,
        'N_coupl_LiqMA_Crop':              App_LiqN_crop_wddt,
        'N_coupl_SldMA_Crop':              App_SldN_crop_wddt,
        'N_coupl_ManrGraz_excr_Gras':      DepoN_gras_wddt,
        'Land':                            land_dict,
    }

    # SUMMARY — zonal statistics of base maps per stage (same structure as
    # N_flows_en_NH3_byStage.xlsx: one sheet per stage, products as columns)
    _summary_path = FABIO_pj_path.Prj_Gene_output_wd + f'{suffix}_BaseMaps_LandenNflow_byProdStage.xlsx'
    _tmp = _summary_path.replace('.xlsx', '_{}_tmp.xlsx')
    with pd.ExcelWriter(_summary_path, engine='xlsxwriter') as writer:
        for stage_name, stage_dict in Nflow_byprod_wddt.items():
            tmp_path = _tmp.format(stage_name)
            Imp_func.zonal_summary(
                list(stage_dict.keys()), list(stage_dict.values()),
                Air_pj_path.EFTA_UK_wd, 32, 'sum', -999, tmp_path,
            )
            pd.read_excel(tmp_path).to_excel(writer,\
                sheet_name=stage_name, index=False)
            os.remove(tmp_path)

    return Nflow_byprod_wddt, _summary_path



#%%
# ---------------------------------------------------------------------------
# Summa_FABIO_Nflow_Targets  — align FABIO N flows and extract calibration targets
# ---------------------------------------------------------------------------

def Summa_FABIO_Land_en_Nflow_Targets(Scenarios_Name):
    '''
    Align FABIO production-side N-flow data to AP-AMMO product classification,
    write per-stage aggregated Excels, and return per-stage calibration targets.

    Returns
    -------
    Nflow_FABIO_Emi_extr_dt: dict  {stage: DataFrame of FABIO targets}
    '''
    Para_wd = FABIO_pj_path.Prj_input_wd + \
        'Processing_plot_new.xlsx'
    #FABIO target data, from C12d
    Prod_Flow_dt         = open_plk(FABIO_pj_path.Prj_Pkl_output_wd + r'Prod_Land_en_Nflows.pkl')
    Standard_EUEFTA_head = pd.read_excel(Para_wd, sheet_name='Country_name')
    Items_head           = pd.read_excel(Para_wd, sheet_name='Food_group')

    AggNflow_wd = FABIO_pj_path.Prj_Gene_output_wd + Scenarios_Name + '_Nflow_ProdSide_Aggr4Map/'

    # Align FABIO N flows to AP-AMMO classification
    Nflow_excel_wddt    = Prod_Flow_dt[Scenarios_Name]
    Nflow_FABIO_Prod_dt = {}

    for Stage in list(Nflow_excel_wddt.keys()):
        Nflow_Prod_df = pd.read_excel(Nflow_excel_wddt[Stage], sheet_name='Sheet1')
        Nflow_Prod_df.fillna(0, inplace=True)
        Nflow_Prod_df.replace([np.inf, -np.inf], 0, inplace=True)

        Nflow_Prod_col = list(Nflow_Prod_df.columns[6:])
        Nflow_Prod_column_sum = pd.DataFrame({
            'iso3c': Nflow_Prod_df['iso3c'],
            'items': Nflow_Prod_df['item'],
            Stage:   Nflow_Prod_df[Nflow_Prod_col].sum(axis=1),
        })

        Nflow_Prod_pivot = pd.pivot_table(
            Nflow_Prod_column_sum,
            index=['iso3c'], columns=['items'],
            values=[Stage], aggfunc=[np.sum], fill_value=0,
        )
        Nflow_Prod_pivot.columns = list(Nflow_Prod_pivot.columns.get_level_values('items'))

        Nflow_Prod_pivot_trans = Nflow_Prod_pivot.T
        Nflow_Prod_pivot_trans.insert(0, 'item_names', Nflow_Prod_pivot_trans.index)
        Nflow_Prod_pivot_trans = Nflow_Prod_pivot_trans.reset_index(drop=True)

        Nflow_Prod_pivot_trans_new = pd.merge(
            Items_head, Nflow_Prod_pivot_trans,
            how='left', left_on='Item_FABIO', right_on='item_names',
        )
        Nflow_Prod_pivot_trans_sum = Nflow_Prod_pivot_trans_new.groupby('AP-AMMO_prod')[
            list(Nflow_Prod_pivot_trans_new.columns)[13:]].sum().reset_index()

        Nflow_Prod_pivot_sum = Nflow_Prod_pivot_trans_sum.T
        Nflow_Prod_pivot_sum.columns = Nflow_Prod_pivot_sum.iloc[0]
        Nflow_Prod_pivot_sum_new = Nflow_Prod_pivot_sum.drop('AP-AMMO_prod', axis=0)
        Nflow_Prod_pivot_sum_new = Nflow_Prod_pivot_sum_new.drop('item_names', axis=0)
        Nflow_Prod_pivot_sum_new = Nflow_Prod_pivot_sum_new.clip(lower=0)

        Nflow_Prod_pivot_sum_new2 = pd.merge(
            Standard_EUEFTA_head, Nflow_Prod_pivot_sum_new,
            how='left', left_on='Name_ISO', right_index=True,
        )
        Nflow_FABIO_Prod_dt[Stage] = Nflow_Prod_pivot_sum_new2

        # OUTPUT_FILE — per-stage aggregated N-flow Excel
        Nflow_Prod_pivot_sum_new2.to_excel(
            AggNflow_wd + 'Aggr_ProdNflows_' + Stage + '.xlsx',
            sheet_name='Sheet1', index=False,
        )

    # Extract per-stage calibration targets
    Useful_Emi_FABIO_ProdEmi_dt = Imp_func.deepcopy(Nflow_FABIO_Prod_dt)
    Imp_func.del_keys_dict(Useful_Emi_FABIO_ProdEmi_dt, ['ManrMS_Liq_N', 'ManrMS_Sld_N'])
    Useful_Emi_FABIO_ProdEmi_dt = Imp_func.replace_keys(
        Useful_Emi_FABIO_ProdEmi_dt, AMMO_NFLOW_IMPORTANT_SHETNAME)

    Nflow_FABIO_Emi_extr_dt = {}

    for Stage in AMMO_NFLOW_IMPORTANT_SHETNAME:
        Useful_Emi = Useful_Emi_FABIO_ProdEmi_dt[Stage].reindex(columns=NEW_COL_ORDER)
        Useful_Emi.reset_index(drop=True, inplace=True)

        if Stage in ['N_coupl_Syntfert','Land']:
            Useful_Emi_new = Useful_Emi[FABIO_CROPNAME_LIST]
        elif Stage in ['N_coupl_LiqMA_Crop', 'N_coupl_SldMA_Crop']:
            Useful_Emi_new = Useful_Emi[FABIO_CROPMANR_LIST]
        elif Stage in ['N_coupl_ManrInhous_Liqexcr_Liv', 'N_coupl_ManrInhous_Sldexcr_Liv',
                       'N_coupl_LiqMA_Liv', 'N_coupl_SldMA_Liv']:
            Useful_Emi_new = Useful_Emi[FABIO_LIVESTKNAME_LIST]
        elif Stage == 'N_coupl_ManrGraz_excr_Liv':
            Useful_Emi_new = Useful_Emi[['Dair', 'Othcatl', 'Shep', 'Goat']]

        Nflow_FABIO_Emi_extr_dt[Stage] = Useful_Emi_new
        print(list(Useful_Emi_new.columns))

    # OUTPUT_FILE — write check Excel
    check_excel_path = FABIO_pj_path.Prj_Gene_output_wd + f'{Scenarios_Name}_FABIO_LandenNflow_check.xlsx'
    with pd.ExcelWriter(check_excel_path, engine='xlsxwriter') as writer:
        for sheet_name, df in Nflow_FABIO_Emi_extr_dt.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return check_excel_path

