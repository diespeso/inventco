from tabla_simulacion import TablaSimulacion
from sistema_db.db_productos import sistema
import utils
class MotorExperimentos:
    """Se encarga de contener una ;lista enlazada; con los experimentos
    donde cada experimento es una tablasimulacion con un q y r diferentes
    Por regla el primer elemento tiene los valores q y r originales"""

    def __init__(self, q, r, inicial, predicciones):
        """El motor experimentos genera una combinación de 9 variaciones de q y r, incluyendo q y r originales como la combinación 0
        después se encarga de generar una tabla de simulación para cada una de las 9 combinaciones de q y r"""
        self.experimentos = []
        self.contador = 0

        self.combs = gen_combinaciones(q, r)

        for comb in self.combs:
            self.experimentos.append(TablaSimulacion(comb[0], comb[1], inicial, predicciones))

    def get_actual(self):
        return self.experimentos[self.contador]
    
    def mov_siguiente(self):
        self.contador += 1
        if len(self.experimentos) == self.contador:
            self.contador = 0

    def mov_anterior(self):
        self.contador -= 1
        if len(self.experimentos) == 0:
            self.contador = len(self.experimentos) - 1
    
    def to_bd(self, nombre_producto):
        """Guarda este motor de experimentos en la base de datos, llamando una función auxiliar del sistema de bd"""
        for i in range(1, 9): #por cada una de las 9 combinaciones generadas
            sistema.actualizar_en_experimento(nombre_producto, i, self.combs[i][1], self.combs[i][0])
        for i in range(0, 9):
            tabla = self.experimentos[i]
            for m in range(1, 13):
                renglon = tabla.get_renglon(m - 1) #no se busca demanda porque la demanda es de la tabla de prediccion
                #print('renglon: ', renglon)
                sistema.actualizar_en_simulacion(nombre_producto, i, utils.to_mes(m), renglon['inicial'], renglon['final'], renglon['faltante'], renglon['orden'])
            producto = sistema.get_producto(nombre_producto)

            sistema.registrar_costo_experimento(nombre_producto, i, self.experimentos[i].calcular_costo_total(producto['c_pedido'], producto['c_faltante'], producto['c_inventario']))

def gen_combinaciones(q, r):
    """genera 8 combinaciones de q y r a ser usadas por el motor de experimentos
    se varía el 25% """
    combinaciones = []
    com_q = q
    com_r = r
    f = 0.25 #factor de variabilidad
    combinaciones.append([com_q, com_r])
    combinaciones.append([com_q, int(com_r*(1+f))])
    combinaciones.append([com_q, int(com_r*(1-f))])
    combinaciones.append([int(com_q*(1-f)), com_r])
    combinaciones.append([int(com_q*(1-f)), int(com_r*(1+f))])
    combinaciones.append([int(com_q*(1-f)), int(com_r*(1-f))])
    combinaciones.append([int(com_q*(1+f)), int(com_r)])
    combinaciones.append([int(com_q*(1+f)), int(com_r*(1+f))])
    combinaciones.append([int(com_q*(1+f)), int(com_r*(1-f))])

    return combinaciones


if __name__ == "__main__": #pruebas
    gen_combinaciones(100, 200)
    motor = MotorExperimentos(100, 200, 300,
    [221, 140, 110, 130, 255, 381, 104, 208, 374, 394, 378, 354])
    for i in range(0, 10):
        act = motor.get_actual()
        print("{}, {}".format(act.cantidad_orden, act.punto_reorden))
        print(act)
        print(act.calcular_costo_total(0.5, 0.6, 0.7))
        motor.mov_anterior()