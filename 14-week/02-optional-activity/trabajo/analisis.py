import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Cargar la serie temporal
df = pd.read_csv("produccion.csv", parse_dates=["fecha"])
print("Filas:", len(df), "| Nulos:", int(df.isnull().sum().sum()))

# 2. Total diario de las dos plantas
diario = df.groupby("fecha")["unidades"].sum()

# 3. Agregar por mes (resample) y media movil
mensual = diario.resample("MS").sum()
media_movil_3m = mensual.rolling(3).mean()
media_movil_7d = diario.rolling(7).mean()
print("\nProduccion mensual (primeros 6 meses):")
print(mensual.head(6))

# 4. Tendencia: comparar 2025 contra 2024
por_anio = mensual.groupby(mensual.index.year).sum()
print("\nTotal por anio:\n", por_anio)
print(f"Cambio 2025 vs 2024: {(por_anio[2025] / por_anio[2024] - 1) * 100:.1f}%")

# 5. Estacionalidad: promedio por mes del calendario
por_mes = mensual.groupby(mensual.index.month).mean().round(0)
print("\nPromedio por mes del calendario:\n", por_mes)
print(f"Nov-Dic vs promedio general: {por_mes[[11, 12]].mean() / por_mes.mean() * 100 - 100:.1f}%")
print(f"Enero vs promedio general: {por_mes[1] / por_mes.mean() * 100 - 100:.1f}%")

# 6. Efecto fin de semana
entre = diario[diario.index.dayofweek < 5].mean()
fin = diario[diario.index.dayofweek >= 5].mean()
print(f"\nPromedio diario entre semana: {entre:.0f} | fin de semana: {fin:.0f}")

# 7. Grafico 1: evolucion
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(mensual.index, mensual.values / 1000, marker="o", color="#9aa5b1", label="Producción mensual")
ax.plot(media_movil_3m.index, media_movil_3m.values / 1000, color="#c0392b", linewidth=2.5,
        label="Media móvil de 3 meses")
ax.set_ylim(0, None)
ax.set_title("La producción crece cada año y se dispara en noviembre y diciembre")
ax.set_xlabel("Mes")
ax.set_ylabel("Unidades producidas (miles)")
ax.legend(loc="lower right")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("grafico_evolucion.png", dpi=150)

# 8. Grafico 2: comparacion de plantas por anio
tot = df.assign(anio=df["fecha"].dt.year).groupby(["anio", "planta"])["unidades"].sum().unstack() / 1000
print("\nTotal por planta y anio (miles):\n", tot.round(1))
fig, ax = plt.subplots(figsize=(7, 4.5))
tot.plot(kind="bar", ax=ax, color=["#2c3e50", "#e67e22"], rot=0)
for c in ax.containers:
    ax.bar_label(c, fmt="%.0f", padding=2)
ax.set_ylim(0, 225)
ax.set_title("La planta Norte produce entre 18% y 21% más que la Sur cada año")
ax.set_xlabel("Año")
ax.set_ylabel("Unidades producidas (miles)")
ax.legend(title="Planta", loc="upper left", ncol=2)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("grafico_comparacion.png", dpi=150)
print("\nGraficos guardados.")
