#!/usr/bin/python3.9

from pathlib import Path
from distribuidor_tabla import DistribuidorDeTabla

"""Toma 3 documentos y los convierte en las tablas necesarias:
	factores
	demanda
	espera
"""

def leer_archivo(nombre_archivo):
	with open(nombre_archivo, 'r') as archivo:
		return archivo.read()[:-1]

def parse_file(nombre_archivo, distribucion=False, decimal=False):
	"""Intenta traducir un archivo de texto en el mismo folder que el
	ejecutable.
	Si la distribucion es true, entonces intenta
	convertirlo en un DistribuidorDeTabla
	sino, lo convierte en un arreglo
	"""
	with open(nombre_archivo, 'r') as archivo:
		contenido = archivo.read()[:-1]
		
		if distribucion:
			return DistribuidorDeTabla(contenido)
		else:
			contenido = contenido.split(sep="\n")
			arreglo = []
			for num in contenido:
				if decimal:
					arreglo.append(float(num))
				else:
					arreglo.append(int(num))
			return arreglo	
			


if __name__ == '__main__':
	print("parser!")
	factores = parse_file("factores", decimal=True)
	demanda = parse_file("demanda", distribucion=True)
	espera = parse_file("espera", distribucion=True)
	print(factores)
	demanda.mostrar()
	espera.mostrar(distribucion=True)