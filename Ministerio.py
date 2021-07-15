# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:10:56 2021

@author: Juan
"""

def main(DIRECTORIO, FOLDER, legajo, titulo_araucano, sede_araucano, promedio_con_aplazos, promedio_sin_aplazos):

    # Se importan las funciones propias para querys y generación de txts
    from functions_min import query_ministerio_academicos, query_ministerio_personales, query_ministerio_analitico, generar_textfile
    
    # Se importan las librerías para conectar a PostgreSQL y la creación de carpetas
    import psycopg2
    import os

    # Se genera una carpeta con el nombre ingresado en el directorio definido para
    # la creación de los archivos de salida
    DIRECTORIO_TXTS = DIRECTORIO + FOLDER + '/'
    try:
        os.mkdir(DIRECTORIO_TXTS)
        put_text('Se crea el directorio...').style('color: red')
    except:
        put_text('El directorio ya estaba creado...').style('color: red')

    # Se genera la conexión a la db postgresql
    conn = psycopg2.connect(host="localhost", port = 5432, database="exportaciones_unlu", user="postgres", password="888888")

    # Se transcriben los querys con los parámetros
    query_academicos = query_ministerio_academicos(legajo, titulo_araucano, sede_araucano, promedio_con_aplazos, promedio_sin_aplazos)
    query_personales = query_ministerio_personales(legajo)
    query_analitico = query_ministerio_analitico(legajo)

    # Se generan los txt
    generar_textfile(conn, query_academicos, DIRECTORIO_TXTS+'academicos.txt')
    generar_textfile(conn, query_personales, DIRECTORIO_TXTS+'personales.txt')
    generar_textfile(conn, query_analitico, DIRECTORIO_TXTS+'analitico.txt', multi_rows=True)

    # Zipeo la carpeta resultante en el directorio definido
    import shutil
    shutil.make_archive(DIRECTORIO_TXTS, 'zip', DIRECTORIO_TXTS)

    # Cierro la conexión con PostgreSQL
    conn.close()

    # Se devuelve cadena de finalización del proceso
    return 'El proceso de generación de los archivos zip ha finalizado'
   

if __name__ == '__main__':

    # Importo las librerías para la renderización
    from pywebio.input import input, input_group, NUMBER, FLOAT   
    from pywebio.output import put_text
    
    # Se define el directorio de creación por defecto          
    DIRECTORIO = 'C:/Users/Juan/Desktop/'
    
    # Se define el formulario de ingreso de datos
    data = input_group("Generación de información para legalizaciones ante el Ministerio",[
      input('Nombre de Carpeta de Salida (Convención: Apellido estudiante)', name='folder', required=True),
      input('Legajo del estudiante', name='legajo', type=NUMBER, required=True),
      input('Código de Tí­tulo Araucano', name='titulo_araucano', type=NUMBER, required=True),
      input('Código de Sede Araucano', name='sede_araucano', type=NUMBER, required=True),
      input('Promedio con aplazos', name='promedio_con_aplazos', type=FLOAT, required=True),
      input('Promedio sin aplazos', name='promedio_sin_aplazos', type=FLOAT, required=True),
      input('Directorio de trabajo', name='DIRECTORIO', required=True, value=DIRECTORIO),
    ])
    
    # Llamo a la función principal de procesamiento de datos
    result = main(data['DIRECTORIO'], data['folder'], data['legajo'], data['titulo_araucano'], data['sede_araucano'], data['promedio_con_aplazos'], data['promedio_sin_aplazos'])
    
    # Se muestra el resultado
    put_text(result).style('color: red')