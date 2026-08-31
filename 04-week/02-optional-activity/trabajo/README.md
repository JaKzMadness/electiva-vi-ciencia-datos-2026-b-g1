# Ciencia de Datos – Corte 1
## Diagnóstico de datos de un proceso — Actividad Calificable

## Solución

**Problema real:** Productos electrónicos que, durante el control de calidad (encendido, respuesta de componentes y conexiones), presentan fallas que impiden su correcto funcionamiento.

**Pregunta de datos planteada:** ¿Qué aspectos del proceso de producción son más propensos a generar productos defectuosos?

## Inventario de datos

| Dato | Fuente | Tipo de dato |
|---|---|---|
| Resultados del control de calidad y tipo de falla | Sistemas de pruebas eléctricas y de función | Estructurado |
| Estaciones de trabajo donde se procesaron los productos | Sistema MES [software utilizado para monitorear y controlar procesos de fabricación (IBM, 2023)] | Estructurado |
| Parámetros de fabricación utilizados en las estaciones de trabajo | PLC de la maquinaria utilizada [El PLC es un controlador lógico programable el cual ejecuta un ciclo continuo de lectura de sensores, procesamiento y escritura de salidas cada 1 a 20 milisegundos (Autevo, 2026)] | Estructurado |
| Lote y proveedor de los componentes electrónicos implementados | Base de datos de inventario mediante un ERP (sistema de planeación de recursos empresariales) | Estructurado |
| Identificación del operario a cargo de cada estación de ensamblaje | Registro de turnos / control de personal | Estructurado |
| Reporte de incidencias que ocurrieron durante el proceso de producción | Reporte de planta | No estructurado |
| Especificaciones técnicas de diseño de cada producto | Documentación técnica | Semiestructurado |

## Tipos de analítica a utilizar y comprobación de "V" del Big Data

Este caso se apoya principalmente en analítica descriptiva y diagnóstica, con potencial de evolucionar hacia analítica predictiva y prescriptiva conforme se disponga de más datos históricos:

- **Analítica descriptiva (aplicada):** inicialmente se analiza la cantidad de unidades que mostraron alguna falla durante los procesos de control de calidad y se define en qué estaciones de trabajo se concentran la mayor parte de las fallas.

- **Analítica diagnóstica (aplicada):** unir y comparar los datos recopilados durante las pruebas de calidad con las variables de producción para encontrar la combinación de datos que provoca mayores fallas durante su producción.

- **Analítica predictiva (proyección futura):** con suficiente historial acumulado, se podría predecir la probabilidad de que cada unidad producida falle antes de que llegue a los procesos de control de calidad, de acuerdo con los parámetros utilizados durante su producción.

- **Analítica prescriptiva (proyección futura):** más adelante se podrían proponer ajustes automáticos y concretos para minimizar las probabilidades de que ocurran estos defectos de fábrica.

Por otro lado, esta problemática entra dentro de un caso de Big Data (Badman & Kosinski, 2024) al estar presentes las siguientes "V":

- **Volumen:** cada unidad producida pasa por varios sistemas los cuales generan registros de datos a lo largo de la jornada de trabajo, provocando que sea difícil seguirle el ritmo mediante herramientas como una hoja de cálculo.

- **Velocidad:** el PLC de la maquinaria que se utiliza durante el proceso de fabricación ejecuta múltiples lecturas en poco tiempo, generando datos en tiempo real durante todo el tiempo de uso.

- **Variedad:** en este caso, se utilizan los tres tipos de datos (estructurado, semiestructurado y no estructurado) dentro del inventario de datos.

- **Veracidad:** para este elemento se presentan dos posibles riesgos donde se pueden generar los suficientes errores para que se ejecute erróneamente una decisión, siendo que los sensores de los PLC se encuentren mal calibrados y que operarios reporten o no adecuadamente los incidentes que puedan ocurrir dentro de la jornada laboral.

- **Valor:** lograr identificar las fallas que ocurren durante el proceso de fabricación permite reducir reprocesos y desperdicios de componentes electrónicos.

## Esquema del ciclo de vida del proyecto

```
1. PREGUNTA
   ¿Qué aspectos del proceso de producción son más propensos
   a generar productos defectuosos?
        |
        v
2. OBTENER
   Extraer datos del sistema de pruebas, MES, PLC, ERP,
   registro de turnos y reportes de operarios.
        |
        v
3. LIMPIAR / PREPARAR
   Filtrar registros incompletos, corregir formatos y unir
   las fuentes por número de unidad o lote.
        |
        v
4. ANALIZAR / EXPLORAR
   Cruzar el resultado de la prueba de calidad con las
   variables de producción para encontrar patrones y causas.
        |
        v
5. VISUALIZAR
   Gráficos y dashboard de tasa de defectos por estación,
   operario y lote.
        |
        v
6. DECIDIR / ACTUAR
   Ajustar parámetros críticos de producción, reforzar
   capacitación o mantenimiento donde corresponda.
```

## Problem & data

Electronic products sometimes fail during quality control testing (power-on, component response, and connections), preventing them from working correctly. This problem makes it difficult to identify which stage of the production process is generating these failures. To address this, the project asks: which aspects of the production process are more likely to generate defective products? The data needed includes quality test results, the assembly station where each unit was processed, the soldering and connection parameters used, the component batch and supplier, the operator in charge, incident reports from the production floor, and the technical specification sheets for each product. This project relies mainly on descriptive and diagnostic analytics to quantify defect rates and identify their root causes, with the potential to evolve into predictive and prescriptive analytics as more historical data becomes available.

## Referencias bibliográficas

IBM. (2023, 23 de mayo). *¿Qué es un sistema de ejecución de fabricación (MES)?* IBM Think. https://www.ibm.com/mx-es/think/topics/mes-system

Badman, A., & Kosinski, M. (2024, 18 de noviembre). *What is big data?* IBM Think. https://www.ibm.com/think/topics/big-data

Autevo. (2026, 28 de agosto). *¿Qué es un PLC y cómo funciona en la automatización industrial?* Autevo Colombia. https://autevoco.com/que-es-un-plc-y-como-funciona-en-la-automatizacion-industrial/