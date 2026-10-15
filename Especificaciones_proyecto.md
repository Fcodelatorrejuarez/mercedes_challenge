# III Malackathon 2026

## Mercedes-Benz Group Services Madrid

# Clustering the Star

¿Te interesa la ciencia de datos aplicada al mundo real del automóvil?

Te invitamos a participar en el III Malackathon, en el reto de la empresa Mercedes-Benz, reto diseñado para aplicar tus habilidades en un problema real de la industria.

En esta edición, proponemos segmentar la base de clientes de Mercedes-Benz mediante técnicas de aprendizaje no supervisado (clustering), con el objetivo de habilitar estrategias de marketing personalizadas:

- Ofertas de vehículos
- Planes de mantenimiento
- Campañas de fidelización
- Comunicaciones dirigidas

Trabajaremos con un dataset de datos reales de clientes proporcionado por Mercedes-Benz. El reto básico consiste en explorar los datos, preparar las features adecuadas e implementar un modelo de clustering K-Means que segmente a los clientes en grupos homogéneos, interpretando cada segmento con sentido de negocio. El resto de herramientas, lenguajes de programación y librerías de visualización es de libre elección, aunque se recomienda realizarlo con Python (pandas y scikit-learn) o R.

## ¿Qué aprenderás participando?

- **Procesamiento de datos a escala:** preparación, limpieza y transformación real.
- **Ingeniería de características:** cómo seleccionar, crear y codificar variables relevantes para un modelo de machine learning no supervisado.
- **Segmentación de clientes:** diseño, implementación y evaluación de modelos de clustering.
- **Pensamiento analítico de negocio:** cómo traducir resultados técnicos en perfiles de cliente e insights accionables para un equipo.
- **Visualización avanzada:** diseño de gráficos y dashboards que comunican los segmentos de forma clara y atractiva.

El Malackathon tiene dos tipos de retos: retos básicos y retos avanzados. Estos últimos son los que darán acceso a la final del viernes. Cada uno de estos retos avanzados será evaluado por los mentores de los patrocinadores de cada premio. Para poder ser evaluado en alguno de los retos avanzados, debes haber cubierto completamente todos los retos básicos.

# Retos básicos

## 1. Reto de exploración y calidad de datos

Deberás acceder a los datos de cliente. Esta tabla integra información de múltiples dimensiones: perfil demográfico del cliente, características del vehículo, relación con la marca, consentimientos de comunicación y poder adquisitivo por zona geográfica.

Se pide realizar un análisis exploratorio de datos (EDA) completo que incluya:

- Estadísticas descriptivas de variables principales.
- Análisis de valores nulos e inconsistencias, con una propuesta de tratamiento justificada.
- Distribuciones de variables clave.
- Identificación y exclusión justificada de columnas de metadatos e identificadores que no aportan valor analítico.

**Para evaluar el reto se debe proporcionar:**

- Notebook con el EDA ejecutado y documentado.
- Breve resumen de hallazgos y conclusiones:
  - ¿Cuáles son las principales características de los clientes?
  - ¿Qué problemas de calidad habéis encontrado y cómo habéis resuelto?

## 2. Reto de feature engineering

El grupo deberá seleccionar y preparar las variables que alimentarán el modelo de clustering. No se trata de usar todas las columnas a ciegas, sino de pensar como un analista de negocio. ¿Qué información es realmente útil para segmentar clientes?

Se pide:

- Selección justificada de features a incluir.
- Creación de al menos una feature derivada. Como sugerencia:
  - Antigüedad del vehículo a partir de la fecha de registro.
- Tratamiento adecuado de variables categóricas: codificación adecuada.
- Tratamiento adecuado de variables numéricas: imputación de nulos o eliminación y escalado de las variables.
- Construcción de un pipeline que encapsule todo el proceso de transformación.

**Para evaluar el reto se debe proporcionar:**

- Notebook con el pipeline de preparación ejecutado y documentado.
- Listado de features seleccionadas con justificación breve de cada una.
- Descripción de las features derivadas creadas.

## 3. Reto: modelo de clustering (K-Means)

El grupo deberá implementar un modelo de clustering K-Means sobre los datos preparados en el reto anterior.

Se pide:

- Ejecución de K-Means para un rango de valores de *k* (hace referencia al número de clústeres seleccionados).
- Cálculo del método del codo para seleccionar el *k* óptimo.
- Cálculo del Silhouette Score para cada valor de *k*.
- Entrenamiento del modelo final con el *k* elegido.
- Distribución de clientes por clúster.

