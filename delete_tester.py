import os

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from inventco.app_prediccion import sistema_prediccion

def eliminar_producto(producto):
    if os.path.exists("{}.txt".format(producto)):
        print("removiendo .txt")
        os.remove("{}.txt".format(producto))
    if os.path.exists("graficas\\{}.svg".format(producto)):
        os.remove("graficas\\{}.svg".format(producto))
        print("removiendo grafica")
    if os.path.exists("predicciones\\{}.txt".format(producto)):
        os.remove("predicciones\\{}.txt".format(producto))
        print("removiendo prediccion")
if __name__ == '__main__':
    print("productos: ", sistema_prediccion.productos)
    eliminar_producto("salchichas")