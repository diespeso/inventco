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
                PRIMARY KEY (nombre)
            );
            ''')#grafica_predccion siempre no
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
            self.registrar_en_experimento(datos['nombre'], datos['punto_reorden'], datos['cantidad_orden'])
            self.registrar_en_historico(datos)
            self.init_predicciones(datos['nombre'])
            self.registrar_en_simulacion(datos['nombre'])
            self.connection.commit()

    def init_predicciones(self, producto):
        """crea placeholders en la tabla de predicciones para ser editados despues"""
        for i in range(0, 12):
            self.cursor.execute("INSERT INTO prediccion VALUES('{}', '{}', {});".format(
                producto, utils.to_mes(i + 1), 0)
            )
    def registrar_en_producto(self, datos_producto):
        datos = datos_producto
        """toma un diccionario ya procesado desde json y registra el producto en la bd producto"""
        #el ultimo elemento: grafica_prediccion no esta disponible hasta 
        #despues de simular
        self.cursor.execute(
           "INSERT INTO producto VALUES('{}', {}, {}, {}, {});".format(
                datos['nombre'],
                datos['costo_pedido'],
                datos['costo_faltante'],
                datos['costo_inventario'],
                datos['inventario_inicial']
            )
        )
    
    def registrar_en_experimento(self, nombre_producto, punto_reorden, cantidad_orden):
        #cuando se registra el producto se registra el experimento 0: el original
        self.cursor.execute(
            "INSERT INTO experimento VALUES ('{}', 0, {}, {});".format(
                nombre_producto,
                punto_reorden,
                cantidad_orden,
            )
        )
        for i in range(1, 9):
            self.cursor.execute(
                "INSERT INTO experimento VALUES ('{}', {}, 0, 0);".format(
                    nombre_producto, i
                )
            )
            print("datos_reg: ", nombre_producto, punto_reorden, cantidad_orden)

    def actualizar_en_experimento(self, nombre_producto, numero, punto_reorden, cantidad_orden):
        print("datos: ", nombre_producto, numero, punto_reorden, cantidad_orden)
        self.cursor.execute(
            """UPDATE experimento SET nombre_producto = '{}',
            numero = {},
            punto_reorden = {},
            cantidad_orden = {} WHERE nombre_producto = '{}' AND numero = {}""".format(nombre_producto, numero, punto_reorden, cantidad_orden, nombre_producto, numero)
        )
        self.connection.commit()

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

    def registrar_en_simulacion(self, nombre_producto):
        """Inicializa la tabla de simulación a valores por defecto, 9 experimentos, 12 meses, esto por cada producto"""
        for e in range(0, 9):
            for m in range(1, 13):
                self.cursor.execute("""INSERT INTO simulacion VALUES ('{}', {}, '{}', 0, 0, 0, 0);""".format(
                    nombre_producto, e, utils.to_mes(m)
                ))
    
    def actualizar_en_simulacion(self, nombre_producto, no_experimento, mes, inv_inicial, inv_final, faltante, orden):
        #print("actualizando")
        #print(nombre_producto, no_experimento, mes, inv_inicial, inv_final, faltante, orden)
        if orden == None:
            orden = 'null'
        self.cursor.execute("""UPDATE simulacion SET nombre_producto = '{}',
        no_experimento = {}, mes = '{}', inv_inicial = {}, inv_final = {}, faltante = {}, orden = {}
        WHERE nombre_producto = '{}' AND no_experimento = {} AND mes = '{}'""".format(
            nombre_producto, no_experimento, mes, inv_inicial, inv_final, faltante, orden, nombre_producto, no_experimento, mes
        ))
        self.connection.commit()



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

    def registrar_predicciones(self, producto, predicciones):
        #todo maybe: quizas deberia asegurarme de que el producto exista antes
        #aunque creo que la bd lo hace sola, nvm?
        if len(predicciones) == 12:
            for i in range(0, len(predicciones)):
                self.cursor.execute(
                    """UPDATE prediccion SET demanda = {}
                    WHERE nombre_producto = '{}'
                    AND mes = '{}';""".format(
                predicciones[i], producto, utils.to_mes(i + 1)
            ))
            self.connection.commit()
        else:
            raise Exception("No se puede registrar a bd una lista de predicciones que no tenga exactamente 12 elementos")

    def get_producto(self, producto):
        self.cursor.execute("SELECT * FROM producto WHERE nombre = '{}';".format(producto))
        self.connection.commit()
        return db_producto_to_dic(self.cursor.fetchone())

    def get_experimento(self, producto, numero):
        self.cursor.execute(
        """SELECT * FROM experimento
        WHERE numero = {}
        AND nombre_producto = '{}';""".format(numero, producto))
        self.connection.commit()
        return db_experimento_to_dic(self.cursor.fetchone())

    def get_predicciones(self, producto):
        self.cursor.execute(
        """SELECT * FROM prediccion
        WHERE nombre_producto = '{}';
        """.format(producto)
        )
        self.connection.commit()
        return db_predicciones_to_dic_array(self.cursor.fetchall())

    def get_simulacion(self, producto): #hay algo mal
        """Regresa una lista con 9 tablas de arreglos con datos de simulación correspondientes a cada experimento en el producto.
        contempla también la demanda de la predicción. Osea que regresa el formato como para la ventana de simular"""
        self.cursor.execute("""SELECT experimento.numero, simulacion.mes, simulacion.nombre_producto, simulacion.inv_inicial, prediccion.demanda, simulacion.inv_final, simulacion.faltante, simulacion.orden
        FROM simulacion inner join prediccion ON simulacion.nombre_producto = prediccion.nombre_producto AND simulacion.mes = prediccion.mes
        inner join experimento ON experimento.nombre_producto = simulacion.nombre_producto AND simulacion.no_experimento = experimento.numero where simulacion.nombre_producto = '{}' group by experimento.numero, simulacion.mes""".format(producto))
        self.connection.commit()
        return self.cursor.fetchall()

    def get_simulacion_ordenada(self, producto):
        """Regresa un arreglo de listas con datos de la simulación, la columna demanda está incluida aunque no sea parte 
        de la tabla simular como tal"""
        print("obtiendo sim ordenada de '{}'".format(producto))
        conjunto = self.get_simulacion(producto)
        tablas = [[]]
        cont = 1
        ex = 0
        #acomodar dimension de experimentos
        for i in range(0, 12 * 9): #por cada mes de cada experimento
            if(cont == 13): #nuevo experimento
                cont = 1
                ex += 1
                tablas.append([]) #nuevo espacio para otro experimento
            
            tablas[ex].append(conjunto[i])
            cont += 1
        res = []
        c = 0

        for ex in tablas: #acomodar dimension por mes
            res.append([])
            meses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for mes in ex:
                print(mes)
                
                meses[utils.int_from_mes(mes[1]) - 1] = mes
            print("")
            res[c] = meses
            c += 1

        return res


sistema = SistemaProductos() #singleton i guess

def db_producto_to_dic(producto):
    """toma un arreglo que representa un producto extraido de la bd
    y lo convierte en un diccionario para su facil manipulacion"""
    pro = {'nombre': producto[0], 'c_pedido': producto[1],
    'c_faltante': producto[2], 'c_inventario': producto[3],
    'inv_inicial': producto[4]}
    return pro

def db_experimento_to_dic(experimento):
    """toma un arreglo que representa un experimento extraido de la bd
    y lo convierte en un diccionario para su facil manipulacion"""
    exp = {'nombre_producto': experimento[0], 'numero': experimento[1],
    'punto_reorden': experimento[2], 'cantidad_orden': experimento[3]}
    return exp

def db_predicciones_to_dic_array(predicciones):
    arreglo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for prediccion in predicciones:
        arreglo[utils.int_from_mes(prediccion[1]) - 1] = {'nombre_producto': prediccion[0],
        'mes': prediccion[1], 'demanda': prediccion[2]}
    return arreglo
    
if __name__ == '__main__':
    
    sistema.cursor.execute('select * from producto;')
    rows = sistema.cursor.fetchall()
    print('producto:')
    print('nombre|c_pedido|c_faltante|c_inventario|inicial')
    for row in rows:
        print(row)

    sistema.cursor.execute('select * from prediccion;')
    rows = sistema.cursor.fetchall()
    print('prediccion:')
    print('nombre|mes|demanda')
    for row in rows:
        print(row)
    
    sistema.cursor.execute('select * from experimento;')
    r2 = sistema.cursor.fetchall()
    print('experimento:')
    print('nombre|num|r|q')
    for row in r2:
        print(row)

    sistema.cursor.execute('select * from simulacion;')
    rows = sistema.cursor.fetchall()
    print('simulacion:')
    print('nombre|n_ex|mes|inicial|fina|falta|orden')
    for row in rows:
        print(row)

    sistema.cursor.execute('select * from historico;')
    rows = sistema.cursor.fetchall()
    print('historico:')
    print('nombre|anio|mes|demanda')
    for row in rows:
        print(row)

    print("simimi")
    print(sistema.get_simulacion('salchichas'))
    print(sistema.get_experimento('salchichas', 1))
    