**Para evaluar el reto se debe proporcionar:**

- Notebook con el modelo ejecutado, gráficos generados de codo y silhouette junto con su documentación.
- Selección y justificación del número óptimo de clústeres.

## 4. Interpretación de los segmentos

El grupo deberá describir los clústeres obtenidos en lenguaje de negocio, no solo en términos técnicos. Cada segmento debe tener un perfil claro que un equipo de marketing pueda entender y utilizar.

Se pide:

- Perfil del cliente de cada clúster.
- Nombre descriptivo para cada segmento. Por ejemplo, “Premium Tradicional”, “Joven Digital”...

**Para evaluar el reto se debe proporcionar:**

- Notebook con las tablas y gráficos de perfilado por clúster.

# Retos avanzados

## 1. Comparativa de algoritmos de clustering

Comparad los resultados de K-Means con al menos otro algoritmo de clustering que esté disponible (DBSCAN, Gaussian Mixture Models, Agglomerative Clustering...).

Se pide:

- Entrenar el/los algoritmo(s) alternativos con el mismo *k* y los mismos datos preparados.
- Comparar los Silhouette Scores de todos los algoritmos.
- Analizar si los segmentos cambian significativamente entre algoritmos.
- Gráfico comparativo de rendimiento.

**Para evaluar el reto se debe proporcionar:**

- Notebook con la comparativa ejecutada.
- Tabla y gráfico comparativo de métricas.
- Conclusión razonada sobre el algoritmo más adecuado.

## 2. Reducción de dimensionalidad y visualización

Aplicad técnicas de reducción de dimensionalidad (PCA) para visualizar los clústeres en un espacio 2D o 3D.

Se pide:

- Aplicar PCA sobre las features.
- Indicar la varianza explicada por cada componente principal y la acumulada.
- Gráfico scatter 2D (y opcionalmente 3D) coloreado por clúster.
- Análisis de qué variables originales pesan más en cada componente principal.

**Para evaluar el reto se debe proporcionar:**

- Notebook con PCA ejecutado y gráficos generados.
- Interpretación de las componentes principales.
- Valoración: ¿los clústeres son visualmente separables?

## 3. Estabilidad de clústeres: Jackknife Clustering

Un modelo de clustering puede ofrecer buenos valores de Silhouette y sin embargo producir segmentos inestables: pequeñas variaciones en los datos de entrada provocan que los clústeres cambien drásticamente.

Para validar que la segmentación de clientes es robusta y fiable antes de basar decisiones de marketing en ella, se pide aplicar la técnica de Jackknife Clustering.

La idea es la siguiente: si eliminamos un subconjunto aleatorio de clientes y re-entrenamos el modelo, ¿se mantienen los mismos segmentos? Si los clústeres son estables, las asignaciones deberían ser consistentes independientemente de qué clientes se excluyan.

Se pide:

- Implementar Jackknife Clustering: generar N submuestras del dataset (por ejemplo, 20), cada una excluyendo un porcentaje de los datos (por ejemplo, 10-20%). Entrenar el K-Means con el mismo *k* óptimo sobre cada submuestra.
- Medir la estabilidad de las asignaciones: para los clientes presentes en múltiples submuestras, comparar sus asignaciones de clúster entre ejecuciones. Utilizar métricas como el porcentaje de coincidencia de asignación.
- Análisis por clúster: ¿hay algún segmento que sea especialmente inestable? ¿Algún grupo de clientes que “salta” entre clústeres en distintas ejecuciones?

**Para evaluar el reto se debe proporcionar:**

- Notebook con la implementación anterior.
- Gráficos que muestren las conclusiones anteriores.
- Análisis de los clústeres más/menos estables y por qué.
- Recomendación final.

# Diccionario de datos

