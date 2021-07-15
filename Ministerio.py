# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:10:56 2021

@author: Juan
"""

def main(db_name, db_user, db_host, db_port, db_password, data):

    # Se importan las funciones propias para querys y generación de txts
    from functions_min import query_ministerio_academicos, query_ministerio_personales, query_ministerio_analitico
    from functions_min import generar_textfile, get_info_araucano
    
    # Se importan las librerías para conectar a PostgreSQL y la creación de carpetas
    import psycopg2
    import os

    # Se genera una carpeta con el nombre ingresado en el directorio definido para
    # la creación de los archivos de salida
    DIRECTORIO_TXTS = DIRECTORIO + data['folder'] + '/'
    try:
        os.mkdir(DIRECTORIO_TXTS)
        put_text('Se crea el directorio...').style('color: red')
    except:
        put_text('El directorio ya estaba creado...').style('color: red')

    # Se genera la conexión a la db postgresql
    conn = psycopg2.connect(host=db_host, port = db_port, database=db_name, user=db_user, password=db_password)

    data['sede_araucano'], data['titulo_araucano'] = get_info_araucano(data['PATH_INFO_ARAUCANO'], conn, data['legajo'])
    # Se transcriben los querys con los parámetros
    query_academicos = query_ministerio_academicos(data['legajo'], data['titulo_araucano'], data['sede_araucano'], data['promedio_con_aplazos'], data['promedio_sin_aplazos'])
    query_personales = query_ministerio_personales(data['legajo'])
    query_analitico = query_ministerio_analitico(data['legajo'])

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

    # Importo los datos de la base de datos
    from database import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS
    
    # Importo las librerías para la renderización
    from pywebio.input import input, input_group, NUMBER, FLOAT   
    from pywebio.output import put_text, clear
    
    # Se define el directorio de creación por defecto          
    DIRECTORIO = 'C:/Users/Juan/Desktop/'
    
    # Se define el origen del archivo con los códigos de Araucano por defecto
    PATH_INFO_ARAUCANO = 'C:/Users/Juan/Documents/GitHub/scripts_ministerio/codigos-ministerio.xlsx'

    # Limpio la pantalla
    clear()
    
    # Se define el formulario de ingreso de datos
    data = input_group("Generación de información para legalizaciones ante el Ministerio",[
      input('Nombre de archivo .zip (convención: apellido del estudiante)', name='folder', required=True),
      input('Legajo del estudiante', name='legajo', type=NUMBER, required=True),
      input('Promedio con aplazos', name='promedio_con_aplazos', type=FLOAT, required=True),
      input('Promedio sin aplazos', name='promedio_sin_aplazos', type=FLOAT, required=True),
      input('Directorio de trabajo', name='PATH_INFO_ARAUCANO', required=True, value=PATH_INFO_ARAUCANO, readonly=True),
      input('Archivo con códigos Araucano', name='DIRECTORIO', required=True, value=DIRECTORIO),
    ])

    # Llamo a la función principal de procesamiento de datos
    result = main(DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS, data)
    
    # Se muestra el resultado
    put_text(result).style('color: red')