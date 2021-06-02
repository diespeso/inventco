from tkinter import *
from tkinter import ttk #importar cosas que vaya a utilizar de tkinter, a veces
                        #necesitarán importar aparte otras cosas como messageboxes
from tkinter import messagebox

from interfaz.ventana import * #importar modulo de la ventana

from sistema_db import db_productos;
from sistema_db.db_productos import sistema;

import json

#valores de espacio entre entradas y labels 
#estos son valores de estilo que elegi cuando hice la app, pueden solo copiarlos y pegarlos
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10


class InterfazAppRegistrar(Frame):
    #hacer que tu pestaña herede de Frame
    def __init__(self, master):
        #el constructor debe llamar al constructor de su padre.
        Frame.__init__(self, master)
        self.master = master
        #aqui termina la parte obligatoria del constructor

        #definir todas las variables que queramos obtener de esta pestaña
        #recomiendo inicializar sus tipos de forma explicita
        self.nombre_producto = ""
        self.costo_pedido = 0.0
        self.costo_faltante = 0.0
        self.costo_inventario = 0.0 #costo por tenerlo en el inventario
        self.inventario_inicial = 0
        self.punto_reorden = 0
        self.cantidad_ordenar = 0

        #definir todos los elementos graficos estaticos que usaremos,
        #inicializarlos a None
        #si son entradas prefijo entry, botones btn, si son labels lbl o txt
        self.entry_nombre_producto = None
        self.entry_costo_pedido = None
        self.entry_costo_faltante = None
        self.entry_costo_inventario = None
        self.entry_inventario_inicial = None
        self.entry_punto_reorden = None
        self.entry_cantidad_ordenar = None 

        self.btn_registrar = None
         
        #busqueda
        self.entry_busqueda = None
        self.btn_buscar = None
        self.lbl_encontrado = None

        #OBLIGATORIO DEFINIR ESTA FUNCION DONDE SE CREARAN TODOS LOS COMPONENTES GRAFICOS
        self.init_interfaz()

    def init_interfaz(self):
        #aqui se crean todos los componentes graficos estaticos
        #osea componentes que se veran en cuanto se abra esta pestaña

        #a mi me gusta separar la creacion de entradas y labels y ponerla
        #en dos funciones porque suelen ser muchas, pero ustedes decidan
        self.add_labels()
        self.add_entradas()
        

        #al final establecer los botones
        #asi se crea un button, command es una funcion que se llamara cada vez
        #que se de click en el boton, esta funcion debe aceptar solo self como argumento
        self.btn_registrar = ttk.Button(self, text="Registrar", command=self.registrar)
        #luego de crearlo debemos ponerlo en la pestaña
        self.btn_registrar.grid(column=2, row=10)
        self.add_ui_buscar()

    def add_ui_buscar(self):
        ttk.Label(self, text='Cargar producto:').grid(
            column = 3, row = 2, padx = p_x_l, pady = p_y
        )
        self.entry_busqueda = ttk.Entry(self, width=w * 2)
        self.entry_busqueda.grid(
            column = 4, row = 2, padx=p_x_l, pady = p_y
        )
        self.btn_buscar = ttk.Button(self, text="Buscar", command=self.buscar_producto)
        self.btn_buscar.grid(
            column = 5, row = 2, padx = p_x_l, pady = p_y
        )

        self.lbl_encontrado = ttk.Label(self)
        self.lbl_encontrado.grid(
            column = 7, row = 3, padx = p_x_l, pady = p_y
        )

    def buscar_producto(self):
        nombre_producto = self.entry_busqueda.get()
        if nombre_producto in sistema.get_productos():
            self.master.nombre_producto = nombre_producto #establecer que ahora estaremos trabajando con este producto
            self.cargar_producto(nombre_producto)
        else:
            messagebox.showwarning(title = 'Producto no encontrado' ,message='Ese producto no existe')
    def add_labels(self):
        #recomiendo poner en orden las labels y recordar
        #que primero es label y a su derecha una entrada
        #esta label esta en (1,2), su entry debe estar en (2,2)
        ttk.Label(self, text="Nombre del producto:").grid(
            column = 1, row = 2, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Costo por pedido:").grid(
            column = 1, row = 3, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text ="Costo por faltante:").grid(
            column = 1, row = 4, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Costo de almacén:").grid(
            column = 1, row = 5, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Inventario actual:").grid(
            column = 1, row = 6, padx = p_x_l, pady = p_y
        )

        ttk.Label(self, text="Cantidad por orden:").grid(
            column = 1, row = 8, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Punto de reorden:").grid(
            column = 1, row = 9, padx = p_x_l, pady = p_y
        )
    
    def add_entradas(self):
        #hacer la entrada, w esta declarada hasta arriba en este archivo
        self.entry_nombre_producto = ttk.Entry(self, width=w*2) 
        self.entry_nombre_producto.grid(column = 2, row = 2, padx = p_x_l, pady = p_y)
        
        self.entry_costo_pedido = ttk.Entry(self, width=w)
        self.entry_costo_pedido.grid(column = 2, row = 3, padx = p_x_l, pady = p_y)

        self.entry_costo_faltante = ttk.Entry(self, width=w)
        self.entry_costo_faltante.grid(column = 2, row = 4, padx = p_x_l, pady = p_y)

        self.entry_costo_inventario = ttk.Entry(self, width=w)
        self.entry_costo_inventario.grid(column = 2, row = 5, padx = p_x_l, pady = p_y)

        self.entry_inventario_inicial = ttk.Entry(self, width=w)
        self.entry_inventario_inicial.grid(column =2, row = 6, padx = p_x_l, pady = p_y)

        self.entry_cantidad_ordenar = ttk.Entry(self, width=w)
        self.entry_cantidad_ordenar.grid(column = 2, row = 8, padx = p_x_l, pady = p_y)

        self.entry_punto_reorden = ttk.Entry(self, width=w)
        self.entry_punto_reorden.grid(column = 2, row = 9, padx = p_x_l, pady = p_y)
    
    def registrar(self):
        entradas = self.validar_entradas()
        j = json.dumps(entradas)
        sistema.registrar_producto(j)
        self.nombre_producto = entradas['nombre']
        self.master.nombre_producto = self.nombre_producto
        #almacenar

        
    def cargar_producto(self, nombre_producto):
        self.limpiar_entries()
        producto = sistema.get_producto(nombre_producto)
        exp = sistema.get_experimento(nombre_producto, 0) #el primero es el original
        #cargar vars
        self.nombre_producto = producto['nombre']
        self.costo_pedido = producto['c_pedido']
        self.costo_faltante = producto['c_faltante']
        self.costo_inventario = producto['c_inventario']
        self.inv_inicial = producto['inv_inicial']
        self.punto_reorden = exp['punto_reorden']
        self.cantidad_ordenar = exp['cantidad_orden']
        #cargar entries
        self.entry_nombre_producto.insert(0, "{}".format(self.nombre_producto))
        self.entry_costo_pedido.insert(0, "{}".format(self.costo_pedido))
        self.entry_costo_faltante.insert(0, "{}".format(self.costo_faltante))
        self.entry_costo_inventario.insert(0, "{}".format(self.costo_inventario))
        self.entry_inventario_inicial.insert(0, "{}".format(self.inv_inicial))
        self.entry_cantidad_ordenar.insert(0, "{}".format(self.cantidad_ordenar))
        self.entry_punto_reorden.insert(0, "{}".format(self.punto_reorden))
        

    def limpiar_entries(self):
        self.entry_nombre_producto.delete(0, 'end')
        self.entry_costo_pedido.delete(0, 'end')
        self.entry_costo_faltante.delete(0, 'end')
        self.entry_costo_inventario.delete(0, 'end')
        self.entry_inventario_inicial.delete(0, 'end')
        self.entry_cantidad_ordenar.delete(0, 'end')
        self.entry_punto_reorden.delete(0, 'end')

    def validar_entradas(self):
        captura = {}
        try:
            captura["nombre"] = self.entry_nombre_producto.get()
            captura["costo_pedido"] = float(self.entry_costo_pedido.get())
            captura["costo_faltante"] = float(self.entry_costo_faltante.get())
            captura["costo_inventario"] = float(self.entry_costo_inventario.get())
            captura["inventario_inicial"] = int(self.entry_inventario_inicial.get())
            captura["cantidad_orden"] = int(self.entry_cantidad_ordenar.get())
            captura["punto_reorden"] = int(self.entry_punto_reorden.get())
        except Exception as e:
            messagebox.showwarning(message="Revise que los datos del producto sean correctos.", title="Error al leer los datos")
            return None
        #self.set_nombre_producto(captura['nombre'])
        return captura

    def set_nombre_producto(self, nombre):
        self.nombre_producto = nombre
        #sistema.set_nombre_producto(nombre)