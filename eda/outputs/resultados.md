# Resultados del EDA (generado por eda/EDA_reto1.ipynb)

### 1.1 Dimensiones

- Filas: **302,850**  ·  Columnas: **39** (incluida la columna sin nombre `Unnamed: 0`)

- Clientes únicos: **173,456**  ·  Vehículos únicos: **244,519**

- Filas duplicadas completas: **0**  ·  pares (client_id, vehicle_id) duplicados: **0**

- `Unnamed: 0` es igual al índice posicional 0..n-1: **True**


### 1.2 Tipos, cardinalidad y nulos por columna

|                                     | dtype pandas   |   n_unique |   % nulos | ejemplo                                                          |
|:------------------------------------|:---------------|-----------:|----------:|:-----------------------------------------------------------------|
| client_id                           | str            |     173456 |      0.00 | 000144e39c02702f821f69beeb7036f40cf8505051050f38ea776337ef9b6f3c |
| vehicle_id                          | str            |     244519 |      0.00 | db75a50f450de43f5f7a94d2a05b605fdc1a5d84913ba668615a17eaf663d6a0 |
| age_range                           | str            |          6 |      0.00 | 35-44                                                            |
| gender_derived                      | str            |          2 |     11.20 | female                                                           |
| model_series                        | str            |         88 |      0.00 | 177                                                              |
| vehicle_type                        | str            |       1436 |      0.30 | A 180 d                                                          |
| model_class                         | str            |         42 |      1.11 | A-Class                                                          |
| product_group                       | str            |          4 |      0.00 | P                                                                |
| engine_concept                      | str            |          4 |     44.38 | COMBUSTION                                                       |
| country_code                        | str            |          2 |      0.00 | AT                                                               |
| fuel_type                           | str            |          7 |     59.02 | PETROL_PLUS                                                      |
| date_of_first_registration          | str            |       5316 |      1.38 | 2019-08-06                                                       |
| is_current_vehicle                  | bool           |          2 |      0.00 | False                                                            |
| role                                | str            |          5 |      0.00 | OWNER                                                            |
| role_type                           | str            |          2 |      0.00 | B2C                                                              |
| months_as_mb_customer               | float64        |        121 |      0.00 | 36.0                                                             |
| currently_connected_vehicles        | int64          |         22 |      0.00 | 1                                                                |
| finance_leasing_status              | str            |          4 |      0.00 | never_active                                                     |
| workshop_visits_warranty_goodwill   | int64          |         36 |      0.00 | 0                                                                |
| consent_phone_communication_channel | bool           |          2 |      0.00 | False                                                            |
| consent_epost_communication_channel | bool           |          2 |      0.00 | True                                                             |
| consent_post_communication_channel  | bool           |          2 |      0.00 | False                                                            |
| purchasing_power_per_inhabitant_eur | float64        |       5032 |      6.30 | 31518.15                                                         |
| purchasing_power_per_household_eur  | float64        |       5035 |      6.30 | 59705.4                                                          |
| population                          | float64        |       3231 |      6.28 | 104752.0                                                         |
| zipcode                             | str            |       4610 |      5.33 | 4020                                                             |
| trip_distance_average               | float64        |       5476 |     61.37 | 9.59                                                             |
| trip_distance_mode                  | str            |        108 |     59.38 | 7.5                                                              |
| trip_distance_median                | float64        |         13 |     59.38 | 7.5                                                              |
| trip_distance_all_counter           | float64        |      10780 |     59.38 | 1305.0                                                           |
| operating_hours_total               | float64        |      80943 |     57.57 | 295.98                                                           |
| fuel_consumption_average            | float64        |       2267 |     59.67 | 6.61                                                             |
| speed_average                       | float64        |       8248 |     60.22 | 40.34                                                            |
| speed_mode                          | str            |         17 |     59.82 | 30                                                               |
| speed_median                        | float64        |         12 |     59.82 | 30.0                                                             |
| speed_all_counter                   | float64        |     117441 |     59.82 | 1066745.6                                                        |
| number_of_households                | float64        |       2296 |      6.28 | 55298.0                                                          |
| purchasing_power_millions_eur       | float64        |       4973 |      6.30 | 3301.589                                                         |


### 2.1 Distribución de filas por cliente y por vehículo

|       |   filas por cliente |   filas por vehículo |
|:------|--------------------:|---------------------:|
| count |          173,456.00 |           244,519.00 |
| mean  |                1.75 |                 1.24 |
| std   |                5.51 |                 0.57 |
| min   |                1.00 |                 1.00 |
| 50%   |                1.00 |                 1.00 |
| 75%   |                2.00 |                 1.00 |
| 90%   |                2.00 |                 2.00 |
| 95%   |                3.00 |                 2.00 |
| 99%   |               10.00 |                 3.00 |
| 99.9% |               74.00 |                 5.00 |
| max   |              561.00 |                36.00 |


### 2.2 ¿Qué atributos son del cliente y cuáles de la relación?

|                                     |   % clientes multi-fila con >1 valor |   % vehículos multi-fila con >1 valor |
|:------------------------------------|-------------------------------------:|--------------------------------------:|
| age_range                           |                                 0.00 |                                nan    |
| gender_derived                      |                                 0.00 |                                nan    |
| country_code                        |                                 0.00 |                                nan    |
| months_as_mb_customer               |                                 0.00 |                                nan    |
| currently_connected_vehicles        |                                 0.00 |                                nan    |
| finance_leasing_status              |                                 0.00 |                                nan    |
| consent_phone_communication_channel |                                 0.00 |                                nan    |
| consent_epost_communication_channel |                                 0.00 |                                nan    |
| consent_post_communication_channel  |                                 0.00 |                                nan    |
| zipcode                             |                                 0.00 |                                nan    |
| purchasing_power_per_inhabitant_eur |                                 0.00 |                                nan    |
| purchasing_power_per_household_eur  |                                 0.00 |                                nan    |
| population                          |                                 0.00 |                                nan    |
| number_of_households                |                                 0.00 |                                nan    |
| purchasing_power_millions_eur       |                                 0.00 |                                nan    |
| role                                |                                25.99 |                                nan    |
| role_type                           |                                 1.18 |                                nan    |
| model_series                        |                               nan    |                                  0.00 |
| vehicle_type                        |                               nan    |                                  0.00 |
| model_class                         |                               nan    |                                  0.00 |
| product_group                       |                               nan    |                                  0.00 |
| engine_concept                      |                               nan    |                                  0.00 |
| fuel_type                           |                               nan    |                                  0.00 |
| date_of_first_registration          |                               nan    |                                  0.00 |
| workshop_visits_warranty_goodwill   |                               nan    |                                 62.79 |
| is_current_vehicle                  |                               nan    |                                 63.39 |
| operating_hours_total               |                               nan    |                                 56.24 |
| trip_distance_average               |                               nan    |                                 53.58 |
| speed_average                       |                               nan    |                                 53.34 |


### 2.3 Clientes con muchas relaciones (posibles concesionarios, flotas, rent-a-car)

| umbral filas/cliente   |   clientes |   filas que acumulan |   % filas |
|:-----------------------|-----------:|---------------------:|----------:|
| >10                    |       1706 |                60530 |     19.99 |
| >20                    |        833 |                47677 |     15.74 |
| >50                    |        295 |                30754 |     10.15 |
| >100                   |        102 |                17283 |      5.71 |

