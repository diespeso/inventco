#!/usr/bin/python3.9

from tkinter import *
from tkinter import ttk

from ttkthemes import ThemedTk

import sys
from interfaz.ventana import Ventana

import utils

def main():
	datos = None
	if len(sys.argv) > 1: #esto lo usaba para llamar el programa para pruebas con argumentos, no lo vamos a usar.
		datos = {}
		datos["semilla"] = int(sys.argv[1])
		datos["constante"] = int(sys.argv[2])
		datos["multiplicador"] = int(sys.argv[3])
		datos["modulo"] = int(sys.argv[4])
		datos["tamano"] = int(sys.argv[5])

	#root = Tk() #el holder de la gui
	root = ThemedTk(theme='clearlooks')
	root.geometry("690x405") # tamanio de la ventana
	
	#poner icono
	icono = utils.to_dir_file_local('interfaz', 'icono.png')
	img = PhotoImage(file=icono)
	root.iconphoto(False, img)

	app = Ventana(root) # ventana es una clase en el folder interfaz, estoy haciendo una instancia.
	root.mainloop() # correr la gui
import subprocess

if __name__ == '__main__':
	motor = "C:\\Users\\CDT\\Documents\\tec\\ingenieria de software\\inventco\\motor_prediccion.exe"
	args = "salchichas.txt"
	#subprocess.call([motor, args])
	main() # solo corre main si se llamo directamente este archivo.
