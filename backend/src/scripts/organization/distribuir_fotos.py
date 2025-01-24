import os
import random
import json
import shutil

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


def mover_archivos(selecciones: dict(), ruta_origen_base: str, ruta_destino_base: str):
    """
    Simula el movimiento de archivos a las carpetas correspondientes.
    """
    for denominacion, casos in selecciones.items():
        for caso, caras in casos.items():
            for cara, grupos in caras.items():
                for grupo, fotos_seleccionadas in grupos.items():
                    # Construir la ruta de destino (sin estructura de carpetas adicional)
                    ruta_destino = os.path.join(ruta_destino_base, grupo, "images")
                    # Crear la carpeta de destino si no existe
                    os.makedirs(ruta_destino, exist_ok=True)

                    for foto in fotos_seleccionadas:
                        # Construir la ruta de origen y destino de la foto
                        ruta_origen = os.path.join(ruta_origen_base, denominacion, caso, cara, foto)
                        ruta_destino_foto = os.path.join(ruta_destino, foto)

                        # Simular el movimiento de la foto
                        print(f"Moviendo {ruta_origen} a {ruta_destino_foto}")
                        # shutil.move(ruta_origen, ruta_destino_foto)  # Comentado para simular


# Ruta base donde están las carpetas con las imágenes
ruta_origen_base = "backend/src/data/img-data-vef/processed/"

# Ruta base donde se moverán las imágenes (datasets, valid, test)
ruta_destino_base = "backend/Dollar_Bill_Detection_VEF/"

# Ruta del archivo JSON
ruta_json = "backend/src/scripts/organization/resultados.json"

# Cargar el JSON desde el archivo
datos_json = cargar_json_desde_archivo(ruta_json)

# Generar las selecciones de fotos
selecciones = generar_selecciones_por_denominacion(ruta_origen_base, datos_json)

# Mover (simular) los archivos a las carpetas correspondientes
mover_archivos(selecciones, ruta_origen_base, ruta_destino_base)