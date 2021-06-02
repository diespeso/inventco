from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from interfaz.ventana import * 

#from app_alimentar import Alimentar

from sistema_db import db_productos
from sistema_db import tabla_historico
from sistema_db.db_productos import sistema

from app_prediccion import sistema_prediccion
from motor_experimentos import MotorExperimentos

from utils import MESES
from utils import try_parse_demanda_entry
from utils import set_entry
from utils import demanda_or_empty

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
        #se inicializa con el producto que estaba en registrar, podria ser none
        #si no se registro o si estaba duplicado
        self.nombre_producto = None

        self.lista_demandas = []
        self.anio_uno = []
        self.anio_dos = []
        self.anio_tres = []

        self.entries_anio_uno = []
        self.entries_anio_dos = []
        self.entries_anio_tres = []


        self.btn_alimentar = None
        self.btn_guardar = None

        self.init_interfaz()

    def init_interfaz(self):
        self.add_anios()

        self.btn_alimentar = ttk.Button(self, text="Alimentar", command=self.alimentar)
        self.btn_alimentar.grid(column = 2, row=14)

        self.btn_guardar = ttk.Button(self, text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column = 3, row = 14)


    #todo: mejorar   
    def buscar_producto(self, nombre_producto):
            th = tabla_historico.TablaHistorico()
            if th.from_db(nombre_producto):
                #self.lbl_encontrado.config(text = 'producto encontrado')
                demandas = th.demandas
                self.cargar_demandas(demandas)
                
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

    def registrar_experimentos(self, nombre_producto):
        dic = sistema.get_producto(nombre_producto)
        ex = sistema.get_experimento(nombre_producto, 0) #el original
        motor = MotorExperimentos(ex['cantidad_orden'], ex['punto_reorden'], dic['inv_inicial'], sistema.get_predicciones(nombre_producto))
        motor.to_bd(nombre_producto)
        
    
    def alimentar(self):
        """triggerea la predicción y con ello el llenar la ventana de simulación"""
        
        t = self.guardar()
        if t.is_complete():
            sistema_prediccion.predecir_producto(self.nombre_producto, t)
            sistema_prediccion.leer_y_registrar_prediccion(self.nombre_producto)

            self.master.nombre_producto = self.nombre_producto
            self.registrar_experimentos(self.master.nombre_producto)
        else:
            messagebox.showerror(message="No se puede alimentar una tabla incompleta", title="Fallo al alimentar.")

        #revisar si las demandas estan completas
        #si si lo estan, alimentar y producir la simulación
    
    def revisar_y_advertir(self):
        """revisa todas las entradas de demanda y si encuentra alguna que no pueda
        convertir a null o a un entero, entonces manda un messagebox, y aparte muestra
        en rojo la entry exacta donde está el error
        
        si todo sale bien, regresa una array 2D con las demandas sean numeros o nulls"""
        demandas = []
        flag_error = False

        demandas.append([])
        for i in range(0, len(self.entries_anio_uno)):
            demanda = try_parse_demanda_entry(self.entries_anio_uno[i])
            if demanda == None: #dato invalido
                #colorear rojo
                self.entries_anio_uno[i].configure(foreground="#ff0000")
                flag_error = True
            else:
                self.entries_anio_uno[i].configure(foreground='#000000')
                demandas[0].append(demanda)

        demandas.append([])
        for i in range(0, len(self.entries_anio_dos)):
            demanda = try_parse_demanda_entry(self.entries_anio_dos[i])
            if demanda == None:
                self.entries_anio_dos[i].configure(foreground="#ff0000")
                flag_error = True
            else:
                self.entries_anio_dos[i].configure(foreground="#000000")
                demandas[1].append(demanda)

        demandas.append([])
        for i in range(0, len(self.entries_anio_tres)):
            demanda = try_parse_demanda_entry(self.entries_anio_tres[i])
            if demanda == None:
                self.entries_anio_tres[i].configure(foreground="#ff0000")
                flag_error = True
            else:
                self.entries_anio_tres[i].configure(foreground='#000000')
                demandas[2].append(demanda)
        if flag_error:
            messagebox.showerror(message="Revise las entradas de demanda", title="Error al interpretar demandas")
            return None #falló, no regresar la tabla de demandas
        else:
            return demandas

    def guardar(self):
        """intenta guardar una tabla de demandas de la interfaz sin importar si está
        completa o no, regresa la tabla obtenida siempre y cuando no haya habido errores
        en parsing

        """
        demandas = self.revisar_y_advertir()
        
        if demandas != None:
            t = tabla_historico.TablaHistorico()
            t.from_tabla(demandas)
            #t.set_nombre_producto(self.master.nombre_producto)
            self.nombre_producto = tabla_historico.sistema.producto_actual
            self.master.nombre_producto = self.nombre_producto
            if self.nombre_producto == None:
                messagebox.showerror(message="No se pueden editar las demandas", title='Producto no encontrado o no editable')
                return
            t.to_db(self.nombre_producto)
        return t

    def cargar_demandas(self, demandas):
        #hace lo contrario que guardar: toma una tabla de 36 demandas y la muestra en las entradas de texto
        for i in range(0, 12):
            set_entry(self.entries_anio_uno[i], demanda_or_empty(demandas[0][i]))
        for i in range(0, 12):
            set_entry(self.entries_anio_dos[i], demanda_or_empty(demandas[1][i]))
        for i in range(0, 12):
            set_entry(self.entries_anio_tres[i], demanda_or_empty(demandas[2][i]))
       


            