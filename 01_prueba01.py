import os
import pandas as pd
from bs4 import BeautifulSoup


def extraer_info(carpeta_entrada, archivo_salida):
    datos_extraidos = [
        ['Canal', 'Frecuencia (MHz)', 'Nivel (dBmV)', 'MER (dB)', 'BER (Previo)', 'BER (Posterior)', 'Eco (dBc)',
         'Retardo de grupo (ns)', 'ICFR (dB)', 'Zumbido (%)', 'DQI', 'Estrés AGC', 'Delta de canal adyacente (dB)']]
    archivos_html = [f for f in os.listdir(carpeta_entrada) if f.endswith('.html')]

    for archivo_html in archivos_html:
        ruta_html = os.path.join(carpeta_entrada, archivo_html)
        nombre_archivo = archivo_html

        with open(ruta_html, 'r') as file:
            contenido = file.read()

        soup = BeautifulSoup(contenido, 'html.parser')
        estructuras = soup.find_all('th')

        for estructura in estructuras:
            valor_th = estructura.get_text()
            datos = estructura.find_next_siblings('td')
            fila_datos = [valor_th] + [dato.get_text() for dato in datos]
            fila_datos.insert(13, nombre_archivo)

            if len(fila_datos) >= 8:
                datos_extraidos.append(fila_datos)

    df = pd.DataFrame(datos_extraidos)
    df.to_excel(archivo_salida, index=False, header=False)

    print("Los datos se han extraído y guardado en el archivo Excel correctamente.")


carpeta_entrada = 'datos'
archivo_salida = 'datos.xlsx'
extraer_info(carpeta_entrada, archivo_salida)
