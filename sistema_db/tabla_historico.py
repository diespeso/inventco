from tkinter import messagebox

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from inventco import utils

from .db_productos import sistema

class TablaHistorico:

    def __init__(self):
        self.demandas = []

    def set_nombre_producto(self, producto):
        return sistema.set_producto_actual(producto)

    def set_nombre_producto_repetido(self, producto):
        return sistema.set_producto_actual_repetido(producto)

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
        #se debe garantizar que la tabla de demandas
        #ya haya sido correctamente formateada
        """if sistema.producto_actual == None:
            messagebox.showerror(message="No se pueden alimentar demandas a un producto ya registrado si no se está en modo de edición", title='Imposible editar')
            return
        """
        print("demandas: {}", self.demandas)

        for anio in range(1, 4):
            for j in range(1, 13):
                demanda = self.demandas[anio - 1][j - 1]
                    #insertar o mas bien cambiar, mejor cambiar
                    #hacer que se inserten los valores al registrar el product
                    #y aqui solo modificarlos de null a un valor verdadero
                    
                print('producto: {}'.format(producto))
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
                        demanda, sistema.producto_actual, anio, utils.to_mes(j)
                    )
                )
                sistema.connection.commit()
        
    def update_from_bd(self):
        #updates the demanda table from the bd if it exists
        #if exists
        #put from db
        pass
    def is_complete(self):
        print("is complete?")
        #self.demandas = 
        for i in range(0, 3):
            for j in range(0, 12):
                try: #no puede estar vacio
                    print('demanda actual: ', self.demandas[i][j])
                    int(self.demandas[i][j]) #si falla en convertirla en entero
                    #entonces hay un dato vacio y no se puede considerar completa
                except Exception: #debe de ser de 3x12
                    return False
        return True

    def from_db(self, producto):
        #aun no esta terminado

        if self.set_nombre_producto_repetido(producto): #si ya existe
            sistema.cursor.execute(
            """SELECT anio, mes, demanda FROM historico where nombre_producto = '{}'
                ORDER BY anio;""".format(producto)
            )
            rows = sistema.cursor.fetchall()
            print("bd rows:", rows)
            rows = utils.ordenar_tabla_demandas(rows)
            print('bd rows ordenadas:', rows)
            demandas = []
            counter = 0
            for i in range(0, 3):
                demandas.append([])
                for j in range(0, 12):
                    demandas[i].append(rows[counter][2])
                    counter += 1
            self.demandas = demandas
            print('db final:', demandas)
            return True
        return False
            
    def write_to_file(self, filename):
        """deprecated, no usar"""
        #toma esta tabla de demandas si esta completa y la escribe
        #en un archivo con el nombre del producto
        #se asume que la tabla de este objeto está ordenada correctamente
        print('escribiendo a archivo: {}.txt'.format(filename))
        if self.is_complete():
            str_salida = ""
            for i in range(0, 3):
                for j in range(0, 12):
                    str_salida += str(self.demandas[i][j]) + ' '
            str_salida = str(str_salida[:-1])
            print("string de salida: ", str_salida)
            f = open('{}.txt'.format(filename), 'w')
            f.write(str_salida)
            f.close()
            print('archivo {}.txt escrito'.format(filename))
        else:
            raise Exception("Se intentó escribir a archivo una tabla de demandas incompleta")