import os
import pandas as pd
from bs4 import BeautifulSoup

def extraer_info(carpeta_entrada, archivo_salida):
    # Crear una lista para almacenar los datos extraídos
    datos_extraidos = []

    # Agregar la lista de encabezados al principio de los datos extraídos
    encabezados = [
        'Canal', 'Frecuencia (MHz)', 'Nivel (dBmV)', 'MER (dB)', 'BER (Previo)',
        'BER (Posterior)', 'Eco (dBc)', 'Retardo de grupo (ns)', 'ICFR (dB)',
        'Zumbido (%)', 'DQI', 'Estrés AGC', 'Delta de canal adyacente (dB)'
    ]
    datos_extraidos.append(encabezados)

    # Obtener la lista de archivos HTML en la carpeta de entrada
    archivos_html = [f for f in os.listdir(carpeta_entrada) if f.endswith('.html')]

    # Procesar cada archivo HTML en la carpeta
    for archivo_html in archivos_html:
        # Crear la ruta completa al archivo HTML
        ruta_html = os.path.join(carpeta_entrada, archivo_html)

        # Obtener el nombre del archivo actual
        nombre_archivo = archivo_html

        # Abrir el archivo de entrada en modo lectura
        with open(ruta_html, 'r') as file:
            # Leer el contenido del archivo
            contenido = file.read()

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(contenido, 'html.parser')

        # Encontrar todas las estructuras con etiquetas <th> en el HTML
        estructuras = soup.find_all('th')

        # Procesar cada estructura
        for estructura in estructuras:
            # Obtener el valor dentro de la etiqueta <th>
            valor_th = estructura.get_text()

            # Encontrar los datos relacionados en la estructura
            datos = estructura.find_next_siblings('td')

            # Crear una lista con el nombre del archivo, el valor del <th> y los datos de las <td>
            fila_datos = [valor_th] + [dato.get_text() for dato in datos] 

            # Insertar el nombre del archivo en la quinta posición
            fila_datos.insert(6, nombre_archivo)

            # Verificar que la fila tenga al menos 8 columnas
            if len(fila_datos) >= 8:
                # Agregar la fila de datos a la lista de datos extraídos
                datos_extraidos.append(fila_datos)

    # Crear un DataFrame a partir de los datos extraídos
    df = pd.DataFrame(datos_extraidos)

    # Eliminar la columna B y las columnas G en adelante
    df.drop(columns=[1], inplace=True)  # Eliminar la columna B (índice 1)
    df = df.iloc[:, :6]  # Mantener solo las primeras 7 columnas

    # Guardar el DataFrame en un archivo Excel
    df.to_excel(archivo_salida, index=False, header=False)

    print("Los datos se han extraído y guardado en el archivo Excel correctamente.")

# Ejemplo de uso
carpeta_entrada = 'datos'
archivo_salida = 'datos.xlsx'

extraer_info(carpeta_entrada, archivo_salida)