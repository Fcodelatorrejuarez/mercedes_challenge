# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Reto básico 1: exploración y calidad de datos (EDA)
#
# **III Malackathon 2026 · Mercedes-Benz Group Services Madrid · "Clustering the Star"**
#
# Este notebook es el entregable del reto 1 definido en `Especificaciones_proyecto.md`. Incluye:
#
# 1. **Estadísticos descriptivos** de las variables principales (§5, §6).
# 2. **Valores nulos e inconsistencias**, con el tratamiento aplicado y justificado (§3, §4, §9, §10).
# 3. **Distribuciones** de las variables clave (§6–§8).
# 4. **Exclusión justificada** de identificadores y metadatos (§9.1).
#
# El tratamiento de nulos parte de la decisión del equipo (`Descripcion_uso_de_datos`), con las
# correcciones necesarias para que el dataset resultante sea **coherente** (§9–§10).
# Las conclusiones breves están en `eda/Resumen_reto1.md`.
#
# **Cómo ejecutarlo:** desde la raíz del repositorio, con el entorno de `requirements.txt`, abrir y ejecutar
# este notebook. Alternativamente, `python eda/eda_reto1.py` produce las mismas salidas: figuras en
# `eda/figures/`, tablas en `eda/outputs/resultados.md` y datos tratados en `data/processed/`.
# El `.py` y el `.ipynb` están emparejados con jupytext.

# %%
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

try:  # dentro de Jupyter las figuras se muestran en línea; como script se guardan sin ventana
    get_ipython()  # noqa: F821
    IN_NOTEBOOK = True
except NameError:
    IN_NOTEBOOK = False
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if IN_NOTEBOOK:
    from IPython.display import Markdown, display

pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 200)

# Rutas: funciona tanto desde la raíz del repo como desde eda/
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "data" / "datos_reto_mercedes_benz_malackathon.csv").exists())
RAW = ROOT / "data" / "datos_reto_mercedes_benz_malackathon.csv"
FIG = ROOT / "eda" / "figures"
OUT = ROOT / "eda" / "outputs"
PROC = ROOT / "data" / "processed"
for p in (FIG, OUT, PROC):
    p.mkdir(parents=True, exist_ok=True)

# Fecha de referencia: la matriculación más reciente del fichero es del 2026-10-02.
REF_DATE = pd.Timestamp("2026-10-15")

STR_COLS = {c: str for c in ["client_id", "vehicle_id", "model_series", "zipcode",
                             "trip_distance_mode", "speed_mode"]}

TELEMETRY = ["trip_distance_average", "trip_distance_mode", "trip_distance_median",
             "trip_distance_all_counter", "operating_hours_total",
             "fuel_consumption_average", "speed_average", "speed_mode",
             "speed_median", "speed_all_counter"]
SOCIO = ["purchasing_power_per_inhabitant_eur", "purchasing_power_per_household_eur",
         "population", "number_of_households", "purchasing_power_millions_eur"]
CONSENTS = ["consent_phone_communication_channel", "consent_epost_communication_channel",
            "consent_post_communication_channel"]
CLIENT_COLS = ["age_range", "gender_derived", "country_code", "months_as_mb_customer",
               "currently_connected_vehicles", "finance_leasing_status", *CONSENTS,
               "zipcode", *SOCIO]
VEHICLE_COLS = ["model_series", "vehicle_type", "model_class", "product_group",
                "engine_concept", "fuel_type", "date_of_first_registration"]
AGE_ORDER = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]

# Estilo de gráficos (paleta categórica validada para daltonismo)
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLUE = CAT[0]
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DIV = ["#e34948", "#f0efec", "#2a78d6"]  # rojo <-> gris <-> azul

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelsize": 9, "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.axisbelow": True, "axes.spines.top": False,
    "axes.spines.right": False, "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
    "legend.frameon": False, "legend.fontsize": 8, "figure.dpi": 110,
})


def save(fig, name):
    """Guarda la figura en eda/figures y, en el notebook, la muestra."""
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=130, bbox_inches="tight")
    if IN_NOTEBOOK:
        plt.show()
    plt.close(fig)


def barh(ax, s: pd.Series, fmt="{:,.0f}", color=BLUE, title=None, xlabel=None):
    """Barras horizontales finas con etiqueta de valor al final."""
    s = s[::-1]
    ax.barh(s.index.astype(str), s.values, height=0.62, color=color, edgecolor=SURFACE, linewidth=1)
    ax.grid(axis="y", visible=False)
    xmax = s.max()
    for i, v in enumerate(s.values):
        ax.text(v + xmax * 0.01, i, fmt.format(v), va="center", fontsize=7.5, color=INK2)
    ax.set_xlim(0, xmax * 1.15)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)


def pct(x, d=1):
    return f"{100 * x:.{d}f} %"


# Las tablas se muestran en el notebook y además se acumulan en eda/outputs/resultados.md
_md: list[str] = []


def md(title: str, obj=None, floatfmt=",.2f", index=True):
    block = [f"\n### {title}\n"]
    if obj is not None:
        if isinstance(obj, pd.Series):
            obj = obj.to_frame()
        block += [obj.to_markdown(floatfmt=floatfmt, index=index), ""]
    _md.extend(block)
    if IN_NOTEBOOK:
        display(Markdown("\n".join(block)))


def note(text: str):
    _md.append(text + "\n")
    if IN_NOTEBOOK:
        display(Markdown(text))

# %%

# %% [markdown]
# ## 1. Carga y estructura
#
# El CSV tiene 302.850 filas y 39 columnas. `zipcode`, `model_series` y las columnas `*_mode` se leen como texto:
# son códigos o listas, y con la inferencia automática `zipcode` sale con tipos mixtos porque hay CP como `A-2100`.
# La primera columna (`Unnamed: 0`) es un índice de pandas exportado. No hay filas duplicadas y el par
# (`client_id`, `vehicle_id`) es único.

# %%
# ==========================================================================
# 1. CARGA Y ESTRUCTURA
# ==========================================================================
print("Cargando datos...")
raw = pd.read_csv(RAW, dtype=STR_COLS, low_memory=False)
df = raw.copy()

md("1.1 Dimensiones")
note(f"- Filas: **{len(df):,}**  ·  Columnas: **{df.shape[1]}** (incluida la columna sin nombre `{df.columns[0]}`)")
note(f"- Clientes únicos: **{df.client_id.nunique():,}**  ·  Vehículos únicos: **{df.vehicle_id.nunique():,}**")
note(f"- Filas duplicadas completas: **{raw.drop(columns=raw.columns[0]).duplicated().sum()}**  ·  "
     f"pares (client_id, vehicle_id) duplicados: **{df.duplicated(['client_id', 'vehicle_id']).sum()}**")
unnamed = df.columns[0]
note(f"- `{unnamed}` es igual al índice posicional 0..n-1: **{(df[unnamed].astype(int) == np.arange(len(df))).all()}**")
df = df.drop(columns=unnamed)

# Tipos
dtypes = pd.DataFrame({"dtype pandas": df.dtypes.astype(str),
                       "n_unique": df.nunique(),
                       "% nulos": df.isna().mean() * 100,
                       "ejemplo": df.apply(lambda s: s.dropna().iloc[0] if s.notna().any() else None)})
md("1.2 Tipos, cardinalidad y nulos por columna", dtypes, floatfmt=".2f")


# %% [markdown]
# ## 2. Granularidad: qué es cada fila
#
# **Cada fila es una relación cliente–vehículo, no un cliente.** Se comprueba qué atributos son constantes
# por cliente y cuáles por vehículo.

# %%
# ==========================================================================
# 2. GRANULARIDAD
# ==========================================================================
rpc = df.groupby("client_id").size()
rpv = df.groupby("vehicle_id").size()
gran = pd.DataFrame({
    "filas por cliente": rpc.describe(percentiles=[.5, .75, .9, .95, .99, .999]),
    "filas por vehículo": rpv.describe(percentiles=[.5, .75, .9, .95, .99, .999]),
})
md("2.1 Distribución de filas por cliente y por vehículo", gran)

# Atributos constantes por cliente / vehículo
multi_c = rpc[rpc > 1].index
nu_c = df[df.client_id.isin(multi_c)].groupby("client_id")[CLIENT_COLS + ["role", "role_type"]].nunique(dropna=False)
const_c = (nu_c > 1).mean().mul(100).rename("% clientes multi-fila con >1 valor")
multi_v = rpv[rpv > 1].index
vcols = VEHICLE_COLS + ["workshop_visits_warranty_goodwill", "is_current_vehicle",
                        "operating_hours_total", "trip_distance_average", "speed_average"]
nu_v = df[df.vehicle_id.isin(multi_v)].groupby("vehicle_id")[vcols].nunique(dropna=False)
const_v = (nu_v > 1).mean().mul(100).rename("% vehículos multi-fila con >1 valor")
md("2.2 ¿Qué atributos son del cliente y cuáles de la relación?", pd.concat([const_c, const_v], axis=1), floatfmt=".2f")

heavy = pd.DataFrame({
    "umbral filas/cliente": [">10", ">20", ">50", ">100"],
    "clientes": [(rpc > t).sum() for t in (10, 20, 50, 100)],
    "filas que acumulan": [rpc[rpc > t].sum() for t in (10, 20, 50, 100)],
})
heavy["% filas"] = heavy["filas que acumulan"] / len(df) * 100
md("2.3 Clientes con muchas relaciones (posibles concesionarios, flotas, rent-a-car)", heavy, index=False, floatfmt=",.2f")
big = rpc[rpc > 20].index
hv = df[df.client_id.isin(big)]
note(f"- En clientes con >20 relaciones solo el **{pct(hv.is_current_vehicle.mean())}** de filas es vehículo actual "
     f"(vs {pct(df[~df.client_id.isin(big)].is_current_vehicle.mean())} en el resto); "
     f"rol OWNER en el {pct((hv.role == 'OWNER').mean())} de sus filas y role_type B2C en el {pct((hv.role_type == 'B2C').mean())}.")

md("2.4 role vs role_type", pd.crosstab(df.role, df.role_type, margins=True))
md("2.5 role vs is_current_vehicle", pd.crosstab(df.role, df.is_current_vehicle, margins=True))


