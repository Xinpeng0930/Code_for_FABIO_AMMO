# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# F2 — calorie intake charts (Fig. 3a, SI S3)
# Functions:
#   diet_calories_chart()     — calorie intake by food group
#   regional_calories_chart() — regional calorie intake
import os

from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path
from APSP_proc import Z_Proj_paths as Air_path
from APSP_proc import Z_Plotting_functions
import seaborn as sns

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(FILE_DIR, "Figures")
os.makedirs(FIG_DIR, exist_ok=True)


def diet_calories_chart():
    Plot_wd = FABIO_path.Prj_input_wd+\
        r'Processing_plot_new.xlsx'


    #----------------------------------------------------processing_module----------------------------------------------------
    ## Diet data
    Diet_df = Imp_func.pd.read_excel(Plot_wd,\
        sheet_name='Realistic_diet_data')

    ### Define food groups and their categories
    Diet_df_cate = Diet_df[['Food type', 'Scale class']].drop_duplicates()

    #### Build food_group_categories dynamically
    food_group_categories = {}
    for category, group in Diet_df_cate.groupby('Scale class'):
        food_group_categories[category] = group['Food type'].tolist()

    #### Generate gradient colors for each category
    n_dict = {k: len(v) for k, v in food_group_categories.items()}

    colors_plant_protein = sns.color_palette("Greens", n_dict.get('Plant protein', 0)).as_hex()[::-1]
    colors_animal_protein = sns.color_palette("Reds", n_dict.get('Animal protein', 0)).as_hex()[::-1]
    colors_other_foods = sns.color_palette("Blues", n_dict.get('Other foods', 0)).as_hex()[::-1]
    colors_fats_oils = sns.color_palette("autumn_r", n_dict.get('Fats and oils', 0)).as_hex()[::-1]


    # Build final color mapping
    category_colors = {
            'Other foods':    colors_other_foods,
            'Plant protein':  colors_plant_protein,
            'Animal protein': colors_animal_protein,
            'Fats and oils':  colors_fats_oils,
        }

    food_colors = {}
    for category, foods in food_group_categories.items():
        for food, color in zip(foods, category_colors[category]):
            food_colors[food] = color

    ### Transpose the dataframe to stack by different dimension
    Diet_df_new = Diet_df.set_index('Food type').T.iloc[1:]

    ### Reorder columns so items within the same category are grouped together
    category_order = ['Animal protein', 'Fats and oils', 'Other foods', 'Plant protein']
    grouped_col_order = [food for cat in category_order for food in food_group_categories.get(cat, [])]
    Diet_df_new = Diet_df_new[[col for col in grouped_col_order if col in Diet_df_new.columns]]

    ### Ensure the order of colors matches the columns in Diet_df_new
    Plotting_colors = [food_colors[col] for col in Diet_df_new.columns]


    #%%
    #----------------------------------------------------plotting_module----------------------------------------------------
    #PLOT
    # Set figure size
    #Z_Plotting_functions.plt.figure(figsize=(12, 3)) 

    # Set global font for consistency
    Z_Plotting_functions.plt.rcParams['font.family'] = 'sans-serif'


    # Plot stacked bar chart
    ax = Diet_df_new.plot(
            kind='bar',
            stacked=True,
            color=Plotting_colors,
            figsize=(6,8))

    ## Concrete labels
    ax.set_ylabel('Calorie intake (kcal capita$^{-1}$ d$^{-1}$)')
    ax.set_xlabel('Dietary scenarios')
    ax.set_xticklabels(ax.get_xticklabels(), style='italic', rotation=45, ha='right')


    # Adjust layout
    legend = ax.legend(
        title='Food groups',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False  # cleaner look
    )


    Z_Plotting_functions.plt.tight_layout()
    Z_Plotting_functions.plt.subplots_adjust(right=0.75)  # Reserve space on the right

    #save and show plot
    Z_Plotting_functions.plt.savefig(os.path.join(FIG_DIR, "Realisticcalories_chart_adj.png"),
        dpi=300)
    Z_Plotting_functions.plt.show()



    # %%


def regional_calories_chart():
    Plot_wd = FABIO_path.Prj_input_wd+r'Processing_plot_new.xlsx'


    #----------------------------------------------------processing_module----------------------------------------------------
    ## Diet data
    Diet_df = Imp_func.pd.read_excel(Plot_wd,sheet_name='Regional_diet_data')

    ### Define food groups and their categories
    Diet_df_cate = Diet_df[['Food type', 'Scale class']].drop_duplicates()

    #### Build food_group_categories dynamically
    food_group_categories = {}
    for category, group in Diet_df_cate.groupby('Scale class'):
        food_group_categories[category] = group['Food type'].tolist()

    #### Generate gradient colors for each category
    n_dict = {k: len(v) for k, v in food_group_categories.items()}

    colors_plant_protein = sns.color_palette("Greens", n_dict.get('Plant protein', 0)).as_hex()[::-1]
    colors_animal_protein = sns.color_palette("Reds", n_dict.get('Animal protein', 0)).as_hex()[::-1]
    colors_other_foods = sns.color_palette("Blues", n_dict.get('Other foods', 0)).as_hex()[::-1]
    colors_fats_oils = sns.color_palette("autumn_r", n_dict.get('Fats and oils', 0)).as_hex()[::-1]


    # Build final color mapping
    category_colors = {
            'Other foods':    colors_other_foods,
            'Plant protein':  colors_plant_protein,
            'Animal protein': colors_animal_protein,
            'Fats and oils':  colors_fats_oils,
        }

    food_colors = {}
    for category, foods in food_group_categories.items():
        for food, color in zip(foods, category_colors[category]):
            food_colors[food] = color

    ### Transpose the dataframe to stack by different dimension
    Diet_df_new = Diet_df.set_index('Food type').T.iloc[1:]

    ### Reorder columns so items within the same category are grouped together
    category_order = ['Animal protein', 'Fats and oils', 'Other foods', 'Plant protein']
    grouped_col_order = [food for cat in category_order for food in food_group_categories.get(cat, [])]
    Diet_df_new = Diet_df_new[[col for col in grouped_col_order if col in Diet_df_new.columns]]

    ### Ensure the order of colors matches the columns in Diet_df_new
    Plotting_colors = [food_colors[col] for col in Diet_df_new.columns]


    #%%
    #----------------------------------------------------plotting_module----------------------------------------------------
    #PLOT
    # Set figure size
    #Z_Plotting_functions.plt.figure(figsize=(12, 3)) 

    # Set global font for consistency
    Z_Plotting_functions.plt.rcParams['font.family'] = 'sans-serif'


    # Plot stacked bar chart
    ax = Diet_df_new.plot(
            kind='barh',
            stacked=True,
            color=Plotting_colors,
            figsize=(10,4))

    ## Concrete labels
    ax.set_xlabel('Calorie intake (kcal capita$^{-1}$ d$^{-1}$)')
    ax.set_ylabel('Dietary scenarios')
    ax.set_yticklabels(ax.get_yticklabels(), style='italic')


    # Adjust layout
    legend = ax.legend(
        title='Food groups',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False  # cleaner look
    )


    Z_Plotting_functions.plt.tight_layout()
    Z_Plotting_functions.plt.subplots_adjust(right=0.7)  # Reserve space on the right

    #save and show plot
    Z_Plotting_functions.plt.savefig(os.path.join(FIG_DIR, "Regcalories_chart_adj.png"),
        dpi=300)
    Z_Plotting_functions.plt.show()



    # %%


if __name__ == "__main__":
    diet_calories_chart()
    regional_calories_chart()
