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
    