# %% [markdown]
# **Lectura:**
#
# - Los atributos de cliente (edad, país, consentimientos, CP, socio-demografía) y los de vehículo (serie, motor,
#   fecha) son **100 % consistentes** entre filas. Las visitas al taller y la telemetría varían por relación.
# - 833 "clientes" tienen más de 20 relaciones. Suman el 16 % de las filas y solo el 10 % de sus vehículos es actual:
#   probablemente son concesionarios, flotas o rent-a-car.
# - `role_type = B2B` ⇔ `role = DRIVER` en el 100 % de los casos.
#
# → **El clustering debe hacerse sobre una vista agregada por cliente.**

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
bins = [1, 2, 3, 4, 5, 6, 11, 21, 51, 101, 600]
labels = ["1", "2", "3", "4", "5", "6-10", "11-20", "21-50", "51-100", ">100"]
cnt = pd.cut(rpc, bins=bins, right=False, labels=labels).value_counts().reindex(labels)
axes[0].bar(labels, cnt.values, width=0.62, color=BLUE)
axes[0].set_yscale("log")
axes[0].set_title("Relaciones (filas) por cliente")
axes[0].set_ylabel("Nº de clientes (escala log)")
axes[0].grid(axis="x", visible=False)
for i, v in enumerate(cnt.values):
    axes[0].text(i, v * 1.15, f"{v:,}", ha="center", fontsize=7, color=INK2)
cntv = rpv.clip(upper=6).value_counts().sort_index()
axes[1].bar([str(i) if i < 6 else "6+" for i in cntv.index], cntv.values, width=0.62, color=BLUE)
axes[1].set_yscale("log")
axes[1].set_title("Clientes por vehículo")
axes[1].set_ylabel("Nº de vehículos (escala log)")
axes[1].grid(axis="x", visible=False)
for i, v in enumerate(cntv.values):
    axes[1].text(i, v * 1.15, f"{v:,}", ha="center", fontsize=7, color=INK2)
save(fig, "fig01_granularidad.png")


# %% [markdown]
# ## 3. Valores nulos
#
# Los nulos aparecen **en bloques** (telemetría, motorización, socio-demografía). Eso apunta a que su origen está
# en las fuentes de datos y no en errores de captura fila a fila.

# %%
# ==========================================================================
# 3. VALORES NULOS
# ==========================================================================
na = df.isna().mean().sort_values(ascending=False) * 100
na = na[na > 0]
fig, ax = plt.subplots(figsize=(8, 7))
colors = [CAT[1] if c in TELEMETRY else CAT[0] if c in SOCIO + ["zipcode"] else CAT[6] for c in na.index]
s = na[::-1]
ax.barh(s.index, s.values, height=0.62, color=colors[::-1])
for i, v in enumerate(s.values):
    ax.text(v + 0.6, i, f"{v:.1f} %", va="center", fontsize=7.5, color=INK2)
ax.set_xlim(0, 75)
ax.grid(axis="y", visible=False)
ax.set_xlabel("% de filas nulas")
ax.set_title("Porcentaje de nulos por columna")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=CAT[1], label="Telemetría"), Patch(color=CAT[0], label="Socio-demográfico / CP"),
                   Patch(color=CAT[6], label="Cliente / vehículo")], loc="lower right")
save(fig, "fig02_nulos_por_columna.png")

# Matriz de nulos sobre muestra ordenada
sample = df.sample(4000, random_state=42)
order_cols = [c for c in df.columns if df[c].isna().any()]
sample = sample.sort_values(["operating_hours_total", "population", "engine_concept"], na_position="last")
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.imshow(sample[order_cols].isna().T.values, aspect="auto", cmap=matplotlib.colors.ListedColormap([SEQ[4], "#f0efec"]),
          interpolation="nearest")
ax.set_yticks(range(len(order_cols)))
ax.set_yticklabels(order_cols, fontsize=7)
ax.set_xticks([])
ax.grid(False)
ax.set_xlabel("4.000 filas de muestra (ordenadas por presencia de telemetría y socio-demografía)")
ax.set_title("Mapa de nulos: azul = dato presente, gris = nulo")
save(fig, "fig03_mapa_nulos.png")


# %% [markdown]
# ### 3.1 Telemetría: mecanismo de ausencia
#
# El 52 % de las filas no tiene ninguna telemetría. La ausencia depende del rol, de si la relación es actual y de
# la antigüedad del coche: los anteriores a 2012 casi no tienen datos y los de 2026 aún no los han acumulado. Es una
# ausencia **estructural (MNAR)**: rellenarla con la media inventaría comportamiento de conducción.

# %%
# Patrones del bloque de telemetría
pat = df[TELEMETRY].notna().astype(int).astype(str).agg("".join, axis=1)
patt = pat.value_counts().head(8).rename("filas").to_frame()
patt["% filas"] = patt["filas"] / len(df) * 100
patt.index.name = "patrón (1=presente) " + "/".join(c.replace("trip_distance_", "td_").replace("speed_", "sp_")
                                                   .replace("operating_hours_total", "op_h")
                                                   .replace("fuel_consumption_average", "fuel") for c in TELEMETRY)
md("3.1 Patrones conjuntos de nulos en el bloque de telemetría", patt, floatfmt=",.2f")

df["has_telemetry"] = df[TELEMETRY].notna().any(axis=1)
df["reg_date"] = pd.to_datetime(df.date_of_first_registration, errors="coerce")
df["reg_year"] = df.reg_date.dt.year

def avail(by):
    return df.groupby(by).has_telemetry.mean().mul(100)

tel_tab = pd.concat({
    "is_current_vehicle": avail("is_current_vehicle"),
    "role": avail("role"),
    "product_group": avail("product_group"),
    "country_code": avail("country_code"),
}).rename("% filas con alguna telemetría").to_frame()
md("3.2 Disponibilidad de telemetría por grupo (mecanismo de ausencia)", tel_tab, floatfmt=".1f")

fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), gridspec_kw={"width_ratios": [1.2, 1, 2.4]})
r = avail("role").sort_values()
axes[0].barh(r.index, r.values, height=0.62, color=BLUE)
axes[0].set_xlim(0, 100); axes[0].grid(axis="y", visible=False)
axes[0].set_title("Por rol")
for i, v in enumerate(r.values):
    axes[0].text(v + 1.5, i, f"{v:.0f} %", va="center", fontsize=7.5, color=INK2)
c = avail("is_current_vehicle")
axes[1].bar(["No actual", "Actual"], c.values, width=0.55, color=BLUE)
axes[1].set_ylim(0, 100); axes[1].grid(axis="x", visible=False)
axes[1].set_title("Relación actual")
for i, v in enumerate(c.values):
    axes[1].text(i, v + 2, f"{v:.0f} %", ha="center", fontsize=7.5, color=INK2)
yy = df[df.reg_year >= 2009].groupby("reg_year").has_telemetry.mean().mul(100)
axes[2].plot(yy.index, yy.values, color=BLUE, lw=2, marker="o", ms=4)
axes[2].set_ylim(0, 100)
axes[2].set_title("Por año de 1ª matriculación")
axes[2].set_xticks(yy.index[::2])
for ax in axes:
    ax.set_ylabel("")
fig.suptitle("% de filas con algún dato de telemetría", x=0.01, ha="left", fontsize=11, fontweight="bold")
save(fig, "fig04_disponibilidad_telemetria.png")


# %% [markdown]
# ### 3.2 Motorización, género y socio-demografía
#
# - `engine_concept` (44 % nulo) y `fuel_type` (59 %) **nunca se contradicen**, y cuando falta el motor falta
#   también el combustible. La ausencia depende de la antigüedad y del producto (smart: 100 %). La nomenclatura
#   comercial (`EQ…`, `… e`, `… d`) permite recuperar buena parte de la información.
# - El género desconocido se concentra en usuarios secundarios (TEMP_USER, USER) y en los extremos de edad:
#   es un nulo **no aleatorio**.
# - Socio-demografía: cada (país, CP) tiene un único valor y **ningún CP mezcla filas con y sin dato**. 993 CP
#   existen en AT y en CH a la vez, así que la clave tiene que ser (país, CP).

# %%
# Nulos de motorización / combustible por año de matriculación
eng_year = df[df.reg_year >= 2009].groupby("reg_year").agg(
    filas=("reg_date", "size"),
    engine_na=("engine_concept", lambda s: s.isna().mean() * 100),
    fuel_na=("fuel_type", lambda s: s.isna().mean() * 100),
    telem_na=("has_telemetry", lambda s: (~s).mean() * 100))
md("3.3 Nulos de engine_concept / fuel_type / telemetría por año de matriculación (%)", eng_year, floatfmt=",.1f")

md("3.4 engine_concept vs fuel_type (filas)", pd.crosstab(df.engine_concept.fillna("<NA>"), df.fuel_type.fillna("<NA>")))

# Género por rol y edad
md("3.5 gender_derived por rol (% columna)",
   pd.crosstab(df.gender_derived.fillna("<NA>"), df.role, normalize="columns").mul(100), floatfmt=".1f")

# Socio-demográficos
note("**Socio-demográficos y CP:**")
zip_nosoc = df.zipcode.notna() & df.population.isna()
note(f"- Filas sin CP: **{df.zipcode.isna().sum():,}**; con CP pero sin cruce socio-demográfico: **{zip_nosoc.sum():,}**; "
     f"con CP y población pero sin poder adquisitivo: **{(df.population.notna() & df.purchasing_power_per_inhabitant_eur.isna()).sum():,}** "
     f"(todas con population = 0).")
z = df.zipcode.dropna()
note(f"- CP con formato no estándar (no 4 dígitos): **{(~z.str.fullmatch(r'\d{4}')).sum()}** → "
     f"{sorted(z[~z.str.fullmatch(r'\d{4}')].unique().tolist())}")
note(f"- CP que existen en AT y en CH a la vez: **{len(set(df[df.country_code == 'AT'].zipcode.dropna()) & set(df[df.country_code == 'CH'].zipcode.dropna())):,}** "
     "→ el CP solo identifica una zona junto con `country_code`.")
note(f"- (country, CP) con más de un valor socio-demográfico: **{(df.dropna(subset=['zipcode']).groupby(['country_code', 'zipcode']).population.nunique() > 1).sum()}**")
md("3.6 % nulos por país", df.groupby("country_code")[["gender_derived", "zipcode", "population",
                                                       "purchasing_power_per_inhabitant_eur", "engine_concept",
                                                       "fuel_type", "has_telemetry"]]
   .agg(lambda s: (s.isna() if s.name != "has_telemetry" else ~s).mean() * 100), floatfmt=".2f")


# %% [markdown]
# ## 4. Inconsistencias y anomalías
#
# Se buscan relaciones deterministas (columnas que son copia de otras), taxonomías solapadas, valores imposibles
# y artefactos.

# %%
# ==========================================================================
# 4. INCONSISTENCIAS Y ANOMALÍAS
# ==========================================================================
# 4.1 Redundancias exactas
s = df.dropna(subset=["population", "purchasing_power_per_inhabitant_eur"]).query("population > 0 and number_of_households > 0")
err1 = ((s.purchasing_power_per_inhabitant_eur * s.population / 1e6 - s.purchasing_power_millions_eur).abs()
        / s.purchasing_power_millions_eur)
err2 = ((s.purchasing_power_millions_eur * 1e6 / s.number_of_households - s.purchasing_power_per_household_eur).abs()
        / s.purchasing_power_per_household_eur)