- En clientes con >20 relaciones solo el **10.4 %** de filas es vehículo actual (vs 68.7 % en el resto); rol OWNER en el 87.9 % de sus filas y role_type B2C en el 92.5 %.


### 2.4 role vs role_type

| role      |   B2B |    B2C |    All |
|:----------|------:|-------:|-------:|
| DRIVER    |  5521 |      0 |   5521 |
| LEGACY    |     0 |  11314 |  11314 |
| OWNER     |     0 | 264418 | 264418 |
| TEMP_USER |     0 |   3966 |   3966 |
| USER      |     0 |  17631 |  17631 |
| All       |  5521 | 297329 | 302850 |


### 2.5 role vs is_current_vehicle

| role      |   False |   True |    All |
|:----------|--------:|-------:|-------:|
| DRIVER    |    4972 |    549 |   5521 |
| LEGACY    |    6094 |   5220 |  11314 |
| OWNER     |  102782 | 161636 | 264418 |
| TEMP_USER |    3795 |    171 |   3966 |
| USER      |    5041 |  12590 |  17631 |
| All       |  122684 | 180166 | 302850 |


### 3.1 Patrones conjuntos de nulos en el bloque de telemetría

|   patrón (1=presente) td_average/td_mode/td_median/td_all_counter/op_h/fuel/sp_average/sp_mode/sp_median/sp_all_counter |      filas |   % filas |
|------------------------------------------------------------------------------------------------------------------------:|-----------:|----------:|
|                                                                                                              0000000000 | 156,819.00 |     51.78 |
|                                                                                                              1111111111 |  96,680.00 |     31.92 |
|                                                                                                              1111000000 |  15,587.00 |      5.15 |
|                                                                                                              0000111111 |  14,151.00 |      4.67 |
|                                                                                                              0000110000 |   7,009.00 |      2.31 |
|                                                                                                              1111101111 |   4,449.00 |      1.47 |
|                                                                                                              0111111111 |   3,276.00 |      1.08 |
|                                                                                                              0111101111 |   1,113.00 |      0.37 |


### 3.2 Disponibilidad de telemetría por grupo (mecanismo de ausencia)

|                               |   % filas con alguna telemetría |
|:------------------------------|--------------------------------:|
| ('is_current_vehicle', False) |                            33.4 |
| ('is_current_vehicle', True)  |                            58.3 |
| ('role', 'DRIVER')            |                            10.1 |
| ('role', 'LEGACY')            |                            13.0 |
| ('role', 'OWNER')             |                            50.8 |
| ('role', 'TEMP_USER')         |                             3.4 |
| ('role', 'USER')              |                            54.7 |
| ('product_group', 'F')        |                             0.0 |
| ('product_group', 'G')        |                            49.2 |
| ('product_group', 'P')        |                            48.4 |
| ('product_group', 'T')        |                            48.3 |
| ('country_code', 'AT')        |                            49.4 |
| ('country_code', 'CH')        |                            47.6 |


### 3.3 Nulos de engine_concept / fuel_type / telemetría por año de matriculación (%)

|   reg_year |    filas |   engine_na |   fuel_na |   telem_na |
|-----------:|---------:|------------:|----------:|-----------:|
|    2,009.0 |    493.0 |       100.0 |     100.0 |       99.8 |
|    2,010.0 |    710.0 |        99.7 |     100.0 |       98.7 |
|    2,011.0 |  1,074.0 |        96.6 |      99.2 |       96.0 |
|    2,012.0 |  1,614.0 |        84.4 |      89.7 |       93.0 |
|    2,013.0 |  2,182.0 |        66.4 |      76.1 |       87.8 |
|    2,014.0 |  3,173.0 |        44.4 |      76.5 |       83.5 |
|    2,015.0 |  5,376.0 |        29.7 |      74.1 |       77.2 |
|    2,016.0 |  9,501.0 |        27.3 |      71.8 |       64.1 |
|    2,017.0 | 14,956.0 |        24.3 |      72.2 |       56.7 |
|    2,018.0 | 19,183.0 |        41.9 |      73.0 |       55.7 |
|    2,019.0 | 26,700.0 |        51.5 |      67.4 |       50.5 |
|    2,020.0 | 29,449.0 |        48.4 |      58.0 |       44.1 |
|    2,021.0 | 33,606.0 |        51.0 |      61.1 |       41.9 |
|    2,022.0 | 33,531.0 |        50.6 |      59.7 |       43.4 |
|    2,023.0 | 35,910.0 |        45.4 |      54.8 |       45.4 |
|    2,024.0 | 34,625.0 |        40.5 |      48.3 |       47.4 |
|    2,025.0 | 28,417.0 |        38.9 |      46.6 |       51.5 |
|    2,026.0 | 18,135.0 |        30.6 |      37.0 |       72.4 |


### 3.4 engine_concept vs fuel_type (filas)

| engine_concept   |   <NA> |   DIESEL |   DIESEL,ELECTRIC |   ELECTRIC |   PETROL |   PETROL,ELECTRIC |   PETROL_PLUS |   PETROL_PLUS,ELECTRIC |
|:-----------------|-------:|---------:|------------------:|-----------:|---------:|------------------:|--------------:|-----------------------:|
| <NA>             | 134390 |        0 |                 0 |          0 |        0 |                 0 |             0 |                      0 |
| COMBUSTION       |  43915 |    28475 |                 0 |          0 |    14422 |                 0 |         11612 |                      0 |
| ELECTRIC         |      0 |        0 |                 0 |      20944 |        0 |                 0 |             0 |                      0 |
| MILD_HYBRID      |     29 |     7418 |                 0 |          0 |    17946 |                 0 |          2362 |                      0 |
| PLUGIN_HYBRID    |    411 |        0 |              8604 |          0 |        0 |              7371 |             0 |                   4951 |


### 3.5 gender_derived por rol (% columna)

| gender_derived   |   DRIVER |   LEGACY |   OWNER |   TEMP_USER |   USER |
|:-----------------|---------:|---------:|--------:|------------:|-------:|
| <NA>             |      4.1 |     11.9 |     9.2 |        38.1 |   36.2 |
| female           |      4.7 |      9.8 |    15.0 |         8.8 |   24.6 |
| male             |     91.2 |     78.3 |    75.7 |        53.1 |   39.2 |

**Socio-demográficos y CP:**

- Filas sin CP: **16,135**; con CP pero sin cruce socio-demográfico: **2,879**; con CP y población pero sin poder adquisitivo: **73** (todas con population = 0).

- CP con formato no estándar (no 4 dígitos): **5** → ['55605', 'A-2100', 'CH-6340', 'Ottenbach']

- CP que existen en AT y en CH a la vez: **993** → el CP solo identifica una zona junto con `country_code`.

- (country, CP) con más de un valor socio-demográfico: **0**


### 3.6 % nulos por país

| country_code   |   gender_derived |   zipcode |   population |   purchasing_power_per_inhabitant_eur |   engine_concept |   fuel_type |   has_telemetry |
|:---------------|-----------------:|----------:|-------------:|--------------------------------------:|-----------------:|------------:|----------------:|
| AT             |            13.42 |      6.85 |         8.30 |                                  8.33 |            43.55 |       56.65 |           50.63 |
| CH             |             9.94 |      4.46 |         5.13 |                                  5.15 |            44.84 |       60.37 |           52.44 |

