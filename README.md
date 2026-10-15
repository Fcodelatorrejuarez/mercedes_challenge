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
se apartan como segmento propio. Se usan 10 features de modelo sobre edad, relación con la marca (vehículos actuales,
leasing), gama de la flota, electrificación y antigüedad del vehículo, con log1p y `StandardScaler` dentro de un
`Pipeline`. La telemetría, el país, los meses como cliente, el poder adquisitivo relativo y las visitas al taller se usan
solo para describir los segmentos: con ellos dentro, el clustering era menos estable (ARI Jackknife 0,69 frente a 0,91).
La binaria `tiene_vehiculo_actual` se eliminó por redundante con `n_vehiculos_actuales` (0 = sin vehículo actual).

**Modelo (reto 3).** K-Means con k = 2…10. Se elige **k = 7**: silhouette 0,240 y Davies-Bouldin 1,42, casi igual que
k = 8 (0,255), pero mucho más estable (ARI Jackknife 0,91 frente a 0,82; todos los segmentos con Jaccard ≥ 0,87).

**Segmentos (reto 4).**

| Segmento | % clientes | En una frase | Acción |
|---|---:|---|---|
| Compacto al contado | 23,4 | A, B/GLA/GLB o CLA de unos 5 años, sin financiación | Renovación a compacto nuevo o EQA/EQB con financiación |
| Berlina clásica al contado | 20,9 | C/E y algo de GLC, unos 7 años, sin financiación ni electrificación | Mantenimiento fuera de garantía y renovación con financiación |
| Familia SUV híbrida | 16,8 | GLC/GLE, dos tercios electrificada | Paso a SUV eléctrico, accesorios y servicio de híbridos |
| Urbano financiado | 12,6 | 100 % leasing, compactos nuevos, 19 % BEV | Renovación anticipada al vencer el contrato, upgrade a EQ |
| Entusiasta AMG | 11,2 | Flota casi solo AMG, joven y suizo | Experiencias y eventos AMG, mantenimiento premium |
| Trabajador profesional que utiliza furgoneta | 10,2 | V-Class, Vito o Sprinter | Paquetes de taller prioritario, eVans |
| Élite eléctrica y lujo | 4,4 | EQE/EQS, Clase S, AMG GT; la mitad BEV; zona más rica | Gestor dedicado, acceso preferente |
| Flota / Profesional | 0,5 | Más de 20 relaciones | Gestión B2B |

Los ex-clientes (~10 %, sin vehículo actual) no son un segmento aparte: se reparten según la gama de su último coche y
se activan con una campaña de recuperación transversal (`n_vehiculos_actuales = 0`) adaptada a su segmento.

**Avanzados.**
1. K-Means tiene el mejor silhouette (0,240) frente a MiniBatch, GMM, Ward y Birch. MiniBatch es casi igual (ARI 0,73).
   GMM y Ward reproducen furgonetas, élite y AMG. DBSCAN no encaja con estos datos.
2. PCA: hacen falta 7 componentes para explicar el 80 % de la varianza. En 3D los segmentos conservan casi toda su
   separación (silhouette 0,236 frente a 0,239 en el espacio completo).
3. Jackknife (20 submuestras, excluyendo el 15 % cada vez): **ARI medio de 0,91** y 94 % de coincidencia por cliente.
   Los 7 segmentos son muy estables (Jaccard ≥ 0,87). Los pocos saltos se dan sobre todo entre Compacto al contado y
   Urbano financiado.
