from tkinter import *
from tkinter import ttk

from sistema_db.db_productos import sistema

#valores de espacio entre entradas y labels 
#estos son valores de estilo que elegi cuando hice la app, pueden solo copiarlos y pegarlos
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10

class InterfazAppResultados(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        ttk.Label(self, text="Producto").grid(column = 0, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="R óptima").grid(column = 1, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="Q óptima").grid(column = 2, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="Gráfica").grid(column = 3, row = 0, padx = p_x_l, pady = p_y)
        #mockup
        ttk.Label(self, text="Producto1").grid(column = 0, row = 1, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="100").grid(column = 1, row = 1, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="200").grid(column = 2, row = 1, padx = p_x_l, pady = p_y)
        ttk.Button(self, text="ver").grid(column = 3, row = 1, padx = p_x_l, pady = p_y)
        self.init_interfaz()
    
    def init_interfaz(self):
        pass