note("**Redundancias deterministas:**")
note(f"- `purchasing_power_millions_eur` = `purchasing_power_per_inhabitant_eur` × `population` / 1e6 → error relativo máx. **{err1.max():.1e}**")
note(f"- `purchasing_power_per_household_eur` = `purchasing_power_millions_eur` × 1e6 / `number_of_households` → error relativo máx. **{err2.max():.1e}**")
hh = s.population / s.number_of_households
note(f"- Tamaño medio del hogar (population / households): mediana **{hh.median():.2f}**, p1–p99 [{hh.quantile(.01):.2f}, {hh.quantile(.99):.2f}]")
note(f"- `role_type` = B2B ⇔ `role` = DRIVER en el **100 %** de filas (ver 2.4).")
ms_conf = (df.dropna(subset=["model_class"]).groupby("model_series").model_class.nunique() > 1).sum()
note(f"- `model_series` → `model_class` es una función: series con >1 clase = **{ms_conf}**.")


# %% [markdown]
# **Redundancias encontradas:** PA total = PA/hab × población / 1e6 y PA/hogar = PA total / hogares (error < 0,1 %);
# población ↔ hogares (ρ = 0,998); `model_series` → `model_class` es una función exacta.
#
# A continuación: taxonomía de `model_class` (etiquetas solapadas de distintas épocas y series nuevas de 2026 sin clase),
# fechas y antigüedad como cliente.

# %%
# 4.2 Taxonomía de model_class
mc = df.model_class.value_counts(dropna=False)
md("4.1 model_class (filas) - taxonomía solapada", mc.rename("filas"))
mc_na = df[df.model_class.isna()].groupby("model_series").agg(
    filas=("vehicle_id", "size"),
    vehicle_types=("vehicle_type", lambda s: ", ".join(s.value_counts().head(3).index)),
    año_mediano=("reg_year", "median"))
md("4.2 model_class nulo: series de modelo nuevas sin clase asignada", mc_na.sort_values("filas", ascending=False), floatfmt=",.0f")
md("4.3 product_group vs nº de clases", df.groupby("product_group").agg(
    filas=("vehicle_id", "size"), clases=("model_class", lambda s: ", ".join(s.value_counts().head(5).index))))

# 4.3 vehicle_type con códigos técnicos (vans)
vt = df.vehicle_type.dropna()
tech = vt[vt.str.contains(r"\dX\d|\s{2,}")]
note(f"- `vehicle_type` con códigos técnicos (furgonetas, p. ej. `{tech.value_counts().index[0]}`): **{len(tech):,}** filas, "
     f"{tech.nunique()} valores distintos. Cardinalidad total: **{vt.nunique():,}** valores.")

# 4.4 Fechas
note("**Fechas de primera matriculación:**")
note(f"- Rango: **{df.reg_date.min().date()}** → **{df.reg_date.max().date()}**; nulas: **{df.reg_date.isna().sum():,}**; "
     f"posteriores a la fecha de referencia ({REF_DATE.date()}): **{(df.reg_date > REF_DATE).sum()}**; anteriores a 2009: **{(df.reg_year < 2009).sum()}**")
df["vehicle_age_years"] = (REF_DATE - df.reg_date).dt.days / 365.25

# 4.5 months_as_mb_customer
cl0 = df.drop_duplicates("client_id")
months = cl0.months_as_mb_customer
vc_m = months.value_counts()
note("**`months_as_mb_customer` (a nivel cliente):**")
note(f"- Valor 36: **{vc_m.get(36.0, 0):,}** clientes ({pct(vc_m.get(36.0, 0) / len(cl0))}) frente a "
     f"{vc_m.get(35.0, 0):,} en 35 y {vc_m.get(37.0, 0):,} en 37 → pico artificial (≈ ×{vc_m.get(36.0, 0) / np.mean([vc_m.get(35.0, 0), vc_m.get(37.0, 0)]):.0f}).")
note(f"- Valor 0: **{vc_m.get(0.0, 0):,}** clientes; máximo **{months.max():.0f}** meses (10 años, posible truncado); nulos: **{months.isna().sum()}**.")
first_reg = df.groupby("client_id").reg_date.min()
m36 = cl0.set_index("client_id").months_as_mb_customer
diff = m36 - (REF_DATE - first_reg).dt.days / 30.44
note(f"- `months_as_mb_customer` − meses desde la matriculación más antigua del cliente: mediana **{diff.median():.1f}** "
     f"(p5 {diff.quantile(.05):.0f}, p95 {diff.quantile(.95):.0f}). La relación con la marca empieza en la *conexión* "
     "(Mercedes me), no en la matriculación: lo normal es que sea más corta que la edad del coche (vehículos de ocasión, "
     "conexión posterior). Los clientes con 36 meses tienen su primer coche matriculado sobre todo en "
     f"{', '.join(map(str, first_reg[m36[m36 == 36].index].dt.year.value_counts().head(3).index.astype(int)))}.")

# currently_connected_vehicles vs filas actuales
ncur = df.groupby("client_id").is_current_vehicle.sum()
ccv = cl0.set_index("client_id").currently_connected_vehicles
note(f"- `currently_connected_vehicles` = nº de filas con `is_current_vehicle` = True del cliente en el **{pct((ccv == ncur[ccv.index]).mean(), 3)}** "
     f"de clientes (discrepancias: {(ccv != ncur[ccv.index]).sum()}). Clientes sin ningún vehículo actual: **{(ncur == 0).sum():,}** ({pct((ncur == 0).mean())}).")


# %% [markdown]
# **Lectura de lo anterior:**
#
# - `months_as_mb_customer` tiene un **pico artificial en 36 meses**: el 12 % de los clientes, 8 veces más que los
#   meses vecinos. Su máximo es exactamente 120.
# - `currently_connected_vehicles` cuadra con `is_current_vehicle` en el 99,998 % de los clientes. El 10,4 % de los
#   clientes no tiene ningún vehículo actual.
#
# ### 4.1 Telemetría: valores imposibles y artefactos
#
# Hay velocidades medias por debajo de 1 km/h, horas a 0, contadores a 0 con métricas informadas y valores en los
# topes del sensor. Las medianas y modas son marcas de clase de **dos esquemas de bins distintos**, y las modas son
# texto con empates.

# %%
# 4.6 Telemetría: anomalías
anom = pd.DataFrame({
    "regla": [
        "speed_average < 1 km/h",
        "speed_average ≥ 150 km/h",
        "operating_hours_total = 0",
        "operating_hours_total > 5.000 h",
        "trip_distance_all_counter = 0 con mediana/moda informada",
        "speed_all_counter = 0",
        "fuel_consumption_average en tope inferior (3,0)",
        "fuel_consumption_average en tope superior (50,0)",
        "trip_distance_average en tope (300 km)",
        "fuel_consumption_average informado en ELECTRIC",
        "trip_distance_mode con varios valores (empate)",
        "speed_mode con varios valores (empate)",
    ],
    "filas": [
        (df.speed_average < 1).sum(),
        (df.speed_average >= 150).sum(),
        (df.operating_hours_total == 0).sum(),
        (df.operating_hours_total > 5000).sum(),
        ((df.trip_distance_all_counter == 0) & df.trip_distance_median.notna()).sum(),
        (df.speed_all_counter == 0).sum(),
        (df.fuel_consumption_average == 3.0).sum(),
        (df.fuel_consumption_average == 50.0).sum(),
        (df.trip_distance_average == 300.0).sum(),
        ((df.engine_concept == "ELECTRIC") & df.fuel_consumption_average.notna()).sum(),
        df.trip_distance_mode.str.contains(",", na=False).sum(),
        df.speed_mode.str.contains(",", na=False).sum(),
    ]})
md("4.4 Anomalías detectadas en telemetría", anom, index=False, floatfmt=",.0f")
note(f"- Valores únicos de `trip_distance_median`: {sorted(df.trip_distance_median.dropna().unique().tolist())}")
note(f"- Valores únicos de `speed_median`: {[round(x, 4) for x in sorted(df.speed_median.dropna().unique().tolist())]}")
note("- Son marcas de clase de histogramas: conviven **dos esquemas de bins** (1/3/7,5/15/27,5/42,5… y 2,5/10/22,5…), "
     "probablemente por distintas generaciones de la unidad telemática. `speed_median` incluye el artefacto de coma flotante 220.00000000000003.")
md("4.5 Consumo medio por fuel_type (l/100 km)", df.groupby(df.fuel_type.fillna("<NA>")).fuel_consumption_average.describe(), floatfmt=",.2f")


# %% [markdown]
# ## 5. Estadísticos descriptivos
#
# A nivel fila (relación). Las variables de uso y de tamaño de zona tienen colas largas (asimetría de 3 a 8), así que
# K-Means necesitará transformación logarítmica o winsorización antes de escalar. `currently_connected_vehicles`
# sale inflado a nivel fila por los clientes con muchas filas: la media es 2,15 por fila frente a 1,04 por cliente.

# %%
# ==========================================================================
# 5. ESTADÍSTICOS DESCRIPTIVOS
# ==========================================================================
num_cols = ["months_as_mb_customer", "currently_connected_vehicles", "workshop_visits_warranty_goodwill",
            "vehicle_age_years", *SOCIO, "trip_distance_average", "trip_distance_median", "trip_distance_all_counter",
            "operating_hours_total", "fuel_consumption_average", "speed_average", "speed_median", "speed_all_counter"]
desc = df[num_cols].describe(percentiles=[.01, .25, .5, .75, .99]).T
desc["skew"] = df[num_cols].skew()
desc["% nulos"] = df[num_cols].isna().mean() * 100
md("5.1 Estadísticos descriptivos numéricos (nivel fila cliente-vehículo)", desc, floatfmt=",.2f")

# IQR outliers
iqr = {}
for c in num_cols:
    x = df[c].dropna()
    q1, q3 = x.quantile([.25, .75])
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    iqr[c] = {"límite inf.": lo, "límite sup.": hi, "% outliers (IQR)": ((x < lo) | (x > hi)).mean() * 100}
md("5.2 Outliers por regla IQR (1,5×)", pd.DataFrame(iqr).T, floatfmt=",.2f")

cat_cols = ["age_range", "gender_derived", "country_code", "product_group", "model_class", "engine_concept",
            "fuel_type", "role", "role_type", "finance_leasing_status", "is_current_vehicle", *CONSENTS]
cat_desc = pd.DataFrame({
    "n_unique": df[cat_cols].nunique(),
    "moda": df[cat_cols].mode().iloc[0],
    "% moda": [df[c].value_counts(normalize=True).iloc[0] * 100 for c in cat_cols],
    "% nulos": df[cat_cols].isna().mean() * 100})
md("5.3 Descriptivos categóricos (nivel fila)", cat_desc, floatfmt=".2f")


# %% [markdown]
# ## 6. Perfil del cliente (una fila por cliente, n = 173.456)