| Columna | Descripción | Tipo de dato | Ejemplo |
|---|---|---|---|
| `client_id` | Identificador del cliente | string | `12345` |
| `vehicle_id` | Identificador de vehículo | string | `12345` |
| `age_range` | Rango de edad | string | `20-30` |
| `gender_derived` | Género del cliente derivado (inferido) a partir de otra información del cliente; no es un dato declarado directamente. | string | `female` |
| `model_series` | Número de la serie del modelo del vehículo. | string | `205` |
| `vehicle_type` | Denominación comercial específica del tipo o acabado del vehículo (C 200, GLE 450 4MATIC). | string | `C 200 d` |
| `model_class` | Clase o categoría del vehículo (p. ej., Clase A – Clase S, Clase GLE/GLS). | string | `C-Class` |
| `product_group` | Grupo de producto para identificar si es un Passenger car (P), Vans (V), etc. | string | `P` |
| `engine_concept` | Concepto de motorización del vehículo (p. ej., combustión, híbrido o eléctrico). | string | `ICE` |
| `country_code` | Código de país ISO. En los datos de cliente, país de mercado del cliente; en la relación cliente-vehículo, país en el que se establece la conexión con el vehículo; en los datos sociodemográficos, país al que corresponde el código postal. | string | `DE` |
| `fuel_type` | Tipo de combustible del vehículo (p. ej., diésel, gasolina, eléctrico). | string | `Diesel` |
| `date_of_first_registration` | Día del primer registro de matriculación del vehículo en cuestión. | date | `2021-02-01` |
| `is_current_vehicle` | Indicador que señala si la relación con este vehículo está actualmente activa. | boolean | `false` |
| `role` | Rol del cliente en relación con el vehículo (p. ej., Driver, Owner). | string | `Owner` |
| `role_type` | Clasificación de la relación con el vehículo, si forma parte de una empresa (B2B: flota/empresa) o consumidor (B2C: particular). | string | `B2C` |
| `months_as_mb_customer` | Meses desde que inició su relación con la marca (meses desde su primera conexión a un coche). | integer | `76` |
| `currently_connected_vehicles` | Número de vehículos actualmente vinculados al cliente. | integer | `1` |
| `finance_leasing_status` | Situación del cliente en relación con operaciones de financiación mediante leasing financiero (FL) y compras al contado (Cash). | string | `was_active` |
| `workshop_visits_warranty_goodwill` | Número de visitas al taller durante el periodo de garantía. | int | `3` |
| `consent_phone_communication_channel` | Indica si el cliente ha dado su consentimiento para ser contactado por teléfono con fines de comunicación comercial. | boolean | `true` |
| `consent_epost_communication_channel` | Indica si el cliente ha dado su consentimiento para ser contactado por canal electrónico (ePost / correo electrónico) con fines de comunicación comercial. | boolean | `true` |
| `consent_post_communication_channel` | Indica si el cliente ha dado su consentimiento para ser contactado por correo postal con fines de comunicación comercial. | boolean | `false` |
| `purchasing_power_per_inhabitant_eur` | Poder adquisitivo medio estimado por habitante del código postal, expresado en euros. | double | `7425.96` |
| `purchasing_power_per_household_eur` | Poder adquisitivo medio estimado por hogar del código postal, expresado en euros. | double | `20601.05` |
| `population` | Población total de la zona geográfica correspondiente al código postal. | integer | `688` |
| `zipcode` | Código postal asociado al cliente / correspondiente a la zona geográfica de los datos sociodemográficos. | string | `81925` |
| `trip_distance_average` | Distancia media recorrida por trayecto (km). | double | — |
| `trip_distance_mode` | Distancia recorrida por trayecto que aparece con mayor frecuencia (moda). | string | — |
| `trip_distance_median` | Distancia mediana recorrida por trayecto. | double | — |
| `trip_distance_all_counter` | Número total de trayectos utilizados para calcular las métricas de distancia. | double | — |
| `operating_hours_total` | Número total de horas de funcionamiento del vehículo. | double | — |
| `fuel_consumption_average` | Consumo medio de combustible del vehículo. | double | — |
| `speed_average` | Velocidad media del vehículo. | double | — |
| `speed_mode` | Velocidad que aparece con mayor frecuencia (moda). | string | — |
| `speed_median` | Velocidad mediana. | double | — |
| `speed_all_counter` | Número total de mediciones utilizadas para calcular las métricas de velocidad. | double | — |
| `number_of_households` | Número total de hogares de la zona geográfica correspondiente al código postal. | integer | `248` |
| `purchasing_power_millions_eur` | Poder adquisitivo total estimado de la población correspondiente al código postal, expresado en millones de euros. | double | `5.109` |

# Información del premio

- **Nombre del premio:** AirPods.
- **Los equipos serán de:** 4.
- **Empresa:** Mercedes-Benz Group Services Madrid.
- **Premio:** Premio a los ganadores del grupo con unos AirPods.
- **Título:** Premiar a los alumnos que mejor interpreten el problema de clustering y mejor perfilen al tipo de cliente de Mercedes-Benz con sentido de negocio y utilidad comercial.

[https://u.uma.es/ita/](https://u.uma.es/ita/)
