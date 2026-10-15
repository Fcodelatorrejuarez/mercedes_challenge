"""
Reto básico 1 - Exploración y calidad de datos (EDA)
III Malackathon 2026 - Mercedes-Benz "Clustering the Star"

Script reproducible que genera todas las tablas y figuras citadas en
eda/EDA_reto1.md y aplica la propuesta de limpieza documentada.

Uso (desde la raíz del repositorio):
    python eda/eda_reto1.py

Salidas:
    eda/figures/*.png               -> figuras del informe
    eda/outputs/resultados.md       -> todas las tablas en Markdown
    data/processed/relaciones_limpio.parquet  -> dataset cliente-vehículo tratado
    data/processed/clientes.parquet           -> vista agregada a nivel cliente
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Rutas y constantes
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "datos_reto_mercedes_benz_malackathon.csv"
FIG = ROOT / "eda" / "figures"
OUT = ROOT / "eda" / "outputs"
PROC = ROOT / "data" / "processed"
for p in (FIG, OUT, PROC):
    p.mkdir(parents=True, exist_ok=True)

# Fecha de referencia del análisis: la fecha de registro máxima del fichero es
# 2026-10-02, así que el extracto es de principios de octubre de 2026.
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

# --------------------------------------------------------------------------
# Estilo de gráficos (paleta de referencia validada, ver skill dataviz)
# --------------------------------------------------------------------------
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
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=130, bbox_inches="tight")
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


# --------------------------------------------------------------------------
# Salida de tablas a Markdown
# --------------------------------------------------------------------------
_md: list[str] = []


def md(title: str, obj=None, floatfmt=",.2f", index=True):
    _md.append(f"\n### {title}\n")
    if obj is None:
        return
    if isinstance(obj, pd.Series):
        obj = obj.to_frame()
    _md.append(obj.to_markdown(floatfmt=floatfmt, index=index))
    _md.append("")


def note(text: str):
    _md.append(text + "\n")


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

# ==========================================================================
# 9. TRATAMIENTO DE NULOS - decisión del equipo (Descripcion_uso_de_datos)
# ==========================================================================
# El documento referencia las columnas por su letra al abrir el CSV en Excel:
# A = primera columna (índice sin nombre), B = client_id, ..., AM = purchasing_power_millions_eur.
print("Aplicando tratamiento...")
RAW_COLS = list(raw.columns)


def col_letter(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


LETTER = {col_letter(i): c for i, c in enumerate(RAW_COLS)}
L = LETTER  # alias corto: L["AA"] -> "zipcode"

DECISION = {
    "A": "Quitar (ruido)", "B": "Quitar (ruido)", "C": "Quitar (ruido)", "H": "Quitar (ruido)",
    "D": "Label encoding", "E": "Label encoding · nulos → nueva categoría", "F": "Label encoding",
    "G": "Label encoding · nulos → moda de su model_series", "I": "Label encoding (umbrales)",
    "J": "Label encoding · nulos → moda", "K": "Label encoding (puede haber varios países)",
    "L": "Label encoding · se saca a partir de J", "M": "Label encoding (?) · tratamiento pendiente",
    "O": "Label encoding · nulos → OWNER (moda)", "Q": "Label encoding · nulos → 0.0",
    "R": "Label encoding · nulos → 1 (moda)", "S": "Label encoding · nulos → never_active",
    "N": "One-hot · nulos → False", "P": "One-hot · nulos → B2C (moda)", "U": "One-hot · nulos → False",
    "V": "One-hot · nulos → False", "W": "One-hot · nulos → False",
    "T": "Directo · nulos → moda",
    "X": "Directo · nulos → media del CP (o media de la misma serie en el mismo CP)",
    "Y": "Directo · nulos → media del CP", "Z": "Directo · nulos → media del CP",
    "AA": "Nulos → número aleatorio entre el mín. y el máx. de los CP del país",
    "AB": "Nulos → 0", "AC": "Nulos → 0", "AD": "Nulos → 0", "AE": "Nulos → 0", "AF": "Nulos → 0", "AG": "Nulos → 0",
    "AH": "Nulos → velocidad moda de su model_series", "AI": "Nulos → moda de AH en su model_series",
    "AJ": "Nulos → mediana de AH en su model_series", "AK": "Nulos → 1",
    "AL": "Nulos → moda de hogares de su CP", "AM": "Nulos → moda del poder adquisitivo de su CP",
}
mapping = pd.DataFrame({"letra": list(LETTER), "columna": list(LETTER.values()),
                        "nulos originales": [raw[c].isna().sum() for c in LETTER.values()],
                        "decisión del equipo": [DECISION.get(k, "—") for k in LETTER]})
md("9.1 Correspondencia letra → columna y decisión del equipo (Descripcion_uso_de_datos)", mapping, index=False,
   floatfmt=",.0f")

t = df.drop(columns=["has_telemetry", "reg_year", "vehicle_age_years"]).copy()
t["reg_year"] = df.reg_year
log = []


def step(letra, desc, n):
    log.append({"letra": letra, "columna": L.get(letra, "—"), "tratamiento": desc, "valores afectados": int(n)})


def fill(col, values, letra, desc):
    m = t[col].isna()
    t.loc[m, col] = values[m] if isinstance(values, pd.Series) else values
    step(letra, desc, m.sum() - t[col].isna().sum())


def series_mode(s: pd.Series):
    s = s.dropna()
    return s.mode().iloc[0] if len(s) else np.nan


# --- 9.0 Limpieza previa de valores erróneos (no nulos), se mantiene del análisis ---
bad_zip = t.zipcode.notna() & ~t.zipcode.str.fullmatch(r"\d{4}")
t.loc[bad_zip, "zipcode"] = t.loc[bad_zip, "zipcode"].str.extract(r"^(?:A-|CH-)?(\d{4})$")[0]
step("AA", "Limpieza previa: CP normalizado ('A-'/'CH-' fuera; texto o 5 dígitos → nulo)", bad_zip.sum())
n_bad = t.notna().sum()
t.loc[t.speed_average < 1, "speed_average"] = np.nan
t.loc[t.operating_hours_total <= 0, "operating_hours_total"] = np.nan
t.loc[t.trip_distance_all_counter == 0, ["trip_distance_average", "trip_distance_median", "trip_distance_mode"]] = np.nan
t.loc[t.speed_all_counter == 0, ["speed_average", "speed_median", "speed_mode"]] = np.nan
t["speed_median"] = t.speed_median.round(4)
step("AB–AJ", "Limpieza previa: valores imposibles (vel. < 1, horas = 0, contadores = 0) → nulo",
     (n_bad - t.notna().sum()).sum())
for letra in ["AB", "AF", "AG", "AH"]:
    c = L[letra]
    lo, hi = t[c].quantile([.01, .99])
    step(letra, f"Limpieza previa: winsorización p1–p99 de los observados [{lo:,.2f}, {hi:,.2f}]",
         ((t[c] < lo) | (t[c] > hi)).sum())
    t[c] = t[c].clip(lo, hi)  # sobre valores observados, antes de rellenar

# Flags que conservan la información de "dato ausente" antes de rellenar
t["has_telemetry"] = t[["trip_distance_average", "operating_hours_total", "fuel_consumption_average",
                        "speed_average"]].notna().any(axis=1)
t["socio_imputed"] = t.purchasing_power_per_inhabitant_eur.isna()
t["zip_imputed"] = t.zipcode.isna()
t["engine_imputed"] = t.engine_concept.isna()
t["reg_date_imputed"] = t.reg_date.isna()
t["months_is_36_spike"] = t.months_as_mb_customer == 36
before = t.copy()  # foto previa al relleno para medir impacto

# --- Label encoding: D, E, F, G, I, J, K, L, M, O, Q, R, S ---
fill(L["E"], "unknown", "E", "nulo → nueva categoría 'unknown'")
vt_mode = t.groupby("model_series").vehicle_type.agg(series_mode)
fill(L["G"], t.model_series.map(vt_mode), "G", "nulo → vehicle_type más frecuente de su model_series")
fill(L["G"], series_mode(t.vehicle_type), "G", "nulo restante (serie sin ningún vehicle_type) → moda global")
ec_mode = series_mode(t.engine_concept)
fill(L["J"], ec_mode, "J", f"nulo → moda de la columna ({ec_mode})")
fuel_by_engine = before.dropna(subset=["fuel_type"]).groupby("engine_concept").fuel_type.agg(series_mode)
fill(L["L"], t.engine_concept.map(fuel_by_engine), "L",
     "nulo → fuel_type más frecuente para su engine_concept (sacado de J): "
     + ", ".join(f"{k}→{v}" for k, v in fuel_by_engine.items()))
# M: el documento lo deja abierto ("M?"); se mantiene provisionalmente la mediana de su model_series + flag
med_by_series = t.groupby("model_series").reg_date.median()
t.loc[t.reg_date.isna(), "reg_date"] = t.loc[t.reg_date.isna(), "model_series"].map(med_by_series)
t.loc[t.reg_date.isna(), "reg_date"] = t.reg_date.median()
step("M", "PENDIENTE de decisión ('M?'): provisionalmente mediana de su model_series + flag", before.reg_date.isna().sum())
t["date_of_first_registration"] = t.reg_date.dt.strftime("%Y-%m-%d")
t["vehicle_age_years"] = (REF_DATE - t.reg_date).dt.days / 365.25
fill(L["O"], "OWNER", "O", "nulo → OWNER (moda)")
fill(L["Q"], 0.0, "Q", "nulo → 0.0")
fill(L["R"], 1, "R", "nulo → 1 (moda)")
fill(L["S"], "never_active", "S", "nulo → never_active")
for letra in ["D", "F", "I", "K"]:
    step(letra, "sin nulos (solo codificación)", 0)

# --- One-hot: N, P, U, V, W ---
fill(L["N"], False, "N", "nulo → False")
fill(L["P"], "B2C", "P", "nulo → B2C (moda)")
for letra in ["U", "V", "W"]:
    fill(L[letra], False, letra, "nulo → False")

# --- Directo: T, X, Y, Z ---
fill(L["T"], series_mode(t[L["T"]]), "T", "nulo → moda")

# AA (zipcode): número aleatorio entre el mín. y el máx. de los CP del país (semilla fija)
rng = np.random.default_rng(42)
zip_num = pd.to_numeric(t.zipcode, errors="coerce")
zr = zip_num[zip_num >= 1000].groupby(t.country_code).agg(["min", "max"])  # CP válidos AT/CH: 1000-9999
m = t.zipcode.isna()
rand = [f"{rng.integers(zr.loc[c, 'min'], zr.loc[c, 'max'] + 1):04d}" for c in t.loc[m, "country_code"]]
t.loc[m, "zipcode"] = rand
known_zip = set(zip(before.country_code, before.zipcode))
known_soc = set(zip(before.dropna(subset=["population"]).country_code, before.dropna(subset=["population"]).zipcode))
gen = list(zip(t.loc[m, "country_code"], t.loc[m, "zipcode"]))
zip_hit = np.mean([g in known_zip for g in gen])
zip_soc_hit = np.mean([g in known_soc for g in gen])
step("AA", f"nulo → CP aleatorio en [mín, máx] del país ({', '.join(f'{c}: {int(r["min"])}–{int(r["max"])}' for c, r in zr.iterrows())})",
     m.sum())

# X, Y, Z, AL, AM: valor del CP (media / moda). Los datos socio-demográficos son constantes por (país, CP)
# y en el dataset NUNCA hay un CP con unas filas informadas y otras nulas, así que el valor del CP solo
# rellena las filas cuyo CP aleatorio (AA) coincide con un CP real con datos. Para no dejar nulos se
# añade un respaldo (no previsto en el documento): mediana de la región (2 primeros dígitos) y del país.
t["zip_region"] = t.zipcode.str[:2]
zone = before.dropna(subset=["zipcode"]).drop_duplicates(["country_code", "zipcode"])
zone = zone.assign(zip_region=zone.zipcode.str[:2])
for letra, agg in [("X", "mean"), ("Y", "mean"), ("Z", "mean"), ("AL", series_mode), ("AM", series_mode)]:
    c = L[letra]
    by_zip = before.groupby(["country_code", "zipcode"])[c].agg(agg)
    key = pd.MultiIndex.from_arrays([t.country_code, t.zipcode])
    fill(c, pd.Series(by_zip.reindex(key).values, index=t.index), letra,
         f"nulo → {'media' if agg == 'mean' else 'moda'} de su CP")
    if letra == "X":  # variante del documento: misma serie en el mismo CP (equivale al CP: dato de zona)
        by_zs = before.groupby(["country_code", "zipcode", "model_series"])[c].mean()
        key3 = pd.MultiIndex.from_arrays([t.country_code, t.zipcode, t.model_series])
        fill(c, pd.Series(by_zs.reindex(key3).values, index=t.index), letra, "nulo → media de su serie en su CP")
    reg = zone.groupby(["country_code", "zip_region"])[c].median()
    keyr = pd.MultiIndex.from_arrays([t.country_code, t.zip_region])
    fill(c, pd.Series(reg.reindex(keyr).values, index=t.index), letra,
         "RESPALDO (no en el documento): mediana de su región CP")
    fill(c, t.country_code.map(zone.groupby("country_code")[c].median()), letra,
         "RESPALDO (no en el documento): mediana del país")

# --- Telemetría: AB-AG → 0; AH, AI, AJ por model_series; AK → 1 ---
for letra in ["AB", "AC", "AD", "AE", "AF", "AG"]:
    fill(L[letra], "0" if t[L[letra]].dtype == object or str(t[L[letra]].dtype) == "str" else 0.0, letra, "nulo → 0")
ah_obs = before[["model_series", "speed_average"]].dropna()
ah_mode = ah_obs.assign(v=ah_obs.speed_average.round()).groupby("model_series").v.agg(series_mode)
ah_glob = series_mode(ah_obs.speed_average.round())
fill(L["AH"], t.model_series.map(ah_mode), "AH", "nulo → velocidad moda (redondeada a 1 km/h) de su model_series")
fill(L["AH"], ah_glob, "AH", "nulo restante (serie sin datos) → moda global")
fill(L["AI"], t.model_series.map(ah_mode).map(lambda v: f"{v:g}" if pd.notna(v) else np.nan), "AI",
     "nulo → moda de AH en su model_series")
fill(L["AI"], f"{ah_glob:g}", "AI", "nulo restante → moda global de AH")
ah_med = ah_obs.groupby("model_series").speed_average.median()
fill(L["AJ"], t.model_series.map(ah_med), "AJ", "nulo → mediana de AH en su model_series")
fill(L["AJ"], ah_obs.speed_average.median(), "AJ", "nulo restante → mediana global de AH")
fill(L["AK"], 1.0, "AK", "nulo → 1")

md("9.2 Registro de tratamientos aplicados (en orden)", pd.DataFrame(log), index=False, floatfmt=",.0f")
note(f"- CP aleatorios (AA) generados: **{m.sum():,}**. Solo el **{pct(zip_hit)}** coincide con un CP que existe en el "
     f"dataset para ese país y el **{pct(zip_soc_hit)}** con un CP con datos socio-demográficos. El resto son códigos "
     "inventados que no corresponden a ninguna zona real.")
note("- Los datos socio-demográficos son constantes dentro de cada (país, CP) y ningún CP tiene a la vez filas con dato "
     "y filas nulas, así que la regla 'media del CP' no puede rellenar una fila cuyo CP original existe: solo actúa "
     "sobre CP aleatorios que coinciden con uno real. Por eso hacen falta los respaldos de región y país.")

# --- Impacto del tratamiento ---
# 1) engine_concept: moda frente a la cascada validada del análisis (reglas con 99-100 % de acierto)
def name_rule(vt):
    if not isinstance(vt, str):
        return np.nan
    v = vt.upper()
    if v.startswith(("EQ", "AMG EQ")) or "ELECTRIC" in v or re.match(r"^(E-?SPRINTER|E-?VITO|E-?CITAN|EQV)", v.replace(" ", "")):
        return "ELECTRIC"
    if re.search(r"\b\d{3}\s?(E|DE)\b", v) or "HYBRID" in v or "E PERFORMANCE" in v:
        return "PLUGIN_HYBRID"
    return np.nan


def consistent_lookup(key):
    k = df.dropna(subset=["engine_concept"])
    return k.groupby(key).engine_concept.agg(
        lambda s: s.mode().iloc[0] if s.value_counts(normalize=True).iloc[0] >= .9 else np.nan).dropna()


k = df[df.engine_concept.notna()]
nr = k.vehicle_type.map(name_rule)
old = k[(k.reg_year <= 2018) & nr.isna()]
valid = pd.DataFrame([
    {"regla": "Nombre EQ*/electric → ELECTRIC; 'e'/'de'/Hybrid → PLUGIN_HYBRID", "filas evaluables": nr.notna().sum(),
     "acierto %": (nr[nr.notna()] == k.engine_concept[nr.notna()]).mean() * 100},
    {"regla": "Matriculado ≤ 2018 y sin nombre eléctrico → COMBUSTION", "filas evaluables": len(old),
     "acierto %": (old.engine_concept == "COMBUSTION").mean() * 100},
    {"regla": f"Moda global ({ec_mode}) asignada a cualquier fila", "filas evaluables": len(k),
     "acierto %": (k.engine_concept == ec_mode).mean() * 100},
])
md("9.3 Fiabilidad de reglas de motorización medida sobre filas con dato conocido", valid, index=False, floatfmt=",.2f")

miss = df[df.engine_concept.isna()].copy()
casc = pd.Series(np.nan, index=miss.index, dtype=object)
for fn in [lambda d: d.vehicle_type.map(consistent_lookup("vehicle_type")),
           lambda d: d.vehicle_type.map(name_rule),
           lambda d: d.model_series.map(consistent_lookup("model_series")),
           lambda d: d.reg_year.le(2018).map({True: "COMBUSTION"})]:
    mm = casc.isna()
    casc[mm] = fn(miss[mm])
cmp_eng = casc.fillna("indeterminado").value_counts().rename("filas").to_frame()
cmp_eng["%"] = cmp_eng.filas / len(miss) * 100
cmp_eng.index.name = "motorización que indican las reglas validadas (filas con J nulo)"
md(f"9.4 Filas con engine_concept nulo (todas imputadas como {ec_mode}): qué indican las reglas validadas", cmp_eng,
   floatfmt=",.2f")
ec_cmp = pd.concat([
    df.engine_concept.value_counts(normalize=True).mul(100).rename("% original (sobre conocidos)"),
    t.engine_concept.value_counts(normalize=True).mul(100).rename("% tras moda (decisión equipo)"),
    pd.concat([df.engine_concept.dropna(), casc.fillna("UNKNOWN")]).value_counts(normalize=True).mul(100)
    .rename("% con cascada validada (alternativa)")], axis=1)
md("9.5 Distribución de engine_concept: original / decisión del equipo / alternativa", ec_cmp, floatfmt=".2f")
md("9.6 fuel_type tras el tratamiento (filas)", t.fuel_type.value_counts().rename("filas"))

# 2) Telemetría: efecto de rellenar con 0 / moda por serie
imp = []
for c in ["trip_distance_average", "trip_distance_median", "trip_distance_all_counter", "operating_hours_total",
          "fuel_consumption_average", "speed_average", "speed_median", "speed_all_counter",
          "purchasing_power_per_inhabitant_eur", "population"]:
    b, a = before[c], t[c]
    imp.append({"columna": c, "media antes (observados)": b.mean(), "media después": a.mean(),
                "mediana antes": b.median(), "mediana después": a.median(),
                "% filas = 0 después": (a == 0).mean() * 100, "% filas imputadas": b.isna().mean() * 100})
md("9.7 Impacto del relleno en las variables numéricas", pd.DataFrame(imp), index=False, floatfmt=",.2f")
ev = t[t.engine_concept == "ELECTRIC"]
note(f"- Con la regla AG (consumo nulo → 0) los **{len(ev):,}** vehículos eléctricos pasan a tener consumo 0 l/100 km "
     "(coherente: no gastan combustible) y quedan mezclados con los vehículos térmicos sin telemetría, que también valen 0.")

# Figura: impacto en distribuciones
fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
for ax, (c, lab, rg) in zip(axes, [("trip_distance_average", "Distancia media por trayecto (km)", (0, 50)),
                                    ("fuel_consumption_average", "Consumo medio (l/100 km)", (0, 20)),
                                    ("speed_average", "Velocidad media (km/h)", (0, 85))]):
    bins = np.linspace(*rg, 51)
    ax.hist(t[c].clip(*rg), bins=bins, color=CAT[1], label="tras tratamiento", edgecolor=SURFACE, linewidth=0.4)
    ax.hist(before[c].dropna().clip(*rg), bins=bins, color=BLUE, label="observados", edgecolor=SURFACE, linewidth=0.4)
    ax.set_title(lab, fontsize=9.5)
    ax.set_ylabel("filas")
axes[0].legend(loc="upper right")
fig.suptitle("Efecto del relleno de nulos de telemetría (decisión del equipo)", x=0.01, ha="left", fontsize=11,
             fontweight="bold")
save(fig, "fig17_impacto_relleno_telemetria.png")

fig, ax = plt.subplots(figsize=(8, 3.6))
ec_plot = ec_cmp.drop(columns="% original (sobre conocidos)").fillna(0).T[["COMBUSTION", "MILD_HYBRID", "PLUGIN_HYBRID",
                                                                             "ELECTRIC", "UNKNOWN"]]
leftp = np.zeros(len(ec_plot))
for i, col in enumerate(ec_plot.columns):
    color = CAT[i] if col != "UNKNOWN" else "#c3c2b7"
    ax.barh(ec_plot.index, ec_plot[col], left=leftp, height=0.55, color=color, edgecolor=SURFACE, linewidth=2, label=col)
    for j, v in enumerate(ec_plot[col].values):
        if v > 4:
            ax.text(leftp[j] + v / 2, j, f"{v:.0f}", ha="center", va="center", fontsize=8, color="white")
    leftp += ec_plot[col].values
ax.set_xlim(0, 100); ax.grid(axis="y", visible=False); ax.invert_yaxis()
ax.set_xlabel("% de filas")
ax.set_title("engine_concept tras imputar: moda frente a reglas validadas")
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.22))
save(fig, "fig18_engine_moda_vs_reglas.png")

# --- Exclusión ("quitar ruido") y guardado ---
drop_cols = [L["A"], L["H"]]  # A y H se eliminan
key_cols = [L["B"], L["C"]]   # B y C también son ruido para el modelo; se guardan solo como claves
clean = t.drop(columns=[c for c in drop_cols if c in t.columns] + ["reg_date", "reg_year", "zip_region"],
               errors="ignore")
na_after = clean.isna().sum()
md("9.8 Nulos que quedan tras el tratamiento", na_after[na_after > 0].rename("nulos") if (na_after > 0).any()
   else pd.Series({"(ninguna columna)": 0}, name="nulos"))
note(f"- Columnas eliminadas por ruido: {', '.join(f'`{c}`' for c in drop_cols)}. "
     f"{', '.join(f'`{c}`' for c in key_cols)} también son ruido para el modelo, pero se conservan en el fichero "
     "**solo como claves** (sin ellas no se puede agregar por cliente). No deben entrar como features.")
clean.to_parquet(PROC / "relaciones_limpio.parquet", index=False)

# Vista cliente para retos posteriores
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
for c in ["trip_distance_average", "operating_hours_total", "fuel_consumption_average", "speed_average"]:
    clients[c] = gc[c].mean()
clients.to_parquet(PROC / "clientes.parquet")
md("9.9 Vista agregada a nivel cliente (data/processed/clientes.parquet)", clients.describe(include="all").T
   .drop(columns=["top", "freq"], errors="ignore"), floatfmt=",.2f")

(OUT / "resultados.md").write_text("# Resultados del EDA (generado por eda/eda_reto1.py)\n" + "\n".join(_md), encoding="utf-8")
print(f"OK -> {OUT / 'resultados.md'} | figuras en {FIG} | {len(clean):,} filas limpias, {len(clients):,} clientes")
