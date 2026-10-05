# Actividad calificable · Corte 2 — Modelo, consulta y limpieza de datos

**Curso:** Electiva VI — Ciencia de Datos (2026-B)
**Caso:** Tienda de tecnología (celulares, computadores, televisores, accesorios y periféricos) con local físico y plataforma online, enfocada en la gestión de inventario durante eventos de rebajas de noviembre (Black Friday, Cyber Monday).

---

## 1. Modelo de datos (ERD)

Se diseñó un modelo relacional con 4 entidades: **Cliente**, **Producto**, **Venta** y **Detalle_Venta** (tabla intermedia que resuelve la relación muchos a muchos entre Venta y Producto).

```
┌───────────────────────┐              ┌───────────────────────┐
│        CLIENTE         │              │         VENTA           │
├───────────────────────┤              ├───────────────────────┤
│ PK id_cliente           │   1      N │ PK id_venta              │
│    nombre               ├──────────────┤ FK id_cliente           │
│    correo               │              │    fecha                │
│    telefono             │              │    canal                │
│    canal_registro       │              │    total                │
└───────────────────────┘              └───────────────────────┘
                                                    │ 1
                                                    │
                                                    │ N
                                        ┌───────────────────────┐
                                        │    DETALLE_VENTA        │
                                        ├───────────────────────┤
                                        │ FK id_venta              │
                                        │ FK id_producto           │
                                        │    cantidad              │
                                        │    precio_unitario       │
                                        └───────────────────────┘
                                                    │ N
                                                    │
                                                    │ 1
                                        ┌───────────────────────┐
                                        │        PRODUCTO         │
                                        ├───────────────────────┤
                                        │ PK id_producto           │
                                        │    nombre                │
                                        │    categoria             │
                                        │    precio                │
                                        │    stock_disponible      │
                                        └───────────────────────┘
```

**Relaciones:**
- **Cliente — Venta**: 1:N (un cliente puede realizar muchas ventas; cada venta pertenece a un solo cliente).
- **Venta — Producto**: N:M, resuelta mediante la tabla intermedia **Detalle_Venta** (una venta puede incluir varios productos, y un producto puede aparecer en varias ventas).

---

## 2. Carga y limpieza de datos

**Archivo fuente:** [`ventas_sucias.csv`](./ventas_sucias.csv)
**Script:** [`limpieza.py`](./limpieza.py)
**Resultado:** [`ventas_limpio.csv`](./ventas_limpio.csv)

Se construyó un dataset simulado de 20 registros de ventas (basado en las entidades Venta/Detalle_Venta del modelo anterior) con problemas típicos de calidad de datos, y se limpió con **pandas** siguiendo estos pasos:

1. **Conteo de nulos** con `df.isnull().sum()`.
2. **Eliminación de duplicados** exactos con `drop_duplicates()`.
3. **Eliminación de filas** sin `id_cliente` (dato que no se puede inventar) con `dropna(subset=['id_cliente'])`.
4. **Imputación** de `precio_unitario` y `cantidad` faltantes con la mediana de su categoría, usando `fillna()`.
5. **Corrección de tipos**: `fecha` a `datetime` con `pd.to_datetime()`, y columnas numéricas con `pd.to_numeric()`.
6. **Normalización de formatos**: texto limpiado con `.str.strip().str.title()`, y categorías/canales equivalentes unificados (ej. "TV", "tv" y "Television" → "Televisor").

### Reporte antes / después

| Indicador | Antes | Después |
|---|---|---|
| Filas | 20 | 16 |
| Valores nulos (total) | 6 | 0 |
| Filas duplicadas | 2 | 0 |
| Categorías únicas | 11 (mal escritas) | 5 (normalizadas) |
| Canales únicos | 4 (`Online`/`online`/`Tienda`/`tienda`) | 2 (`Online`, `Tienda`) |
| Tipo de dato `fecha` | texto, 3 formatos distintos | `datetime64` uniforme |
| Tipo de dato `precio_unitario` | texto (con `$` y puntos) | `float64` |

---

## 3. Consultas y hallazgos

**Script:** [`consultas.py`](./consultas.py)

### Pregunta 1: ¿Qué categoría de producto genera más ingresos en el canal Online?

```python
ventas_online = df[df["canal"] == "Online"]
ingresos_por_categoria = (
    ventas_online.groupby("categoria")["total"].sum().sort_values(ascending=False)
)
```

**Hallazgo:** la categoría **Celular** es la que más ingresos genera en el canal Online ($6.800.000), seguida de Televisor. Esto confirma que los celulares son el producto más fuerte en las ventas digitales, lo cual es relevante para priorizar su disponibilidad en línea durante los eventos de rebajas.

### Pregunta 2: ¿Qué canal mueve más unidades en compras de 2 o más unidades?

```python
compras_multiples = df[df["cantidad"] >= 2]
unidades_por_canal = (
    compras_multiples.groupby("canal")["cantidad"].sum().sort_values(ascending=False)
)
```

**Hallazgo:** el canal **Online** concentra la mayor cantidad de unidades vendidas en compras múltiples (22 unidades frente a 7 en tienda), lo que sugiere que los clientes compran mayores volúmenes a través de la plataforma digital. Este dato es clave para reforzar el stock disponible del canal online durante Black Friday y Cyber Monday.

---

## 4. Data & cleaning (English)

The dataset contains 20 sales records from the technology store, covering phones, computers, TVs, accessories, and peripherals sold through both the online platform and the physical store. Before cleaning, the data had several quality issues: missing values in `id_cliente`, `cantidad`, and `precio_unitario`, two exact duplicate rows, dates written in three different formats, and inconsistent text in the `categoria` and `canal` columns (for example, "TV", "tv", and "Television" all referring to the same category). Using pandas, duplicates were removed with `drop_duplicates()`, rows missing a customer ID were dropped since that value cannot be reasonably guessed, and the missing price and quantity values were imputed with the median of their category using `fillna()`. Dates were converted to a proper `datetime` type, numeric columns were corrected with `pd.to_numeric()`, and text fields were normalized with `.str.strip()` and `.str.title()`, leaving a clean dataset with 16 rows and zero nulls or duplicates. Two business questions were then answered through filtering and aggregation: the first showed that phones generate the highest revenue in the online channel, and the second showed that the online channel accounts for most of the units sold in multi-item purchases. These findings suggest that inventory planning for sales events should prioritize stock availability for the online channel, especially for phones.

---

## 5. Archivos del repositorio

| Archivo | Descripción |
|---|---|
| `README.md` | Este documento |
| `ventas_sucias.csv` | Dataset original con problemas de calidad |
| `limpieza.py` | Script de limpieza con pandas (antes/después) |
| `ventas_limpio.csv` | Dataset resultante, limpio |
| `consultas.py` | Script con las 2 consultas (filtro + agregación) y hallazgos |
