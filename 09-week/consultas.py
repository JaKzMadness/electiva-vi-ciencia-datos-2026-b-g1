import pandas as pd

df = pd.read_csv("ventas_limpio.csv", parse_dates=["fecha"])

# ===========================================================
# Consulta 1: ¿Qué categoría de producto generó más ingresos
# durante las ventas en línea (Online)?
# Filtro: canal == 'Online'
# Agregación: suma de 'total' agrupada por categoria
# ===========================================================
print("=" * 60)
print("CONSULTA 1: Ingresos por categoría en el canal Online")
print("=" * 60)

ventas_online = df[df["canal"] == "Online"]
ingresos_por_categoria = (
    ventas_online.groupby("categoria")["total"]
    .sum()
    .sort_values(ascending=False)
)
print(ingresos_por_categoria)

categoria_top = ingresos_por_categoria.idxmax()
monto_top = ingresos_por_categoria.max()
print(f"\nHallazgo: la categoría '{categoria_top}' es la que más ingresos "
      f"genera en el canal Online, con ${monto_top:,.0f}.")

# ===========================================================
# Consulta 2: ¿Qué canal mueve más unidades en ventas con
# cantidad igual o mayor a 2 (compras de más de una unidad)?
# Filtro: cantidad >= 2
# Agregación: suma de 'cantidad' agrupada por canal
# ===========================================================
print("\n" + "=" * 60)
print("CONSULTA 2: Unidades vendidas por canal (compras de 2+ unidades)")
print("=" * 60)

compras_multiples = df[df["cantidad"] >= 2]
unidades_por_canal = (
    compras_multiples.groupby("canal")["cantidad"]
    .sum()
    .sort_values(ascending=False)
)
print(unidades_por_canal)

canal_top = unidades_por_canal.idxmax()
unidades_top = unidades_por_canal.max()
print(f"\nHallazgo: en las compras de 2 o más unidades, el canal "
      f"'{canal_top}' concentra la mayor cantidad de unidades vendidas "
      f"({unidades_top} unidades).")