# %%
# ==========================================================================
# 6. VISTA A NIVEL CLIENTE
# ==========================================================================
g = df.groupby("client_id")
cl = cl0.set_index("client_id")[CLIENT_COLS].copy()
cl["n_relaciones"] = g.size()
cl["n_vehiculos_actuales"] = g.is_current_vehicle.sum()
cl["es_b2b"] = g.role_type.apply(lambda s: (s == "B2B").any())
cur = df[df.is_current_vehicle]
cl["edad_media_vehiculo_actual"] = cur.groupby("client_id").vehicle_age_years.mean()
cl["tiene_electrificado_actual"] = cur.groupby("client_id").engine_concept.apply(
    lambda s: s.isin(["ELECTRIC", "PLUGIN_HYBRID"]).any()).reindex(cl.index)
cl["visitas_taller_total"] = g.workshop_visits_warranty_goodwill.sum()
cl["tiene_telemetria"] = g.has_telemetry.any()

clv = {}
for c in ["age_range", "gender_derived", "country_code", "finance_leasing_status"]:
    t = cl[c].fillna("<NA>").value_counts()
    clv[c] = pd.DataFrame({"clientes": t, "%": t / len(cl) * 100})
md("6.1 Perfil demográfico y comercial (nivel cliente)",
   pd.concat(clv, names=["variable", "valor"]), floatfmt=",.2f")

cc = cl[CONSENTS].astype(int).astype(str).agg("".join, axis=1).value_counts()
cct = pd.DataFrame({"clientes": cc, "%": cc / len(cl) * 100})
cct.index.name = "teléfono/email/correo (1=sí)"
md("6.2 Combinaciones de consentimiento (nivel cliente)", cct, floatfmt=",.2f")
md("6.3 Tasa de consentimiento por canal y país (%)", cl.groupby("country_code")[CONSENTS].mean() * 100, floatfmt=".1f")

cln = cl[["months_as_mb_customer", "currently_connected_vehicles", "n_relaciones", "visitas_taller_total",
          "edad_media_vehiculo_actual", "purchasing_power_per_inhabitant_eur"]].describe(
    percentiles=[.25, .5, .75, .9, .99]).T
md("6.4 Descriptivos numéricos a nivel cliente", cln, floatfmt=",.2f")

md("6.5 Edad × financiación (% fila)", pd.crosstab(cl.age_range, cl.finance_leasing_status, normalize="index")
   .reindex(AGE_ORDER).mul(100), floatfmt=".1f")
md("6.6 País × financiación (% fila)", pd.crosstab(cl.country_code, cl.finance_leasing_status, normalize="index").mul(100), floatfmt=".1f")
md("6.7 Edad × género (% columna)", pd.crosstab(cl.gender_derived.fillna("<NA>"), cl.age_range, normalize="columns")[AGE_ORDER].mul(100), floatfmt=".1f")
md("6.8 Poder adquisitivo por habitante (mediana €) por país y edad",
   cl.pivot_table(index="age_range", columns="country_code", values="purchasing_power_per_inhabitant_eur", aggfunc="median").reindex(AGE_ORDER),
   floatfmt=",.0f")
note(f"- Clientes con algún vehículo electrificado (BEV/PHEV) actual: **{pct(cl.tiene_electrificado_actual.fillna(False).mean())}**; "
     f"clientes multi-vehículo (≥2 actuales): **{pct((cl.n_vehiculos_actuales >= 2).mean())}**; B2B: **{pct(cl.es_b2b.mean(), 2)}**.")


# %% [markdown]
# **Lectura:**
#
# - La base es **madura**: el 61 % tiene 45 años o más.
# - Género: 65 % hombres, 18 % mujeres y 17 % desconocido. País: 66 % Suiza.
# - El **81 % tiene un único vehículo conectado**.
# - El 71 % no ha usado nunca leasing. El leasing llega al 29 % en Suiza frente al 13 % en Austria, con un pico del
#   33 % entre los 35 y los 44 años.
# - El 81 % acepta todos los canales de contacto.

# %%
# Figuras demográficas
fig, axes = plt.subplots(2, 2, figsize=(10, 6.4))
a = cl.age_range.value_counts().reindex(AGE_ORDER)
axes[0, 0].bar(a.index, a.values / len(cl) * 100, width=0.62, color=BLUE)
axes[0, 0].set_title("Rango de edad (% clientes)"); axes[0, 0].grid(axis="x", visible=False)
for i, v in enumerate(a.values / len(cl) * 100):
    axes[0, 0].text(i, v + 0.4, f"{v:.1f}", ha="center", fontsize=7.5, color=INK2)
gd = cl.gender_derived.fillna("desconocido").value_counts() / len(cl) * 100
barh(axes[0, 1], gd, fmt="{:.1f} %", title="Género derivado (% clientes)")
ct = cl.country_code.value_counts() / len(cl) * 100
barh(axes[1, 0], ct.rename({"CH": "Suiza (CH)", "AT": "Austria (AT)"}), fmt="{:.1f} %", title="País (% clientes)")
fl = cl.finance_leasing_status.value_counts() / len(cl) * 100
barh(axes[1, 1], fl, fmt="{:.1f} %", title="Situación de financiación / leasing (% clientes)")
save(fig, "fig05_perfil_cliente.png")

fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
mm = cl.months_as_mb_customer.dropna()
axes[0].hist(mm, bins=np.arange(-0.5, 121.5, 1), color=BLUE, edgecolor=SURFACE, linewidth=0.6)
axes[0].axvline(36, color=CAT[7], lw=1, ls="--")
axes[0].annotate("pico en 36 meses", xy=(36, (mm == 36).sum()), xytext=(55, (mm == 36).sum() * 0.9),
                 fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
axes[0].set_title("Meses como cliente MB"); axes[0].set_xlabel("meses"); axes[0].set_ylabel("clientes")
cv = cl.currently_connected_vehicles.clip(upper=6).value_counts().sort_index()
axes[1].bar([str(i) if i < 6 else "6+" for i in cv.index], cv.values / len(cl) * 100, width=0.62, color=BLUE)
axes[1].set_title("Vehículos conectados actualmente"); axes[1].set_ylabel("% clientes"); axes[1].grid(axis="x", visible=False)
for i, v in enumerate(cv.values / len(cl) * 100):
    axes[1].text(i, v + 1, f"{v:.1f}", ha="center", fontsize=7.5, color=INK2)
wv = df.workshop_visits_warranty_goodwill.clip(upper=12)
w = wv.value_counts().sort_index()
axes[2].bar([str(i) if i < 12 else "12+" for i in w.index], w.values, width=0.62, color=BLUE)
axes[2].set_title("Visitas taller en garantía (por relación)"); axes[2].set_ylabel("filas"); axes[2].grid(axis="x", visible=False)
save(fig, "fig06_relacion_marca.png")

fig, ax = plt.subplots(figsize=(7.5, 4.2))
ct6 = pd.crosstab(cl.age_range, cl.finance_leasing_status, normalize="index").reindex(AGE_ORDER).mul(100)
ct6 = ct6[["never_active", "active_FL_only", "active_FL_and_CASH", "was_active"]]
left = np.zeros(len(ct6))
for i, col in enumerate(ct6.columns):
    ax.barh(ct6.index, ct6[col], left=left, height=0.62, color=CAT[i], edgecolor=SURFACE, linewidth=2, label=col)
    for j, v in enumerate(ct6[col].values):
        if v > 6:
            ax.text(left[j] + v / 2, j, f"{v:.0f}", ha="center", va="center", fontsize=7.5, color="white")
    left += ct6[col].values
ax.set_xlim(0, 100); ax.invert_yaxis(); ax.grid(axis="y", visible=False)
ax.set_xlabel("% de clientes del rango de edad")
ax.set_title("Financiación / leasing por rango de edad")
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.17))
save(fig, "fig07_financiacion_edad.png")


# %% [markdown]
# ## 7. Vehículo
#
# - Dominan GLC, C, A y B/GLA/GLB. El 59 % es 4MATIC, el 13 % es AMG y el 14 % son furgonetas.
# - La electrificación se acelera: los BEV pasan del 2,5 % de las matriculaciones de 2019 al 37,5 % de las de 2026.
#   Austria está más electrificada que Suiza.
# - Las visitas en garantía crecen hasta los 4–5 años de antigüedad.

# %%
# ==========================================================================
# 7. VEHÍCULO
# ==========================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1.6, 1]})
mct = df.model_class.fillna("<sin clase>").value_counts().head(15)
barh(axes[0], mct, title="Top 15 model_class (filas)")
ecv = df.engine_concept.fillna("<NA>").value_counts()
barh(axes[1], ecv / len(df) * 100, fmt="{:.1f} %", title="engine_concept (% filas)")
save(fig, "fig08_vehiculo_clase_motor.png")

fig, ax = plt.subplots(figsize=(10, 4.2))
ey = df[(df.reg_year >= 2015) & df.engine_concept.notna()]
ey = pd.crosstab(ey.reg_year.astype(int), ey.engine_concept, normalize="index").mul(100)[
    ["COMBUSTION", "MILD_HYBRID", "PLUGIN_HYBRID", "ELECTRIC"]]
bottom = np.zeros(len(ey))
for i, col in enumerate(ey.columns):
    ax.bar(ey.index.astype(str), ey[col], bottom=bottom, width=0.7, color=CAT[i], edgecolor=SURFACE, linewidth=2, label=col)
    bottom += ey[col].values
ax.set_ylim(0, 100); ax.grid(axis="x", visible=False)
ax.set_ylabel("% de vehículos con motorización conocida")
ax.set_title("Mix de motorización por año de primera matriculación")
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.1))
save(fig, "fig09_electrificacion_por_anio.png")
md("7.1 Mix de motorización por año de matriculación (% sobre conocidos)", ey, floatfmt=".1f")

fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
va = df.vehicle_age_years.dropna()
axes[0].hist(va.clip(upper=20), bins=40, color=BLUE, edgecolor=SURFACE, linewidth=0.6)
axes[0].axvline(va.median(), color=CAT[7], lw=1, ls="--")
axes[0].text(va.median() + 0.3, axes[0].get_ylim()[1] * 0.9, f"mediana {va.median():.1f} años", fontsize=7.5, color=INK2)
axes[0].set_title("Antigüedad del vehículo (años, recortada a 20)"); axes[0].set_ylabel("filas")
wb = df.groupby(pd.cut(df.vehicle_age_years, [0, 1, 2, 3, 4, 5, 7, 10, 40])).workshop_visits_warranty_goodwill.mean()
axes[1].bar(["0-1", "1-2", "2-3", "3-4", "4-5", "5-7", "7-10", ">10"], wb.values, width=0.62, color=BLUE)
axes[1].set_title("Visitas medias en garantía por antigüedad"); axes[1].set_ylabel("visitas / relación")
axes[1].grid(axis="x", visible=False)
save(fig, "fig10_antiguedad_taller.png")
md("7.2 Visitas en garantía medias por antigüedad del vehículo", wb.rename("visitas medias"), floatfmt=".2f")

