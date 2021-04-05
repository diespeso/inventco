from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from utils import MESES
import utils

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

        self.init_interfaz()

    def init_interfaz(self):
        self.add_columnas()
        self.add_meses()
        self.add_entries_inicial()

        self.btn_anterior = ttk.Button(self, text="<", command=self.ir_anterior)
        self.btn_anterior.grid(column = 0, row = 14)

        self.btn_siguiente = ttk.Button(self, text=">", command = self.ir_siguiente)
        self.btn_siguiente.grid(column = 6, row = 14)
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
        pass

    def ir_anterior(self):
        pass
    def ir_siguiente(self):
        pass