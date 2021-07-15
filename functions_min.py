# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:15:34 2021

@author: Juan
"""

def generar_textfile(conexion, query, file_name, multi_rows=False):
    import csv
    # Genero el cursor y ejecuto el query
    cur = conexion.cursor()
    cur.execute(query)
    with open(file_name, 'w') as f:
        writer = csv.writer(f, lineterminator='\n', delimiter='|')
        if multi_rows:
             result = cur.fetchall()
             for registro in result:
                 writer.writerow(registro)
        else:
            result = cur.fetchall()[0]
            writer.writerow(result)
    cur.close()

def query_ministerio_analitico(legajo):
    '''
    Parameters
    ----------
    legajo : integer
        legajo del estudiante

    Returns
    -------
    STRING con el query para PostgreSQL.

    '''
    query = f'''
                SELECT	'DNI',
                    	e.numero_documento,
                    	(select a.denominacion from asignaturas a where a.codigo=f.asignatura limit 1),
                    	f.fecha_examen,
                    	f.calificacion,
                    	CASE WHEN (f.calificacion>=1 and f.calificacion<=99) THEN f.libro ELSE 000 END,
                    	f.folio,
                    	CASE 	WHEN (f.condicion='P') THEN f.condicion 
                    		WHEN (f.condicion='R' or f.condicion='L') THEN 'E' 
                    		WHEN (f.condicion='E' or f.condicion='I') THEN 'Q'
                    	ELSE 'R' END,
                    	CASE	WHEN (f.calificacion>=4 and f.calificacion<=10) THEN 'A' 
                    		WHEN (f.condicion='X' or f.condicion='E' or f.condicion='I') THEN 'A' 
                    		ELSE 'D' END
                FROM finales f
                INNER JOIN estudiantes e ON e.legajo=f.legajo
                WHERE e.legajo={legajo} and f.calificacion<>99  --Modificar legajo
                and f.asignatura in (select codigo from asignaturas where plan=e.plan_estudios);
            '''
    return query

def query_ministerio_personales(legajo):
    '''
    Parameters
    ----------
    legajo : integer
        legajo del estudiante

    Returns
    -------
    STRING con el query para PostgreSQL.

    '''
    query = f'''
                SELECT 'DNI',
                    	numero_documento,
                        substr(apellido_nombre,1,strpos(apellido_nombre,',') -1),
                    	substr(apellido_nombre,strpos(apellido_nombre,',')+1),
                    	54,
                    	fecha_nacimiento,
                    	54,
                    	'',
                    	'',
                    	calle || ' ' || numero_direccion
                FROM estudiantes e
                WHERE legajo={legajo}; --Modificar legajo
            '''
    return query

def query_ministerio_academicos(legajo, titulo, sede, prom_ap, prom_sin_ap):
    '''
    Parameters
    ----------
    legajo : integer
        legajo del estudiante
    titulo : integer
        código araucano
    sede : integer
        sede araucano
    prom_ap, prom_sin_ap: float
        promedio del estudiante con y sin aplazos

    Returns
    -------
    STRING con el query para PostgreSQL.

    '''
    query = f'''
                SELECT	'DNI',
                    	numero_documento,
                    	{sede}, --Modificar sede
                    	{titulo},  --Modificar titulo Araucano
                    	'',
                    	'S',
                    	'',
                    	'',
                    	'',
                    	(select min(fecha_examen) from finales where calificacion>=4 and calificacion<=10 and legajo=e.legajo),
                    	(select max(fecha_examen) from finales where calificacion>=4 and calificacion<=10 and legajo=e.legajo),
                    	'S',
                    	1,
                    	titulo_ingreso,
                    	titulo_ingreso,
                    	'',
                    	'',
                    	'',
                    	{prom_ap},     --Modificar promedio sin aplazos
                    	{prom_sin_ap}, --Modificar promedio con aplazos
                    	'N'
                FROM estudiantes e
                WHERE legajo={legajo}; --Modificar legajo'
            '''
    return query


def get_info_araucano(PATH_FILE_MIN, conexion, legajo):
    '''
    Función que en función del legajo del estudiante, busca en postgresql 
    la sede y el título y lo traduce a la codificación araucano
    Parameters
    ----------
    PATH_FILE_MIN : text
        Ubicación del xlsx con los códigos (título y sede) de Araucano
    conexion : conx PostgreSQL
        Base con los datos de los estudiantes
    legajo : integer
        Legajo del estudiante en cuestión

    Returns
    -------
    info_araucano : diccionario
        código de sede y título araucano para el estudiante
    '''    
    import pandas as pd

    # Cargo los títulos araucano en un dataframe y modifico los nombres de columna
    pd_titulos = pd.read_excel(PATH_FILE_MIN, sheet_name='Títulos').iloc[:,0:4]
    pd_titulos.columns = ['codigo_araucano', 'codigo_sca', 'denominacion_titulo', 'tipo_oferta']

    # Me quedo solo con los títulos finales
    pd_titulos = pd_titulos.loc[pd_titulos['tipo_oferta'] != 'Título Intermedio']

    # Elimino el ciclo de complementación de Sistemas para que no haya dos códigos
    # Araucano para la misma carrera
    pd_titulos = pd_titulos.loc[pd_titulos['denominacion_titulo'] != 'Licenciado en Sistemas de Información - Ciclo de Licenciatura']

    # Cargo las sedes araucano en un dataframe y modifico los nombres de columna
    pd_sedes = pd.read_excel(PATH_FILE_MIN, sheet_name='Sedes').iloc[:,0:2]
    pd_sedes.columns = ['codigo_araucano', 'descripcion_sede']

    # Genero el cursor y ejecuto el query
    cur = conexion.cursor()
    query = f'''SELECT plan_estudios/100 as carrera_sca,
                       sede as sede_sca
                FROM estudiantes
                WHERE legajo={legajo}'''
               
    cur.execute(query)
    info_sca = cur.fetchall()[0]
    carrera_sca, sede_sca = info_sca
    cur.close() 

    # Me guardo los datos en dos variables
    sede_araucano = int(pd_sedes.loc[pd_sedes['descripcion_sede'] == sede_sca]['codigo_araucano'])
    titulo_araucano = int(pd_titulos.loc[pd_titulos['codigo_sca'] == carrera_sca]['codigo_araucano'])

    return sede_araucano, titulo_araucano
