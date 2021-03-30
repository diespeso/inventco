import sys
sys.path.append("..") # Adds higher directory to python modules path.
from inventco import utils

from .db_productos import sistema

class TablaHistorico:

    def __init__(self):
        self.demandas = []
        self.producto = None

    def set_nombre_producto(self, producto):
        self.producto = producto


    def from_tabla(self, tabla):
        self.demandas = []
        """toma un arreglo 3x3 de demandas en total y los trae a este objeto
        si no hay demanda en un punto, entonces es un valor None"""
        #primero asegurarse de que esta en el formato correcto
        #si esto falla, entonces no estaba bien formateada

        #preparar el arreglo
        for i in range(0, 3):#hardcoded para 36 meses
            self.demandas.append([])
            for j in range(0, 12):
                self.demandas[i].append(None) 

        #llenar el arreglo
        for i in range(0, len(tabla)):
            for j in range(0, len(tabla[i])):
                self.demandas[i][j] = tabla[i][j]

    def to_db(self, producto):
        self.producto = producto

        print("demandas: {}", self.demandas)

        for anio in range(1, 4):
            for j in range(1, 13):
                demanda = self.demandas[anio - 1][j - 1]
                if demanda == '':
                    demanda = 'null'
                else:
                    demanda = int(demanda)
                    #insertar o mas bien cambiar, mejor cambiar
                    #hacer que se inserten los valores al registrar el product
                    #y aqui solo modificarlos de null a un valor verdadero
                    
                print('producto: {}'.format(self.producto))
                print('anio: {}'.format(anio))
                print('mes: {}'.format(utils.to_mes(j)))
                print('demanda: {}'.format(demanda))

                sistema.cursor.execute(
                    """UPDATE historico SET
                    demanda = {} WHERE
                    nombre_producto = '{}' 
                    AND anio = {}
                    AND mes = '{}';
                    """.format(
                        demanda, producto, anio, utils.to_mes(j)
                    )
                )
                sistema.connection.commit()
        

    def is_complete(self):
        for i in range(0, 3):
            for j in range(1, 13):
                try: #no puede estar vacio
                    if(self.demandas[i][j]) == None:
                        return False
                except Exception: #debe de ser de 3x12
                    return False
        return True

    def from_db(self, producto):
        #aun no esta terminado
        sistema.cursor.execute(
            "SELECT demanda FROM historico where nombre_producto = '{}';".format(producto)
        )
        if sistema.cursor.fetchone():
            self.producto = producto
            rows = sistema.cursor.fetchall()
            for i in range(0, len(rows)):
                print("demanda del mes {}: {}", i, rows[i])
        else:
            print("no encontrado")
            return None
            