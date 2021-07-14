# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:10:56 2021

@author: Juan
"""

DIRECTORIO = 'C:/Users/Juan/Desktop/'

##########################################################################
######################### DATOS DEL ESTUDIANTE ###########################

APELLIDO = 'DIAZ'
LEGAJO = 117260
TITULO_ARAUCANO = 442
SEDE_ARAUCANO = 292
PROMEDIO_APLAZOS = 8.51
PROMEDIO_SIN_APLAZOS = 8.51

##########################################################################
##########################################################################

from functions_min import query_ministerio_academicos, query_ministerio_personales, query_ministerio_analitico, generar_textfile
import psycopg2
import os

# Se genera una carpeta con el apellido
DIRECTORIO_TXTS = DIRECTORIO + APELLIDO + '/'

try:
    os.mkdir(DIRECTORIO_TXTS)
    print('Se crea el directorio...')
except:
    print('El directorio ya estaba creado...')

# Se genera la conexión
conn = psycopg2.connect(host="localhost", port = 5432, database="exportaciones_unlu", user="postgres", password="888888")

# Se transcriben los querys con los parámetros
query_academicos = query_ministerio_academicos(LEGAJO, TITULO_ARAUCANO, SEDE_ARAUCANO, PROMEDIO_APLAZOS, PROMEDIO_SIN_APLAZOS)
query_personales = query_ministerio_personales(LEGAJO)
query_analitico = query_ministerio_analitico(LEGAJO)

generar_textfile(conn, query_academicos, DIRECTORIO_TXTS+'academicos.txt')
generar_textfile(conn, query_personales, DIRECTORIO_TXTS+'personales.txt')
generar_textfile(conn, query_analitico, DIRECTORIO_TXTS+'analitico.txt', multi_rows=True)

# Zipeo la nota resultante
import shutil
shutil.make_archive(DIRECTORIO_TXTS, 'zip', DIRECTORIO_TXTS)

# Cierro la conexión
conn.close()
