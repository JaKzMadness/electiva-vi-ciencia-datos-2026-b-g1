import numpy as np
import pandas as pd

# Datos simulados: ventas de "Repuestos del Sur", una tienda de repuestos con 3 sucursales (2024 y 2025)
rng = np.random.default_rng(15)
fechas = pd.date_range("2024-01-01", "2025-12-31", freq="D")
sucursales = ["Neiva", "Pitalito", "Garzón"]
categorias = ["Frenos", "Filtros", "Aceites", "Baterías"]
pesos_categoria = [0.35, 0.25, 0.25, 0.15]

filas = []
for i, dia in enumerate(fechas):
    mes = dia.month
    # estacionalidad: sube en junio y diciembre, baja en enero y febrero
    factor_mes = {12: 1.35, 6: 1.15, 1: 0.85, 2: 0.9}.get(mes, 1.0)
    factor_dia = 0.7 if dia.dayofweek == 6 else 1.0          # domingo se vende menos
    tendencia = 1 + 0.0006 * i                                 # crece poco a poco
    n_ventas = max(1, int(rng.poisson(8 * factor_mes * factor_dia * tendencia)))
    for _ in range(n_ventas):
        filas.append({
            "fecha": dia,
            "sucursal": rng.choice(sucursales, p=[0.34, 0.33, 0.33]),
            "categoria": rng.choice(categorias, p=pesos_categoria),
            "total": int(rng.normal(120, 25) * 1000)           # pesos
        })

detalle = pd.DataFrame(filas)
detalle.insert(0, "id_venta", range(1, len(detalle) + 1))
detalle.to_csv("ventas_detalle.csv", index=False)

# Serie diaria: total vendido por dia (miles de pesos)
serie = detalle.groupby("fecha")["total"].sum().div(1000).round(0).rename("ventas").reset_index()
serie.to_csv("serie_ventas.csv", index=False)
print(detalle.shape, serie.shape)
