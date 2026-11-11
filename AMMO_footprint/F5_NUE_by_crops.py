# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/10.5281/zenodo.24146167 (Zenodo)

# F5 — nitrogen-use efficiency by crop (SI S7)
# Function: nue_boxplot()
import os

from APSP_proc import Z_Important_functions as Imp_func
from APSP_proc import Z_fabio_prj_paths as FABIO_path
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import seaborn as sns

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(FILE_DIR, "Figures")
os.makedirs(FIG_DIR, exist_ok=True)


def nue_boxplot():
    NUE_df = Imp_func.pd.read_excel(
        FABIO_path.Prj_input_wd+'Processing_plot_new.xlsx',\
        sheet_name='NUE_boxplot')


    ## the data for plotting box plot
    NUE_data = NUE_df.to_dict(orient="list")

    NUE_vertical_df = Imp_func.pd.DataFrame(NUE_data).melt(var_name='Crop', value_name='NUE')


    # Create a single figure
    Imp_func.plt.figure(figsize=(8, 8))
    ax = Imp_func.plt.gca()


    # Create the boxplot
    sns.boxplot(x='NUE', y='Crop', \
        data = NUE_vertical_df,\
        palette='pastel',\
        width = 0.8, \
        gap=0.5,
        ax=ax,\
        zorder=10)


    # Customize the plot
    ax.set_xlabel('NUE', fontsize=20, fontname='Times New Roman')


    # Set tick parameters
    ax.tick_params(axis='both', which='major', labelsize=20)

    # Set x-axis limits
    ax.set_xlim(0, 3)

    # Set the font of tick labels to Times New Roman
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname('Times New Roman')


    # Use MaxNLocator to limit each axis to 4 ticks
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))

    # Format ticks to show only one decimal place
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))



    # Enable grid
    ax.grid(True)

    # Optional: Adjust layout to prevent label cutoff
    Imp_func.plt.subplots_adjust(left=0.2, top=0.95, bottom=0.08)

    # Export the figure
    Imp_func.plt.savefig(os.path.join(FIG_DIR, "NUE_boxplot.png"), dpi=300)

    # Show the plot
    Imp_func.plt.show()


    # %%


if __name__ == "__main__":
    nue_boxplot()
