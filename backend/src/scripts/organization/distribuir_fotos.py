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
    if not os.path.exists(ruta):
        print(f"Advertencia: La carpeta {ruta} no existe.")
        return []
    return [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]


def seleccionar_fotos_aleatorias(cantidad: int, fotos_disponibles: list) -> list:
    """
    Selecciona una cantidad específica de fotos de forma aleatoria.
    Si no hay suficientes fotos disponibles, devuelve todas las disponibles.
    """
    if cantidad > len(fotos_disponibles):
        print(f"Advertencia: No hay suficientes fotos disponibles. Seleccionando todas las {len(fotos_disponibles)} fotos.")
        return fotos_disponibles
    return random.sample(fotos_disponibles, cantidad)


def generar_selecciones_por_denominacion(ruta_base: str, datos_json: dict()) -> dict():
    """
    Genera las selecciones de fotos para cada denominación, caso y cara.
    Asegura que las fotos seleccionadas no se solapen entre grupos.
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

                if not fotos_disponibles:
                    print(f"Advertencia: No hay fotos disponibles en {ruta_carpeta}.")
                    continue

                # Copiar la lista de fotos disponibles para evitar modificarla directamente
                fotos_disponibles_restantes = fotos_disponibles.copy()

                for grupo, cantidad in grupos.items():
                    # Seleccionar las fotos de forma aleatoria
                    selecciones[denominacion][caso][cara][grupo] = seleccionar_fotos_aleatorias(
                        cantidad, fotos_disponibles_restantes
                    )
                    # Eliminar las fotos seleccionadas de la lista de disponibles
                    fotos_disponibles_restantes = [
                        foto for foto in fotos_disponibles_restantes
                        if foto not in selecciones[denominacion][caso][cara][grupo]
                    ]

    return selecciones


def mover_archivos_y_etiquetas(selecciones: dict(), ruta_origen_base: str, ruta_destino_base: str):
    """
    Mueve archivos y etiquetas a las carpetas correspondientes usando shutil.move.
    Maneja excepciones si un archivo no existe.
    """
    for denominacion, casos in selecciones.items():
        for caso, caras in casos.items():
            for cara, grupos in caras.items():
                for grupo, fotos_seleccionadas in grupos.items():
                    # Construir las rutas de destino para imágenes y etiquetas
                    ruta_destino_imagenes = os.path.join(ruta_destino_base, grupo, "images")
                    ruta_destino_etiquetas = os.path.join(ruta_destino_base, grupo, "labels")
                    # Crear las carpetas de destino si no existen
                    os.makedirs(ruta_destino_imagenes, exist_ok=True)
                    os.makedirs(ruta_destino_etiquetas, exist_ok=True)

                    for foto in fotos_seleccionadas:
                        # Construir la ruta de origen y destino de la imagen
                        ruta_origen_imagen = os.path.join(ruta_origen_base, denominacion, caso, cara, foto)
                        ruta_destino_imagen = os.path.join(ruta_destino_imagenes, foto)

                        # Construir la ruta de origen y destino de la etiqueta
                        nombre_etiqueta = os.path.splitext(foto)[0] + ".txt"
                        ruta_origen_etiqueta = os.path.join(ruta_origen_base, denominacion, caso, "label", nombre_etiqueta)
                        ruta_destino_etiqueta = os.path.join(ruta_destino_etiquetas, nombre_etiqueta)

                        # Mover la imagen (manejar excepciones si no existe)
                        try:
                            shutil.move(ruta_origen_imagen, ruta_destino_imagen)
                            print(f"Movida imagen: {ruta_origen_imagen} a {ruta_destino_imagen}")
                        except FileNotFoundError:
                            print(f"Advertencia: No se encontró la imagen {ruta_origen_imagen}. Se omite.")

                        # Mover la etiqueta (manejar excepciones si no existe)
                        try:
                            shutil.move(ruta_origen_etiqueta, ruta_destino_etiqueta)
                            print(f"Movida etiqueta: {ruta_origen_etiqueta} a {ruta_destino_etiqueta}")
                        except FileNotFoundError:
                            print(f"Advertencia: No se encontró la etiqueta {ruta_origen_etiqueta}. Se omite.")


# Ruta base donde están las carpetas con las imágenes
ruta_origen_base = "backend/src/data/img-data-vef/processed/"

# Ruta base donde se moverán las imágenes y etiquetas (datasets, valid, test)
ruta_destino_base = "backend/Dollar_Bill_Detection_VEF/"

# Ruta del archivo JSON
ruta_json = "backend/src/scripts/organization/resultados.json"

# Cargar el JSON desde el archivo
datos_json = cargar_json_desde_archivo(ruta_json)

# Generar las selecciones de fotos
selecciones = generar_selecciones_por_denominacion(ruta_origen_base, datos_json)

# Mover los archivos y etiquetas a las carpetas correspondientes
mover_archivos_y_etiquetas(selecciones, ruta_origen_base, ruta_destino_base)