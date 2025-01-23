#Creado para dividir el dataset de dollar para entrenarlo mejor

import os
import shutil
import re

def get_first_two_digits_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        match = re.search(r'\d{1,2}', content)
        if match:
            return match.group()
    return None

def process_files(label_dir, image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for txt_file in os.listdir(label_dir):
        if txt_file.endswith('.txt'):
            txt_path = os.path.join(label_dir, txt_file)
            first_two_digits = get_first_two_digits_from_file(txt_path)

            if first_two_digits is not None:
                image_name = os.path.splitext(txt_file)[0] + '.jpg'  # Asume que la imagen tiene extensión .jpg
                image_path = os.path.join(image_dir, image_name)
                
                if os.path.exists(image_path):
                    subfolder_path = os.path.join(output_dir, first_two_digits)
                    image_folder_path = os.path.join(subfolder_path, 'images')
                    txt_folder_path = os.path.join(subfolder_path, 'labels')
                    
                    # Crear las subcarpetas si no existen
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    if not os.path.exists(txt_folder_path):
                        os.makedirs(txt_folder_path)
                    
                    # Copiar la imagen y el archivo .txt en sus respectivas subcarpetas
                    shutil.copy(image_path, image_folder_path)
                    shutil.copy(txt_path, txt_folder_path)
                    print(f"Imagen {image_name} copiada a {image_folder_path} y archivo {txt_file} copiado a {txt_folder_path}")
                else:
                    print(f"Imagen {image_name} no encontrada en {image_dir}")
            else:
                print(f"No se encontraron cifras en el archivo {txt_file}")

# Configuración
label_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\dataset_ordenado\label'
image_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\dataset_ordenado\image'
output_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\dataset_ordenado\output'

process_files(label_dir, image_dir, output_dir)