pgt = df.product_group.value_counts().rename("filas").to_frame()
pgt["% filas"] = pgt.filas / len(df) * 100
pgt["significado (deducido de model_class)"] = pgt.index.map(
    {"P": "Turismos", "T": "Furgonetas / transporter (V-Class, Vito, Sprinter, Citan, X-Class)",
     "G": "Clase G (todoterreno)", "F": "smart (fortwo/forfour)"})
md("7.3 product_group", pgt, floatfmt=",.2f")
flags = pd.Series({
    "AMG (vehicle_type empieza por 'AMG')": df.vehicle_type.fillna("").str.startswith("AMG").mean() * 100,
    "4MATIC (tracción integral)": df.vehicle_type.fillna("").str.contains("4MATIC").mean() * 100,
    "Maybach": df.vehicle_type.fillna("").str.contains("Maybach", case=False).mean() * 100,
}, name="% filas")
md("7.4 Señales de gama extraíbles de vehicle_type", flags, floatfmt=".2f")
md("7.5 engine_concept por país (% fila, sobre conocidos)",
   pd.crosstab(df.country_code, df.engine_concept, normalize="index").mul(100), floatfmt=".1f")


# %% [markdown]
# ## 8. Socio-demografía, uso y correlaciones
#
# - El poder adquisitivo depende sobre todo del país: mediana de 30 k€ por habitante en AT frente a 51 k€ en CH.
#   Conviene estandarizarlo dentro de cada país.
# - Uso típico: trayectos de 14 km a 49 km/h y unas 400 h acumuladas.
# - El consumo es coherente con el combustible: diésel < gasolina < súper plus (AMG).

# %%
# ==========================================================================
# 8. SOCIO-DEMOGRAFÍA Y TELEMETRÍA: DISTRIBUCIONES
# ==========================================================================
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for i, (cc_, lab) in enumerate([("AT", "Austria"), ("CH", "Suiza")]):
    x = cl.loc[cl.country_code == cc_, "purchasing_power_per_inhabitant_eur"].dropna() / 1000
    axes[i].hist(x, bins=50, color=CAT[i], edgecolor=SURFACE, linewidth=0.5)
    axes[i].axvline(x.median(), color=INK2, lw=1, ls="--")
    axes[i].text(x.median() * 1.03, axes[i].get_ylim()[1] * 0.9, f"mediana {x.median():.1f} k€", fontsize=7.5, color=INK2)
    axes[i].set_title(f"Poder adquisitivo/hab. - {lab}")
    axes[i].set_xlabel("miles de € por habitante"); axes[i].set_ylabel("clientes")
pop = cl.population.dropna()
axes[2].hist(np.log10(pop[pop > 0]), bins=50, color=BLUE, edgecolor=SURFACE, linewidth=0.5)
axes[2].set_title("Población del CP (log10)"); axes[2].set_xlabel("log10(habitantes)"); axes[2].set_ylabel("clientes")
save(fig, "fig11_socio_demografia.png")
md("8.1 Socio-demografía por país (mediana, nivel cliente)", cl.groupby("country_code")[SOCIO].median(), floatfmt=",.1f")

tel_num = [("trip_distance_average", "Distancia media por trayecto (km)", (0, 60)),
           ("operating_hours_total", "Horas de funcionamiento totales", (0, 3500)),
           ("fuel_consumption_average", "Consumo medio (l/100 km)", (0, 25)),
           ("speed_average", "Velocidad media (km/h)", (0, 110)),
           ("trip_distance_all_counter", "Nº de trayectos medidos", (0, 12000)),
           ("workshop_visits_warranty_goodwill", "Visitas en garantía", (0, 15))]
fig, axes = plt.subplots(2, 3, figsize=(12, 6))
for ax, (c, lab, rng) in zip(axes.flat, tel_num):
    x = df[c].dropna()
    b = np.arange(rng[0] - 0.5, rng[1] + 1.5, 1) if c == "workshop_visits_warranty_goodwill" else 50
    ax.hist(x.clip(*rng), bins=b, range=None if c == "workshop_visits_warranty_goodwill" else rng, color=BLUE,
            edgecolor=SURFACE, linewidth=0.5)
    ax.axvline(x.median(), color=CAT[7], lw=1, ls="--")
    ax.set_title(lab, fontsize=9.5)
    ax.text(0.98, 0.92, f"n={len(x):,}\nmediana={x.median():,.1f}\nskew={x.skew():.1f}", transform=ax.transAxes,
            ha="right", va="top", fontsize=7.5, color=INK2)
fig.suptitle("Distribuciones de uso del vehículo (valores > rango agrupados en el último bin)", x=0.01, ha="left",
             fontsize=11, fontweight="bold")
save(fig, "fig12_distribuciones_telemetria.png")

fig, ax = plt.subplots(figsize=(9, 3.8))
order = ["DIESEL", "PETROL", "PETROL_PLUS", "DIESEL,ELECTRIC", "PETROL,ELECTRIC", "PETROL_PLUS,ELECTRIC"]
data = [df.loc[df.fuel_type == f, "fuel_consumption_average"].dropna().values for f in order]
bp = ax.boxplot(data, orientation="horizontal", widths=0.5, showfliers=False, patch_artist=True,
                medianprops=dict(color=INK, lw=1.2), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED))
for b in bp["boxes"]:
    b.set(facecolor=SEQ[1], edgecolor=SEQ[4])
ax.set_yticks(range(1, len(order) + 1)); ax.set_yticklabels(order)
ax.set_xlabel("l/100 km (sin outliers)"); ax.grid(axis="y", visible=False)
ax.set_title("Consumo medio por tipo de combustible")
save(fig, "fig13_consumo_por_combustible.png")


# %% [markdown]
# ### 8.1 Correlaciones
#
# Hay bloques redundantes (|ρ| ≥ 0,93): población ↔ hogares ↔ PA total, PA/habitante ↔ PA/hogar, y horas ↔
# contadores. Fuera de esos bloques, casi todas las variables son independientes (|ρ| < 0,3), así que cada bloque
# aporta información distinta para segmentar. Hay relaciones con sentido de negocio, como más uso → más taller
# (ρ = 0,38–0,45).

# %%
# Correlación de Spearman
corr_cols = ["months_as_mb_customer", "currently_connected_vehicles", "workshop_visits_warranty_goodwill",
             "vehicle_age_years", "purchasing_power_per_inhabitant_eur", "purchasing_power_per_household_eur",
             "population", "number_of_households", "purchasing_power_millions_eur", "trip_distance_average",
             "trip_distance_median", "trip_distance_all_counter", "operating_hours_total",
             "fuel_consumption_average", "speed_average", "speed_median", "speed_all_counter"]
corr = df[corr_cols].corr(method="spearman")
short = {"months_as_mb_customer": "meses cliente", "currently_connected_vehicles": "veh. conectados",
         "workshop_visits_warranty_goodwill": "visitas garantía", "vehicle_age_years": "antigüedad veh.",
         "purchasing_power_per_inhabitant_eur": "PA/habitante", "purchasing_power_per_household_eur": "PA/hogar",
         "population": "población", "number_of_households": "nº hogares", "purchasing_power_millions_eur": "PA total M€",
         "trip_distance_average": "dist. media", "trip_distance_median": "dist. mediana",
         "trip_distance_all_counter": "nº trayectos", "operating_hours_total": "horas func.",
         "fuel_consumption_average": "consumo", "speed_average": "vel. media", "speed_median": "vel. mediana",
         "speed_all_counter": "nº med. velocidad"}
fig, ax = plt.subplots(figsize=(9.5, 8))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("div", DIV)
im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1)
ax.set_xticks(range(len(corr))); ax.set_yticks(range(len(corr)))
ax.set_xticklabels([short[c] for c in corr.columns], rotation=60, ha="right", fontsize=7.5)
ax.set_yticklabels([short[c] for c in corr.index], fontsize=7.5)
ax.grid(False)
for i in range(len(corr)):
    for j in range(len(corr)):
        v = corr.values[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6, color="white" if abs(v) > 0.6 else INK2)
fig.colorbar(im, ax=ax, shrink=0.7, label="ρ de Spearman")
ax.set_title("Correlación de Spearman entre variables numéricas")
save(fig, "fig14_correlacion_spearman.png")
strong = corr.where(np.triu(np.ones(corr.shape, dtype=bool), 1)).stack()
strong = strong[strong.abs() >= 0.7].sort_values(key=abs, ascending=False).rename("ρ Spearman")
strong.index = [f"{a} ↔ {b}" for a, b in strong.index]
md("8.2 Pares con |ρ| ≥ 0,7 (candidatos a redundancia)", strong, floatfmt=".3f")

# Bins de mediana: dos esquemas
fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
tm = df.trip_distance_median.value_counts().sort_index()
axes[0].bar([f"{v:g}" for v in tm.index], tm.values, width=0.62, color=BLUE)
axes[0].set_yscale("log"); axes[0].set_title("Valores de trip_distance_median (km)"); axes[0].set_ylabel("filas (log)")
axes[0].grid(axis="x", visible=False); axes[0].tick_params(axis="x", rotation=45)
sm = df.speed_median.round(4).value_counts().sort_index()
axes[1].bar([f"{v:g}" for v in sm.index], sm.values, width=0.62, color=BLUE)
axes[1].set_yscale("log"); axes[1].set_title("Valores de speed_median (km/h)"); axes[1].set_ylabel("filas (log)")
axes[1].grid(axis="x", visible=False); axes[1].tick_params(axis="x", rotation=45)
save(fig, "fig15_medianas_discretizadas.png")

# Consentimientos
fig, ax = plt.subplots(figsize=(7, 3.2))
names = {"111": "Todos los canales", "010": "Solo email", "110": "Teléfono + email", "011": "Email + correo",
         "001": "Solo correo postal", "100": "Solo teléfono", "101": "Teléfono + correo", "000": "Ninguno"}
c2 = (cc / len(cl) * 100).rename(index=names)
barh(ax, c2, fmt="{:.1f} %", title="Combinaciones de consentimiento (% clientes)")
save(fig, "fig16_consentimientos.png")

