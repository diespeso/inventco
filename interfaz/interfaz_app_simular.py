from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from interfaz.ventana import * 

from utils import MESES
import utils

from sistema_db.db_productos import sistema;

#valores de espacio entre entradas y labels 
#estos son valores de estilo que elegi cuando hice la app, pueden solo copiarlos y pegarlos
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10

class InterfazAppSimular(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.btn_anterior = None
        self.btn_siguiente = None

        self.renglones = []
        self.contador = 0

        self.simulaciones = None
        self.exps = []
        self.c_exps = 0

        self.lbl_counter = ttk.Label(self, text="uwu")
        self.lbl_counter.grid(column = 3, row = 14, padx = p_x_l, pady = p_y)

        self.entry_q = None
        self.entry_r = None

        self.init_interfaz()

    def init_interfaz(self):
        self.add_columnas()
        self.add_meses()
        self.add_entries_inicial()

        self.btn_anterior = ttk.Button(self, text="<", command=self.ir_anterior)
        self.btn_anterior.grid(column = 0, row = 14)

        self.btn_siguiente = ttk.Button(self, text=">", command = self.ir_siguiente)
        self.btn_siguiente.grid(column = 6, row = 14)

        ttk.Label(self, text="Q:").grid(column = 6, row = 1, padx = p_x_l, pady = p_y)
        self.entry_q = ttk.Entry(self, width=w)
        self.entry_q.grid(column = 7, row = 1, padx = p_x_l, pady = p_y)
        
        self.entry_r = ttk.Entry(self, width=w)
        self.entry_r.grid(column = 7, row = 2, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="R:").grid(column = 6, row = 2, padx = p_x_l, pady = p_y)

    def correr(self):
        self.simulaciones = sistema.get_simulacion_ordenada(self.master.nombre_producto) #depende de que interfaz_app_alimentar inicialice self.master.nombre_producto
        for i in range(0, 9):
            self.exps.append(sistema.get_experimento(self.master.nombre_producto, i))
        self.cargar_tabla()

    def cargar_tabla(self):
        #limpiar todo
        self.limpiar_tabla()
        self.lbl_counter.config(text='{}/9'.format(self.c_exps + 1))
        simulacion = self.simulaciones[self.contador]
        print(simulacion)

        self.entry_q.insert(0, "{}".format(self.exps[self.c_exps]['cantidad_orden']))
        self.entry_r.insert(0, "{}".format(self.exps[self.c_exps]['punto_reorden']))

        for mes in range(0, len(simulacion)):
            self.renglones[mes]['inicial'].insert(0, "{}".format(simulacion[mes][3]))
            self.renglones[mes]['demanda'].insert(0, "{}".format(simulacion[mes][4]))
            self.renglones[mes]['final'].insert(0, "{}".format(simulacion[mes][5]))
            self.renglones[mes]['faltante'].insert(0, "{}".format(simulacion[mes][6]))
            if simulacion[mes][7] == None:
                self.renglones[mes]['orden'].insert(0, "-")
            else:
                self.renglones[mes]['orden'].insert(0, "{}".format(simulacion[mes][7]))
    def ir_anterior(self):
        if self.contador == 0:
            self.contador = len(self.simulaciones) - 1
            self.c_exps = len(self.simulaciones) - 1
        else:
            self.contador -= 1
            self.c_exps -= 1
        self.cargar_tabla()

    def ir_siguiente(self):
        if self.contador == len(self.simulaciones) - 1:
            self.contador = 0
            self.c_exps = 0
        else:
            self.contador += 1
            self.c_exps += 1
        self.cargar_tabla()

    def limpiar_tabla(self):
        self.entry_q.delete(0, 'end')
        self.entry_r.delete(0, 'end')
        for renglon in self.renglones:
            for llave in renglon:
                renglon[llave].delete(0, 'end')

    def add_columnas(self):
        ttk.Label(self, text="Mes").grid(
            column = 0, row = 0, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Inicial").grid(
            column = 1, row = 0, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Demanda").grid(
            column = 2, row = 0, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Final").grid(
            column = 3, row = 0, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Faltante").grid(
            column = 4, row = 0, padx = p_x_l, pady = p_y
        )
        ttk.Label(self, text="Orden").grid(
            column = 5, row = 0, padx = p_x_l, pady = p_y
        )
    
    def add_meses(self):
        for i in range(0, len(MESES)):
            ttk.Label(self, text=utils.to_mes(i + 1)).grid(
                column = 0, row = i + 1, padx = p_x_l, pady = p_y
            )

    def add_entries_inicial(self):
        c = 1
        for i in range(1, 13):
            inicial = ttk.Entry(self, width=w)
            inicial.grid(column = 1, row = i, padx = p_x_l, pady = p_y)
            demanda = ttk.Entry(self, width=w)
            demanda.grid(column = 2, row = i, padx = p_x_l, pady = p_y)
            final = ttk.Entry(self, width=w)
            final.grid(column = 3, row = i, padx = p_x_l, pady = p_y)
            faltante = ttk.Entry(self, width=w)
            faltante.grid(column = 4, row = i, padx = p_x_l, pady = p_y)
            orden = ttk.Entry(self, width=w)
            orden.grid(column = 5, row = i, padx = p_x_l, pady = p_y)
            self.renglones.append({"inicial": inicial, "demanda": demanda, "final": final, "faltante": faltante, "orden": orden})
            c += 1