**Redundancias deterministas:**

- `purchasing_power_millions_eur` = `purchasing_power_per_inhabitant_eur` × `population` / 1e6 → error relativo máx. **7.4e-04**

- `purchasing_power_per_household_eur` = `purchasing_power_millions_eur` × 1e6 / `number_of_households` → error relativo máx. **7.4e-04**

- Tamaño medio del hogar (population / households): mediana **2.24**, p1–p99 [1.85, 2.76]

- `role_type` = B2B ⇔ `role` = DRIVER en el **100 %** de filas (ver 2.4).

- `model_series` → `model_class` es una función: series con >1 clase = **0**.


### 4.1 model_class (filas) - taxonomía solapada

| model_class             |   filas |
|:------------------------|--------:|
| GLC-Class               |   44198 |
| C-Class                 |   34990 |
| A-Class                 |   32524 |
| B-/GLA-/GLB-Class       |   28497 |
| V-Class / Vito          |   27349 |
| E-Class                 |   21171 |
| GLE-/GLS-Class          |   19170 |
| CLA-Class               |   15791 |
| EQA-/EQB-Class          |   11559 |
| Sprinter                |   10466 |
| EQE-Class               |    4947 |
| S-Class                 |    4892 |
| GLA-Class               |    4760 |
| G-Class                 |    4373 |
| EQC-Class               |    4059 |
| Citan                   |    3477 |
| E-Class Coupé/Cabriolet |    3397 |
| nan                     |    3369 |
| M-/GL-/GLE-/GLS-Class   |    3138 |
| B-Class                 |    3135 |
| EQS-Class               |    2331 |
| CLS-Class               |    2191 |
| CLE-Class               |    2187 |
| A-Class/CLA-Class       |    2113 |
| AMG GT                  |    1355 |
| SL-Class                |    1313 |
| GLE-Class               |    1184 |
| AMG GT 4-Door           |    1038 |
| fortwo / forfour        |     936 |
| SLK-/SLC-Class          |     788 |
| S-Class Coupé/Cabriolet |     656 |
| X-Class                 |     442 |
| M-/GL-Class             |     269 |
| SLK-Class               |     212 |
| Viano/Vito              |     202 |
| SLS AMG                 |     130 |
| CLK-Class               |      85 |
| R-Class                 |      61 |
| AMG ONE                 |      41 |
| CL-Class                |      36 |
| M-Class                 |      12 |
| SLR McLaren             |       3 |
| Maybach                 |       3 |


### 4.2 model_class nulo: series de modelo nuevas sin clase asignada

|   model_series |   filas | vehicle_types                           |   año_mediano |
|---------------:|--------:|:----------------------------------------|--------------:|
|            540 |    1645 | GLC 400 4MATIC, GLC 250                 |         2,026 |
|            244 |     955 | GLB 350 4MATIC, GLB 250+, GLB 200+      |         2,026 |
|            178 |     489 | CLA 220 4MATIC, CLA 200 4MATIC, CLA 180 |         2,026 |
|            248 |     206 | GLB 220 4MATIC, GLB 200 4MATIC, GLB 200 |         2,026 |
|            520 |      73 | C 400 4MATIC electric                   |         2,026 |
|            449 |       1 | 300  VLE  4X2   3342                    |           nan |


### 4.3 product_group vs nº de clases

| product_group   |   filas | clases                                                  |
|:----------------|--------:|:--------------------------------------------------------|
| F               |     936 | fortwo / forfour                                        |
| G               |    4373 | G-Class                                                 |
| P               |  255604 | GLC-Class, C-Class, A-Class, B-/GLA-/GLB-Class, E-Class |
| T               |   41937 | V-Class / Vito, Sprinter, Citan, X-Class, Viano/Vito    |

- `vehicle_type` con códigos técnicos (furgonetas, p. ej. `V 300AVG/L4X2   3200`): **41,059** filas, 660 valores distintos. Cardinalidad total: **1,436** valores.

**Fechas de primera matriculación:**

- Rango: **1987-01-14** → **2026-10-02**; nulas: **4,182**; posteriores a la fecha de referencia (2026-10-15): **0**; anteriores a 2009: **33**

**`months_as_mb_customer` (a nivel cliente):**

- Valor 36: **21,179** clientes (12.2 %) frente a 2,619 en 35 y 2,770 en 37 → pico artificial (≈ ×8).

- Valor 0: **7,254** clientes; máximo **120** meses (10 años, posible truncado); nulos: **2**.

- `months_as_mb_customer` − meses desde la matriculación más antigua del cliente: mediana **-27.2** (p5 -102, p95 -1). La relación con la marca empieza en la *conexión* (Mercedes me), no en la matriculación: lo normal es que sea más corta que la edad del coche (vehículos de ocasión, conexión posterior). Los clientes con 36 meses tienen su primer coche matriculado sobre todo en 2019, 2020, 2018.

- `currently_connected_vehicles` = nº de filas con `is_current_vehicle` = True del cliente en el **99.998 %** de clientes (discrepancias: 4). Clientes sin ningún vehículo actual: **18,048** (10.4 %).


### 4.4 Anomalías detectadas en telemetría

| regla                                                    |   filas |
|:---------------------------------------------------------|--------:|
| speed_average < 1 km/h                                   |     889 |
| speed_average ≥ 150 km/h                                 |      26 |
| operating_hours_total = 0                                |     140 |
| operating_hours_total > 5.000 h                          |     427 |
| trip_distance_all_counter = 0 con mediana/moda informada |    6027 |
| speed_all_counter = 0                                    |    1223 |
| fuel_consumption_average en tope inferior (3,0)          |      20 |
| fuel_consumption_average en tope superior (50,0)         |       8 |
| trip_distance_average en tope (300 km)                   |      34 |
| fuel_consumption_average informado en ELECTRIC           |       0 |
| trip_distance_mode con varios valores (empate)           |    7049 |
| speed_mode con varios valores (empate)                   |    1223 |

- Valores únicos de `trip_distance_median`: [1.0, 2.5, 3.0, 7.5, 10.0, 15.0, 22.5, 27.5, 42.5, 62.5, 87.5, 150.0, 300.0]

- Valores únicos de `speed_median`: [0.125, 10.0625, 15.0625, 30.0, 40.0, 45.0, 50.0, 75.0, 110.0, 150.0, 165.0, 220.0]

- Son marcas de clase de histogramas: conviven **dos esquemas de bins** (1/3/7,5/15/27,5/42,5… y 2,5/10/22,5…), probablemente por distintas generaciones de la unidad telemática. `speed_median` incluye el artefacto de coma flotante 220.00000000000003.


### 4.5 Consumo medio por fuel_type (l/100 km)

