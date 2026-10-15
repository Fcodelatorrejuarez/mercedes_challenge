# Reto 1: resumen de hallazgos y conclusiones

El análisis completo está en el notebook [`EDA_reto1.ipynb`](../eda/EDA_reto1.ipynb). El dataset tiene 302.850 filas,
**173.456 clientes** y 244.519 vehículos de Suiza y Austria. Cada fila es una relación **cliente–vehículo**, así que
para segmentar hay que agregar por cliente.

## ¿Cuáles son las principales características de los clientes?

- **Particulares:** el 99,4 % son B2C y el 61 % tiene 45 años o más. El 65 % son hombres, el 18 % mujeres y del 17 % no se conoce el género.
- **Mayoría en Suiza** (66 %). El poder adquisitivo de su zona es unas 1,7 veces el de Austria (51 k€ frente a 30 k€ por habitante).
- **Un solo coche conectado** en el 81 % de los casos. El 10 % no tiene ningún vehículo actual (ex-clientes).
- **Relación de unos 3 años con la marca.** El 71 % no ha usado nunca leasing; el leasing es más habitual en Suiza (29 %) y entre los 35 y los 44 años.
- **Fáciles de contactar:** el 81 % acepta teléfono, email y correo postal.
- **SUV y compactos premium** (GLC, C, A, B/GLA/GLB), con un 13 % de AMG y un 14 % de furgonetas. Antigüedad mediana del coche: 4,7 años.
- **Electrificación en plena subida:** los eléctricos pasan del 2,5 % de las matriculaciones de 2019 al 37,5 % de las de 2026.
- **Uso urbano:** trayectos de unos 14 km a unos 49 km/h. A más uso, más visitas al taller.

## ¿Qué problemas de calidad hemos encontrado y cómo los hemos resuelto?

| Problema | Solución |
|---|---|
| Columnas sin valor analítico: índice exportado, IDs y `model_class` (que se deduce de la serie) | Eliminadas. Los IDs se guardan solo como clave para agrupar por cliente |
| Telemetría ausente en el 52 % de las filas (coches no conectados, antiguos o relaciones pasadas) | Sin telemetría → todo a 0 + indicador `has_telemetry`. Telemetría parcial → mediana o moda de su serie |
| Motorización nula en el 44 % y combustible en el 59 % | Reglas basadas en el nombre comercial, la serie y el año, con un 99–100 % de acierto en los datos conocidos. Solo el resto se rellena con la moda |
| Código postal nulo (5 %) o mal escrito, y datos de zona nulos (6 %) | Se asigna un código postal real del país, el mismo para todas las filas del cliente. Los datos de zona se toman de ese código postal o, si no hay, de la región |
| Valores imposibles: velocidad media < 1 km/h, horas a 0, contadores a 0 | Se tratan como nulos. Además, los valores extremos se recortan a los percentiles 1 y 99 |
| Género inferido y desconocido en el 17 % de los clientes | Categoría `unknown` |
| Pico artificial en 36 meses como cliente (12 % de los clientes) | Se conserva el valor y se marca con un indicador |

Tras el tratamiento no queda **ningún nulo** y las 15 comprobaciones de coherencia (por cliente, por vehículo, zona,
motor y combustible, telemetría) dan 0 errores. Queda **pendiente** decidir cómo tratar las fechas de matriculación
nulas (1,4 %); de momento se rellenan con la mediana de su serie.

Los datos tratados están en `data/processed/relaciones_limpio.csv` (una fila por relación) y `data/processed/clientes.csv` (una fila por cliente).
