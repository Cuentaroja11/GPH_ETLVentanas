import os
import pandas as pd
from bs4 import BeautifulSoup

def extraer_info(carpeta_entrada):
    archivos_html = [f for f in os.listdir(carpeta_entrada) if f.endswith('.html')]

    # Crear carpeta de salida si no existe
    carpeta_salida = os.path.join(os.path.dirname(carpeta_entrada), 'OFDMFiles')
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for archivo_html in archivos_html:
        ruta_html = os.path.join(carpeta_entrada, archivo_html)
        nombre_archivo = os.path.splitext(archivo_html)[0]
        archivo_salida = os.path.join(carpeta_salida, f'{nombre_archivo}.xlsx')

        with open(ruta_html, 'r') as file:
            contenido = file.read()

        soup = BeautifulSoup(contenido, 'html.parser')
        tablas = soup.find_all('table', class_='table table-fixed')

        for tabla in tablas:
            encabezados = tabla.find_all('th')
            if len(encabezados) >= 2 and encabezados[1].get_text() == 'OFDM 1':
                datos_extraidos = []
                fila_encabezados = [encabezados[0].get_text(), encabezados[1].get_text()]
                datos_extraidos.append(fila_encabezados)

                filas_datos = tabla.find_all('tr')
                for fila in filas_datos[1:]:
                    celdas = fila.find_all(['th', 'td'])
                    datos_fila = [celda.get_text() for celda in celdas[0:2]]  # Obtener solo los datos de las primeras dos columnas
                    datos_extraidos.append(datos_fila)

                # Agregar última fila con el nombre del archivo analizado
                nombre_archivo_fila = ['Archivo', nombre_archivo]
                datos_extraidos.append(nombre_archivo_fila)

                df = pd.DataFrame(datos_extraidos).transpose()  # Transponer el DataFrame
                df.to_excel(archivo_salida, index=False, header=False)

                print(f"Se ha extraído la tabla del archivo {nombre_archivo} y se ha guardado en el archivo Excel {archivo_salida}.")

carpeta_entrada = 'datos'
extraer_info(carpeta_entrada)