| fuel_type            |     count |   mean |    std |    min |    25% |    50% |    75% |    max |
|:---------------------|----------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| <NA>                 | 74,244.00 |   8.63 |   3.02 |   3.00 |   6.82 |   8.25 |   9.73 |  50.00 |
| DIESEL               | 18,465.00 |   7.65 |   2.94 |   3.00 |   5.94 |   6.75 |   8.86 |  50.00 |
| DIESEL,ELECTRIC      |  3,575.00 |   5.65 |   2.11 |   3.00 |   4.22 |   5.29 |   6.72 |  48.25 |
| ELECTRIC             |      0.00 | nan    | nan    | nan    | nan    | nan    | nan    | nan    |
| PETROL               | 14,187.00 |   8.91 |   2.99 |   3.00 |   7.38 |   8.34 |   9.51 |  50.00 |
| PETROL,ELECTRIC      |  3,077.00 |   6.24 |   2.48 |   3.00 |   4.47 |   5.93 |   7.63 |  38.25 |
| PETROL_PLUS          |  6,546.00 |  12.48 |   3.96 |   5.23 |   9.87 |  11.42 |  14.28 |  46.71 |
| PETROL_PLUS,ELECTRIC |  2,031.00 |   7.93 |   4.11 |   3.00 |   4.89 |   7.09 |   9.96 |  42.61 |


### 5.1 Estadísticos descriptivos numéricos (nivel fila cliente-vehículo)

|                                     |      count |         mean |          std |       min |        1% |        25% |          50% |          75% |           99% |              max |   skew |   % nulos |
|:------------------------------------|-----------:|-------------:|-------------:|----------:|----------:|-----------:|-------------:|-------------:|--------------:|-----------------:|-------:|----------:|
| months_as_mb_customer               | 302,846.00 |        43.87 |        26.89 |      0.00 |      0.00 |      25.00 |        39.00 |        60.00 |        115.00 |           120.00 |   0.60 |      0.00 |
| currently_connected_vehicles        | 302,850.00 |         2.15 |         3.53 |      0.00 |      0.00 |       1.00 |         1.00 |         2.00 |         19.00 |            21.00 |   3.46 |      0.00 |
| workshop_visits_warranty_goodwill   | 302,850.00 |         1.75 |         2.43 |      0.00 |      0.00 |       0.00 |         1.00 |         3.00 |         10.00 |            44.00 |   2.19 |      0.00 |
| vehicle_age_years                   | 298,668.00 |         5.09 |         3.19 |      0.04 |      0.16 |       2.57 |         4.74 |         7.13 |         14.37 |            39.75 |   0.71 |      1.38 |
| purchasing_power_per_inhabitant_eur | 283,763.00 |    46,481.17 |    17,294.53 | 19,701.53 | 24,291.65 |  31,518.15 |    46,165.64 |    54,210.68 |    106,183.57 |       148,353.74 |   1.74 |      6.30 |
| purchasing_power_per_household_eur  | 283,763.00 |   104,766.27 |    41,597.55 | 45,087.34 | 51,698.89 |  71,961.82 |   102,246.51 |   122,300.85 |    246,174.02 |       342,497.95 |   1.73 |      6.30 |
| population                          | 283,836.00 |    19,664.85 |    36,803.22 |      0.00 |    470.00 |   3,135.00 |     7,132.00 |    17,625.00 |    220,313.00 |       220,794.00 |   3.65 |      6.28 |
| number_of_households                | 283,836.00 |     9,336.42 |    17,781.94 |      0.00 |    209.00 |   1,344.00 |     3,145.00 |     8,353.00 |    102,026.00 |       102,998.00 |   3.49 |      6.28 |
| purchasing_power_millions_eur       | 283,763.00 |       733.17 |     1,042.27 |      0.65 |     20.48 |     139.21 |       329.27 |       873.42 |      5,324.88 |         5,998.91 |   2.81 |      6.30 |
| trip_distance_average               | 116,993.00 |        16.16 |        10.67 |      1.00 |      2.84 |      10.15 |        14.02 |        19.53 |         49.39 |           300.00 |   7.62 |     61.37 |
| trip_distance_median                | 123,020.00 |         6.62 |         7.77 |      1.00 |      1.00 |       3.00 |         7.50 |         7.50 |         27.50 |           300.00 |  19.16 |     59.38 |
| trip_distance_all_counter           | 123,020.00 |     2,351.70 |     2,768.20 |      0.00 |      0.00 |     518.00 |     1,593.00 |     3,321.00 |     11,404.62 |        89,078.00 |   4.94 |     59.38 |
| operating_hours_total               | 128,492.00 |       620.27 |       742.61 |      0.00 |      0.09 |     137.48 |       406.51 |       855.95 |      3,393.64 |        26,842.00 |   4.06 |     57.57 |
| fuel_consumption_average            | 122,125.00 |         8.56 |         3.26 |      3.00 |      3.59 |       6.58 |         8.11 |         9.72 |         19.00 |            50.00 |   3.60 |     59.67 |
| speed_average                       | 120,468.00 |        48.67 |        14.21 |      0.12 |      2.29 |      41.23 |        49.34 |        57.25 |         80.45 |           220.00 |  -0.30 |     60.22 |
| speed_median                        | 121,691.00 |        42.63 |        17.41 |      0.12 |      0.12 |      30.00 |        50.00 |        50.00 |         75.00 |           220.00 |   0.13 |     59.82 |
| speed_all_counter                   | 121,691.00 | 2,530,486.84 | 7,269,688.37 |      0.00 |      0.00 | 628,505.80 | 1,698,968.30 | 3,382,487.15 | 13,326,747.63 | 1,452,478,022.80 | 145.80 |     59.82 |


### 5.2 Outliers por regla IQR (1,5×)

|                                     |   límite inf. |   límite sup. |   % outliers (IQR) |
|:------------------------------------|--------------:|--------------:|-------------------:|
| months_as_mb_customer               |        -27.50 |        112.50 |               1.50 |
| currently_connected_vehicles        |         -0.50 |          3.50 |              11.03 |
| workshop_visits_warranty_goodwill   |         -4.50 |          7.50 |               3.39 |
| vehicle_age_years                   |         -4.27 |         13.96 |               1.22 |
| purchasing_power_per_inhabitant_eur |     -2,520.64 |     88,249.48 |               2.71 |
| purchasing_power_per_household_eur  |     -3,546.74 |    197,809.40 |               3.59 |
| population                          |    -18,600.00 |     39,360.00 |               9.76 |
| number_of_households                |     -9,169.50 |     18,866.50 |              10.42 |
| purchasing_power_millions_eur       |       -962.10 |      1,974.72 |               8.16 |
| trip_distance_average               |         -3.92 |         33.60 |               4.67 |
| trip_distance_median                |         -3.75 |         14.25 |              13.54 |
| trip_distance_all_counter           |     -3,686.50 |      7,525.50 |               4.14 |
| operating_hours_total               |       -940.22 |      1,933.65 |               4.64 |
| fuel_consumption_average            |          1.87 |         14.43 |               3.75 |
| speed_average                       |         17.20 |         81.28 |               3.74 |
| speed_median                        |          0.00 |         80.00 |               0.43 |
| speed_all_counter                   | -3,502,466.23 |  7,513,459.18 |               4.64 |


### 5.3 Descriptivos categóricos (nivel fila)

