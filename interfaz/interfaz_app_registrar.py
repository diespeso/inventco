from tkinter import *
from tkinter import ttk

from interfaz.ventana import *

#from appRegistrar import Registrar
#
#este es un ejemplo, deben separar la funcionalidad del apartado grafico
#yo generalmente primero programo "un motor" que hace todo lo que necesito sin gui
#y luego lo importo para usarlo conectando entrys de la interfaz a atributos
# del objeto. haganlo asi, muy recomendado.

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
        self.punto_reorden = 0
        self.cantidad_ordenar = 0

        #definir todos los elementos graficos estaticos que usaremos,
        #inicializarlos a None
        #si son entradas prefijo entry, botones btn, si son labels lbl o txt
        self.entry_nombre_producto = None
        self.entry_costo_pedido = None
        self.entry_costo_faltante = None
        self.entry_costo_inventario = None
        self.entry_punto_reorden = None
        self.entry_cantidad_ordenar = None 

        self.btn_registrar = None

        #definir los componentes que harán el trabajo de procesamiento de los
        #datos, osea el motor que se haya programado,
        #si el constructor no necesita datos, entonces hacer el objeto de una
        #vez
        #self.registrar = None #el constructor necesita datos
        #self.registrar = Registrar() # el constructor no necesita datos

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
        self.btn_registrar.grid(column=1, row=3)

    def add_labels(self):
        #recomiendo poner en orden las labels y recordar
        #que primero es label y a su derecha una entrada
        #esta label esta en (1,2), su entry debe estar en (2,2)
        ttk.Label(self, text="Nombre:").grid(
            column = 1, row = 2, padx = p_x_l, pady = p_y)
    
    def add_entradas(self):
        #hacer la entrada, w esta declarada hasta arriba en este archivo
        self.entry_nombre_producto = ttk.Entry(self, width=w) 
        self.entry_nombre_producto.grid(column = 2, row = 2, padx = p_x_l, pady = p_y)
    
    def registrar(self):
        #ejemplo: tomamos el valor que se haya introducido en la entrada de nombre
        #de producto
        self.nombre_producto = self.entry_nombre_producto.get()
        #lo imprimimos en consola
        print(self.nombre_producto)
        pass #aqui deberia ir el codigo que use las variables de este modulo
        #para realizar procesos cuando se haga click en btn_registrar