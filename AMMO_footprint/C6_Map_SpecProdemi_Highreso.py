# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# C6_Map_SpecProdemi_Highreso — high-resolution maps of specific production emissions
'''
This script aims to map new emissions under the different scenario to
high-resolution maps based on AP-AMMO dataset

This script can run automatically
'''

#%%
# Necessary packages
from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_Proj_paths as Pj_path
from APSP_proc import Z_fabio_prj_paths as FABIO_Pj_path
import gc


#%%
def Mapping_fp_Food_Diet(Scenarios_Name, Food):
    #----------------------------------------------------input_module----------------------------------------------------
    Base_mapfac_dt = Imp_func.open_plk(FABIO_Pj_path.Prj_Pkl_output_wd + \
        r'Cali_Consup_Scen.pkl')
    
    Base_map_wddt = Base_mapfac_dt['Basemap'][Scenarios_Name]
    Emi_FABIOextr_dt = Base_mapfac_dt['Emi_FABIOextr'][Scenarios_Name][Food]
    Fac_cali_dt = Base_mapfac_dt['Cali_fac'][Scenarios_Name][Food]
    
    ## Store rescaled emissions at high resolution
    Higreso_path = Pj_path.output_wd + f'{Scenarios_Name}_Emi_Specdrivn/'


    #----------------------------------------------------processing_module----------------------------------------------------
    ### Execute the calibrations
    # OUTPUT_FILE
    for k in ['EuroEmi','NonEuroEmi']:
        for i in list(Emi_FABIOextr_dt[k].keys()):
            EAT_emifac_data = Fac_cali_dt[k][i]
            EAT_emifac_data = EAT_emifac_data.fillna(0)

            if i == 'NH3_Syntfert':
                for j in Pj_path.MainCpNam:
                    Imp_func.cali_fig_filter(Base_map_wddt[i][j],Pj_path.Exam_crop_reson_wd,\
                        Pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                        EAT_emifac_data.columns.tolist()[list(Base_map_wddt[i].keys()).index(j)+1],\
                        #must ensure the same order in the two lists
                        0.0833333333333333,Higreso_path+f"{Food}_drivn/{k}/"+\
                            i.split("_")[1]+f'_byprod/'+j+r'_fertemi.tif')
            

            elif i in ['NH3_ManrInhous_Liqexcr_Liv', 'NH3_ManrInhous_Sldexcr_Liv',\
                'NH3_Liqstor_Liv','NH3_Sldstor_Liv']:
                for j in Pj_path.Ani_name:
                    Imp_func.cali_fig_filter(Base_map_wddt[i][j],Pj_path.Exam_crop_reson_wd,\
                        Pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                        EAT_emifac_data.columns.tolist()[list(Base_map_wddt[i].keys()).index(j)+1],\
                        0.0833333333333333,Higreso_path+f"{Food}_drivn/{k}/"+\
                            i.split("_")[1]+'_'+i.split("_")[2]+'_byprod/'+j+'_'+i.split("_")[0]+'_emi.tif')
            
            
            elif i in ['NH3_LiqMA_Crop','NH3_SldMA_Crop']:
                for j in Imp_func.del_elemt_list(Pj_path.MainCpNam,[5,8,10,14]):
                    Imp_func.cali_fig_filter(Base_map_wddt[i][j],Pj_path.Exam_crop_reson_wd,\
                        Pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                        EAT_emifac_data.columns.tolist()[list(Base_map_wddt[i].keys()).index(j)+1],\
                        0.0833333333333333,Higreso_path+f"{Food}_drivn/{k}/"+\
                            i.split("_")[1]+'_byprod/'+j+'_'+i.split("_")[0]+'_emi.tif')
            
            elif i in ['NH3_ManrGraz_excr_Liv']:
                for j in ['dair','othcatl','shep','goat']:
                    Imp_func.cali_fig_filter(Base_map_wddt[i][j],Pj_path.Exam_crop_reson_wd,\
                        Pj_path.EFTA_UK_wd,EAT_emifac_data,'FID_1','Country',\
                        EAT_emifac_data.columns.tolist()[list(Base_map_wddt[i].keys()).index(j)+1],\
                        0.0833333333333333,Higreso_path+f"{Food}_drivn/{k}/"+\
                            i.split("_")[1]+'_byprod/'+j+'_'+i.split("_")[0]+'_emi.tif')

    return