|                                     |   n_unique | moda         |   % moda |   % nulos |
|:------------------------------------|-----------:|:-------------|---------:|----------:|
| age_range                           |          6 | 45-54        |    22.54 |      0.00 |
| gender_derived                      |          2 | male         |    82.96 |     11.20 |
| country_code                        |          2 | CH           |    63.69 |      0.00 |
| product_group                       |          4 | P            |    84.40 |      0.00 |
| model_class                         |         42 | GLC-Class    |    14.76 |      1.11 |
| engine_concept                      |          4 | COMBUSTION   |    58.43 |     44.38 |
| fuel_type                           |          7 | DIESEL       |    28.92 |     59.02 |
| role                                |          5 | OWNER        |    87.31 |      0.00 |
| role_type                           |          2 | B2C          |    98.18 |      0.00 |
| finance_leasing_status              |          4 | never_active |    58.28 |      0.00 |
| is_current_vehicle                  |          2 | True         |    59.49 |      0.00 |
| consent_phone_communication_channel |          2 | True         |    85.64 |      0.00 |
| consent_epost_communication_channel |          2 | True         |    98.32 |      0.00 |
| consent_post_communication_channel  |          2 | True         |    85.13 |      0.00 |


### 6.1 Perfil demográfico y comercial (nivel cliente)

|                                                  |   clientes |     % |
|:-------------------------------------------------|-----------:|------:|
| ('age_range', '45-54')                           |  36,439.00 | 21.01 |
| ('age_range', '65+')                             |  35,057.00 | 20.21 |
| ('age_range', '55-64')                           |  34,007.00 | 19.61 |
| ('age_range', '35-44')                           |  32,747.00 | 18.88 |
| ('age_range', '25-34')                           |  26,970.00 | 15.55 |
| ('age_range', '<25')                             |   8,236.00 |  4.75 |
| ('gender_derived', 'male')                       | 112,726.00 | 64.99 |
| ('gender_derived', 'female')                     |  31,332.00 | 18.06 |
| ('gender_derived', '<NA>')                       |  29,398.00 | 16.95 |
| ('country_code', 'CH')                           | 114,763.00 | 66.16 |
| ('country_code', 'AT')                           |  58,693.00 | 33.84 |
| ('finance_leasing_status', 'never_active')       | 122,401.00 | 70.57 |
| ('finance_leasing_status', 'active_FL_only')     |  41,173.00 | 23.74 |
| ('finance_leasing_status', 'was_active')         |   5,646.00 |  3.26 |
| ('finance_leasing_status', 'active_FL_and_CASH') |   4,236.00 |  2.44 |


### 6.2 Combinaciones de consentimiento (nivel cliente)

|   teléfono/email/correo (1=sí) |   clientes |     % |
|-------------------------------:|-----------:|------:|
|                            111 | 140,639.00 | 81.08 |
|                            010 |  17,442.00 | 10.06 |
|                            110 |   7,149.00 |  4.12 |
|                            011 |   5,256.00 |  3.03 |
|                            001 |   1,471.00 |  0.85 |
|                            100 |   1,011.00 |  0.58 |
|                            101 |     488.00 |  0.28 |


### 6.3 Tasa de consentimiento por canal y país (%)

| country_code   |   consent_phone_communication_channel |   consent_epost_communication_channel |   consent_post_communication_channel |
|:---------------|--------------------------------------:|--------------------------------------:|-------------------------------------:|
| AT             |                                  84.9 |                                  98.0 |                                 85.8 |
| CH             |                                  86.7 |                                  98.4 |                                 85.0 |


### 6.4 Descriptivos numéricos a nivel cliente

|                                     |      count |      mean |       std |       min |       25% |       50% |       75% |       90% |        99% |        max |
|:------------------------------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|-----------:|-----------:|
| months_as_mb_customer               | 173,454.00 |     33.90 |     20.73 |      0.00 |     18.00 |     36.00 |     47.00 |     62.00 |      91.00 |     120.00 |
| currently_connected_vehicles        | 173,456.00 |      1.04 |      0.88 |      0.00 |      1.00 |      1.00 |      1.00 |      1.00 |       3.00 |      21.00 |
| n_relaciones                        | 173,456.00 |      1.75 |      5.51 |      1.00 |      1.00 |      1.00 |      2.00 |      2.00 |      10.00 |     561.00 |
| visitas_taller_total                | 173,456.00 |      3.06 |      4.70 |      0.00 |      0.00 |      2.00 |      4.00 |      7.00 |      18.00 |     206.00 |
| edad_media_vehiculo_actual          | 154,053.00 |      4.69 |      2.96 |      0.04 |      2.32 |      4.32 |      6.70 |      8.66 |      12.85 |      39.75 |
| purchasing_power_per_inhabitant_eur | 158,097.00 | 47,189.33 | 17,304.08 | 19,701.53 | 32,072.80 | 46,753.32 | 54,750.58 | 64,734.05 | 106,183.57 | 148,353.74 |


### 6.5 Edad × financiación (% fila)

| age_range   |   active_FL_and_CASH |   active_FL_only |   never_active |   was_active |
|:------------|---------------------:|-----------------:|---------------:|-------------:|
| <25         |                  1.7 |             20.5 |           75.4 |          2.4 |
| 25-34       |                  2.2 |             26.5 |           67.0 |          4.4 |
| 35-44       |                  3.0 |             29.8 |           63.3 |          3.9 |
| 45-54       |                  3.2 |             27.8 |           65.7 |          3.3 |
| 55-64       |                  2.9 |             23.8 |           70.6 |          2.8 |
| 65+         |                  1.2 |             12.4 |           84.0 |          2.4 |


### 6.6 País × financiación (% fila)

| country_code   |   active_FL_and_CASH |   active_FL_only |   never_active |   was_active |
|:---------------|---------------------:|-----------------:|---------------:|-------------:|
| AT             |                  2.3 |             13.3 |           82.4 |          2.0 |
| CH             |                  2.5 |             29.1 |           64.5 |          3.9 |


### 6.7 Edad × género (% columna)

| gender_derived   |   <25 |   25-34 |   35-44 |   45-54 |   55-64 |   65+ |
|:-----------------|------:|--------:|--------:|--------:|--------:|------:|
| <NA>             |  40.5 |    18.7 |    14.4 |    10.8 |     8.5 |  27.1 |
| female           |  18.3 |    23.2 |    19.6 |    19.6 |    17.8 |  11.3 |
| male             |  41.1 |    58.2 |    66.0 |    69.6 |    73.8 |  61.6 |


### 6.8 Poder adquisitivo por habitante (mediana €) por país y edad

| age_range   |     AT |     CH |
|:------------|-------:|-------:|
| <25         | 29,981 | 49,656 |
| 25-34       | 29,930 | 50,223 |
| 35-44       | 30,045 | 51,100 |
| 45-54       | 30,180 | 51,765 |
| 55-64       | 30,379 | 51,887 |
| 65+         | 30,494 | 52,772 |

- Clientes con algún vehículo electrificado (BEV/PHEV) actual: **15.5 %**; clientes multi-vehículo (≥2 actuales): **8.4 %**; B2B: **0.56 %**.


### 7.1 Mix de motorización por año de matriculación (% sobre conocidos)

