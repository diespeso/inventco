#!/usr/bin/python3.9

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

from interfaz.ventana import *

from app_inventario import SimInventario
from distribuidor_tabla import DistribuidorDeTabla
from parser_tablas import leer_archivo


#valores de espacio entre entradas y labels
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10

class InterfazAppInventario(Frame):
	#cualquier tab debe heredar de Frame (se importa con tkinter import *)
	def __init__(self, master):
		#OBLIGATORIO
		Frame.__init__(self, master)
		self.master = master
		#OBLIGATORIO

		self.q = 0
		self.r = 0
		self.inv_inicial = 0
		self.din_inventario = 0
		self.din_ordenar = 0
		self.din_faltante = 0
		self.din_total = 0.0

		self.entry_q = None
		self.entry_w = None
		self.entry_inv_inicial = None

		self.entry_meses = None

		self.entry_din_inventario = None
		self.entry_din_ordenar = None
		self.entry_din_faltante = None

		self.txt_simulacion = None
		self.txt_registros = None
		self.btn_simular = None
		self.simulacion = None #SimInventario

		self.txt_conclusion = None

		self.is_registros_iniciado = False
		self.btn_registrar = None
		self.registro_actual = None
		self.registros = []
		self.optimo = None

		self.numero = None

		self.entradas = None

		#OBLIGATORIO DEFINIR ESTA FUNCION DONDE SE CREARAN TODOS LOS COMPONENTES GRAFICOS
		self.init_interfaz()

	def init_interfaz(self):

		self.txt_simulacion = scrolledtext.ScrolledText(self,
			width=68, height=20)
		self.txt_simulacion.grid( columnspan =5, rowspan=3,
			column = 2,  row = 4, padx = p_x_l, pady = p_y)

		self.txt_registros = scrolledtext.ScrolledText(self,
			width=23, height= 10)
		self.txt_registros.grid( columnspan = 2,
			column = 0, row = 5, padx = p_x_l, pady = p_y)
		
		self.btn_simular = ttk.Button(self, text="Simular", command = self.simular)
		self.btn_simular.grid(
			column = 0, row = 2, padx = p_x_l, pady = p_y)

		self.btn_registrar = ttk.Button(self, text="Registrar", command = self.registrar_actual)
		self.btn_registrar.grid(
			column = 7, row = 5, padx = p_x_l, pady = p_y)


		self.add_labels()
		self.add_entradas()

		self.add_encabezado_simulacion()

	def set_numeros(self, numeros):
		self.numeros = numeros

	def add_labels(self):
		ttk.Label(self, text="Q:").grid(
			column = 0, row = 0, padx = p_x_l, pady = p_y)
		ttk.Label(self, text="R:").grid(
			column = 0, row = 1, padx = p_x_l, pady = p_y)
		ttk.Label(self, text="inicial:").grid(
			column = 2, row = 0, padx = p_x_l, pady = p_y)
		ttk.Label(self, text="meses:").grid(
			column = 2, row = 1, padx = p_x_l, pady = p_y)

		ttk.Label(self, text="Registros").grid(
			column = 0, row = 4, padx = p_x_l, pady = p_y)

		ttk.Label(self, text="$invent").grid(
			column = 4, row = 0, padx = p_x_l, pady = p_y)
		ttk.Label(self, text="$orden").grid(
			column = 4, row = 1, padx = p_x_l, pady = p_y)
		ttk.Label(self, text="$faltante").grid(
			column = 4, row = 2, padx = p_x_l, pady = p_y)

		ttk.Label(self, text="conclusion:").grid(
			column = 0, row = 7, padx = p_x_l, pady = p_y + 10)

	def add_entradas(self):
		self.entry_q = ttk.Entry(self, width=w)
		self.entry_q.grid(
			column = 1, row = 0, padx = 0, pady = 0)
		self.entry_r = ttk.Entry(self, width=w)
		self.entry_r.grid(
			column = 1, row = 1, padx = 0, pady = 0)
		self.entry_inv_inicial = ttk.Entry(self, width=w)
		self.entry_inv_inicial.grid(
			column = 3, row = 0, padx = p_x_l, pady = p_y)
		self.entry_meses = ttk.Entry(self, width=w)
		self.entry_meses.grid(
			column = 3, row = 1, padx = p_x_l, pady = p_y)

		self.entry_din_inventario = ttk.Entry(self, width=w)
		self.entry_din_inventario.grid(
			column = 5, row = 0, padx = p_x_l, pady = p_y)
		self.entry_din_ordenar = ttk.Entry(self, width=w)
		self.entry_din_ordenar.grid(
			column = 5, row = 1, padx = p_x_l, pady = p_y)
		self.entry_din_faltante = ttk.Entry(self, width=w)
		self.entry_din_faltante.grid(
			column = 5, row = 2, padx = p_x_l, pady = p_y)

		self.txt_conclusion = ttk.Entry(self, width=w * 6)
		self.txt_conclusion.grid(columnspan = 6,
			column = 1, row = 7, padx = p_x_l, pady = p_y + 10)


	def add_encabezado_simulacion(self):
		self.txt_simulacion.insert(INSERT,
			"n. mes\tmes\tinicial\tdemanda\tfinal\tfalta\torden\tmensual\n",
			"encabezado")
		self.txt_simulacion.tag_config("encabezado", foreground="blue")

	def limpiar_txt_simulacion(self):
		self.txt_simulacion.delete("1.0", END)
		self.add_encabezado_simulacion()

	def capturar_datos(self):
		self.entradas = self.validar_entradas()
		if self.entradas:
			self.q = self.entradas["q"]
			self.r = self.entradas["r"]
			self.inv_inicial = self.entradas["inv_inicial"]
			self.din_inventario = self.entradas["din_inventario"]
			self.din_ordenar = self.entradas["din_ordenar"]
			self.din_faltante = self.entradas["din_faltante"]
			self.meses = self.entradas["meses"]
			if self.numeros:
				self.simulacion = SimInventario(self.q, self.r, self.inv_inicial, self.numeros)
				tablas = self.leer_archivos_tablas()
				self.simulacion.set_distribucion_demanda(
					DistribuidorDeTabla(tablas["demanda"]))
				self.simulacion.set_factores_estacionales(
					tablas["factores"])
				self.simulacion.set_distribucion_entrega(
					DistribuidorDeTabla(tablas["p_entregas"]))
			else:
				print("no se inicializó números")

	def validar_entradas(self):
		captura = {}
		try:
			captura["q"] = int(self.entry_q.get())
			captura["r"] = int(self.entry_r.get())
			captura["inv_inicial"] = int(self.entry_inv_inicial.get())
			captura["din_inventario"] = int(self.entry_din_inventario.get())
			captura["din_ordenar"] = int(self.entry_din_ordenar.get())
			captura["din_faltante"] = int(self.entry_din_faltante.get())
			captura["meses"] = int(self.entry_meses.get())

		except Exception as e:
			messagebox.showwarning(message="Revise las entradas, hay un error.", title="Fallo al leer entradas")
			return None
		return captura

	def leer_archivos_tablas(self):
		demanda = leer_archivo("demanda")
		factores = leer_archivo("factores")
		p_entregas = leer_archivo("espera")

		return {"demanda": demanda,
		"factores": factores,
		"p_entregas": p_entregas}

	def actualizar_registros(self):
		"""Lee todos los renglones del registro
		y decide cual es el menor para marcarlo
		"""
		self.mostrar_registros()
		pass

	def mostrar_registros(self):
		"""muestra todos los registros en el cuado de registros
		"""
		self.limpiar_txt_registros()

		if len(self.registros) >= 2:
			optimo = self.get_mejor_registro()
			self.actualizar_conclusion()
		else:
			optimo = None
		print(optimo)
		for i in range(0, len(self.registros)):
			registro = self.registros[i]
			str_registro = "Q= {}, R= {}, Costo= ${}".format(
				registro["q"], registro["r"], registro["costo"])
			if optimo:
				if i == optimo:
					self.txt_registros.insert(INSERT,
						str_registro + "\n", "optimo")
					continue # pasa al siguiente
			self.txt_registros.insert(INSERT,
						str_registro + "\n")
		self.txt_registros.tag_config("optimo", foreground="green")

	def limpiar_txt_registros(self):
		self.txt_registros.delete("1.0", END)

	def actualizar_conclusion(self):
		self.txt_conclusion.delete(0, 'end') #limpiar
		self.txt_conclusion.insert(0, 
			"La mejor solución se da cuando Q = {} y R = {}, con un costo de ${}".format(
				self.optimo["q"], self.optimo["r"], self.optimo["costo"]))


	def get_mejor_registro(self):
		""" compara todos los registros y devuelve el mas barato,
		tambien actualiza el registro self.optimo a ese mas barato
		"""
		index = 0
		menor = self.registros[index]
		for i in range(0, len(self.registros)):
			if self.registros[i]["costo"] < menor["costo"]:
				menor = self.registros[i]
				index = i
		self.optimo = self.registros[index]

		#revisar si se repiten los menores
		repetidos = 0
		for i in range(0, len(self.registros)):
			if self.registros[i]["costo"] == menor["costo"]:
				repetidos += 1
		if repetidos >= 2:
			messagebox.showwarning(message="El costo mínimo se repite, cualquiera que se elija será el correcto.")
		return index

	def simular(self):
		#prueba: self.limpiar_txt_simulacion()
		self.limpiar_txt_simulacion()
		self.capturar_datos()
		if self.entradas:
			for i in range(0, self.meses):
				self.txt_simulacion.insert(INSERT,
					self.simulacion.simular() + "\n"
				);
			self.armar_registro_actual()

	def armar_registro_actual(self):
		"""Solo debe ser llamada luego de terminar una simulación
		arma una estructura de diccionario registro
		"""
		self.registro_actual = {}
		self.registro_actual["q"] = self.q
		self.registro_actual["r"] = self.r
		self.registro_actual["costo"] = self.simulacion.obtener_costo(
			self.din_faltante, self.din_ordenar, self.din_inventario)

	def registrar_actual(self):
		"""Añade el registro actual al arreglo
		"""
		if self.simulacion.is_simulado:
			if not self.registro_actual in self.registros: #si no se ha registrado antes
				self.registros.append(self.registro_actual)
				self.is_registros_iniciado = True
			self.mostrar_registros()
