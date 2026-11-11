import sqlite3
import time
import pandas as pd

# Cargar las ventas en una base SQLite (tabla "ventas")
con = sqlite3.connect(":memory:")
pd.read_csv("ventas_detalle.csv").to_sql("ventas", con, index=False)

# ANTES (lenta): trae todas las columnas y aplica una funcion sobre la fecha.
# En MySQL se escribiria  WHERE YEAR(fecha) = 2025 ; en SQLite es strftime.
lenta = """
SELECT *
FROM ventas
WHERE strftime('%Y', fecha) = '2025'
"""

# DESPUES (rapida): solo las columnas necesarias, filtro por rango de fechas y un indice sobre fecha
rapida = """
SELECT id_venta, sucursal, total
FROM ventas
WHERE fecha >= '2025-01-01' AND fecha < '2026-01-01'
"""

# Misma respuesta: mismas filas y mismo total vendido
a = pd.read_sql(lenta, con)
print("Lenta : filas", len(a), "| columnas", len(a.columns), "| total", int(a["total"].sum()))

con.execute("CREATE INDEX idx_ventas_fecha ON ventas(fecha)")
b = pd.read_sql(rapida, con)
print("Rapida: filas", len(b), "| columnas", len(b.columns), "| total", int(b["total"].sum()))
assert len(a) == len(b) and int(a["total"].sum()) == int(b["total"].sum())

# Plan de ejecucion de cada consulta
for nombre, q in [("LENTA", lenta), ("RAPIDA", rapida)]:
    plan = con.execute("EXPLAIN QUERY PLAN " + q).fetchall()
    print(f"Plan {nombre}:", [p[3] for p in plan])

# Tiempo (se repite 200 veces porque la tabla es chica)
for nombre, q in [("LENTA", lenta), ("RAPIDA", rapida)]:
    ini = time.perf_counter()
    for _ in range(200):
        con.execute(q).fetchall()
    print(f"{nombre}: {(time.perf_counter() - ini) / 200 * 1000:.3f} ms por consulta")