|   reg_year |   COMBUSTION |   MILD_HYBRID |   PLUGIN_HYBRID |   ELECTRIC |
|-----------:|-------------:|--------------:|----------------:|-----------:|
|       2015 |        100.0 |           0.0 |             0.0 |        0.0 |
|       2016 |        100.0 |           0.0 |             0.0 |        0.0 |
|       2017 |        100.0 |           0.0 |             0.0 |        0.0 |
|       2018 |         97.4 |           2.6 |             0.0 |        0.0 |
|       2019 |         78.2 |          19.2 |             0.1 |        2.5 |
|       2020 |         71.2 |          17.0 |             5.0 |        6.7 |
|       2021 |         61.3 |          17.9 |            11.2 |        9.6 |
|       2022 |         52.4 |          18.3 |            11.2 |       18.1 |
|       2023 |         42.8 |          18.3 |            19.6 |       19.3 |
|       2024 |         31.7 |          26.2 |            25.6 |       16.5 |
|       2025 |         29.4 |          25.2 |            28.6 |       16.8 |
|       2026 |         18.2 |          22.8 |            21.5 |       37.5 |


### 7.2 Visitas en garantía medias por antigüedad del vehículo

| vehicle_age_years   |   visitas medias |
|:--------------------|-----------------:|
| (0, 1]              |             0.25 |
| (1, 2]              |             1.08 |
| (2, 3]              |             1.90 |
| (3, 4]              |             2.45 |
| (4, 5]              |             2.67 |
| (5, 7]              |             2.45 |
| (7, 10]             |             1.39 |
| (10, 40]            |             0.75 |


### 7.3 product_group

| product_group   |   filas |   % filas | significado (deducido de model_class)                              |
|:----------------|--------:|----------:|:-------------------------------------------------------------------|
| P               |  255604 |     84.40 | Turismos                                                           |
| T               |   41937 |     13.85 | Furgonetas / transporter (V-Class, Vito, Sprinter, Citan, X-Class) |
| G               |    4373 |      1.44 | Clase G (todoterreno)                                              |
| F               |     936 |      0.31 | smart (fortwo/forfour)                                             |


### 7.4 Señales de gama extraíbles de vehicle_type

|                                      |   % filas |
|:-------------------------------------|----------:|
| AMG (vehicle_type empieza por 'AMG') |     12.76 |
| 4MATIC (tracción integral)           |     58.90 |
| Maybach                              |      0.14 |


### 7.5 engine_concept por país (% fila, sobre conocidos)

| country_code   |   COMBUSTION |   ELECTRIC |   MILD_HYBRID |   PLUGIN_HYBRID |
|:---------------|-------------:|-----------:|--------------:|----------------:|
| AT             |         54.7 |       16.7 |          11.8 |            16.8 |
| CH             |         60.6 |        9.9 |          19.2 |            10.2 |


### 8.1 Socio-demografía por país (mediana, nivel cliente)

| country_code   |   purchasing_power_per_inhabitant_eur |   purchasing_power_per_household_eur |   population |   number_of_households |   purchasing_power_millions_eur |
|:---------------|--------------------------------------:|-------------------------------------:|-------------:|-----------------------:|--------------------------------:|
| AT             |                              30,177.6 |                             66,938.2 |      9,856.0 |                4,580.0 |                           309.7 |
| CH             |                              51,433.6 |                            116,082.4 |      6,695.0 |                2,979.0 |                           374.4 |


### 8.2 Pares con |ρ| ≥ 0,7 (candidatos a redundancia)

|                                                                          |   ρ Spearman |
|:-------------------------------------------------------------------------|-------------:|
| population ↔ number_of_households                                        |        0.998 |
| population ↔ purchasing_power_millions_eur                               |        0.967 |
| number_of_households ↔ purchasing_power_millions_eur                     |        0.965 |
| purchasing_power_per_inhabitant_eur ↔ purchasing_power_per_household_eur |        0.956 |
| operating_hours_total ↔ speed_all_counter                                |        0.930 |
| trip_distance_all_counter ↔ speed_all_counter                            |        0.870 |
| speed_average ↔ speed_median                                             |        0.846 |
| trip_distance_all_counter ↔ operating_hours_total                        |        0.799 |
| trip_distance_average ↔ speed_average                                    |        0.733 |


### 9.1 Columnas (letra del documento) y tratamiento aplicado

| letra   | columna                             |   nulos originales | tratamiento aplicado                                                           |
|:--------|:------------------------------------|-------------------:|:-------------------------------------------------------------------------------|
| A       | Unnamed: 0                          |                  0 | Quitar (ruido)                                                                 |
| B       | client_id                           |                  0 | Quitar (ruido) · se conserva solo como clave                                   |
| C       | vehicle_id                          |                  0 | Quitar (ruido) · se conserva solo como clave                                   |
| D       | age_range                           |                  0 | Sin nulos                                                                      |
| E       | gender_derived                      |              33923 | Nulos → 'unknown'                                                              |
| F       | model_series                        |                  0 | Sin nulos                                                                      |
| G       | vehicle_type                        |                922 | Nulos → moda de su model_series                                                |
| H       | model_class                         |               3369 | Quitar (ruido): función exacta de F                                            |
| I       | product_group                       |                  0 | Sin nulos                                                                      |
| J       | engine_concept                      |             134390 | Nulos → cascada validada (nombre, serie, año) → moda de la serie → moda global |
| K       | country_code                        |                  0 | Sin nulos                                                                      |
| L       | fuel_type                           |             178745 | Nulos → derivado de J + nombre comercial                                       |
| M       | date_of_first_registration          |               4182 | PENDIENTE (?): provisional mediana de su serie + flag                          |
| N       | is_current_vehicle                  |                  0 | Nulos → False                                                                  |
| O       | role                                |                  0 | Nulos → OWNER (moda)                                                           |
| P       | role_type                           |                  0 | Nulos → B2C (moda)                                                             |
| Q       | months_as_mb_customer               |                  4 | Nulos → 0.0                                                                    |
| R       | currently_connected_vehicles        |                  0 | Nulos → 1 (moda)                                                               |
| S       | finance_leasing_status              |                  0 | Nulos → never_active                                                           |
| T       | workshop_visits_warranty_goodwill   |                  0 | Nulos → moda                                                                   |
| U       | consent_phone_communication_channel |                  0 | Nulos → False                                                                  |
| V       | consent_epost_communication_channel |                  0 | Nulos → False                                                                  |
| W       | consent_post_communication_channel  |                  0 | Nulos → False                                                                  |
| X       | purchasing_power_per_inhabitant_eur |              19087 | Valor de su CP · respaldo mediana región/país                                  |
| Y       | purchasing_power_per_household_eur  |              19087 | Valor de su CP · si no, recalculado = AM×1e6/AL                                |
| Z       | population                          |              19014 | Valor de su CP · respaldo mediana región/país                                  |
| AA      | zipcode                             |              16135 | Nulos → CP real del país sorteado (ponderado, uno por cliente)                 |
| AB      | trip_distance_average               |             185857 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AC      | trip_distance_mode                  |             179830 | Sin telemetría → '0' · parcial → moda de su serie                              |
| AD      | trip_distance_median                |             179830 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AE      | trip_distance_all_counter           |             179830 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AF      | operating_hours_total               |             174358 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AG      | fuel_consumption_average            |             180725 | Sin telemetría → 0 · parcial → 0 si ELECTRIC, si no mediana de su serie        |
| AH      | speed_average                       |             182382 | Sin telemetría → 0 · parcial → velocidad moda de su serie                      |
| AI      | speed_mode                          |             181159 | Sin telemetría → '0' · parcial → moda de su serie                              |
| AJ      | speed_median                        |             181159 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AK      | speed_all_counter                   |             181159 | Sin telemetría → 0 · parcial → mediana de su serie                             |
| AL      | number_of_households                |              19014 | Valor de su CP · si no, = población / tamaño medio del hogar de la región      |
| AM      | purchasing_power_millions_eur       |              19087 | Valor de su CP · si no, = X × Z / 1e6                                          |


