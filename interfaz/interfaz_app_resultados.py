import os
import tksvg

from tkinter import *
from tkinter import ttk

from sistema_db.db_productos import sistema
import utils

#valores de espacio entre entradas y labels 
#estos son valores de estilo que elegi cuando hice la app, pueden solo copiarlos y pegarlos
p_x = 3
p_y = 3
p_x_l = 10 #p_x largos
p_y_l = 10
w = 10









#todo: no se actualizan los resultados hasta que se cierra la ventana














class InterfazAppResultados(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.c_resultados = 0

        self.resultados = [] #listado de renglones de productos
        self.resultados_ui = []
        self.init_interfaz()
        #self.add_resultados()
        #mockup
        """ttk.Label(self, text="Producto1").grid(column = 0, row = 1, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="100").grid(column = 1, row = 1, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="200").grid(column = 2, row = 1, padx = p_x_l, pady = p_y)
        ttk.Button(self, text="ver").grid(column = 3, row = 1, padx = p_x_l, pady = p_y)
        """
        
    
    def init_interfaz(self):
        ttk.Label(self, text="Producto").grid(column = 0, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="R óptima").grid(column = 1, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="Q óptima").grid(column = 2, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="Costo").grid(column = 3, row = 0, padx = p_x_l, pady = p_y)
        ttk.Label(self, text="Gráfica").grid(column = 4, row = 0, padx = p_x_l, pady = p_y)

    def add_resultados(self):
        self.c_resultados = 0
        self.resultados = []
        self.resultados_ui = []
        #self.borrar_graficos()
        resultados = self.encontrar_resultados()
        res_ui = {}
        for resultado in resultados:
            if resultado == None:
                continue
            self.resultados.append(resultado) #guardar datos de cada resultado
            res_ui['nombre_producto'] = ttk.Label(self, text = resultado['nombre_producto'])
            res_ui['nombre_producto'].grid(column = 0, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)
            res_ui['punto_reorden'] = ttk.Label(self, text = resultado['punto_reorden'])
            res_ui['punto_reorden'].grid(column = 1, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)
            res_ui['cantidad_orden'] = ttk.Label(self, text = resultado['cantidad_orden'])
            res_ui['cantidad_orden'].grid(column = 2, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)
            res_ui['costo'] = ttk.Label(self, text = '$' + str(resultado['costo']))
            res_ui['costo'].grid(column = 3, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)

            res_ui['ver'] = ttk.Button(self, text = 'ver', command = lambda c=self.c_resultados: self.cmd_ver_grafica(c))
            res_ui['ver'].grid(column = 4, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)

            res_ui['borrar'] = ttk.Button(self, text = 'X', command = lambda c=self.c_resultados: self.cmd_borrar(c))
            res_ui['borrar'].grid(column = 5, row = self.c_resultados + 1, padx = p_x_l, pady = p_y)
            self.resultados_ui.append(res_ui) #guardar los componentes de cada resultado
            res_ui ={}
            self.c_resultados += 1

    def cmd_ver_grafica(self, index):
        self.mostrar_grafica(self.resultados[index]['nombre_producto'])

    def borrar_graficos(self):
       for i in range(0, len(self.resultados_ui)):
           for componente in self.resultados_ui[i]:
               self.resultados_ui[i][componente].destroy()

    def mostrar_grafica(self, nombre_producto):
        #enviar solo nombre sin .txt
        #nombre_producto += '.txt'
        ventana = Toplevel()
        ventana.geometry("800x400")
        ventana.title("Serie de tiempo de: {}".format(nombre_producto))
        path = os.path.abspath(
            os.path.join(
                    os.path.join(
                        os.getcwd(), 'graficas'),
                    '{}.svg'.format(nombre_producto)
                )
            )
        image = tksvg.SvgImage(file=os.path.join(os.path.dirname(__file__), path))
        label = Label(ventana, image=image)
        label.image = image
        label.grid(column = 0, row = 0)

    def cmd_borrar(self, index):
        #borrar de la bd el producto
        #volver a calcular todo y volver a ponerlo en la gui, sino los indices estarán mal
        #nota: actualmente parece que no hace nada pero es porque no he eliminado de bd el producto
        #recordar tambien eliminar los txt y graficas
        nombre_producto = self.resultados[index]['nombre_producto']
        #for componente in self.resultados_ui[index]:
        #   self.resultados_ui[index][componente].destroy()

        #borrar
        #for i in range(0, len(self.resultados_ui)):
        #    for componente in self.resultados_ui[i]:
        #        self.resultados_ui[i][componente].destroy()
        #borrar de bd
        
        sistema.borrar_producto(nombre_producto)
        self.borrar_graficos()
        #borrar en sistema de archivos
        self.borrar_archivos(nombre_producto)
        #recalcular
        self.add_resultados()

    def borrar_archivos(self, nombre_producto):
        imagen = utils.to_dir_file_local('graficas', '{}.svg'.format(nombre_producto))
        predicciones = utils.to_dir_file_local('predicciones', '{}.txt'.format(nombre_producto))
        productos = utils.to_dir_file_local('productos', '{}.txt'.format(nombre_producto))

        for archivo in [imagen, predicciones, productos]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def encontrar_resultados(self):
        resultados = []
        productos = sistema.get_productos()
        for producto in productos:
            res = {'nombre': producto}
            exps = []
            for exp in range(0, 9):
                exps.append(sistema.get_experimento(producto, exp))
            min = exps[0]['costo']
            if min == None:
                continue
            optimo = None
            for exp in exps:
                if exp['costo'] <= min:
                    min = exp['costo']
                    optimo = exp
            resultados.append(optimo)
        return resultados
