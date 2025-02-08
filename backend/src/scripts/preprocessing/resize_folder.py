import os
from PIL import Image

def resize(image_path, size):
    """
    Redimensiona la imagen en image_path al tamaño especificado (size).
    size debe ser una tupla (ancho, alto).
    La imagen redimensionada sobrescribe la original.
    """
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(image_path, format="JPEG", quality=100)

def resize_images_in_folder(folder_path, target_size):
    """
    Recorre la carpeta en folder_path y redimensiona todas las imágenes a target_size.
    """
    # Extensiones de imagen soportadas
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

    # Recorre todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        # Obtén la extensión del archivo
        file_extension = os.path.splitext(filename)[1].lower()

        # Si el archivo es una imagen, rediménsionalo
        if file_extension in supported_extensions:
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                width, height = img.size
                if (width, height) != target_size:
                    print(f"{image_path} de {width}x{height} a {target_size}...")
                    resize(image_path, target_size)
                else:
                    print(f"{image_path} ya es {target_size}. Ignorando...")

# Ejemplo de uso
carpetas = [
    "backend/Dollar_Bill_Detection_VEF/datasets/images",
    "backend/Dollar_Bill_Detection_VEF/valid/images",
    "backend/Dollar_Bill_Detection_VEF/test/images",
]

for carpeta in carpetas:
    resize_images_in_folder(carpeta, (416, 416))
