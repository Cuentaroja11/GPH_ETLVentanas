import os
import pandas as pd

# Carpeta de origen y archivo de salida
carpeta_origen = "OFDMFiles"
archivo_salida = "OFDMExtract.xlsx"

# Lista para almacenar los datos combinados
datos_combinados = []

# Recorrer todos los archivos en la carpeta de origen
for archivo in os.listdir(carpeta_origen):
    if archivo.endswith(".xlsx"):
        # Leer el archivo Excel
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        datos_excel = pd.read_excel(ruta_archivo)
        
        # Agregar los datos al resultado combinado
        datos_combinados.append(datos_excel)

# Combinar todos los datos en un solo DataFrame
datos_totales = pd.concat(datos_combinados)

# Guardar los datos combinados en un nuevo archivo Excel
datos_totales.to_excel(archivo_salida, index=False)

print("La combinación de los archivos se ha completado.")
