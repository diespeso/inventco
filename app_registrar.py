
class Registrar:
    #clase motor de ejemplo
    #una clase motor es la clase que tiene toda la funcionalidad logica
    #tomando en cuenta solo datos y operaciones, nada grafico
    def __init__(self):
        self.mensaje = ""

    def nombre(self, nombre):
        self.mensaje = nombre
    
    def mostrar_nombre(self):
        print("el nombre fue: {}".format(self.mensaje))

if __name__ == '__main__': #si se corre directamente en consola
    reg = Registrar()
    reg.nombre("Maradonio")
    reg.mostrar_nombre()