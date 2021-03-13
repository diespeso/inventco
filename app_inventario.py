#!/usr/bin/python3.9
precision = 3

import sys


from distribuidor_tabla import DistribuidorDeTabla
from parser_tablas import leer_archivo

def numero_a_mes(num):
	if num == 0:
		return "ENE"
	elif num == 1:
		return "FEB"
	elif num == 2:
		return "MAR"
	elif num == 3:
		return "ABR"
	elif num == 4:
		return "MAY"
	elif num == 5:
		return "JUN"
	elif num == 6:
		return "JUL"
	elif num == 7:
		return "AGO"
	elif num == 8:
		return "SEP"
	elif num == 9:
		return "OCT"
	elif num == 10:
		return "NOV"
	elif num == 11:
		return "DIC"




class Pedido:
	"""Representa una pedido,
	se debe de llamar intentar_entregar a cada paso de la simulación
	el pedido va disminuyendo su contador de meses cada vez que se llama
	esta funcion, y una vez que se acabe el contador, regresa la cantidad
	del pedido, lo entrega.
	"""
	def __init__(self, q, meses):
		"""
		q: cantidad del pedido
		meses: longitud de meses para recibir el pedido
		"""
		self.q = q
		self.meses = meses

	def intentar_entregar(self):
		"""debe llamarse cada vez que la simulación dé un paso
		"""
		if self.meses == 0:
			return self.q
		else:
			self.meses -= 1



class SimInventario:

	"""
	Representa la tabla de la simulación de un inventario
	en n meses
	"""
	def __init__(self, q, r, inicial, numeros):
		""" q: cantidad a pedir
			r: cantidad donde se pide
			incial: inventario de inicio
			numeros: arreglo de números pseudoaleatorios
		"""
		self.q = q
		self.r = r
		self.inicial = inicial
		self.actual = inicial
		self.numeros = numeros
		self.i_pseudo = 0
		self.i_mes = 0
		self.contador_meses = 1

		self.tabla_demanda = None
		self.factores_estacionales = None
		self.tabla_entrega = None

		self.faltante_actual = 0
		self.acumulador_faltante = 0
		self.acumulador_inventario = 0
		self.deuda = 0 # es el faltante acumulado
		self.pedido_actual = 0
		self.contador_pedidos = 0

		self.is_simulado = False

		self.registro = ""

	def procesar_factores_estacionales(self, str_factores):
		"""convierte una cadena de 12 factores en formato:
		1.2
		0.4
		...
		en un arreglo de factores estacionales de 12 meses.
		Devuelve un arreglo de floats con 12 factores
		"""
		str_factores = str_factores.split(sep='\n')
		if len(str_factores) != 12:
			raise Exception("fallo al leer factores estacionales")
		factores = []
		for factor in str_factores:
			factores.append(float(factor))
		return factores

	def set_distribucion_demanda(self, t_demanda):
		"""Le asigna la tabla de distribucion de probabilidades de
		demanda
		"""
		self.tabla_demanda = t_demanda

	def set_factores_estacionales(self, str_factores):
		try:
			self.factores_estacionales = self.procesar_factores_estacionales(str_factores)
		except Exception as e:
			print(e.__str__())

	def set_distribucion_entrega(self, t_entrega):
		self.tabla_entrega = t_entrega

	def simular_demanda(self, pseudo):
		"""Toma un número pseudoaleatorio y regresa un evento
		de demanda simulada"""
		return self.tabla_demanda.obtener_evento(pseudo)

	def next_pseudo(self):
		"""
		Regresa el siguiente número pseudoaleatorio
		"""
		i = self.i_pseudo
		self.i_pseudo += 1
		try:
			return self.numeros[i]
		except IndexError:
			print("NO HAY SUFICIENTES NUMEROS PSEUDO")



	def add_registro(self, dato):
		"""Va formando el registro (renglon) de un paso de la simulacion
		"""
		self.registro += str(dato)
		self.registro += "\t"

	def simular(self, verbose=False):
		"""Simula un mes de inventario.
		Se toma el siguiente número pseudoaleatorio
		se crea un evento de demanda usando ese numero (simular_demanda)
		se multiplica el evento por el factor estacional del mes en curso
		esta es la demanda ajustada, se resta la demanda ajustada al inventario
		inicial.
		Se calcula faltante si demanda > inv_inicial
		si inv_final < r -> pedir_orden

		"""
		#print(self.contador_meses)

		#revisar si se puede recibir pedido
		self.registro = ""
		entrega = None
		if self.pedido_actual:
			entrega = self.pedido_actual.intentar_entregar()

		if entrega:
			#print("Se recibe el pedido No.{}, cantidad: {}".format(
			#	self.contador_pedidos, entrega)
			#)
			self.pedido_actual = None #borrar pedido
			self.actual += entrega #entrega a inventario

		if self.deuda > 0: #si hay deuda, intenta surtirla
			if self.actual >= self.deuda:
				self.actual -= self.deuda
				self.deuda = 0
		
		self.add_registro(self.contador_meses)

		#print(numero_a_mes(self.i_mes)) #porque enero es 0
		self.add_registro(numero_a_mes(self.i_mes))
		#print(self.actual)
		self.add_registro(self.actual)

		pseudo = self.next_pseudo()
		#print(pseudo)
		if verbose:
			self.add_registro(pseudo)
		demanda = self.simular_demanda(pseudo)
		#print("demanda", demanda)
		if verbose:
			self.add_registro(demanda)

		#no se hace +1 porque inicia en 0: enero
		d_ajus = int(round(demanda * self.factores_estacionales[self.i_mes], 0))
		#print("ajustada", d_ajus)
		self.add_registro(d_ajus)

		#entregar orden

		inv_final = 0
		self.faltante_actual = 0 #hacer un arreglo de esto
		if d_ajus > self.actual:
			self.faltante_actual = d_ajus - self.actual
			inv_final = 0
		else:
			self.faltante_actual = 0
			inv_final = self.actual - d_ajus
		self.deuda += self.faltante_actual
		self.acumulador_faltante += self.faltante_actual

		self.add_registro(inv_final)

		#print("faltante", self.faltante_actual)
		self.add_registro(self.faltante_actual)

		if inv_final < self.r: #intentar hacer pedido
			if not self.pedido_actual: #si no hay pedido pendiente
				self.contador_pedidos += 1
				meses = self.tabla_entrega.obtener_evento(self.next_pseudo())
				self.pedido_actual = Pedido(self.q, meses)
				#print("pedido: ", self.contador_pedidos)
				self.add_registro(self.contador_pedidos)
			else:
				self.add_registro("-")
		else:
			self.add_registro("-")


		#print(inv_final)

		inv_mensual = 0
		if inv_final == 0:
			inv_mensual = round(self.actual ** 2 / ( 2 * d_ajus), 2)
		elif self.actual == 0:
			inv_mensual = 0
		else:
			inv_mensual = round((inv_final + self.actual) / 2.0, 2)

		#print(inv_mensual)
		self.acumulador_inventario += round(inv_mensual, 2)
		self.add_registro(inv_mensual)

		#nuevo inventario
		self.actual = inv_final

		self.i_mes += 1
		faltante = 0

		self.contador_meses += 1 #no se reinicia
		if self.i_mes + 1 == 13:
			self.i_mes = 0 #vuelve a enero luego de diciembre

		#print(self.registro)

		if not self.is_simulado:
			self.is_simulado = True
		return self.registro

	def ciclo(self, n):
		"""Simula n veces
		"""
		for i in range(0, n):
			self.simular()

	def obtener_costo(self, c_faltante, c_orden, c_inventario):
		"""Toma los costos de: faltante, orden, inventario
		y calcula el costo total de todos estos
		"""
		total = self.acumulador_faltante * c_faltante
		total += self.contador_pedidos * c_orden
		total += (self.acumulador_inventario * c_inventario) / 12 # anual
		return round(total, 2)


