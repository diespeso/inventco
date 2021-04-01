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