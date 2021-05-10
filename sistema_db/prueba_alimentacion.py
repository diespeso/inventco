from db_productos import sistema
import db_cleaner



class DbTester:
    """Esta clase esta pensada para ser usada despues de alimentar desde la programa
    ya que al alimentar producto y demandas en el programa tambien se triggerea
    la alimentación de otras tablas"""
    def __init__(self):
        print("testing...")

    def limpiar_sistema(self):
        db_cleaner.main()        
    
    def in_producto(self, datos):
        sistema.registrar_en_producto(datos)

    def sel_producto(self, cols, query):
        #nota: el ultimo campo siempre da null porque ya no lo uso
        make_query("producto", cols, query)

    def sel_prediccion(self, cols, query):
        make_query("prediccion", cols, query)

    def sel_experimento(self, cols, query):
        make_query("experimento", cols, query)

    def sel_simulacion(self, cols, query):
        make_query("simulacion", cols, query)

    def sel_historico(self, cols, query):
        make_query("historico", cols, query)

def make_query(table_name, cols, query):
    """Toma el nombre de la tabla,
    las columnas a mostrar,
    y el query (como un where o un inner join), esta parte es opcional
    e imprime el resultado del query"""
    str_query = None
    if query == None:
       str_query = "select {} from {};".format(cols, table_name)
    else:
        str_query = "select {} from {} {};".format(cols, table_name, query)
    print(">>>ejecutando: ", str_query)
    sistema.cursor.execute(str_query);
    for row in sistema.cursor.fetchall():
        print(row)

def gen_producto(nombre, c_p, c_f, c_i, i_i):
    return {
        "nombre": nombre,
        "costo_pedido": c_p,
        "costo_faltante": c_f,
        "costo_inventario": c_i,
        "inventario_inicial": i_i
    }

if __name__ == '__main__':
    test = DbTester()
    #test.in_producto(gen_producto("salchichas3", 0.15, 0.16, 0.17, 100))
    #test.in_producto(gen_producto("salchichas4", 0.17, 0.18, 0.19, 110))
    test.sel_producto("*", None)
    test.sel_producto("nombre", "where inventario_inicial = 89")
    test.sel_prediccion("*", "inner join producto on producto.nombre = prediccion.nombre_producto")
    test.sel_simulacion("simulacion.inv_final", "inner join producto on producto.nombre = simulacion.nombre_producto")
    test.sel_simulacion("*", None)