def Aggre_food_spec_emi(Scenarios_Name, Food):
    # Scenario-based inputs and outputs-----------------------------------------------------------------------
    if Scenarios_Name == 'Curr':
        ## Store FABIO origined emissions with AP-AMMO categories by driven product
        Agg_Emi_wd = FABIO_Pj_path.Prj_Gene_output_wd+ Scenarios_Name +'_ProdSide_Aggr4Map/' 
        
        ## Store rescaled emissions at high resolution.
        Higreso_path =  Pj_path.output_wd + f'{Scenarios_Name}_Emi_Specdrivn/'
        
    elif Scenarios_Name == 'EAT':
        ## Store FABIO origined emissions with AP-AMMO categories by driven product
        Agg_Emi_wd = FABIO_Pj_path.Prj_Gene_output_wd+ Scenarios_Name + '_ProdSide_Aggr4Map/' 
            
        ## Store rescaled delta emissions at high resolution.
        Higreso_path = Pj_path.output_wd + f'{Scenarios_Name}_Emi_Specdrivn/'
        
        
    elif Scenarios_Name == 'EAT_Vegan':
        ## Store FABIO origined delta emissions with AP-AMMO categories by driven product. 
        Agg_Emi_wd= FABIO_Pj_path.Prj_Gene_output_wd+\
            Scenarios_Name+'_ProdSide_Aggr4Map/'
            
        ## Store rescaled emissions at high resolution.
        Higreso_path = Pj_path.output_wd + f'{Scenarios_Name}' + r'_Emi_Specdrivn/'
        
    
    ### Aggregate these stage-specific emissions and get the total delta emissions by the driven food
    # OUTPUT_DATA
    EuroFoodStage_emission_wdlt = Imp_func.glob.glob(
        Higreso_path+f"{Food}_drivn/EuroEmi/**/*.tif",recursive=True)

    NonEuroFoodStage_emission_wdlt = Imp_func.glob.glob(
        Higreso_path+f"{Food}_drivn/NonEuroEmi/**/*.tif",recursive=True)
    
    EuroFood_drvn_emi = Imp_func.aggregate(EuroFoodStage_emission_wdlt)
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(Agg_Emi_wd +f"{Food}_Eurodrivn_emi.tif",\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_drvn_emi)
    del EuroFood_drvn_emi
    gc.collect()

    NonEuroFood_drvn_emi = Imp_func.aggregate(NonEuroFoodStage_emission_wdlt)
    # OUTPUT_FILE
    Imp_func.output_ras_filtered(Agg_Emi_wd +f"{Food}_NonEurodrivn_emi.tif",\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_drvn_emi)
    del NonEuroFood_drvn_emi
    gc.collect()
    
    
    # Use a list comprehension to filter the list
    if Food == 'Beef':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt  if 'dair' in path.lower() or\
            'othcatl' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'dair' not in path.lower() and\
            'othcatl' not in path.lower()]
        
        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt  if 'dair' in path.lower() or\
            'othcatl' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'dair' not in path.lower() and\
            'othcatl' not in path.lower()]
        
        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt),\
            len(EuroAni_direct_wdlt),len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt),\
            len(NonEuroAni_direct_wdlt),len(NonEuroFeed_wdlt))
        
    
    elif Food == 'Pork':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'pig' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'pig' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'pig' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'pig' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))


    elif Food == 'Milk':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'dair' in path.lower() or\
            'othcatl' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'dair' not in path.lower() and\
            'othcatl' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'dair' in path.lower() or\
            'othcatl' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'dair' not in path.lower() and\
            'othcatl' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))


    elif Food == 'Eggs':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'potr' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'potr' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'potr' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'potr' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))


    elif Food == 'Pultry meat':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'potr' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'potr' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'potr' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'potr' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))


    elif Food == 'Animal fats':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'othcatl' in path.lower() or\
            'shep' in path.lower() or 'goat' in path.lower() or 'pig' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'othcatl' not in path.lower() and\
            'shep' not in path.lower() and 'goat' not in path.lower() and 'pig' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'othcatl' in path.lower() or\
            'shep' in path.lower() or 'goat' in path.lower() or 'pig' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'othcatl' not in path.lower() and\
            'shep' not in path.lower() and 'goat' not in path.lower() and 'pig' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))

    elif Food == 'Mutton':
        EuroAni_direct_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'shep' in path.lower() or\
            'goat' in path.lower()]
        EuroFeed_wdlt = [path for path in EuroFoodStage_emission_wdlt if 'shep' not in path.lower() and\
            'goat' not in path.lower()]

        NonEuroAni_direct_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'shep' in path.lower() or\
            'goat' in path.lower()]
        NonEuroFeed_wdlt = [path for path in NonEuroFoodStage_emission_wdlt if 'shep' not in path.lower() and\
            'goat' not in path.lower()]

        EuroFood_real_drivn_emi = Imp_func.aggregate_ori(EuroAni_direct_wdlt)
        EuroFood_feed_drivn_emi = Imp_func.aggregate_ori(EuroFeed_wdlt)
        NonEuroFood_real_drivn_emi = Imp_func.aggregate_ori(NonEuroAni_direct_wdlt)
        NonEuroFood_feed_drivn_emi = Imp_func.aggregate_ori(NonEuroFeed_wdlt)

        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"Euro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',EuroFood_feed_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_real_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_real_drivn_emi)
        Imp_func.output_ras_filtered(Agg_Emi_wd +f"NonEuro_{Food}_feed_drivn_emi.tif",\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',NonEuroFood_feed_drivn_emi)

        print(len(EuroFoodStage_emission_wdlt), len(EuroAni_direct_wdlt), len(EuroFeed_wdlt))
        print(len(NonEuroFoodStage_emission_wdlt), len(NonEuroAni_direct_wdlt), len(NonEuroFeed_wdlt))

    else:
        print(f'{Food} is not a aniaml product')
    
    return  



def Aggre_Ani_Plant_Export(Scenarios_Name):
    # Scenario-based inputs and outputs-----------------------------------------------------------------------
    if Scenarios_Name == 'Curr':
        ## Store FABIO origined emissions with AP-AMMO categories by driven product
        Agg_Emi_wd = FABIO_Pj_path.Prj_Gene_output_wd+ Scenarios_Name +'_ProdSide_Aggr4Map/' 
        
        
    elif Scenarios_Name == 'EAT':
        ## Store FABIO origined emissions with AP-AMMO categories by driven product
        Agg_Emi_wd = FABIO_Pj_path.Prj_Gene_output_wd+ Scenarios_Name + '_ProdSide_Aggr4Map/' 
        
        
    elif Scenarios_Name == 'EAT_Vegan':
        ## Store FABIO origined delta emissions with AP-AMMO categories by driven product. 
        Agg_Emi_wd= FABIO_Pj_path.Prj_Gene_output_wd+\
            Scenarios_Name+'_ProdSide_Aggr4Map/'

        
    elif Scenarios_Name == 'EAT_Meat':
        ## Store FABIO origined delta emissions with AP-AMMO categories by driven product. 
        Agg_Emi_wd = FABIO_Pj_path.Prj_Gene_output_wd+ \
            Scenarios_Name +'_ProdSide_Aggr4Map/'
    
    ## Get the map data driven by different needs
    Plant_drivn_Euro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Plant_food_list,
        Imp_func.glob.glob(Agg_Emi_wd + r'*_Eurodrivn*.tif',recursive=False))
    
    Plant_driven_NonEuro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Plant_food_list,\
        Imp_func.glob.glob(Agg_Emi_wd + r'*_NonEurodrivn*.tif',recursive=False))
    
    Ani_direct_Euro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Ani_food_list,\
        Imp_func.glob.glob(Agg_Emi_wd +\
        r'Euro_*_real_drivn_emi*.tif',recursive=False))
    
    Ani_direct_NonEuro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Ani_food_list,\
        Imp_func.glob.glob(Agg_Emi_wd +\
        r'NonEuro_*_real_drivn_emi*.tif',recursive=False))
    
    Ani_feed_Euro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Ani_food_list,\
        Imp_func.glob.glob(Agg_Emi_wd +\
        r'Euro_*_feed_drivn_emi*.tif',recursive=False))
    
    Ani_feed_NonEuro_wddt = Imp_func.dict_name_path(FABIO_Pj_path.Ani_food_list,\
        Imp_func.glob.glob(Agg_Emi_wd +\
        r'NonEuro_*_feed_drivn_emi*.tif',recursive=False))
    
    
    Scen_drivn_dt = {
        "EuroPlant_drivn":Plant_drivn_Euro_wddt,\
        "NonEuroPlant_drivn":Plant_driven_NonEuro_wddt,\
        "EuroAni_drivn":Ani_direct_Euro_wddt,\
        "NonEuroAni_drivn":Ani_direct_NonEuro_wddt,\
        "EuroAni_feed":Ani_feed_Euro_wddt,\
        "NonEuroAni_feed":Ani_feed_NonEuro_wddt}
    
    Scen_Aggre_drivn_dt = {"EuroPlant_drivn":{}, "NonEuroPlant_drivn":{},\
        "EuroAni_drivn": {}, "NonEuroAni_drivn": {},\
        "EuroAni_feed": {}, "NonEuroAni_feed": {}}
    
    for region_food in Scen_drivn_dt:
        Region_food_emi = Imp_func.aggregate(list(Scen_drivn_dt[region_food].values()))
        Imp_func.output_reso_ras_filtered(FABIO_Pj_path.Prj_Rster_output_wd +\
            f'{Scenarios_Name}_{region_food}.tif',Pj_path.Exam_500area_wd,\
            'EPSG:4326',Region_food_emi)
        Scen_Aggre_drivn_dt[region_food] =  FABIO_Pj_path.Prj_Rster_output_wd + f'{Scenarios_Name}_{region_food}.tif'
    
    # SUMMARY
    Imp_func.zonal_summary(['Euro_' + k for k in list(Plant_drivn_Euro_wddt.keys())]+\
        ['NonEuro_' + k for k in list(Plant_driven_NonEuro_wddt.keys())]+\
        ['Euro_Ani_' + k for k in list(Ani_direct_Euro_wddt.keys())]+\
        ['NonEuro_Ani_' + k for k in list(Ani_direct_NonEuro_wddt.keys())]+\
        ['Euro_feed_' + k for k in list(Ani_feed_Euro_wddt.keys())]+\
        ['NonEuro_feed_' + k for k in list(Ani_feed_NonEuro_wddt.keys())],\
        
        list(Plant_drivn_Euro_wddt.values())+\
        list(Plant_driven_NonEuro_wddt.values())+\
        list(Ani_direct_Euro_wddt.values())+\
        list(Ani_direct_NonEuro_wddt.values())+\
        list(Ani_feed_Euro_wddt.values())+\
        list(Ani_feed_NonEuro_wddt.values()),\
        
        Pj_path.EFTA_UK_wd,32,'sum',-999,\
        
        FABIO_Pj_path.Prj_Gene_output_wd + f'Chek_{Scenarios_Name}_detailfdtype_drvEmi.xlsx')
    
    Imp_func.zonal_summary(list(Scen_Aggre_drivn_dt.keys()),\
        list(Scen_Aggre_drivn_dt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
        FABIO_Pj_path.Prj_Gene_output_wd + f'Chek_{Scenarios_Name}_broadfdtype_drvEmi.xlsx')
    
    
    return Scen_drivn_dt, Scen_Aggre_drivn_dt 


