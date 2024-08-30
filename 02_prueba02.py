import pandas as pd

# Leer el archivo de Excel
df = pd.read_excel('datos.xlsx')

# Ordenar el DataFrame por la primera columna
df_sorted = df.sort_values(by='Canal')

# Guardar el DataFrame ordenado en un nuevo archivo de Excel
df_sorted.to_excel('archivo_ordenado.xlsx', index=False)
