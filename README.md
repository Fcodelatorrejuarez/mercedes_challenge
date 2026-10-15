# Reto de mercedes 

En este documento se detallaran las especificaciones del reto planteado.

## Objetivo

En esta edición, proponemos segmentar la base de clientes de Mercedes-Benz
mediante técnicas de aprendizaje no supervisado (clustering), con el objetivo de
habilitar estrategias de marketing personalizadas:
- Ofertas de vehículos
- Planes de mantenimiento
- Campañas de fidelización
- Comunicaciones dirigidas

## Estructura del proyecto

Cada reto es un notebook ejecutado y documentado. Hay que ejecutarlos **en este orden**, porque cada uno lee los
CSV que genera el anterior (todos en `data/processed/`).

| Reto | Notebook | Genera |
|---|---|---|
| Básico 1: EDA y calidad | [`eda/EDA_reto1.ipynb`](eda/EDA_reto1.ipynb) · resumen en [`eda/Resumen_reto1.md`](modelo/Resumen_reto1.md) | `relaciones_limpio.csv`, `clientes.csv` |
| Básico 2: feature engineering | [`modelo/Reto2_Feature_Engineering.ipynb`](modelo/Reto2_Feature_Engineering.ipynb) | `features_modelo.csv`, `clientes_modelo.csv` |
| Básico 3: K-Means | [`modelo/Reto3_KMeans.ipynb`](modelo/Reto3_KMeans.ipynb) | `segmentos_kmeans.csv`, `centroides_kmeans.csv`, `metricas_kmeans.csv` |
| Básico 4: perfilado | [`modelo/Reto4_Perfilado_Segmentos.ipynb`](modelo/Reto4_Perfilado_Segmentos.ipynb) | `clientes_segmentados.csv`, `nombres_segmentos.csv` |
| Avanzado 1: comparativa de algoritmos | [`modelo/Avanzado1_Comparativa_Algoritmos.ipynb`](modelo/Avanzado1_Comparativa_Algoritmos.ipynb) | `comparativa_algoritmos.csv` |
| Avanzado 2: PCA | [`modelo/Avanzado2_PCA.ipynb`](modelo/Avanzado2_PCA.ipynb) | figuras |
| Avanzado 3: Jackknife | [`modelo/Avanzado3_Jackknife.ipynb`](modelo/Avanzado3_Jackknife.ipynb) | `estabilidad_jackknife.csv` |

Entorno: `pip install -r requirements.txt`. Las figuras se guardan en `eda/figures/` y `modelo/figures/`.

## Resultados en una página

**Datos (reto 1).** 302.850 relaciones cliente–vehículo de 173.456 clientes (Suiza y Austria). El tratamiento de nulos
sigue `Descripcion_uso_de_datos`, con correcciones de coherencia: el dataset tratado no tiene nulos y pasa 15
comprobaciones de coherencia (por cliente, por vehículo, zona, motor y combustible, telemetría).

**Features (reto 2).** Se modela a nivel cliente. Las 833 cuentas con más de 20 relaciones (concesionarios o flotas)
se apartan como segmento propio. Se usan 13 features de modelo sobre perfil, relación con la marca, gama, energía,
antigüedad del vehículo y mantenimiento, con log1p y `StandardScaler` dentro de un `Pipeline`. La telemetría y el país se
usan solo para describir los segmentos: con ellos dentro, el clustering separaba "con datos" de "sin datos". La binaria
`tiene_vehiculo_actual` se eliminó por redundante con `n_vehiculos_actuales` (0 = sin vehículo actual), que duplicaba
el peso de esa dimensión.

**Modelo (reto 3).** K-Means con k = 2…10. Se elige **k = 8**: el mejor silhouette dentro del rango útil para
negocio (0,163) y el mejor Davies-Bouldin (1,74).

**Segmentos (reto 4).**

| Segmento | % clientes | En una frase | Acción |
|---|---:|---|---|
| Compacto al contado | 20,2 | A, B/GLA/GLB o CLA de unos 5 años, sin financiación | Renovación a compacto nuevo o EQA/EQB con financiación |
| Berlina clásica al contado | 18,4 | C/E y algo de GLC, unos 7 años, sin financiación ni electrificación | Mantenimiento fuera de garantía y renovación con financiación |
| Familia SUV híbrida | 15,9 | GLC/GLE, casi dos tercios electrificada | Paso a SUV eléctrico, accesorios y servicio de híbridos |
| Urbano financiado | 12,4 | 100 % leasing, compactos nuevos, 19 % BEV | Renovación anticipada al vencer el contrato, upgrade a EQ |
| Entusiasta AMG | 10,5 | Flota casi solo AMG, joven y suizo | Experiencias y eventos AMG, mantenimiento premium |
| Trabajador profesional que utiliza furgoneta | 9,8 | V-Class, Vito o Sprinter | Paquetes de taller prioritario, eVans |
| Ex-cliente por recuperar | 8,0 | Sin vehículo actual | Campaña de recuperación (ocasión certificada o leasing) |
| Élite eléctrica y lujo | 4,2 | EQE/EQS, Clase S, AMG GT; la mitad BEV; zona más rica | Gestor dedicado, acceso preferente |
| Flota / Profesional | 0,5 | Más de 20 relaciones | Gestión B2B |

**Avanzados.**
1. K-Means tiene el mejor silhouette (0,163) frente a MiniBatch, GMM, Ward y Birch. GMM (ARI 0,47) y Ward (ARI 0,53)
   reproducen los segmentos fuertes (furgoneta, élite, SUV) y fusionan Berlina clásica con Compacto. DBSCAN no encaja con estos datos.
2. PCA: hacen falta 8 componentes para explicar el 80 % de la varianza. En 2D solo los ex-clientes se separan con claridad.
3. Jackknife (20 submuestras, excluyendo el 15 % cada vez): ARI medio de 0,69. Cinco segmentos son estables o muy estables
   (Furgoneta, Élite, AMG, Urbano financiado: Jaccard ≥ 0,91; Familia SUV: 0,76). Berlina clásica, Compacto al contado y
   Ex-cliente son inestables (Jaccard ≈ 0,53–0,55): la frontera entre ellos es la menos estable.
