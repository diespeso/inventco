import utils


class TablaSimulacion:
    def __init__(self, cantidad_orden, punto_reorden, inicial, predicciones):
        self.cantidad_orden = cantidad_orden
        self.punto_reorden = punto_reorden
        self.inicial = inicial
        self.predicciones = predicciones

        self.tabla = []
        self.simular()
    
    def simular(self):
        c_orden = 0
        #todo: añadir cantidad orden despues de cada orden
        if len(self.predicciones) == 12:
            for i in range(0, len(self.predicciones)):
                suma_faltante = 0
                if i == 0:
                    inicial = self.inicial
                    suma_orden = -1 #-1 significa que es el primero y no es nada
                else:
                    inicial = self.tabla[i - 1]['final']
                    suma_orden = 0
                    
                    if suma_orden != -1:
                        suma_orden = 0
                        if self.tabla[i - 1]['orden'] != None:
                            suma_orden = self.cantidad_orden - self.tabla[i - 1]['faltante']
                            #lo que se recibe del pedido menos el faltante anterior
                            print("suma orden:", suma_orden)
                            if suma_orden < 0:
                                inicial = 0
                                suma_faltante = abs(suma_orden)
                            else:
                                inicial += suma_orden
                                suma_faltante = 0
                        

                demanda = self.predicciones[i]
                final_temp = inicial - demanda
                if final_temp < 0:
                    faltante = abs(final_temp) + suma_faltante
                    final = 0
                else:
                    faltante = 0
                    final = final_temp
                orden = None
                if final <= self.punto_reorden:
                    c_orden += 1
                    orden = c_orden
                    
                renglon = {'inicial': inicial, 'demanda': demanda, 'final': final,
                'faltante': faltante, 'orden': orden}
                self.tabla.append(renglon)
        else:
            raise Exception("No se puede hacer una TablaSimulacion con {} predicciones".format(len(self.predicciones)))

    def __str__(self):
        result = "\tInicial\tDemanda\tFinal\tFaltan\tOrden\n"
        for i in range(0, len(self.tabla)):
            renglon = self.tabla[i]
            result += "{}\t{}\t{}\t{}\t{}\t{}\n".format(
                utils.to_mes(i + 1),
                renglon['inicial'],
                renglon['demanda'],
                renglon['final'],
                renglon['faltante'],
                renglon['orden']
            )
        return result

    def calcular_costos(self, c_pedido, c_faltante, c_inventario):
        if self.is_complete():
            t_pedido = 0.0
            t_faltante = 0.0
            t_inventario = 0.0

            for i in range(0, len(self.tabla)):
                renglon = self.tabla[i]
                if renglon['orden'] != None:
                    t_pedido += c_pedido
                t_faltante += c_faltante * renglon['faltante']
                t_inventario += c_inventario * renglon['final']
            return (t_pedido, t_faltante, t_inventario)
        else:
            raise Exception("No se puede calcular los costos de una tabla de simulación incompleta")
    
    def calcular_costo_total(self, c_pedido, c_faltante, c_inventario):
        costos = self.calcular_costos(c_pedido, c_faltante, c_inventario)
        return costos[0] + costos[1] + costos[2]

    def is_complete(self):
        return len(self.tabla) == 12
if __name__ == '__main__':
    tabla = TablaSimulacion(400, 300, 89,
    [221, 140, 11, 130, 655, 381, 104, 408, 574, 394, 578, 354])
    print(tabla)
    print(tabla.calcular_costo_total(100, 2.5, 4.5))