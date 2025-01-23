import os
import random

denominaciones = ['5', '10', '20', '50', '100', '200',]
casos = {
    '1':60, 
    '2':110, 
    '3':30,
    }
caras = ['front', 'back']

def recorrer_por_denominacion(base_path: str):
    for route, dirs, files in os.walk(base_path):
        for direc in dirs:
            if direc.split(' ')[0] in denominaciones:
                recorrer_por_caso(f'{route}{direc}/')

def recorrer_por_caso(bill_path: str):
    for route, dirs, files in os.walk(bill_path):
        for direc in casos.keys():
            recorrer_por_cara(f'{route}{direc}/')

def recorrer_por_cara(case_path: str):
    for route, dirs, files in os.walk(case_path):
        for direc in dirs:
            if direc in caras:
                cantidad_de_img = contar_archivos(f'{route}{direc}/')
                cantidad_caso = casos[route.split('/')[-2]]
                if cantidad_de_img <= cantidad_caso:
                    print(f'OK {cantidad_de_img}-{cantidad_caso} {route}{direc}/')
                else:
                    print(f'\nBAD {cantidad_de_img}-{cantidad_caso} {route}{direc}/')
                    archivos = listar_archivos(f'{route}{direc}/')
                    archivos = selec_random(archivos, cantidad_de_img-cantidad_caso)
                    borrar_imgs(archivos, f'{route}{direc}/')
                    borrar_labels(archivos, f'{route}label/')

def contar_archivos(directorio: str) -> int:
    return len([f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))])

def listar_archivos(directorio: str) -> list[str]:
    contenido = os.listdir(directorio)
    return (archivos := [f for f in contenido if os.path.isfile(os.path.join(directorio, f))])

def selec_random(archivos: list[str], cantidad: int) -> list[str]:
    if len(archivos) < cantidad:
        print("La cantidad solicitada es mayor al número de archivos disponibles.")
        return archivos
    return random.sample(archivos, cantidad)

def borrar_imgs(archivos: list[str], directorio: str):
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio, archivo)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)  # Elimina el archivo
            print(f"Archivo eliminado: {archivo}")

def borrar_labels(labels: list[str], directorio: str):
    for label in labels:
        label = f"{os.path.splitext(label)[0]}.txt"
        ruta_label = os.path.join(directorio, label)
        if os.path.exists(ruta_label):
            os.remove(ruta_label)  # Elimina el label
            print(f"Label eliminado: {label}")

recorrer_por_denominacion(
    base_path='backend/src/data/img-data-vef/processed/'
)