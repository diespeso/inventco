import json
import sqlite3 as sql

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from inventco.app_prediccion import sistema_prediccion

class db_cleaner:
    """Clase para limpiar la base de datos durante las pruebas.
    """
    def __init__(self):
        self.connection = sql.connect('productos.db')
        self.cursor = self.connection.cursor()

    def drop_table(self, table_name):
        self.cursor.execute('DROP TABLE IF EXISTS {};'.format(table_name))


if __name__ == '__main__':
    cleaner = db_cleaner()
    cleaner.drop_table('producto')
    cleaner.drop_table('prediccion')
    cleaner.drop_table('experimento')
    cleaner.drop_table('simulacion')
    cleaner.drop_table('historico')
    sistema_prediccion.clean()
   