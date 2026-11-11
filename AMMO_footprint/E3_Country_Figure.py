# Copyright (C) 2020-2026 Xinpeng Jin and contributors.
# Part of Code_for_FABIO_AMMO. Licensed under the GNU General Public
# License v3.0 (GPL-3.0); see the LICENSE file in the repository root.
#
# If you use this code in your research, please cite:
#   Jin, X., Behrens, P., Erisman, J. W., Navarre, N., & Mogollón, J. M. (2026).
#   Adopting a planetary health diet is critical for reducing ammonia emissions in Europe.
#   Nature Food. https://doi.org/<PAPER_DOI>
#   Code archive: https://doi.org/<ZENODO_DOI> (Zenodo)

# E3 — country comparison against the policy ceilings (SI S8)
# Function: country_figure(tif=None, tag="")
import os
import json

import numpy as np
import rasterio
import fiona
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
UNC_DIR = os.environ.get("AMMO_UNC_DIR", os.path.join(FILE_DIR, "Figures", "uncertainty"))
SHP_PATH = os.environ.get("AMMO_SHP", os.path.join(FILE_DIR, "Data_shp", "Global_map_geo.shp"))


def country_figure(tif=None, tag=""):
    BASE = os.path.dirname(os.path.abspath(__file__))
    OUT = UNC_DIR

    TIF = tif if tif else os.path.join(OUT, "Total_Delta_mean.tif")
    TAG = tag
    SHP = SHP_PATH
    JS = os.path.join(OUT, "country_spatial_bound.json")
    NODATA = -999.0

    TARGETS = {"DNK": "Denmark", "IRL": "Ireland", "NLD": "Netherlands"}
    LABEL_XY = {"DNK": (9.6, 56.2), "IRL": (-11.5, 52.6), "NLD": (5.3, 52.6)}
    LABEL_DX = {"DNK": (5.0, -0.4), "IRL": (-4.2, -1.2), "NLD": (3.6, 0.4)}

    with open(JS, encoding="utf-8") as fh:
        res = json.load(fh)
    share = {r["iso"]: r["share"] for r in res["rows"]}

    with rasterio.open(TIF) as s:
        a = s.read(1).astype("float64")
        b = s.bounds
        ext = (b.left, b.right, b.bottom, b.top)
    a[a == NODATA] = np.nan
    a = a * 1000.0  # kt -> t N per cell (legend units of the original panel)

    bounds = [-1e9, -30, -15, -10, -5, 0, 1e9]
    colors = ["#1a7a3c", "#66bd63", "#a6d96a", "#d9ef8b", "#fee08b", "#d73027"]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.imshow(a, extent=ext, origin="upper", cmap=cmap, norm=norm,
              interpolation="nearest")

    # country outlines
    polys = []
    with fiona.open(SHP) as src:
        for f in src:
            polys.append((f["properties"]["ISO_FABIO"], f["geometry"]))
    for iso, geom in polys:
        if iso not in TARGETS:
            xs, ys = [], []
            if geom["type"] == "Polygon":
                parts = [geom["coordinates"]]
            else:
                parts = geom["coordinates"]
            for part in parts:
                ring = part[0]
                xs = [p[0] for p in ring]
                ys = [p[1] for p in ring]
                ax.plot(xs, ys, color="0.25", lw=0.35, zorder=2)
    for iso in TARGETS:
        for i, g in polys:
            if i != iso:
                continue
            parts = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
            for part in parts:
                ring = part[0]
                ax.plot([p[0] for p in ring], [p[1] for p in ring],
                        color="black", lw=1.6, zorder=4)

    for iso, xy in LABEL_XY.items():
        dx, dy = LABEL_DX[iso]
        abbr = {"DNK": "DK", "IRL": "IE", "NLD": "NL"}[iso]
        txt = f"{abbr}: {share[iso]:.0f}%"
        ax.annotate(txt, xy=xy, xytext=(xy[0] + dx, xy[1] + dy),
                    fontsize=8.5, fontweight="bold", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="black", lw=0.6),
                    arrowprops=dict(arrowstyle="-", lw=0.8, color="black"))

    ax.set_xlim(-15, 32)
    ax.set_ylim(35, 62)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    ax.set_title("c  Total NH$_3$ emission changes [kt N]", fontsize=10, loc="left")

    handles = [Patch(fc=c, ec="none", label=l) for c, l in zip(
        colors, ["< −30", "−30 – −15", "−15 – −10", "−10 – −5", "−5 – 0", "> 0"])]
    handles.append(Line2D([0], [0], color="black", lw=1.6, label="DK / IE / NL"))
    ax.legend(handles=handles, loc="lower left", fontsize=7, frameon=False,
              title="NH$_3$ emission\nchanges [kt N]", title_fontsize=7)

    plt.tight_layout()
    for extn in ("png", "svg"):
        p = os.path.join(OUT, f"country_panel_c{TAG}.{extn}")
        plt.savefig(p, dpi=300 if extn == "png" else None, bbox_inches="tight")
        print("saved", p)


if __name__ == "__main__":
    country_figure()
