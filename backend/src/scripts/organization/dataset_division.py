
"""
Script creado para organizar un dataset original de imágenes y etiquetas en subcarpetas
basadas en los primeros dos dígitos del archivo de etiquetas (.txt).
"""

import os  
import shutil  # Para copiar archivos
import re  # Para usar expresiones regulares

def get_first_two_digits_from_file(file_path):

    #Extrae los primeros dos dígitos encontrados en un archivo de texto.

    with open(file_path, 'r') as file:  # Abre el archivo en modo lectura
        content = file.read().strip()  # Lee el contenido y elimina espacios en blanco
        match = re.search(r'\d{1,2}', content)  # Busca los primeros 1 o 2 dígitos
        if match:
            return match.group()  # Retorna los dígitos encontrados
    return None  # Retorna None si no se encuentran dígitos

def process_files(label_dir, image_dir, output_dir):
    """
    Procesa los archivos de etiquetas e imágenes, organizándolos en subcarpetas
    basadas en los primeros dos dígitos (clases) encontrados en los archivos de etiquetas.
    """
    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Recorre todos los archivos en la carpeta de etiquetas
    for txt_file in os.listdir(label_dir):
        if txt_file.endswith('.txt'):  # Solo procesa archivos con extensión .txt
            txt_path = os.path.join(label_dir, txt_file)  # Ruta completa del archivo .txt
            first_two_digits = get_first_two_digits_from_file(txt_path)  # Obtiene los primeros dos dígitos

            if first_two_digits is not None:  # Si se encontraron dígitos
                # Construye el nombre de la imagen correspondiente (mismo nombre pero con extensión .jpg)
                image_name = os.path.splitext(txt_file)[0] + '.jpg'
                image_path = os.path.join(image_dir, image_name)  # Ruta completa de la imagen

                if os.path.exists(image_path):  # Verifica si la imagen existe
                    # Define las rutas de las subcarpetas para imágenes y etiquetas
                    subfolder_path = os.path.join(output_dir, first_two_digits)
                    image_folder_path = os.path.join(subfolder_path, 'images')
                    txt_folder_path = os.path.join(subfolder_path, 'labels')

                    # Crea las subcarpetas si no existen
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    if not os.path.exists(txt_folder_path):
                        os.makedirs(txt_folder_path)

                    # Copia la imagen y el archivo .txt a sus respectivas subcarpetas
                    shutil.copy(image_path, image_folder_path)
                    shutil.copy(txt_path, txt_folder_path)
                    print(f"Imagen {image_name} copiada a {image_folder_path} y archivo {txt_file} copiado a {txt_folder_path}")
                else:
                    print(f"Imagen {image_name} no encontrada en {image_dir}")
            else:
                print(f"No se encontraron cifras en el archivo {txt_file}")

# Configuración de rutas
label_dir = r'C:\Users\jesus\Downloads\2025-03-10_11k_USD\dataset-extend-USD\train\labels'  # Ruta de la carpeta que contiene los archivos de etiquetas (.txt)
image_dir = r'C:\Users\jesus\Downloads\2025-03-10_11k_USD\dataset-extend-USD\train\images'  # Ruta de la carpeta que contiene las imágenes (.jpg)
output_dir = r'C:\Users\jesus\Downloads\2025-03-10_11k_USD\dataset-extend-USD\train\Output'  # Ruta de la carpeta de salida donde se organizarán los archivos

# Llama a la función para procesar los archivos
process_files(label_dir, image_dir, output_dir)