#!/usr/bin/python3.9
import subprocess
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
#from sistema_db.db_productos import sistema
from inventco.sistema_db.db_productos import sistema

class SistemaPrediccion:
    """Esta clase toma las demandas generadas por la pestaña alimentar y se las manda
    al ejecutable del motor de predicción escrito en Rust, este ejecutable entonces
    escribe las predicciones en una archivo txt, para que despues esta clase haga
    que el administrador de bd guarde las predicciones, hay 12 predicciones por cada
    producto"""
    #TODO: PONER LOS ARCHIVOS .TXT DE DEMANDA EN UNA CARPETA
    def __init__(self):
        """toma objetos tipo tabla_historico y genera predicciones a partir de ellos"""
        self.productos = {}
        self.programa_str = "C:\\Users\\CDT\\Documents\\tec\\ingenieria de software\\inventco\\motor_prediccion.exe"
        pass

    def predecir_producto(self, producto, tabla_historico):
        """"toma el nombre del producto y una tabla de demanda
        y genera: un archivo producto.txt con las demandas
        y después un archivo graficas/producto.svg con la grafica
        de prediccion"""
        if tabla_historico.is_complete():
            self.productos[producto] = tabla_historico
            self.generar_archivo_texto(producto)
            self.generar_grafica_prediccion(producto)
        else:
            raise Exception("No se puede predecir demanda de un producto con una tabla de demandas historicas vacia")
        print("productos: ", self.productos)

    def leer_y_registrar_prediccion(self, producto):
        f = open("predicciones/{}.txt".format(producto), 'r')
        #el ultimo elemento es un espacio en blanco
        nums = []
        for num in f.read().split(' ')[:-1]:
            nums.append(int(num))
        print("leyendo predicciones/{}.txt:".format(producto), nums)
        sistema.registrar_predicciones(producto, nums)
        
    def generar_archivo_texto(self, producto):
        """genera un archivo producto.txt que contiene las demandas
        formateadas para ser pasadas al motor de predicción forust
        """
        print("generando {}.txt...".format(producto))
        tabla = self.productos[producto]
        str_salida = ""
        for i in range(0, 3):
            for j in range(0, 12):
                str_salida += str(tabla.demandas[i][j]) + ' '
        str_salida = str(str_salida[:-1])
        f = open("productos/{}.txt".format(producto), 'w')
        f.write(str_salida)
        f.close()
        print('archivo {}.txt escrito'.format(producto))

    def generar_grafica_prediccion(self, producto):
        """genera un archivo producto.svg en la carpeta graficas
        que es una imagen de la grafica de predicción del producto
        """
        if producto in self.productos:
            subprocess.call([self.programa_str, producto])

    def eliminar_producto(self, producto):
        """funcion para que el sistema de bd llame
        esta función borra el archivo .txt de prediccion y tambien la grafica
        """
        if producto in self.productos:
            if os.path.exists("{}.txt".format(producto)):
                print("removiendo .txt")
                os.remove("{}.txt".format(producto))
            if os.path.exists("graficas\\{}.svg".format(producto)):
                os.remove("graficas\\{}.svg".format(producto))
                print("removiendo grafica")
            if os.path.exists("predicciones\\{}.txt".format(producto)):
                os.remove("predicciones\\{}.txt".format(producto))
                print("removiendo prediccion")
            del self.productos[producto]

    def clean(self):
        print("productos:", self.productos)
        for producto in self.productos.keys():
            print('producto a borrar: ', producto)
            self.eliminar_producto(producto)

sistema_prediccion = SistemaPrediccion()