def main():
	probabilidades = leer_archivo("demanda")

	"""0.01 35
0.015 36
0.020 37
0.020 38
0.022 39
0.023 40
0.025 41
0.027 42
0.028 43
0.029 44
0.035 45
0.045 46
0.060 47
0.065 48
0.070 49
0.080 50
0.075 51
0.070 52
0.065 53
0.060 54
0.050 55
0.040 56
0.030 57
0.016 58
0.015 59
0.005 60"""

	factores = leer_archivo("factores")

	"""1.2
1.0
0.9
0.8
0.8
0.7
0.8
0.9
1.0
1.2
1.3
1.4"""

	p_entregas = leer_archivo("espera")
	"""0.3 1
0.4 2
0.3 3"""
	
	#leer tablas de distribucion y usar generador
	td = DistribuidorDeTabla(probabilidades)
	t_entregas = DistribuidorDeTabla(p_entregas)
	gen = Generador(101, 221, 17001, 17)
	gen.ciclo(325)

	#print(td.obtener_evento(gen.get_generacion()[0]))

	#simulador de inventario
	inv = SimInventario(200, 100, 150, gen.get_generacion())
	inv2 = SimInventario(200, 50, 150, gen.get_generacion())

	#asignar tablas de distribucion
	inv.set_distribucion_demanda(td)
	inv.set_factores_estacionales(factores)
	inv.set_distribucion_entrega(t_entregas)

	inv2.set_distribucion_entrega(t_entregas)
	inv2.set_factores_estacionales(factores)
	inv2.set_distribucion_demanda(td)

	print("mes\tinicial\tpseudo\tdem\tfinal\tfalta\torden\tmensual")
	inv.ciclo(12)
	print("Costo total: ", inv.obtener_costo(25, 50, 26))

	print("mes\tinicial\tpseudo\tdem\tfinal\tfalta\torden\tmensual")
	inv2.ciclo(12)
	print("Costo total: ", inv2.obtener_costo(25, 50, 26))



if __name__ == '__main__':
	main()