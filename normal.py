#!/usr/bin/python3

import math
from scipy import stats

from generador import Generador
from comun import precision

class Normal:
	def __init__(self, mu, sigma):
		self.mu = mu
		self.sigma = sigma
		self.x = None
		self.z = None

	def densidad_puntual(self, x):
		self.x = x
		raiz = math.sqrt(2 * math.pi * self.sigma)
		exponente_2 = (self.x - self.mu) ** 2
		exponente_2 /= -2 * self.sigma ** 2
		return round((math.e ** exponente_2) / raiz, precision)

	def densidad_estandar_acumulada(self, x):
		""" estandariza los valores a zeta, para luego obtener
		la densidad acumulada desde la izquierda
		"""
		self.x = x
		self.z = (self.x - self.mu) / self.sigma
		return round(stats.norm.cdf(self.z), precision)

	def densidad_estandar_acumulada_inversa(self, densidad):
		""" regresa el valor en x desde izquierda de donde se obtiene
		el valor de densidad acumulada dado
		"""
		return round(stats.norm.ppf(densidad), precision)

if __name__ == '__main__':
	normal = Normal(0.53, 0.28)
	print("densidad acumulada en 0.5: {}".format(normal.densidad_estandar_acumulada(0.5)))