MESES = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre'
]

def to_mes(num): #takes from 1 to 12
    return MESES[num - 1]

def int_from_mes(mes):
    #regresa un numero de mes del 1 al 12
    for m in range(0, len(MESES)):
        if MESES[m] == mes:
            return m + 1
    raise Exception("Mes no existente")

def try_parse_demanda_entry(demanda_entry):
    '''if it fails it returns none, if not in returns the correct value.
    an empty entry returns null
    a number entry returns its number
    a entry thats not a number is wrong an returns None'''
    demanda = demanda_entry.get()
    if demanda == '':
        return 'null'
    try:
        demanda = int(demanda)
        if demanda < 0:
            demanda = None #no negativos
    except Exception:
        demanda = None
    finally:
        return demanda

def demanda_or_empty(demanda):
    #regresa el valor de la demanda o un '', usado para cargar demandas
    if demanda == None:
        return ''
    else:
        return demanda

def set_entry(entry, text):
    fin = entry.get()
    entry.delete(0, "end")
    entry.insert(0, text)
    return fin

#funciones para acomodar demandas
def ordenar_tabla_demandas(tabla):
    #debe ingresarse un arreglo con el formato (1, 'Enero', 54)
    #se ignora el anio para el acomodo
    anios = int(len(tabla) / 12)
    demandas = []
    for i in range(0, anios):
        demandas.append([])
    for i in range(0, len(tabla)):
        for j in range(0, anios):
            if tabla[i][0] == j + 1:
                demandas[j].append(tabla[i])
    print('tabla demandas: ', demandas)

    for i in range(0, anios):
        demandas[i] = ordenar_anio_demandas(demandas[i])

    final = []
    for anio in demandas:
        for mes in anio:
            final.append(mes)
    print('final ordenado: ', final)
    return final

def ordenar_anio_demandas(meses):
    #debe ingresarse un arreglo con el formato (1, 'Enero', 54)
    ordenado = []
    for mes in range(0, 12):
        ordenado.append(meses[encontrar_indice_demanda_con_mes(meses, to_mes(mes + 1))])
    return ordenado

def encontrar_indice_demanda_con_mes(demandas, mes):
    for i in range(0, len(demandas)):
        if demandas[i][1] == mes:
            return i