# %% [markdown]
# ## 9. Tratamiento de nulos
#
# Se parte de la decisión del equipo (`Descripcion_uso_de_datos`). El documento nombra las columnas por su
# letra al abrir el CSV en Excel (A = índice sin nombre, …, AM = `purchasing_power_millions_eur`).
#
# Aplicada al pie de la letra, esa decisión generaba **incoherencias** en el dataset:
#
# | Regla original | Incoherencia | Corrección aplicada |
# |---|---|---|
# | J: motor nulo → moda (COMBUSTION) | 7.114 vehículos `EQ…` (eléctricos) quedaban como combustión; la combustión subía del 58 % al 77 % | Cascada de reglas validadas (nombre comercial, serie, año; 99–100 % de acierto). La moda solo se usa para lo que queda: primero la de su serie y después la global |
# | L: combustible derivado de J por moda | 71.283 turismos de gasolina quedaban como DIESEL | Se sigue derivando de J, pero con el nombre comercial (`d`/CDI/BlueTEC → diésel; furgoneta → diésel; resto → gasolina; PHEV `de` → diésel-eléctrico) |
# | AA: CP aleatorio entre el mín. y el máx. | El 68 % de los CP generados no existía; un mismo cliente podía recibir CP distintos en cada fila | CP sorteado **entre los CP reales** del país con datos, ponderado por nº de clientes y **uno por cliente** |
# | X, Y, Z, AL, AM: media/moda del CP | Nunca aplicable a CP existentes (el dato es constante por CP); rellenos independientes rompían las identidades PA total = PA/hab × población | Valor del CP (real o sorteado). Si el CP no tiene datos, mediana de la región para X y Z, y **Y, AL y AM se recalculan** con las identidades |
# | AB–AG → 0 y AH → moda de la serie | Filas sin telemetría con distancia y consumo 0 pero velocidad 50 km/h; filas parciales con 0 trayectos y cientos de horas | **Sin telemetría:** todo a 0, también velocidad y contadores. **Telemetría parcial:** la métrica que falta toma la mediana de su serie (AH: moda de su serie; AC/AI: moda de la serie, que es un bin válido; consumo de un eléctrico: 0) |
# | AK: contador nulo → 1 | Contador 1 con velocidad 0 | 0 si no hay telemetría; mediana de la serie si es parcial |
# | `population = 0` | PA por habitante imputado con población 0 | Se trata como CP sin datos (respaldo de región) |
#
# El resto de reglas del documento se aplica tal cual: E → `unknown`, G → moda de su serie, Q → 0, N/O/P/R/S/T/U/V/W
# (sin nulos en este extracto) y eliminar A, B, C y H. **M** (fecha de matriculación, "?" en el documento) sigue
# **pendiente**: provisionalmente se usa la mediana de su serie, con un flag.
#
# Cada relleno deja un flag (`has_telemetry`, `tel_partial`, `zip_imputed`, `socio_imputed`, `engine_imputed`,
# `fuel_imputed`, `reg_date_imputed`) para poder aislar su efecto en el clustering.

# %%
print("Aplicando tratamiento...")
RAW_COLS = list(raw.columns)


