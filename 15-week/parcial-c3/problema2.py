import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

det = pd.read_csv("ventas_detalle.csv", parse_dates=["fecha"])
det["anio"] = det["fecha"].dt.year
d25 = det[det["anio"] == 2025]

# ---------- Parte A: un grafico para cada tipo de pregunta ----------
mensual = d25.set_index("fecha")["total"].resample("MS").sum() / 1e6
por_sucursal = d25.groupby("sucursal")["total"].sum().sort_values(ascending=False) / 1e6
por_categoria = d25.groupby("categoria")["total"].sum().sort_values(ascending=False) / 1e6
print("Por sucursal (millones):\n", por_sucursal.round(1))
print("Por categoria (millones):\n", por_categoria.round(1))
print("Participacion por categoria (%):\n", (por_categoria / por_categoria.sum() * 100).round(1))

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
# Evolucion -> lineas
meses_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
ax[0].plot(meses_es, mensual.values, marker="o", color="#2c3e50")
ax[0].set_ylim(0, None)
ax[0].set_title("Evolución: las ventas de 2025\nsuben en junio y diciembre")
ax[0].set_xlabel("Mes"); ax[0].set_ylabel("Ventas (millones de pesos)")
ax[0].tick_params(axis="x", labelsize=8)
# Comparacion -> barras
barras = ax[1].bar(por_sucursal.index, por_sucursal.values, color="#2c3e50")
ax[1].bar_label(barras, fmt="%.0f", padding=2)
ax[1].set_ylim(0, por_sucursal.max() * 1.15)
ax[1].set_title("Comparación: las tres sucursales\nvenden casi lo mismo")
ax[1].set_xlabel("Sucursal"); ax[1].set_ylabel("Ventas 2025 (millones de pesos)")
# Proporcion -> torta (solo 4 categorias)
ax[2].pie(por_categoria.values, labels=por_categoria.index, autopct="%1.0f%%", startangle=90,
          colors=["#2c3e50", "#e67e22", "#7f8c8d", "#c0392b"])
ax[2].set_title("Proporción: Frenos aporta\nuna de cada tres ventas")
fig.tight_layout()
fig.savefig("p2_tres_preguntas.png", dpi=150)

# ---------- Parte B1: error de eje truncado ----------
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), sharey=False)
vals = por_sucursal
ax[0].bar(vals.index, vals.values, color="#c0392b")
ax[0].set_ylim(vals.min() * 0.97, vals.max() * 1.01)
ax[0].set_title("ANTES: eje Y truncado\n(Neiva parece vender mucho más que Pitalito)")
ax[0].set_ylabel("Ventas 2025 (millones de pesos)")
ax[1].bar(vals.index, vals.values, color="#2c3e50")
ax[1].bar_label(ax[1].containers[0], fmt="%.0f", padding=2)
ax[1].set_ylim(0, vals.max() * 1.15)
ax[1].set_title("DESPUÉS: eje Y desde 0\n(la diferencia real es de solo 7%)")
ax[1].set_ylabel("Ventas 2025 (millones de pesos)")
fig.tight_layout()
fig.savefig("p2_error_eje.png", dpi=150)
dif = (vals.max() / vals.min() - 1) * 100
print(f"Diferencia real entre la mayor y la menor sucursal: {dif:.1f}%")

# ---------- Parte B2: error de torta saturada ----------
mes25 = d25.groupby(d25["fecha"].dt.month)["total"].sum() / 1e6
nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
ax[0].pie(mes25.values, labels=nombres, autopct="%1.0f%%", startangle=90, textprops={"fontsize": 7})
ax[0].set_title("ANTES: torta con 12 porciones\n(casi no se pueden comparar)")
ordenado = pd.Series(mes25.values, index=nombres)
b = ax[1].bar(nombres, ordenado.values, color="#2c3e50")
ax[1].set_ylim(0, ordenado.max() * 1.15)
ax[1].set_title("DESPUÉS: barras\n(diciembre es el mes más fuerte)")
ax[1].set_xlabel("Mes"); ax[1].set_ylabel("Ventas 2025 (millones de pesos)")
ax[1].tick_params(axis="x", labelsize=8)
fig.tight_layout()
fig.savefig("p2_error_torta.png", dpi=150)
print("Mes mas fuerte:", nombres[int(mes25.values.argmax())], round(mes25.max(), 1))
