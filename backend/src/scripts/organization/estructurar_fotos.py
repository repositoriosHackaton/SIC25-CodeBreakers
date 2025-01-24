def calcular_proporcion_casos(total_fotos: int, casos: dict()) -> dict():
    """
    Calcula la proporción de fotos para cada caso.
    """
    proporciones = dict()
    proporciones['1'] = casos['1'] / total_fotos
    proporciones['2'] = casos['2'] / total_fotos
    proporciones['3'] = casos['3'] / total_fotos
    return proporciones


def calcular_fotos_a_extraer(total_fotos, porcentaje_extraer, proporciones: dict()) -> dict():
    """
    Calcula cuántas fotos extraer de cada caso según la proporción y el porcentaje dado.
    """
    total_a_extraer = total_fotos * (porcentaje_extraer / 100)
    fotos_extraer_casos = dict()
    fotos_extraer_casos['1'] = round(total_a_extraer * proporciones['1'])
    fotos_extraer_casos['2'] = round(total_a_extraer * proporciones['2'])
    fotos_extraer_casos['3'] = round(total_a_extraer * proporciones['3'])
    return fotos_extraer_casos


def calcular_grupos(total_fotos: int, casos: dict(), porcentajes: dict()) -> dict():
    """
    Calcula las fotos a extraer para cada grupo (70%, 20%, 10%).
    """
    # Paso 1: Calcular la proporción de cada caso
    proporciones = calcular_proporcion_casos(total_fotos, casos)

    # Paso 2: Calcular las fotos a extraer para cada grupo
    grupos = dict()
    for grupo, porcentaje in porcentajes.items():
        grupos[grupo] = calcular_fotos_a_extraer(total_fotos, porcentaje, proporciones)

    return grupos


def dividir_fotos_por_cara(casos: dict()) -> dict():
    """
    Divide las fotos de cada caso en "front" y "back" (mitad para cada uno).
    """
    fotos_por_cara = dict()
    fotos_por_cara['front'] = {caso: round(fotos / 2) for caso, fotos in casos.items()}
    fotos_por_cara['back'] = {caso: round(fotos / 2) for caso, fotos in casos.items()}
    return fotos_por_cara


def procesar_denominaciones(denominaciones: dict(), casos: dict(), porcentajes: dict()) -> dict():
    """
    Procesa cada denominación de billete, aplicando el cálculo de grupos a cada cara ("front" y "back").
    """
    resultados = dict()
    for denominacion, total_fotos in denominaciones.items():
        # Dividir las fotos en "front" y "back"
        fotos_por_cara = dividir_fotos_por_cara(casos)

        # Calcular grupos para "front" y "back"
        resultados[denominacion] = dict()
        for cara, casos_cara in fotos_por_cara.items():
            resultados[denominacion][cara] = calcular_grupos(total_fotos, casos_cara, porcentajes)

    return resultados


# Datos de entrada
denominaciones = {
    '5': 400,
    '10': 400,
    '20': 400,
    '50': 400,
    '100': 400,
    '200': 400,
}

casos = {
    '1': 120,
    '2': 220,
    '3': 60,
}

porcentajes = {
    'datasets': 70,  # 70%
    'valid': 20,  # 20%
    'test': 10,  # 10%
}

### Nueva etapa ###

import json

# Función para reorganizar la estructura del diccionario
def reorganizar_estructura(resultados: dict) -> dict:
    nueva_estructura = dict()
    for denominacion, caras in resultados.items():
        nueva_estructura[denominacion] = dict()
        for cara, grupos in caras.items():
            for grupo, fotos_por_caso in grupos.items():
                for caso, cantidad in fotos_por_caso.items():
                    if caso not in nueva_estructura[denominacion]:
                        nueva_estructura[denominacion][caso] = {"front": {}, "back": {}}
                    nueva_estructura[denominacion][caso][cara][grupo] = cantidad
    return nueva_estructura # Simplemente funciona

# Procesar todas las denominaciones
resultados = reorganizar_estructura(procesar_denominaciones(denominaciones, casos, porcentajes))

# Guardar el resultado en un archivo JSON
with open('backend/src/scripts/organization/resultados.json', 'w') as archivo_json:
    json.dump(resultados, archivo_json, indent=4)

# Mostrar resultados
for denominacion, casos in resultados.items():
    print(f"\nResultados para {denominacion}:")
    for caso, caras in casos.items():
        print(f"\nCaso {caso}:")
        for cara, grupos in caras.items():
            print(f"{cara.capitalize()}: {grupos}")