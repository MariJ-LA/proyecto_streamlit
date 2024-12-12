import sqlite3
import os
import pandas as pd

def mapear_datos(nombre_db,formato):
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_db}{formato}')
    return db_path


def cargar_datos(ruta_archivo):
    conn = sqlite3.connect(ruta_archivo)

    dataframes = {}

    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn)

    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)


    conn.close()

    return dataframes



    