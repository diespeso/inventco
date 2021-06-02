#!/usr/bin/pyhton3

from tkinter import ttk
from tkinter import *
import tksvg

import os

from interfaz.interfaz_app_inventario import InterfazAppInventario

#importamos la clase pestaña que construimos
from interfaz.interfaz_app_registrar import InterfazAppRegistrar
from interfaz.interfaz_app_alimentar import InterfazAppAlimentar
from interfaz.interfaz_app_simular import InterfazAppSimular
from interfaz.interfaz_app_resultados import InterfazAppResultados


class Ventana(Frame):
	# solo hay una ventana en el programa, aqui se añaden las pestañas que se vayan a usar.
	def __init__(self, master=None): #constructor de la ventana
		Frame.__init__(self, master)
		self.master = master
		"""
		ventana = Toplevel()
		ventana.geometry("800x400")
		ventana.title("Serie de tiempo de Salchichas")
		print(os.path.join(os.path.dirname(__file__), 'salchichas.svg'))
		image = tksvg.SvgImage(file=os.path.join(os.path.dirname(__file__), 'salchichas.svg'))
		label = Label(ventana, image=image)
		label.image = image
		label.grid(column = 0, row = 0)
		"""
		self.nombre_producto = None
		#declarar todas las pestañas (tabs) que contendrá esta ventana
		self.tab_control = None #controlador que tiene las pestañas
		#self.tab_inventario = None #pestaña del inventario
		self.tab_regitrar = None
		self.tab_alimentar = None
		self.tab_simular = None
		self.tab_resultados = None

		self.init_window() #tareas antes de mostrar ventana
		self.tab_control.bind("<<NotebookTabChanged>>", self.configure_tab_control) #cuando cambia la pestaña, ir a esta funcion


	def init_window(self):
		self.master.title("Simulador de puntos de Reorden Inventco.")
		self.crear_tabs()
	
		self.grid(column = 0, row = 0)
		#self.pack(fill=BOTH, expand=1)

	def configure_tab_control(self, event):
		print(self.tab_control.tab(self.tab_control.select(), "text"))
		if self.tab_control.tab(self.tab_control.select(), "text") == "Registrar":
			pass
		elif self.tab_control.tab(self.tab_control.select(), "text") == "Alimentar":
			pass
		elif self.tab_control.tab(self.tab_control.select(), "text") == "Simular":
			self.tab_simular.correr()
		elif self.tab_control.tab(self.tab_control.select(), 'text') == "Resultados":
			self.tab_resultados.borrar_graficos()
			self.tab_resultados.add_resultados()
		#elif self.tab_control.tab(self.tab_control.select(), "text") == "Resultados":
		#	pass
		self.rellenar_tabs_de_aplicacion()	


	def rellenar_tabs_de_aplicacion(self):
		#aqui se ponen las funciones que rellenan a todas las tabs a usar
		#self.rellenar_tab_inventario()
		pass

	def rellenar_tab_inventario(self):
		#antes se usaba porque habia generador, ahora no hace nada
		#self.tab_inventario.set_numeros(self.tab_generador.generador.get_generacion())
		pass
	

	def crear_tabs(self):
		#crea el control de tabs y todas las tabs de la app
		self.tab_control = ttk.Notebook(self) # tab de control, no es visible pero es el padre de las demas

		self.tab_registrar = InterfazAppRegistrar(self.tab_control)
		self.tab_control.add(self.tab_registrar, text="Registrar")

		self.tab_alimentar = InterfazAppAlimentar(self.tab_control)
		self.tab_control.add(self.tab_alimentar, text="Alimentar")

		self.tab_simular = InterfazAppSimular(self.tab_control)
		self.tab_control.add(self.tab_simular, text= "Simular")
		#se crean los objetos de las pestañas y se añaden a esta ventana
		#self.tab_inventario = InterfazAppInventario(self.tab_control) # se crea una nueva tab, en este caso es una interfazappinventario, se envia al padre que es tab_control
		#self.tab_control.add(self.tab_inventario, text="Inventarios") # se agrega a tab control la nueva tab creada y se pone su titulo "inventarios"
		self.tab_resultados = InterfazAppResultados(self.tab_control)
		self.tab_control.add(self.tab_resultados, text = "Resultados")


		self.tab_control.grid(column= 1, row = 1) #todas las tabs aparecen empezando en la col 1, fila 1.

