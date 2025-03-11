import os

def renombrar_imagen_individual(ruta_archivo):
    """
    Renombra un archivo individual reemplazando '' por '_'
    si está presente en el nombre, sin sobrescribir archivos existentes.
    Si el nuevo nombre ya existe, borra la versión con ''.
    """
    if not os.path.isfile(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe")
        return

    directorio = os.path.dirname(ruta_archivo)
    nombre_archivo = os.path.basename(ruta_archivo)
    
    if '' not in nombre_archivo:
        return  # No requiere renombrado

    nuevo_nombre = nombre_archivo.replace('', '_')
    nueva_ruta = os.path.join(directorio, nuevo_nombre)

    if os.path.exists(nueva_ruta):
        print(f"Omitido: {nuevo_nombre} ya existe, eliminando {nombre_archivo}")
        try:
            os.remove(ruta_archivo)
            print(f"Archivo eliminado: {ruta_archivo}")
        except Exception as e:
            print(f"Error eliminando el archivo: {str(e)}")
        return

    try:
        os.rename(ruta_archivo, nueva_ruta)
        print(f"Renombrado: {nombre_archivo} → {nuevo_nombre}")
    except Exception as e:
        print(f"Error renombrando: {str(e)}")


def renombrar_imagenes_en_directorio(directorio):
    """
    Itera sobre los archivos en un directorio y aplica `renombrar_imagen_individual`
    a cada archivo.
    """
    if not os.path.isdir(directorio):
        print(f"Error: El directorio {directorio} no existe")
        return

    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_completa):
            renombrar_imagen_individual(ruta_completa)

# Ejemplo de uso
directorio = "backend/src/data/img-data-vef/mergeLogs_model"

renombrar_imagenes_en_directorio(directorio)