### 9.3 Validación de las reglas de motorización sobre filas con dato conocido

| regla                                                                            |   filas evaluables |   acierto % |
|:---------------------------------------------------------------------------------|-------------------:|------------:|
| Nombre EQ*/electric → ELECTRIC; 'e'/'de'/Hybrid → PLUGIN_HYBRID                  |              37363 |       99.49 |
| Matriculado ≤ 2018 y sin nombre eléctrico → COMBUSTION                           |              35741 |       99.18 |
| Combustible derivado de engine_concept + nombre (PETROL_PLUS cuenta como PETROL) |             124105 |      100.00 |
| Restricción: consumo de combustible medido ⇒ no ELECTRIC                         |              67018 |      100.00 |
| (Referencia) moda global COMBUSTION para cualquier fila                          |             168460 |       58.43 |

- Clientes sin CP: **14,466**. Todos reciben un CP real con datos: **100.0 %** de CP existentes (frente al 31,6 % del sorteo uniforme entre el mínimo y el máximo).


### 9.6 Registro de tratamientos aplicados (en orden)

| letra   | columna                             | tratamiento                                                                  |   valores |
|:--------|:------------------------------------|:-----------------------------------------------------------------------------|----------:|
| AA      | zipcode                             | CP normalizado ('A-'/'CH-' fuera; texto o 5 dígitos → nulo)                  |         5 |
| Z/AL    | —                                   | population = 0 (CP sin residentes) → zona sin datos                          |        73 |
| AB–AK   | —                                   | valores imposibles (vel. < 1, horas = 0, contadores = 0 con métricas) → nulo |     22779 |
| AB      | trip_distance_average               | winsorización p1–p99 de los observados [2.84; 49.39]                         |      2340 |
| AF      | operating_hours_total               | winsorización p1–p99 de los observados [0.10; 3,394.76]                      |      2507 |
| AG      | fuel_consumption_average            | winsorización p1–p99 de los observados [3.59; 19.00]                         |      2436 |
| AH      | speed_average                       | winsorización p1–p99 de los observados [6.17; 80.50]                         |      2387 |
| E       | gender_derived                      | nulo → nueva categoría 'unknown'                                             |     33923 |
| G       | vehicle_type                        | nulo → vehicle_type más frecuente de su model_series                         |       922 |
| J       | engine_concept                      | nulo → vehicle_type con ≥ 90 % de consistencia                               |     63856 |
| J       | engine_concept                      | nulo → nombre comercial (EQ*, e/de, Hybrid)                                  |      8967 |
| J       | engine_concept                      | nulo → model_series con ≥ 90 % de consistencia                               |     21216 |
| J       | engine_concept                      | nulo → matriculado ≤ 2018 → COMBUSTION                                       |     10819 |
| J       | engine_concept                      | nulo → moda de su model_series                                               |     23885 |
| J       | engine_concept                      | nulo → moda global (COMBUSTION)                                              |      5647 |
| L       | fuel_type                           | nulo → derivado de engine_concept + nombre comercial                         |    178745 |
| M       | date_of_first_registration          | PENDIENTE: provisional mediana de su model_series (+ flag)                   |      4182 |
| Q       | months_as_mb_customer               | nulo → 0.0                                                                   |         4 |
| AA      | zipcode                             | nulo → CP real del país sorteado (ponderado, uno por cliente)                |     16137 |
| X       | purchasing_power_per_inhabitant_eur | nulo → valor de su CP                                                        |     16140 |
| Y       | purchasing_power_per_household_eur  | nulo → valor de su CP                                                        |     16140 |
| Z       | population                          | nulo → valor de su CP                                                        |     16140 |
| AL      | number_of_households                | nulo → valor de su CP                                                        |     16140 |
| AM      | purchasing_power_millions_eur       | nulo → valor de su CP                                                        |     16140 |
| X       | purchasing_power_per_inhabitant_eur | CP sin datos → mediana de su región                                          |      2856 |
| X       | purchasing_power_per_inhabitant_eur | CP sin datos → mediana del país                                              |        91 |
| Z       | population                          | CP sin datos → mediana de su región                                          |      2856 |
| Z       | population                          | CP sin datos → mediana del país                                              |        91 |
| AL      | number_of_households                | CP sin datos → población / tamaño medio del hogar de la región               |      2947 |
| AM      | purchasing_power_millions_eur       | CP sin datos → X × Z / 1e6                                                   |      2947 |
| Y       | purchasing_power_per_household_eur  | CP sin datos → AM × 1e6 / AL                                                 |      2947 |
| AB      | trip_distance_average               | sin telemetría → 0                                                           |    158185 |
| AC      | trip_distance_mode                  | sin telemetría → 0                                                           |    158185 |
| AD      | trip_distance_median                | sin telemetría → 0                                                           |    158185 |
| AE      | trip_distance_all_counter           | sin telemetría → 0                                                           |    158185 |
| AF      | operating_hours_total               | sin telemetría → 0                                                           |    158185 |
| AG      | fuel_consumption_average            | sin telemetría → 0                                                           |    158185 |
| AH      | speed_average                       | sin telemetría → 0                                                           |    158185 |
| AI      | speed_mode                          | sin telemetría → 0                                                           |    158185 |
| AJ      | speed_median                        | sin telemetría → 0                                                           |    158185 |
| AK      | speed_all_counter                   | sin telemetría → 0                                                           |    158185 |
| AG      | fuel_consumption_average            | parcial y ELECTRIC → 0                                                       |     12697 |
| AB      | trip_distance_average               | parcial → mediana de su serie                                                |     21232 |
| AB      | trip_distance_average               | parcial → valor global (serie sin datos)                                     |      6440 |
| AC      | trip_distance_mode                  | parcial → moda de su serie                                                   |     21232 |
| AC      | trip_distance_mode                  | parcial → valor global (serie sin datos)                                     |      6440 |
| AD      | trip_distance_median                | parcial → mediana de su serie                                                |     21232 |
| AD      | trip_distance_median                | parcial → valor global (serie sin datos)                                     |      6440 |
| AE      | trip_distance_all_counter           | parcial → mediana de su serie                                                |     21232 |
| AE      | trip_distance_all_counter           | parcial → valor global (serie sin datos)                                     |      6440 |
| AF      | operating_hours_total               | parcial → mediana de su serie                                                |      3676 |
| AF      | operating_hours_total               | parcial → valor global (serie sin datos)                                     |     12637 |
| AG      | fuel_consumption_average            | parcial → mediana de su serie                                                |      9744 |
| AG      | fuel_consumption_average            | parcial → valor global (serie sin datos)                                     |        99 |
| AH      | speed_average                       | parcial → velocidad moda de su serie                                         |     12342 |
| AH      | speed_average                       | parcial → valor global (serie sin datos)                                     |     12744 |
| AI      | speed_mode                          | parcial → moda de su serie                                                   |     11453 |
| AI      | speed_mode                          | parcial → valor global (serie sin datos)                                     |     12744 |
| AJ      | speed_median                        | parcial → mediana de su serie                                                |     11453 |
| AJ      | speed_median                        | parcial → valor global (serie sin datos)                                     |     12744 |
| AK      | speed_all_counter                   | parcial → mediana de su serie                                                |     11453 |
| AK      | speed_all_counter                   | parcial → valor global (serie sin datos)                                     |     12744 |


