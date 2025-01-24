import os
import random
import json

def cargar_json_desde_archivo(ruta_json: str) -> dict:
    """
    Carga un archivo JSON desde una ruta específica.
    """
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def listar_archivos_en_carpeta(ruta: str) -> list:
    """
    Lista los archivos en una carpeta dada.
    """
    return [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]


def seleccionar_fotos_aleatorias(cantidad: int, fotos_disponibles: list) -> list:
    """
    Selecciona una cantidad específica de fotos de forma aleatoria.
    """
    return random.sample(fotos_disponibles, cantidad)


def generar_selecciones_por_denominacion(ruta_base: str, datos_json: dict()) -> dict():
    """
    Genera las selecciones de fotos para cada denominación, caso y cara.
    """
    selecciones = dict()

    for denominacion, casos in datos_json.items():
        selecciones[denominacion] = dict()

        for caso, caras in casos.items():
            selecciones[denominacion][caso] = dict()

            for cara, grupos in caras.items():
                selecciones[denominacion][caso][cara] = dict()

                # Construir la ruta de la carpeta correspondiente
                ruta_carpeta = os.path.join(ruta_base, denominacion, caso, cara)
                # Listar los archivos disponibles en la carpeta
                fotos_disponibles = listar_archivos_en_carpeta(ruta_carpeta)

                for grupo, cantidad in grupos.items():
                    # Seleccionar las fotos de forma aleatoria
                    selecciones[denominacion][caso][cara][grupo] = seleccionar_fotos_aleatorias(
                        cantidad, fotos_disponibles
                    )

    return selecciones


# Ruta base donde están las carpetas con las imágenes
ruta_base = "backend/src/data/img-data-vef/processed/"

# JSON con las cantidades de fotos a seleccionar
datos_json = cargar_json_desde_archivo("backend/src/scripts/organization/resultados.json")

# Generar las selecciones de fotos
selecciones = generar_selecciones_por_denominacion(ruta_base, datos_json)

# Mostrar las selecciones
for denominacion, casos in selecciones.items():
    print(f"\nSelecciones para {denominacion}:")
    for caso, caras in casos.items():
        print(f"\nCaso {caso}:")
        for cara, grupos in caras.items():
            print(f"\n{cara.capitalize()}:")
            for grupo, fotos_seleccionadas in grupos.items():
                print(f"{grupo.capitalize()}: {fotos_seleccionadas}")