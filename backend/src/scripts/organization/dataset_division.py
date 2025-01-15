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
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                    
                    shutil.copy(image_path, subfolder_path)
                    print(f"Imagen {image_name} copiada a la carpeta {subfolder_path}")
                else:
                    print(f"Imagen {image_name} no encontrada en {image_dir}")
            else:
                print(f"No se encontraron cifras en el archivo {txt_file}")

# Configuración
label_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division\labels'
image_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division\images'
output_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division\output'

process_files(label_dir, image_dir, output_dir)
