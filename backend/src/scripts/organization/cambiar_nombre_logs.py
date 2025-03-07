import os

def reemplazar_caracteres_en_nombre(nombre):
    """Reemplaza los caracteres no deseados en un nombre."""
    return nombre.replace(":", "_").replace("", "_")

def procesar_carpeta(carpeta_base):
    """Recorre recursivamente una carpeta y renombra archivos y subcarpetas."""
    for ruta_actual, subcarpetas, archivos in os.walk(carpeta_base, topdown=False):
        # Procesar archivos en la carpeta actual
        for nombre_archivo in archivos:
            ruta_completa_archivo = os.path.join(ruta_actual, nombre_archivo)
            nuevo_nombre_archivo = reemplazar_caracteres_en_nombre(nombre_archivo)
            
            if nuevo_nombre_archivo != nombre_archivo:
                nueva_ruta_completa_archivo = os.path.join(ruta_actual, nuevo_nombre_archivo)
                os.rename(ruta_completa_archivo, nueva_ruta_completa_archivo)
                print(f'Renombrado archivo: {ruta_completa_archivo} -> {nueva_ruta_completa_archivo}')
        
        # Procesar subcarpetas en la carpeta actual
        for nombre_subcarpeta in subcarpetas:
            ruta_completa_subcarpeta = os.path.join(ruta_actual, nombre_subcarpeta)
            nuevo_nombre_subcarpeta = reemplazar_caracteres_en_nombre(nombre_subcarpeta)
            
            if nuevo_nombre_subcarpeta != nombre_subcarpeta:
                nueva_ruta_completa_subcarpeta = os.path.join(ruta_actual, nuevo_nombre_subcarpeta)
                os.rename(ruta_completa_subcarpeta, nueva_ruta_completa_subcarpeta)
                print(f'Renombrado carpeta: {ruta_completa_subcarpeta} -> {nueva_ruta_completa_subcarpeta}')

# Especifica la carpeta base que deseas procesar
carpeta_base = 'backend/src/data/img-API'
# Llama a la función para procesar la carpeta base y sus subcarpetas
procesar_carpeta(carpeta_base)