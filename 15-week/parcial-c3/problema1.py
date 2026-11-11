import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Cargar con la fecha como fecha y dejarla como indice
df = pd.read_csv("serie_ventas.csv", parse_dates=["fecha"])
df = df.set_index("fecha")
print(df.head(3))
print("Filas:", len(df), "| Nulos:", int(df["ventas"].isnull().sum()))

# 2. Agregar por mes (en pandas 3 el codigo "M" ya no existe: se usa "MS", mes con fecha al inicio)
mensual = df["ventas"].resample("MS").sum()

# 3. Medias moviles: 7 dias sobre la serie diaria y 3 meses sobre la mensual
df["movil7"] = df["ventas"].rolling(7).mean()
movil3m = mensual.rolling(3).mean()

print("\nVentas mensuales (miles de pesos), primeros 6 meses:")
print(mensual.head(6))

# 4. Tendencia: comparar los dos anios
por_anio = mensual.groupby(mensual.index.year).sum()
print("\nTotal por anio:\n", por_anio)
print(f"Cambio 2025 vs 2024: {(por_anio[2025] / por_anio[2024] - 1) * 100:.1f}%")
print(f"Media movil 3 meses: primer dato {movil3m.dropna().iloc[0]:,.0f} -> ultimo {movil3m.iloc[-1]:,.0f}")

# 5. Estacionalidad: promedio por mes del calendario contra el promedio general
por_mes = mensual.groupby(mensual.index.month).mean()
desv = (por_mes / por_mes.mean() - 1) * 100
print("\nDesviacion de cada mes frente al promedio general (%):")
print(desv.round(1))

# 6. Grafico
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(mensual.index, mensual.values / 1000, marker="o", color="#9aa5b1", label="Ventas mensuales")
ax.plot(movil3m.index, movil3m.values / 1000, color="#c0392b", linewidth=2.5, label="Media móvil de 3 meses")
ax.set_ylim(0, None)
ax.set_title("Las ventas crecen cada año y se disparan en diciembre")
ax.set_xlabel("Mes")
ax.set_ylabel("Ventas (millones de pesos)")
ax.legend(loc="lower right")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("p1_serie_mensual.png", dpi=150)
