import sqlite3
import time
import pandas as pd

# Cargar la produccion en una base SQLite y repetir la consulta del indicador
con = sqlite3.connect(":memory:")
pd.read_csv("produccion.csv").to_sql("produccion", con, index=False)

# ANTES: lee todas las columnas y aplica una funcion sobre la fecha (en MySQL seria YEAR(fecha) = 2025)
lenta = """
SELECT *
FROM produccion
WHERE strftime('%Y', fecha) = '2025'
"""
# DESPUES: pide solo lo necesario, filtra con un rango de fechas y deja que el indice trabaje
rapida = """
SELECT planta, SUM(unidades) AS total_unidades
FROM produccion
WHERE fecha >= '2025-01-01' AND fecha < '2026-01-01'
GROUP BY planta
"""
con.execute("CREATE INDEX idx_produccion_fecha ON produccion(fecha)")

# Mismo resultado: total 2025 por planta
total_lenta = pd.read_sql(lenta, con).groupby("planta")["unidades"].sum()
total_rapida = pd.read_sql(rapida, con).set_index("planta")["total_unidades"]
print("Resultado consulta lenta :", total_lenta.to_dict())
print("Resultado consulta rapida:", total_rapida.to_dict())
assert total_lenta.to_dict() == total_rapida.to_dict()

# Plan de ejecucion
for nombre, q in [("LENTA", lenta), ("RAPIDA", rapida)]:
    plan = con.execute("EXPLAIN QUERY PLAN " + q).fetchall()
    print(f"\nPlan {nombre}:", [p[3] for p in plan])

# Filas leidas y columnas devueltas
print("\nColumnas que devuelve la lenta:", len(pd.read_sql(lenta, con).columns),
      "| filas:", len(pd.read_sql(lenta, con)))
print("Columnas que devuelve la rapida:", len(pd.read_sql(rapida, con).columns),
      "| filas:", len(pd.read_sql(rapida, con)))

# Tiempo (se repite 300 veces porque la tabla es chica)
for nombre, q in [("LENTA", lenta), ("RAPIDA", rapida)]:
    ini = time.perf_counter()
    for _ in range(300):
        con.execute(q).fetchall()
    print(f"{nombre}: {(time.perf_counter() - ini) / 300 * 1000:.3f} ms por consulta")
