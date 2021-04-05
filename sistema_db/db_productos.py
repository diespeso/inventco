from tkinter import messagebox

import json
import sqlite3 as sql

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from inventco import utils

NT_PRODUCTOS = 'producto' #nombre tabla productos
NT_PRODUCTO_X_PREDICCION = 'producto_x_prediccion'
NT_PREDICCION = 'prediccion'

class SistemaProductos:
    def __init__(self):
        self.connection = sql.connect('productos.db')
        self.cursor = self.connection.cursor()
        self.producto_actual = None
        """self.cursor.execute(
            '''SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='producto' ''')
        if self.cursor.fetchone()[0] != 1 {
            self.cursor.execute('CREATE TABLE productos')
        }"""
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS producto (
                nombre TEXT NOT NULL,
                costo_pedido REAL NOT NULL,
                costo_faltante REAL NOT NULL,
                costo_inventario REAL NOT NULL,
                inventario_inicial NUMERIC NOT NULL,
                grafica_prediccion BLOB,
                PRIMARY KEY (nombre)
            );
            ''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS prediccion(
                nombre_producto TEXT NOT NULL,
                mes TEXT NOT NULL,
                demanda INTEGER,
                PRIMARY KEY(nombre_producto, mes),
                FOREIGN KEY(nombre_producto) REFERENCES producto(nombre)
            );
            '''
        )

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS experimento(
                nombre_producto TEXT NOT NULL,
                numero NUMERIC NOT NULL,
                punto_reorden NUMERIC NOT NULL,
                cantidad_orden NUMERIC NOT NULL,
                primary key (nombre_producto, numero),
                foreign key (nombre_producto) REFERENCES product(nombre)
            );
            '''
        )
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS simulacion(
                nombre_producto TEXT NOT NULL,
                no_experimento NUMERIC NOT NULL,
                mes TEXT NOT NULL,
                inv_inicial NUMERIC NOT NULL,
                inv_final NUMERIC NOT NULL,
                faltante NUMERIC,
                orden NUMERIC,
                PRIMARY KEY (nombre_producto, no_experimento, mes),
                FOREIGN KEY (nombre_producto) REFERENCES producto(nombre),
                FOREIGN KEY (no_experimento) REFERENCES experimento(numero),
                FOREIGN KEY (mes) REFERENCES prediccion(mes)
                );
            '''
        )

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS historico(
                nombre_producto TEXT NOT NULL,
                anio NUMERIC NOT NULL,
                mes TEXT NOT NULL,
                demanda NUMERIC,
                PRIMARY KEY (nombre_producto, anio, mes),
                FOREIGN KEY (nombre_producto) REFERENCES producto(nombre)
            );
            '''
        )
        self.connection.commit()

    def registrar_producto(self, json_producto):
        #TODO: REVISAR QUE EL PRODUCTO NO EXISTA
        #SI EXISTE NOTIFICAR
        #SINO EXISTE, ENTONCES APARTE DE AñADIR A SU TABLA
        #RELLENAR LA TABLA DE HISTORICO CON VALORES NULOS

        """toma una cadena json representando el producto y lo registra en la bd"""
        datos = json.loads(json_producto)
        
        if self.set_producto_actual(datos['nombre']): #si es nuevo
            self.registrar_en_producto(datos)
            self.registrar_en_experimento(datos)
            self.registrar_en_historico(datos)
            self.connection.commit()

    def registrar_en_producto(self, datos_producto):
        datos = datos_producto
        """toma un diccionario ya procesado desde json y registra el producto en la bd producto"""
        #el ultimo elemento: grafica_prediccion no esta disponible hasta 
        #despues de simular
        self.cursor.execute(
           "INSERT INTO producto VALUES('{}', {}, {}, {}, {}, null);".format(
                datos['nombre'],
                datos['costo_pedido'],
                datos['costo_faltante'],
                datos['costo_inventario'],
                datos['inventario_inicial']
            )
        )
    
    def registrar_en_experimento(self, datos_producto):
        datos = datos_producto
        #cuando se registra el producto se registra el experimento 0: el original
        self.cursor.execute(
            "INSERT INTO experimento VALUES ('{}', 0, {}, {});".format(
                datos['nombre'],
                datos['punto_reorden'],
                datos['cantidad_orden'],
            )
        )

    def registrar_en_historico(self, datos_producto):
        datos = datos_producto
        for anio in range(1, 4):
            for mes in range(1, 13):
                self.cursor.execute(
                    "INSERT INTO historico VALUES('{}', {}, '{}', null);".format(
                        datos['nombre'],
                        anio,
                        utils.to_mes(mes)
                    )
                )

    def buscar_historico_producto(self, producto):
        pass


    def set_producto_actual(self, producto):
        #establece el nombre del producto actual pero solo si no existia antes
        existe = self.cursor.execute("select * from producto where nombre = '{}';".format(
            producto
        ))
        if self.cursor.fetchone():
            messagebox.showwarning(message="Este producto ya ha sido registrado", title='Producto ya registrado')
            self.producto_actual = None
            return False
        else:
            self.producto_actual = producto
            return True

    def set_producto_actual_repetido(self, producto):
        #para productos ya registrados
        existe = self.cursor.execute("select * from producto where nombre = '{}';".format(
            producto
        ))
        if self.cursor.fetchone():
            self.producto_actual = producto
            return True
        else:
            messagebox.showwarning(message="El producto no existe", title='Producto no encontrado')
            self.producto_actual = None
            return False



sistema = SistemaProductos()

if __name__ == '__main__':
    sistema.cursor.execute('select * from producto;')
    rows = sistema.cursor.fetchall()
    print('producto')
    for row in rows:
        print(row)

    sistema.cursor.execute('select * from prediccion;')
    rows = sistema.cursor.fetchall()
    print('prediccion:')
    for row in rows:
        print(row)
    
    sistema.cursor.execute('select * from experimento;')
    r2 = sistema.cursor.fetchall()
    print('experimento')
    for row in r2:
        print(row)

    sistema.cursor.execute('select * from simulacion;')
    rows = sistema.cursor.fetchall()
    print('simulacion')
    for row in rows:
        print(row)

    sistema.cursor.execute('select * from historico;')
    rows = sistema.cursor.fetchall()
    print('historico')
    for row in rows:
        print(row)

    
