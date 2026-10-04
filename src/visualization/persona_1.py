"""Histogramas y boxplots ponderados del tiempo sin convivencia disponible."""
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from src.statistics.descriptivas import VARIABLE, GRUPOS, medidas_localizacion

AZUL = "#31688e"
NARANJA = "#c76b33"


def histograma_ponderado(base):
    x = base[VARIABLE].to_numpy()
    w = base["factor_expansion"].to_numpy().astype(float)
    pesos_porcentaje = 100 * w / w.sum()
    limites = np.arange(np.floor(x.min()) - .5, np.ceil(x.max()) + 2.5, 2)
    loc = medidas_localizacion(x, w)
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(x, bins=limites, weights=pesos_porcentaje, color=AZUL, edgecolor="white", linewidth=.7)
        ax.axvline(loc["media"], color=NARANJA, lw=2, ls="--", label=f"Media ponderada: {loc['media']:.2f} años")
        ax.axvline(loc["mediana"], color="#2c805c", lw=2, label=f"Mediana ponderada: {loc['mediana']:.0f} años")
        ax.set(xlabel="Años sin convivencia con la pareja (0 = menos de un año)", ylabel="Porcentaje ponderado del subconjunto (%)", xlim=(limites[0], limites[-1]))
        ax.set_title("Tiempo sin convivencia: distribucion de los casos disponibles", loc="left", pad=20, fontweight="bold")
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False)
        fig.text(.10, .03, f"n = {base.height:,}. Intervalos de 2 años. Factores normalizados al 100 % de los casos disponibles.\nP4 recupera los codigos válidos de 0 a 9; 0 indica menos de un año. Universo: A2/B1/B2; no son todas las entrevistadas.", fontsize=9, color="#555555")
        fig.subplots_adjust(left=.10, right=.97, top=.88, bottom=.22)
    return fig


def boxplot_ponderado(base):
    cajas, etiquetas = [], []
    for nombre, codigo in GRUPOS:
        datos = base if codigo is None else base.filter(pl.col("sufrio_violencia_pareja") == codigo)
        x, w = datos[VARIABLE].to_numpy(), datos["factor_expansion"].to_numpy()
        loc = medidas_localizacion(x, w)
        q1, q3 = loc["q1"], loc["q3"]
        iqr = q3 - q1
        interiores = x[(x >= q1 - 1.5 * iqr) & (x <= q3 + 1.5 * iqr)]
        low, high = float(interiores.min()), float(interiores.max())
        cajas.append({"q1": q1, "q3": q3, "med": loc["mediana"], "mean": loc["media"],
                      "whislo": low, "whishi": high, "fliers": np.unique(x[(x < low) | (x > high)]).tolist()})
        etiquetas.append(f"{nombre}\nn = {datos.height:,}")
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        fig, ax = plt.subplots(figsize=(10, 6.5))
        artists = ax.bxp(cajas, patch_artist=True, showmeans=True,
                         medianprops={"color": "#252525", "linewidth": 2},
                         meanprops={"marker": "^", "markerfacecolor": "#2c805c", "markeredgecolor": "white", "markersize": 8},
                         flierprops={"marker": "o", "markersize": 3.5, "alpha": .6})
        for caja, color in zip(artists["boxes"], ["#9da9b3", AZUL, NARANJA]):
            caja.set_facecolor(color)
            caja.set_alpha(.75)
        ax.set_xticks([1, 2, 3], etiquetas)
        ax.set_ylabel("Años sin convivencia (0 = menos de un año)")
        ax.set_title("Tiempo sin convivencia: dispersion por violencia reportada", loc="left", pad=20, fontweight="bold")
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        fig.text(.10, .03, "Cajas y mediana: cuantiles ponderados. Triangulo: media ponderada. Bigotes: valores dentro de 1.5 × IQR.\nPuntos: valores fuera de los bigotes, sin multiplicidad. Universo A2/B1/B2; códigos de 0 a 9 recuperados en P4.", fontsize=9, color="#555555")
        fig.subplots_adjust(left=.10, right=.97, top=.88, bottom=.23)
    return fig