def col_letter(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


L = {col_letter(i): c for i, c in enumerate(RAW_COLS)}  # L["AA"] -> "zipcode"
DECISION = {
    "A": "Quitar (ruido)", "B": "Quitar (ruido) · se conserva solo como clave", "C": "Quitar (ruido) · se conserva solo como clave",
    "D": "Sin nulos", "E": "Nulos → 'unknown'", "F": "Sin nulos", "G": "Nulos → moda de su model_series",
    "H": "Quitar (ruido): función exacta de F", "I": "Sin nulos",
    "J": "Nulos → cascada validada (nombre, serie, año) → moda de la serie → moda global",
    "K": "Sin nulos", "L": "Nulos → derivado de J + nombre comercial",
    "M": "PENDIENTE (?): provisional mediana de su serie + flag", "N": "Nulos → False",
    "O": "Nulos → OWNER (moda)", "P": "Nulos → B2C (moda)", "Q": "Nulos → 0.0", "R": "Nulos → 1 (moda)",
    "S": "Nulos → never_active", "T": "Nulos → moda", "U": "Nulos → False", "V": "Nulos → False", "W": "Nulos → False",
    "X": "Valor de su CP · respaldo mediana región/país", "Y": "Valor de su CP · si no, recalculado = AM×1e6/AL",
    "Z": "Valor de su CP · respaldo mediana región/país",
    "AA": "Nulos → CP real del país sorteado (ponderado, uno por cliente)",
    **{k: "Sin telemetría → 0 · parcial → mediana de su serie" for k in ["AB", "AD", "AE", "AF"]},
    "AC": "Sin telemetría → '0' · parcial → moda de su serie",
    "AG": "Sin telemetría → 0 · parcial → 0 si ELECTRIC, si no mediana de su serie",
    "AH": "Sin telemetría → 0 · parcial → velocidad moda de su serie",
    "AI": "Sin telemetría → '0' · parcial → moda de su serie",
    "AJ": "Sin telemetría → 0 · parcial → mediana de su serie",
    "AK": "Sin telemetría → 0 · parcial → mediana de su serie",
    "AL": "Valor de su CP · si no, = población / tamaño medio del hogar de la región",
    "AM": "Valor de su CP · si no, = X × Z / 1e6",
}
mapping = pd.DataFrame({"letra": list(L), "columna": list(L.values()),
                        "nulos originales": [raw[c].isna().sum() for c in L.values()],
                        "tratamiento aplicado": [DECISION.get(k, "—") for k in L]})
md("9.1 Columnas (letra del documento) y tratamiento aplicado", mapping, index=False, floatfmt=",.0f")

# %% [markdown]
# ### 9.2 Limpieza previa y flags
#
# Antes de rellenar se corrigen los valores erróneos detectados en la §4 (no son nulos, pero son imposibles)
# y se guardan los flags que indican qué dato era ausente.

# %%
t = df.drop(columns=["has_telemetry", "reg_year", "vehicle_age_years"]).copy()
t["reg_year"] = df.reg_year
log = []


def step(letra, desc, n):
    log.append({"letra": letra, "columna": L.get(letra, "—"), "tratamiento": desc, "valores": int(n)})


def fill(col, values, letra, desc, mask=None):
    m = t[col].isna() if mask is None else (mask & t[col].isna())
    if isinstance(values, pd.Series):
        t.loc[m, col] = values[m]
    else:
        t.loc[m, col] = values
    step(letra, desc, (m & t[col].notna()).sum())


def series_mode(s: pd.Series):
    s = s.dropna()
    return s.mode().iloc[0] if len(s) else np.nan


# CP con formato erróneo y zonas sin población
bad_zip = t.zipcode.notna() & ~t.zipcode.str.fullmatch(r"\d{4}")
t.loc[bad_zip, "zipcode"] = t.loc[bad_zip, "zipcode"].str.extract(r"^(?:A-|CH-)?(\d{4})$")[0]
step("AA", "CP normalizado ('A-'/'CH-' fuera; texto o 5 dígitos → nulo)", bad_zip.sum())
z0 = t.population == 0
t.loc[z0, SOCIO] = np.nan
step("Z/AL", "population = 0 (CP sin residentes) → zona sin datos", z0.sum())

# Telemetría: valores imposibles → nulo; winsorización p1-p99 de lo observado
n_before = t[TELEMETRY].notna().sum().sum()
t.loc[t.speed_average < 1, "speed_average"] = np.nan
t.loc[t.operating_hours_total <= 0, "operating_hours_total"] = np.nan
t.loc[t.trip_distance_all_counter == 0, ["trip_distance_average", "trip_distance_median", "trip_distance_mode",
                                         "trip_distance_all_counter"]] = np.nan
t.loc[t.speed_all_counter == 0, ["speed_average", "speed_median", "speed_mode", "speed_all_counter"]] = np.nan
t["speed_median"] = t.speed_median.round(4)
step("AB–AK", "valores imposibles (vel. < 1, horas = 0, contadores = 0 con métricas) → nulo",
     n_before - t[TELEMETRY].notna().sum().sum())
for letra in ["AB", "AF", "AG", "AH"]:
    c = L[letra]
    lo, hi = t[c].quantile([.01, .99])
    step(letra, f"winsorización p1–p99 de los observados [{lo:,.2f}; {hi:,.2f}]", ((t[c] < lo) | (t[c] > hi)).sum())
    t[c] = t[c].clip(lo, hi)

# Flags (antes de rellenar)
t["has_telemetry"] = t[TELEMETRY].notna().any(axis=1)
t["tel_partial"] = t.has_telemetry & t[TELEMETRY].isna().any(axis=1)
t["socio_imputed"] = t[SOCIO].isna().any(axis=1)
t["zip_imputed"] = t.zipcode.isna()
t["engine_imputed"] = t.engine_concept.isna()
t["fuel_imputed"] = t.fuel_type.isna()
t["reg_date_imputed"] = t.reg_date.isna()
t["months_is_36_spike"] = t.months_as_mb_customer == 36
before = t.copy()
pd.Series({"filas con telemetría completa": (t.has_telemetry & ~t.tel_partial).sum(),
           "filas con telemetría parcial": t.tel_partial.sum(),
           "filas sin telemetría": (~t.has_telemetry).sum()}, name="filas").to_frame()

# %% [markdown]
# ### 9.3 Perfil, vehículo y motorización (D–M)
#
# Las reglas de motorización se validan antes sobre las filas cuya motorización sí se conoce.

# %%
def name_rule(vt):
    if not isinstance(vt, str):
        return np.nan
    v = vt.upper()
    if v.startswith(("EQ", "AMG EQ")) or "ELECTRIC" in v or re.match(r"^(E-?SPRINTER|E-?VITO|E-?CITAN|EQV)", v.replace(" ", "")):
        return "ELECTRIC"
    if re.search(r"\b\d{3}\s?(E|DE)\b", v) or "HYBRID" in v or "E PERFORMANCE" in v:
        return "PLUGIN_HYBRID"
    return np.nan


def is_diesel_name(s: pd.Series) -> pd.Series:
    return s.fillna("").str.contains(r"\b\d{3}\s?d\b|\bd\s?4MATIC|CDI|BLUETEC|\b\d{3}\s?de\b", case=False, regex=True)


def consistent_lookup(key):
    k = df.dropna(subset=["engine_concept"])
    return k.groupby(key).engine_concept.agg(
        lambda s: s.mode().iloc[0] if s.value_counts(normalize=True).iloc[0] >= .9 else np.nan).dropna()


def fuel_from_engine(d: pd.DataFrame) -> pd.Series:
    dn = is_diesel_name(d.vehicle_type)
    ec = d.engine_concept
    return pd.Series(np.select(
        [ec == "ELECTRIC", (ec == "PLUGIN_HYBRID") & dn, ec == "PLUGIN_HYBRID", dn | (d.product_group == "T")],
        ["ELECTRIC", "DIESEL,ELECTRIC", "PETROL,ELECTRIC", "DIESEL"], "PETROL"), index=d.index)


k = df[df.engine_concept.notna()]
nr = k.vehicle_type.map(name_rule)
old = k[(k.reg_year <= 2018) & nr.isna()]
kf = df.dropna(subset=["engine_concept", "fuel_type"])
fuel_true = kf.fuel_type.str.replace("PETROL_PLUS", "PETROL")
ec_mode = series_mode(df.engine_concept)
valid = pd.DataFrame([
    {"regla": "Nombre EQ*/electric → ELECTRIC; 'e'/'de'/Hybrid → PLUGIN_HYBRID", "filas evaluables": nr.notna().sum(),
     "acierto %": (nr[nr.notna()] == k.engine_concept[nr.notna()]).mean() * 100},
    {"regla": "Matriculado ≤ 2018 y sin nombre eléctrico → COMBUSTION", "filas evaluables": len(old),
     "acierto %": (old.engine_concept == "COMBUSTION").mean() * 100},
    {"regla": "Combustible derivado de engine_concept + nombre (PETROL_PLUS cuenta como PETROL)",
     "filas evaluables": len(kf), "acierto %": (fuel_from_engine(kf) == fuel_true).mean() * 100},
    {"regla": f"(Referencia) moda global {ec_mode} para cualquier fila", "filas evaluables": len(k),
     "acierto %": (k.engine_concept == ec_mode).mean() * 100},
])
md("9.3 Validación de las reglas de motorización sobre filas con dato conocido", valid, index=False, floatfmt=",.2f")

# %%
fill(L["E"], "unknown", "E", "nulo → nueva categoría 'unknown'")
fill(L["G"], t.model_series.map(t.groupby("model_series").vehicle_type.agg(series_mode)), "G",
     "nulo → vehicle_type más frecuente de su model_series")

# J: cascada validada; la moda solo para lo que queda (primero la de su serie, luego la global)
t["engine_concept_source"] = np.where(t.engine_concept.notna(), "original", None)
series_mode_engine = df.dropna(subset=["engine_concept"]).groupby("model_series").engine_concept.agg(series_mode)
for src, desc, fn in [
    ("lookup_vehicle_type", "vehicle_type con ≥ 90 % de consistencia", lambda d: d.vehicle_type.map(consistent_lookup("vehicle_type"))),
    ("regla_nombre", "nombre comercial (EQ*, e/de, Hybrid)", lambda d: d.vehicle_type.map(name_rule)),
    ("lookup_model_series", "model_series con ≥ 90 % de consistencia", lambda d: d.model_series.map(consistent_lookup("model_series"))),
    ("regla_antiguedad", "matriculado ≤ 2018 → COMBUSTION", lambda d: d.reg_year.le(2018).map({True: "COMBUSTION"})),
    ("moda_serie", "moda de su model_series", lambda d: d.model_series.map(series_mode_engine)),
    ("moda_global", f"moda global ({ec_mode})", lambda d: pd.Series(ec_mode, index=d.index)),
]:
    m = t.engine_concept.isna()
    t.loc[m, "engine_concept"] = fn(t.loc[m])
    filled = m & t.engine_concept.notna()
    t.loc[filled, "engine_concept_source"] = src
    step("J", f"nulo → {desc}", filled.sum())

# L: derivado de J + nombre comercial
fill(L["L"], fuel_from_engine(t), "L", "nulo → derivado de engine_concept + nombre comercial")

# M: pendiente de decisión; provisional
med_by_series = t.groupby("model_series").reg_date.median()
m = t.reg_date.isna()
t.loc[m, "reg_date"] = t.loc[m, "model_series"].map(med_by_series)
t.loc[t.reg_date.isna(), "reg_date"] = t.reg_date.median()
t["date_of_first_registration"] = t.reg_date.dt.strftime("%Y-%m-%d")
t["vehicle_age_years"] = (REF_DATE - t.reg_date).dt.days / 365.25
step("M", "PENDIENTE: provisional mediana de su model_series (+ flag)", m.sum())

fill(L["O"], "OWNER", "O", "nulo → OWNER")
fill(L["Q"], 0.0, "Q", "nulo → 0.0")
fill(L["R"], 1, "R", "nulo → 1")
fill(L["S"], "never_active", "S", "nulo → never_active")
fill(L["N"], False, "N", "nulo → False")
fill(L["P"], "B2C", "P", "nulo → B2C")
for letra in ["U", "V", "W"]:
    fill(L[letra], False, letra, "nulo → False")
fill(L["T"], series_mode(t[L["T"]]), "T", "nulo → moda")

# %% [markdown]
# ### 9.4 Código postal y socio-demografía (X, Y, Z, AA, AL, AM)
#
# Los datos socio-demográficos son atributos de la **zona**. Para que el CP imputado y sus valores sean
# coherentes, se sortea un CP **real** del país (con datos y ponderado por número de clientes), una sola vez
# por cliente. Así el cliente recibe todos los valores de esa zona. Los clientes cuyo CP existe pero no tiene
# datos reciben la mediana de su región para X y Z, y las demás columnas se **recalculan** con las identidades
# exactas detectadas en la §4.

# %%
zone = (before.dropna(subset=["zipcode", *SOCIO]).drop_duplicates(["country_code", "zipcode"])
        .set_index(["country_code", "zipcode"])[SOCIO])
clients_per_zone = before.dropna(subset=["zipcode", *SOCIO]).drop_duplicates("client_id").groupby(
    ["country_code", "zipcode"]).size()
rng = np.random.default_rng(42)
nozip = t.loc[t.zipcode.isna(), ["client_id", "country_code"]].drop_duplicates("client_id")
assigned = {}
for ctry, grp in nozip.groupby("country_code"):
    w = clients_per_zone.loc[ctry]
    assigned.update(zip(grp.client_id, rng.choice(w.index.to_numpy(), size=len(grp), p=(w / w.sum()).to_numpy())))
fill("zipcode", t.client_id.map(assigned), "AA", "nulo → CP real del país sorteado (ponderado, uno por cliente)")

key = pd.MultiIndex.from_arrays([t.country_code, t.zipcode])
for letra in ["X", "Y", "Z", "AL", "AM"]:
    c = L[letra]
    fill(c, pd.Series(zone[c].reindex(key).to_numpy(), index=t.index), letra, "nulo → valor de su CP")

# CP existentes sin datos: X y Z por mediana de la región (2 primeros dígitos) o del país; resto por identidad
zone_r = zone.reset_index().assign(zip_region=lambda d: d.zipcode.str[:2],
                                   hh=lambda d: d.population / d.number_of_households)
t["zip_region"] = t.zipcode.str[:2]
keyr = pd.MultiIndex.from_arrays([t.country_code, t.zip_region])
for letra in ["X", "Z"]:
    c = L[letra]
    fill(c, pd.Series(zone_r.groupby(["country_code", "zip_region"])[c].median().reindex(keyr).to_numpy(), index=t.index),
         letra, "CP sin datos → mediana de su región")
    fill(c, t.country_code.map(zone_r.groupby("country_code")[c].median()), letra, "CP sin datos → mediana del país")
hh = pd.Series(zone_r.groupby(["country_code", "zip_region"]).hh.median().reindex(keyr).to_numpy(), index=t.index)
hh = hh.fillna(t.country_code.map(zone_r.groupby("country_code").hh.median()))
fill(L["AL"], (t.population / hh).round(), "AL", "CP sin datos → población / tamaño medio del hogar de la región")
fill(L["AM"], t.purchasing_power_per_inhabitant_eur * t.population / 1e6, "AM", "CP sin datos → X × Z / 1e6")
fill(L["Y"], t.purchasing_power_millions_eur * 1e6 / t.number_of_households, "Y", "CP sin datos → AM × 1e6 / AL")

gen = list(zip(nozip.country_code, nozip.client_id.map(assigned)))
note(f"- Clientes sin CP: **{len(nozip):,}**. Todos reciben un CP real con datos: "
     f"**{np.mean([g in zone.index for g in gen]) * 100:.1f} %** de CP existentes (frente al 31,6 % del sorteo uniforme "
     "entre el mínimo y el máximo).")

# %% [markdown]
# ### 9.5 Telemetría (AB–AK)
#
# - **Sin ninguna telemetría:** todas las métricas valen 0 (también velocidad y contadores). Así el 0 significa
#   siempre "sin datos" y el flag `has_telemetry` lo hace explícito.
# - **Telemetría parcial:** la métrica que falta se rellena con un valor plausible para ese tipo de coche (mediana
#   de su serie; para AH, la velocidad moda de su serie; para las modas en texto, la moda de su serie, que es un bin
#   válido). Si el coche es eléctrico, el consumo de combustible es 0.

# %%
no_tel = ~t.has_telemetry
for c in TELEMETRY:
    letra = next(k for k, v in L.items() if v == c)
    fill(c, "0" if c.endswith("_mode") else 0.0, letra, "sin telemetría → 0", mask=no_tel)

part = t.has_telemetry
fill("fuel_consumption_average", 0.0, "AG", "parcial y ELECTRIC → 0", mask=part & (t.engine_concept == "ELECTRIC"))
obs = before[before.has_telemetry]
for c in TELEMETRY:
    letra = next(k for k, v in L.items() if v == c)
    if c == "speed_average":
        by_series = obs.assign(v=obs[c].round()).groupby("model_series").v.agg(series_mode)
        glob = series_mode(obs[c].round())
        how = "velocidad moda de su serie"
    elif c.endswith("_mode"):
        by_series = obs.groupby("model_series")[c].agg(series_mode)
        glob = series_mode(obs[c])
        how = "moda de su serie"
    else:  # mediana "lower": devuelve un valor observado (en las medianas discretizadas, un bin válido)
        by_series = obs.groupby("model_series")[c].quantile(.5, interpolation="lower")
        glob = obs[c].quantile(.5, interpolation="lower")
        how = "mediana de su serie"
    fill(c, t.model_series.map(by_series), letra, f"parcial → {how}", mask=part)
    fill(c, glob, letra, "parcial → valor global (serie sin datos)", mask=part)

md("9.6 Registro de tratamientos aplicados (en orden)",
   pd.DataFrame(log).query("valores > 0"), index=False, floatfmt=",.0f")

# %% [markdown]
# ## 10. Comprobaciones de coherencia del dataset tratado
#
# Cada comprobación cuenta las filas, clientes o vehículos que la **incumplen**. El objetivo es 0 en todas.

# %%
clean = t.drop(columns=[L["A"], L["H"], "reg_date", "reg_year", "zip_region"], errors="ignore")
cur_cols = [c for c in CLIENT_COLS if c in clean.columns]
veh_cols = ["model_series", "vehicle_type", "product_group", "engine_concept", "fuel_type", "date_of_first_registration"]
real_bins = {c: set(df[c].dropna().unique()) | ({"0"} if c.endswith("_mode") else {0.0})
             for c in ["trip_distance_mode", "speed_mode", "trip_distance_median"]}
real_bins["speed_median"] = set(df.speed_median.dropna().round(4).unique()) | {0.0}
pos = clean.population > 0
tel_core = ["trip_distance_average", "operating_hours_total", "speed_average", "trip_distance_all_counter", "speed_all_counter"]
checks = {
    "Nulos en cualquier columna (celdas)": int(clean.isna().sum().sum()),
    "Clientes con atributos de cliente distintos entre sus filas (incl. CP y socio-demografía)":
        int((clean.groupby("client_id")[cur_cols].nunique() > 1).any(axis=1).sum()),
    "Vehículos con atributos de vehículo distintos entre sus filas":
        int((clean.groupby("vehicle_id")[veh_cols].nunique() > 1).any(axis=1).sum()),
    "(país, CP) con más de un valor socio-demográfico":
        int((clean.groupby(["country_code", "zipcode"])[SOCIO].nunique() > 1).any(axis=1).sum()),
    "CP imputados que no existen en el país": int((~pd.MultiIndex.from_arrays(
        [clean.country_code[clean.zip_imputed], clean.zipcode[clean.zip_imputed]]).isin(zone.index)).sum()),
    "PA total ≠ PA/hab × población / 1e6 (error > 0,1 %)": int((
        (clean.purchasing_power_millions_eur - clean.purchasing_power_per_inhabitant_eur * clean.population / 1e6).abs()
        > 1e-3 * clean.purchasing_power_millions_eur)[pos].sum()),
    "PA/hogar ≠ PA total × 1e6 / hogares (error > 0,1 %)": int((
        (clean.purchasing_power_per_household_eur - clean.purchasing_power_millions_eur * 1e6 / clean.number_of_households).abs()
        > 1e-3 * clean.purchasing_power_per_household_eur)[pos].sum()),
    "Motor y combustible incompatibles": int((
        ((clean.engine_concept == "ELECTRIC") != (clean.fuel_type == "ELECTRIC"))
        | ((clean.engine_concept == "PLUGIN_HYBRID") != clean.fuel_type.str.endswith(",ELECTRIC"))).sum()),
    "Vehículos con nombre eléctrico (EQ…) imputados como no eléctricos": int(
        (clean.engine_imputed & (clean.vehicle_type.map(name_rule) == "ELECTRIC") & (clean.engine_concept != "ELECTRIC")).sum()),
    "Turismos con nombre de gasolina imputados como DIESEL": int(
        (clean.fuel_imputed & ~is_diesel_name(clean.vehicle_type) & (clean.product_group != "T")
         & clean.fuel_type.str.startswith("DIESEL")).sum()),
    "Sin telemetría pero con alguna métrica ≠ 0": int((~clean.has_telemetry & (clean[tel_core + [
        "fuel_consumption_average", "trip_distance_median", "speed_median"]] != 0).any(axis=1)).sum()),
    "Con telemetría pero con alguna métrica básica = 0": int((clean.has_telemetry & (clean[tel_core] == 0).any(axis=1)).sum()),
    "Con telemetría, no eléctrico y consumo = 0": int((clean.has_telemetry & (clean.engine_concept != "ELECTRIC")
                                                      & (clean.fuel_consumption_average == 0)).sum()),
    "Eléctricos con consumo de combustible > 0": int(((clean.engine_concept == "ELECTRIC")
                                                     & (clean.fuel_consumption_average > 0)).sum()),
    "Modas/medianas que no son un bin válido": int(sum((~clean[c].isin(v)).sum() for c, v in real_bins.items())),
}
chk = pd.Series(checks, name="incumplimientos").to_frame()
md("10.1 Comprobaciones de coherencia (objetivo: 0)", chk, floatfmt=",.0f")
assert chk.incumplimientos.eq(0).all(), "Hay comprobaciones de coherencia que fallan"

# %% [markdown]
# ### 10.2 Impacto del tratamiento en las distribuciones

# %%
ec_cmp = pd.concat([
    df.engine_concept.value_counts(normalize=True).mul(100).rename("% original (sobre conocidos)"),
    df.engine_concept.fillna(ec_mode).value_counts(normalize=True).mul(100).rename("% con la moda (regla original J)"),
    clean.engine_concept.value_counts(normalize=True).mul(100).rename("% tratamiento final"),
], axis=1).fillna(0)
md("10.2 engine_concept: original, moda y tratamiento final", ec_cmp, floatfmt=".1f")
md("10.3 Origen del valor final de engine_concept", clean.engine_concept_source.value_counts().rename("filas"))
fb = lambda s: s.str.replace("PETROL_PLUS", "PETROL").str.replace(r"^(DIESEL|PETROL),ELECTRIC$", "PHEV", regex=True)
md("10.4 fuel_type (agrupado): original frente a tratamiento final", pd.concat([
    fb(df.fuel_type.dropna()).value_counts(normalize=True).mul(100).rename("% original (sobre conocidos)"),
    fb(clean.fuel_type).value_counts(normalize=True).mul(100).rename("% tratamiento final")], axis=1), floatfmt=".1f")

imp = []
for c in ["trip_distance_average", "operating_hours_total", "fuel_consumption_average", "speed_average",
          "purchasing_power_per_inhabitant_eur", "population"]:
    b, a, h = before[c], clean[c], clean.has_telemetry if c in TELEMETRY else slice(None)
    imp.append({"columna": c, "mediana observada": b.median(), "mediana final (filas con dato)": a[h].median(),
                "% filas imputadas": b.isna().mean() * 100})
md("10.5 Medianas antes y después (en telemetría, solo sobre filas con telemetría)", pd.DataFrame(imp), index=False,
   floatfmt=",.2f")

fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
for ax, (c, lab, rg) in zip(axes, [("trip_distance_average", "Distancia media por trayecto (km)", (0, 50)),
                                    ("fuel_consumption_average", "Consumo medio (l/100 km)", (0, 20)),
                                    ("speed_average", "Velocidad media (km/h)", (0, 85))]):
    bins = np.linspace(*rg, 51)
    obs_v = before[c].dropna().clip(*rg)
    imp_v = clean.loc[clean.tel_partial & before[c].isna(), c].clip(*rg)
    ax.hist([obs_v, imp_v], bins=bins, stacked=True, color=[BLUE, CAT[1]], edgecolor=SURFACE, linewidth=0.4,
            label=["observado", "imputado (telemetría parcial)"])
    ax.set_title(lab, fontsize=9.5)
    ax.set_ylabel("filas")
    ax.text(0.98, 0.95, f"sin telemetría (= 0): {(~clean.has_telemetry).sum():,} filas", transform=ax.transAxes,
            ha="right", va="top", fontsize=7.5, color=INK2)
axes[0].legend(loc="center right")
fig.suptitle("Telemetría tras el tratamiento (sin contar las filas a 0)", x=0.01, ha="left", fontsize=11, fontweight="bold")
save(fig, "fig17_impacto_relleno_telemetria.png")

fig, ax = plt.subplots(figsize=(8, 3.8))
order = ["COMBUSTION", "MILD_HYBRID", "PLUGIN_HYBRID", "ELECTRIC"]
plot = ec_cmp.T[order]
left = np.zeros(len(plot))
for i, col in enumerate(order):
    ax.barh(plot.index, plot[col], left=left, height=0.55, color=CAT[i], edgecolor=SURFACE, linewidth=2, label=col)
    for j, v in enumerate(plot[col].values):
        if v > 4:
            ax.text(left[j] + v / 2, j, f"{v:.0f}", ha="center", va="center", fontsize=8, color="white")
    left += plot[col].values
ax.set_xlim(0, 100); ax.grid(axis="y", visible=False); ax.invert_yaxis()
ax.set_xlabel("% de filas")
ax.set_title("engine_concept: original, moda y tratamiento final")
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.2))
save(fig, "fig18_engine_moda_vs_reglas.png")

