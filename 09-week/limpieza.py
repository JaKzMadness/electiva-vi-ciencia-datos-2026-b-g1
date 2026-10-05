import re
import pandas as pd
import numpy as np

# =======================================================
# 1. CARGA DEL DATASET
# =======================================================
df = pd.read_csv("ventas_sucias.csv")

print("=" * 60)
print("ANTES DE LA LIMPIEZA")
print("=" * 60)
print(f"\nFilas totales: {len(df)}")
print("\nTipos de dato por columna:")
print(df.dtypes)

print("\nValores nulos por columna:")
print(df.isnull().sum())

print(f"\nFilas duplicadas (exactas): {df.duplicated().sum()}")

print("\nValores únicos en 'categoria' (antes):")
print(sorted(df['categoria'].dropna().unique()))

print("\nValores únicos en 'canal' (antes):")
print(sorted(df['canal'].dropna().unique()))

print("\nMuestra de 'fecha' (antes):")
print(df['fecha'].unique())

print("\nMuestra de 'precio_unitario' (antes):")
print(df['precio_unitario'].unique())

# =======================================================
# 2. LIMPIEZA
# =======================================================

# --- 2.1 Quitar duplicados exactos ---
df = df.drop_duplicates()

# --- 2.2 Eliminar filas sin id_cliente (dato clave que no se puede inventar) ---
df = df.dropna(subset=['id_cliente'])

# --- 2.3 Corregir tipo y limpiar precio_unitario ---
# Quita el símbolo "$" y, solo cuando el punto se usa como separador de miles
# (ej. "1.200.000"), lo elimina; si es un punto decimal (ej. "2500000.0") lo conserva.
def limpiar_precio(valor):
    texto = str(valor).strip().replace('$', '')
    if texto in ('nan', ''):
        return np.nan
    if re.fullmatch(r'\d{1,3}(\.\d{3})+', texto):
        texto = texto.replace('.', '')
    return texto

df['precio_unitario'] = df['precio_unitario'].apply(limpiar_precio)
df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')

# --- 2.4 Imputar precio_unitario y cantidad faltantes con la mediana de su categoría ---
df['categoria_norm_temp'] = df['categoria'].str.strip().str.lower()
df['precio_unitario'] = df.groupby('categoria_norm_temp')['precio_unitario'] \
    .transform(lambda s: s.fillna(s.median()))
df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
df['cantidad'] = df['cantidad'].fillna(df['cantidad'].median())
df = df.drop(columns=['categoria_norm_temp'])

# --- 2.5 Corregir tipos numéricos y de fecha ---
df['cantidad'] = df['cantidad'].astype(int)
df['fecha'] = pd.to_datetime(df['fecha'], format='mixed', dayfirst=True)

# --- 2.6 Normalizar texto (espacios y mayúsculas/minúsculas) ---
df['producto'] = df['producto'].str.strip().str.title()
df['canal'] = df['canal'].str.strip().str.title()

# --- 2.7 Normalizar categorías equivalentes a un único nombre ---
mapa_categorias = {
    'celular': 'Celular',
    'computador': 'Computador',
    'tv': 'Televisor',
    'television': 'Televisor',
    'accesorio': 'Accesorio',
    'periferico': 'Periférico',
}
df['categoria'] = df['categoria'].str.strip().str.lower().map(mapa_categorias)

# --- 2.8 Recalcular el total a partir de cantidad x precio_unitario (ya limpios) ---
df['total'] = (df['cantidad'] * df['precio_unitario']).round(0)

# --- 2.9 Tipos finales ---
df['id_cliente'] = df['id_cliente'].astype(int)
df = df.reset_index(drop=True)

# =======================================================
# 3. DESPUÉS DE LA LIMPIEZA
# =======================================================
print("\n" + "=" * 60)
print("DESPUÉS DE LA LIMPIEZA")
print("=" * 60)
print(f"\nFilas totales: {len(df)}")
print("\nTipos de dato por columna:")
print(df.dtypes)

print("\nValores nulos por columna:")
print(df.isnull().sum())

print(f"\nFilas duplicadas (exactas): {df.duplicated().sum()}")

print("\nValores únicos en 'categoria' (después):")
print(sorted(df['categoria'].unique()))

print("\nValores únicos en 'canal' (después):")
print(sorted(df['canal'].unique()))

print("\nMuestra de 'fecha' (después):")
print(df['fecha'].head())

print("\nDataset limpio (primeras filas):")
print(df.head(10).to_string(index=False))

df.to_csv("ventas_limpio.csv", index=False)
print("\nArchivo 'ventas_limpio.csv' guardado correctamente.")
