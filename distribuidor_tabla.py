precision = 3

import sys

class DistribuidorDeTabla:
	"""Representa una tabla de distribución de probabilidad
	empírica
	"""
	def __init__(self, distribucion):
		"""distribucion: cadena de texto que obedece el formato:
		probabilidad numero, ejemplo:
		0.010 35
		0.015 36
		"""
		self.conjuntos = None
		self.probabilidades = None
		self.eventos = None
		self.relaciones = None
		try:
			self.conjuntos = self.crear_conjuntos(distribucion)
			self.probabilidades, self.eventos = self.crear_tabla(self.conjuntos)
			self.relacion = self.crear_relacion()
		except Exception as e:
			print(e.__str__())
			print(self.relaciones)
			sys.exit(0)

	def mostrar(self, distribucion=False):
		salida = ""
		for i in range(0, len(self.eventos)):
			salida += str(self.eventos[i])
			salida += " -> "
			if distribucion:
				salida += str(self.relaciones[i][0])
				salida += ", "
				salida += str(self.relaciones[i][1])
			else:
				salida += str(self.probabilidades[i + 1])
				# + 1 porque probabilidades empieza en 0.0 para hacer las relaciones
				pass
			salida = ""
		

	def crear_conjuntos(self, distribucion):
		"""Toma una cadena de texto en formato:
		0.010 35
		0.015 36
		y la convierte en series de '0.01 35', '0.015 36'
		"""
		conjuntos = distribucion.split(sep='\n')
		for conjunto in conjuntos:
			if not ' ' in conjunto:
				raise Exception("Fallo al leer la distribución de probabilidad")
		return conjuntos

	def traducir_a_numeros(self, conjuntos):
		"""Toma una serie de '0.01 35', '0.015 36' y la 
		transforma en diccionario 35 -> 0.01
		"""
		pass #quizas no sea util

	def crear_tabla(self, conjuntos):
		"""Toma una serie de '0.01 35', '0.015 36' y la 
		transforma a una serie de probabilidades, hace que la
		serie comience en 0.0 de forma automática

		regresa (serie de probabilidades, serie de eventos)
		"""
		probs = []
		eventos = []
		probs.append(0.0)
		for conjunto in conjuntos:
			s = conjunto.split(sep=' ')
			probs.append(
				float(s[0])
			)
			eventos.append(
				int(s[1])
			)
		return (probs, eventos)

	def crear_relacion(self):
		"""Crea un arreglo de formato
		[
			[0.0, 0.01],
			[0.01, 0.025]
		]

		el índice i representa el número de evento
		que se traducirá el intervalo,ejemplo i = 0 -> self.probs[0] -> 35
		"""
		acumulador = 0.0
		relaciones = []
		for i in range(len(self.probabilidades) - 1):
			j = i + 1
			relacion = []
			relacion.append(acumulador)
			relacion.append(round(acumulador + self.probabilidades[j], precision))
			acumulador = round(acumulador + self.probabilidades[j],
				precision)
			relaciones.append(relacion)
		self.relaciones = relaciones
		self.revisar_relaciones()

	def generar_str(self):
		"""Genera una string que representa la tabla,
		es como regresar a la tabla original
		"""
		str_relacion = ""
		for i in range(0, len(self.relaciones)):
			relacion = self.relaciones[i]
			evento = self.eventos[i]
			str_relacion += str(round(relacion[1] - relacion[0], 5))
			str_relacion += " " +str(evento) + "\n"

		return str_relacion[:-1] #borra la newline que queda al final

	def revisar_relaciones(self):
		if self.relaciones[-1][1] > 1.0 + 0.1: # 0.01: 1porciento de tolerancia:
			print(self.generar_str())
			raise Exception("La distribución de probabilidades no suma 1.0")


	def obtener_evento(self, pseudo):
		"""Toma un número pseudoaleatorio y lo transforma
		a una evento, osea: lo busca en la tabla de probabiliades
		y retorna el valor del evento que corresponde a ese espacio
		"""
		for evento in range(len(self.relaciones)):
			#buscar en que intervalode evento cae el pseudoaleatorio
			limites = self.relaciones[evento]
			if pseudo >= limites[0] and pseudo < limites[1]:
				return self.eventos[evento]
		print(pseudo)
		raise Exception("No se pudo encontrar un evento en ninǵun rango")