# %% [markdown]
# ### 10.3 Datos tratados y vista por cliente
#
# Se eliminan A (índice) y H (`model_class`). `client_id` y `vehicle_id` (B, C) son ruido para el modelo, pero se
# conservan **solo como claves**: sin ellas no se puede agregar por cliente. La vista por cliente calcula la
# telemetría como media **solo de las relaciones con telemetría**; los clientes sin ninguna quedan a 0 con
# `has_telemetry = False`.

# %%
clean.to_parquet(PROC / "relaciones_limpio.parquet", index=False)

gc = clean.groupby("client_id")
cur = clean[clean.is_current_vehicle]
clients = clean.drop_duplicates("client_id").set_index("client_id")[
    ["age_range", "gender_derived", "country_code", "months_as_mb_customer", "months_is_36_spike",
     "currently_connected_vehicles", "finance_leasing_status", *CONSENTS, "purchasing_power_per_inhabitant_eur",
     "population", "socio_imputed", "zip_imputed"]]
clients["n_relaciones"] = gc.size()
clients["is_b2b"] = gc.role_type.apply(lambda s: (s == "B2B").any())
clients["share_owner"] = gc.role.apply(lambda s: (s == "OWNER").mean())
clients["visitas_taller_total"] = gc.workshop_visits_warranty_goodwill.sum()
clients["edad_vehiculo_actual_media"] = cur.groupby("client_id").vehicle_age_years.mean()
clients["share_electrificado_actual"] = cur.groupby("client_id").engine_concept.apply(
    lambda s: s.isin(["ELECTRIC", "PLUGIN_HYBRID"]).mean())
clients["has_telemetry"] = gc.has_telemetry.any()
tel_rel = clean[clean.has_telemetry].groupby("client_id")
for c in ["trip_distance_average", "operating_hours_total", "fuel_consumption_average", "speed_average"]:
    clients[c] = tel_rel[c].mean().reindex(clients.index).fillna(0.0)
clients.to_parquet(PROC / "clientes.parquet")
md("10.6 Vista agregada por cliente (data/processed/clientes.parquet)", clients.describe(include="all").T
   .drop(columns=["top", "freq"], errors="ignore"), floatfmt=",.2f")

(OUT / "resultados.md").write_text("# Resultados del EDA (generado por eda/eda_reto1.py)\n" + "\n".join(_md), encoding="utf-8")
print(f"OK -> {len(clean):,} filas tratadas ({clean.shape[1]} columnas), {len(clients):,} clientes")

# %% [markdown]
# ## 11. Conclusiones
#
# **Principales características de los clientes:** base B2C (99,4 %), madura (61 % con 45 años o más) y mayoritariamente
# masculina, concentrada en Suiza (66 %) y con un único vehículo conectado (81 %). El 71 % nunca ha usado leasing y el
# 81 % acepta todos los canales de contacto. El parque está dominado por SUV y compactos premium (GLC, C, A, B/GLA/GLB),
# con una electrificación que se acelera: los BEV son el 37,5 % de las matriculaciones de 2026.
#
# **Calidad de datos:** el grano es cliente–vehículo; hay telemetría estructuralmente ausente (52 %), motorización
# incompleta (44–59 %), columnas redundantes, un pico artificial en 36 meses como cliente, una taxonomía de modelo solapada
# y CP erróneos. Todo queda tratado, sin nulos y con las comprobaciones de coherencia a 0.
#
# El resumen breve del reto está en `eda/Resumen_reto1.md`.
