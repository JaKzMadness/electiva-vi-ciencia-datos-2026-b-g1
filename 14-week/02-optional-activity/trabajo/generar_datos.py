import numpy as np
import pandas as pd

# Datos simulados: produccion diaria de dos plantas (2024 y 2025)
rng = np.random.default_rng(14)
fechas = pd.date_range("2024-01-01", "2025-12-31", freq="D")
filas = []
for planta, base in [("Norte", 520), ("Sur", 430)]:
    t = np.arange(len(fechas))
    tendencia = base + 0.12 * t                       # sube poco a poco
    mes = fechas.month.to_numpy()
    estacion = np.select([np.isin(mes, [11, 12]), mes == 1, np.isin(mes, [6, 7])],
                         [1.18, 0.85, 0.95], default=1.0)   # pico nov-dic, bajon en enero
    fin_semana = np.where(fechas.dayofweek >= 5, 0.55, 1.0)  # sabado y domingo producen menos
    ruido = rng.normal(0, 18, len(fechas))
    unidades = (tendencia * estacion * fin_semana + ruido).round().astype(int)
    filas.append(pd.DataFrame({"fecha": fechas, "planta": planta, "unidades": unidades}))
df = pd.concat(filas).sort_values(["fecha", "planta"])
df.to_csv("produccion.csv", index=False)
print(df.shape)
