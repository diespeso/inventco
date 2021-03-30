from tkinter import *
from tkinter import ttk

from interfaz.ventana import * 

#from app_alimentar import Alimentar

from sistema_db import db_productos
from sistema_db import tabla_historico

from utils import MESES

#valores de espacio entre entradas y labels 
#estos son valores de estilo que elegi cuando hice la app, pueden solo copiarlos y pegarlos
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10

class InterfazAppAlimentar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.nombre_producto = None

        self.lista_demandas = []
        self.anio_uno = []
        self.anio_dos = []
        self.anio_tres = []

        self.entries_anio_uno = []
        self.entries_anio_dos = []
        self.entries_anio_tres = []

        self.entry_busqueda = None
        self.btn_buscar = None
        self.lbl_encontrado = None

        self.btn_alimentar = None

        self.init_interfaz()

    def init_interfaz(self):
        self.add_anios()
        self.add_ui_buscar()

        self.btn_alimentar = ttk.Button(self, text="Alimentar", command=self.alimentar)
        self.btn_alimentar.grid(column = 2, row=14)

    def add_anios(self):
        #anio uno
        self.entries_anio_uno = [] #reboot
        for mes in range(0, 12):
            ttk.Label(self, text=MESES[mes]).grid(
                column = 0, row = mes, padx = p_x_l, pady = p_y
            )
            self.entries_anio_uno.append(ttk.Entry(self, width=w))
            self.entries_anio_uno[mes].grid(column = 1, row = mes, padx=p_x_l, pady =p_y)
        #anio dos
        self.entries_anio_dos= [] #reboot
        for mes in range(0, 12):
            ttk.Label(self, text=MESES[mes]).grid(
                column = 2, row = mes, padx = p_x_l, pady = p_y
            )
            self.entries_anio_dos.append(ttk.Entry(self, width=w))
            self.entries_anio_dos[mes].grid(column = 3, row = mes, padx=p_x_l, pady =p_y)
        #anio tres
        self.entries_anio_tres = [] #reboot
        for mes in range(0, 12):
            ttk.Label(self, text=MESES[mes]).grid(
                column = 4, row = mes, padx = p_x_l, pady = p_y
            )
            self.entries_anio_tres.append(ttk.Entry(self, width=w))
            self.entries_anio_tres[mes].grid(column = 5, row = mes, padx=p_x_l, pady =p_y)
    
    def add_ui_buscar(self):
        ttk.Label(self, text='Buscar producto:').grid(
            column = 7, row = 0, padx = p_x_l, pady = p_y
        )
        self.entry_busqueda = ttk.Entry(self, width=w * 2)
        self.entry_busqueda.grid(
            column = 8, row = 0, padx=p_x_l, pady = p_y
        )
        self.btn_buscar = ttk.Button(self, text="Buscar", command=self.buscar_producto)
        self.btn_buscar.grid(
            column = 9, row = 0, padx = p_x_l, pady = p_y
        )

        self.lbl_encontrado = ttk.Label(self)
        self.lbl_encontrado.grid(
            column = 7, row = 1, padx = p_x_l, pady = p_y
        )

    def buscar_producto(self):
        producto = self.entry_busqueda.get()
        print(producto)
        self.lbl_encontrado.config(text = 'esto')
        t = tabla_historico.TablaHistorico().from_db(producto)
        print("tabla t: {}".format(t))
        #cargar demanda del producto
    
    def alimentar(self):
        demandas = []
        
        demandas.append([])
        for i in range(0, len(self.entries_anio_uno)):
            demandas[0].append(self.entries_anio_uno[i].get())
        
        demandas.append([])
        for i in range(0, len(self.entries_anio_dos)):
            demandas[1].append(self.entries_anio_dos[i].get())

        demandas.append([])
        for i in range(0, len(self.entries_anio_tres)):
            demandas[2].append(self.entries_anio_tres[i].get())

        t = tabla_historico.TablaHistorico()
        t.from_tabla(demandas)
        #t.set_nombre_producto(self.master.nombre_producto)
        t.to_db(self.master.nombre_producto)


            