### 10.1 Comprobaciones de coherencia (objetivo: 0)

|                                                                                           |   incumplimientos |
|:------------------------------------------------------------------------------------------|------------------:|
| Nulos en cualquier columna (celdas)                                                       |                 0 |
| Clientes con atributos de cliente distintos entre sus filas (incl. CP y socio-demografía) |                 0 |
| Vehículos con atributos de vehículo distintos entre sus filas                             |                 0 |
| (país, CP) con más de un valor socio-demográfico                                          |                 0 |
| CP imputados que no existen en el país                                                    |                 0 |
| PA total ≠ PA/hab × población / 1e6 (error > 0,1 %)                                       |                 0 |
| PA/hogar ≠ PA total × 1e6 / hogares (error > 0,1 %)                                       |                 0 |
| Motor y combustible incompatibles                                                         |                 0 |
| Vehículos con nombre eléctrico (EQ…) imputados como no eléctricos                         |                 0 |
| Turismos con nombre de gasolina imputados como DIESEL                                     |                 0 |
| Sin telemetría pero con alguna métrica ≠ 0                                                |                 0 |
| Con telemetría pero con alguna métrica básica = 0                                         |                 0 |
| Con telemetría, no eléctrico y consumo = 0                                                |                 0 |
| Eléctricos con consumo de combustible > 0                                                 |                 0 |
| Modas/medianas que no son un bin válido                                                   |                 0 |


### 10.2 engine_concept: original, moda y tratamiento final

| engine_concept   |   % original (sobre conocidos) |   % con la moda (regla original J) |   % tratamiento final |
|:-----------------|-------------------------------:|-----------------------------------:|----------------------:|
| COMBUSTION       |                           58.4 |                               76.9 |                  61.4 |
| MILD_HYBRID      |                           16.5 |                                9.2 |                  16.5 |
| PLUGIN_HYBRID    |                           12.7 |                                7.0 |                  12.5 |
| ELECTRIC         |                           12.4 |                                6.9 |                   9.6 |


### 10.3 Origen del valor final de engine_concept

| engine_concept_source   |   filas |
|:------------------------|--------:|
| original                |  168460 |
| lookup_vehicle_type     |   63856 |
| moda_serie              |   23885 |
| lookup_model_series     |   21216 |
| regla_antiguedad        |   10819 |
| regla_nombre            |    8967 |
| moda_global             |    5647 |


### 10.4 fuel_type (agrupado): original frente a tratamiento final

| fuel_type   |   % original (sobre conocidos) |   % tratamiento final |
|:------------|-------------------------------:|----------------------:|
| PETROL      |                           37.3 |                  34.6 |
| DIESEL      |                           28.9 |                  43.2 |
| ELECTRIC    |                           16.9 |                   9.6 |
| PHEV        |                           16.9 |                  12.5 |


### 10.5 Medianas antes y después (en telemetría, solo sobre filas con telemetría)

| columna                             |   mediana observada |   mediana final (filas con dato) |   % filas imputadas |
|:------------------------------------|--------------------:|---------------------------------:|--------------------:|
| trip_distance_average               |               14.02 |                            14.02 |               61.37 |
| operating_hours_total               |              407.25 |                           407.25 |               57.62 |
| fuel_consumption_average            |                8.11 |                             7.80 |               59.67 |
| speed_average                       |               49.43 |                            50.00 |               60.52 |
| purchasing_power_per_inhabitant_eur |           46,165.64 |                        45,740.45 |                6.30 |
| population                          |            7,132.00 |                         7,116.00 |                6.30 |


### 10.6 Vista agregada por cliente (data/processed/clientes.csv)

|                                     |      count |   unique |      mean |       std |       min |       25% |       50% |       75% |        max |
|:------------------------------------|-----------:|---------:|----------:|----------:|----------:|----------:|----------:|----------:|-----------:|
| age_range                           | 173,456.00 |     6.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| gender_derived                      | 173,456.00 |     3.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| country_code                        | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| months_as_mb_customer               | 173,456.00 |   nan    |     33.90 |     20.73 |      0.00 |     18.00 |     36.00 |     47.00 |     120.00 |
| months_is_36_spike                  | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| currently_connected_vehicles        | 173,456.00 |   nan    |      1.04 |      0.88 |      0.00 |      1.00 |      1.00 |      1.00 |      21.00 |
| finance_leasing_status              | 173,456.00 |     4.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| consent_phone_communication_channel | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| consent_epost_communication_channel | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| consent_post_communication_channel  | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| purchasing_power_per_inhabitant_eur | 173,456.00 |   nan    | 46,893.74 | 17,276.80 | 19,701.53 | 31,940.06 | 46,636.14 | 54,450.82 | 148,353.74 |
| population                          | 173,456.00 |   nan    | 20,351.39 | 37,662.54 |     25.00 |  3,114.00 |  7,354.00 | 18,605.00 | 220,794.00 |
| socio_imputed                       | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| zip_imputed                         | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| n_relaciones                        | 173,456.00 |   nan    |      1.75 |      5.51 |      1.00 |      1.00 |      1.00 |      2.00 |     561.00 |
| is_b2b                              | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| share_owner                         | 173,456.00 |   nan    |      0.88 |      0.30 |      0.00 |      1.00 |      1.00 |      1.00 |       1.00 |
| visitas_taller_total                | 173,456.00 |   nan    |      3.06 |      4.70 |      0.00 |      0.00 |      2.00 |      4.00 |     206.00 |
| edad_vehiculo_actual_media          | 155,408.00 |   nan    |      4.72 |      3.01 |      0.04 |      2.33 |      4.33 |      6.71 |      39.75 |
| share_electrificado_actual          | 155,408.00 |   nan    |      0.25 |      0.42 |      0.00 |      0.00 |      0.00 |      0.50 |       1.00 |
| has_telemetry                       | 173,456.00 |     2.00 |    nan    |    nan    |    nan    |    nan    |    nan    |    nan    |     nan    |
| trip_distance_average               | 173,456.00 |   nan    |      9.32 |      9.51 |      0.00 |      0.00 |      9.58 |     15.22 |      49.39 |
| operating_hours_total               | 173,456.00 |   nan    |    369.43 |    532.59 |      0.00 |      0.00 |    142.06 |    530.16 |   3,394.76 |
| fuel_consumption_average            | 173,456.00 |   nan    |      4.50 |      4.47 |      0.00 |      0.00 |      5.46 |      8.14 |      19.00 |
| speed_average                       | 173,456.00 |   nan    |     29.32 |     25.71 |      0.00 |      0.00 |     39.39 |     50.45 |      80.50 |
