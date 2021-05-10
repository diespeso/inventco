from sistema_db.db_productos import sistema
from tabla_simulacion import TablaSimulacion


class AppSimulacion:
    """Se encarga de simular un producto y también de generar los experimentos y las tablassimulacion
    de cada experimento"""
    def __init__(self):
        pass
    def simular_from_db(self, producto):
        """Crea y registra en bd los experimentos del producto dado"""
        producto_db = sistema.get_producto(producto)
        experimento = sistema.get_experimento(producto, 0) #el primero es el original
        factor = 0.1 # una decima parte
        pares = []
        for i in range(0, 3): #q original, factor -, factor +
            for j in range(0, 3): #r original, factor -, factor +
                pares.append([])
        
        predicciones = sistema.get_predicciones(producto)
        preds = []
        print("q: {},r: {}".format(experimento['cantidad_orden'], experimento['punto_reorden']))
        for prediccion in predicciones:
            preds.append(prediccion['demanda'])
        return TablaSimulacion(experimento['cantidad_orden'], experimento['punto_reorden'], 
        producto_db['inv_inicial'], preds)

if __name__ == '__main__':
    sim = AppSimulacion()  
    print("simulador:", sim.simular_from_db("panecitos"))